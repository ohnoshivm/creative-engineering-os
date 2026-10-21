#!/usr/bin/env python3
"""Read-only pinned-reference checks and project evidence gates (stdlib only)."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REPOS = {
    'impeccable': 'pbakaus/impeccable',
    'ui-ux-pro-max': 'nextlevelbuilder/ui-ux-pro-max-skill',
    'react-bits': 'DavidHDev/react-bits',
    'pmndrs-examples': 'pmndrs/examples',
    'gsap-skills': 'greensock/gsap-skills',
    'superpowers': 'obra/superpowers',
    'shadcn-ui': 'shadcn-ui/ui',
}
INTEGRATION_IDS = {
    'impeccable', 'ui-ux-pro-max', 'react-bits', 'pmndrs-examples',
    'gsap-skills', 'superpowers', 'shadcn-ui', 'router',
}
FULL_SHA = re.compile(r'^[0-9a-f]{40}$')


def read_json(path):
    return json.loads(path.read_text())


def route(task, project=None, secondary=False, mode=None, route_id=None):
    """Compatibility entry point; routing policy stays in ceos-route.py."""
    spec = importlib.util.spec_from_file_location('ceos_route', ROOT/'scripts/ceos-route.py')
    router = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(router)
    project = pathlib.Path(project or pathlib.Path.cwd()).expanduser().resolve()
    if not project.is_dir():
        raise ValueError('--project must be an existing directory')
    data = router.load_routes()
    return router.resolve(route_id or task, data, project, mode or 'AUTO', need_secondary=secondary)


def verify_manifest(local=False):
    command = [sys.executable, str(ROOT/'scripts/integrations/generate_manifest.py'), '--check']
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        return []
    message = result.stderr.strip() or result.stdout.strip() or 'manifest verification failed'
    return [message]


def read_tree_hash(path):
    """Return the SKILL.md and deterministic whole-tree hashes without printing file contents."""
    path = pathlib.Path(path).expanduser().resolve()
    skill = path if path.is_file() else path/'SKILL.md'
    if not skill.is_file():
        raise ValueError(f'{path}: missing SKILL.md')
    skill_hash = hashlib.sha256(skill.read_bytes()).hexdigest()
    if path.is_file():
        return skill_hash, skill_hash
    tree_hash = hashlib.sha256()
    entries = sorted(path.rglob('*'))
    for file in entries:
        if not file.is_symlink() and not file.is_file():
            continue
        tree_hash.update(file.relative_to(path).as_posix().encode('utf-8'))
        tree_hash.update(b'\0')
        if file.is_symlink():
            tree_hash.update(b'symlink\0')
            tree_hash.update(str(file.readlink()).encode('utf-8'))
        else:
            tree_hash.update(b'file\0')
            tree_hash.update(file.read_bytes())
        tree_hash.update(b'\0')
    return skill_hash, tree_hash.hexdigest()


def verify_integration_records(installed=False):
    """Check checked-in records; installed checks are opt-in and never mutate or fetch."""
    errors = verify_manifest()
    manifest = read_json(ROOT/'integrations/manifest.json')
    lock = read_json(ROOT/'integrations/UPSTREAM-LOCK.json')
    entries = {entry.get('id'): entry for entry in manifest.get('integrations', [])}
    upstreams = lock.get('upstreams', {})
    if set(entries) != INTEGRATION_IDS:
        errors.append('manifest IDs must contain the seven upstreams and router exactly once')
    if set(upstreams) != INTEGRATION_IDS:
        errors.append('UPSTREAM-LOCK IDs must match the manifest exactly')
    if len(entries) != len(manifest.get('integrations', [])):
        errors.append('manifest contains duplicate integration IDs')

    required = ('repository', 'revision', 'localPath', 'license', 'integrationType',
                'supportedAgents', 'technologies', 'triggers', 'dependencies',
                'verificationStatus', 'updateMethod', 'rollbackMethod', 'evidencePath')
    for integration_id in sorted(INTEGRATION_IDS & set(entries) & set(upstreams)):
        entry = entries[integration_id]
        pinned = upstreams[integration_id]
        for field in required:
            if field not in entry or entry[field] in (None, '', [], {}):
                errors.append(f'{integration_id}: manifest field {field} is missing or empty')
        if not FULL_SHA.fullmatch(str(entry.get('revision', ''))):
            errors.append(f'{integration_id}: manifest revision must be a full 40-character SHA')
        if not isinstance(entry.get('supportedAgents'), list) or any(
                agent not in {'claude', 'codex', 'opencode', 'antigravity'}
                for agent in entry.get('supportedAgents', [])):
            errors.append(f'{integration_id}: supportedAgents contains an unknown agent ID')
        for field in ('repository', 'revision', 'localPath'):
            if entry.get(field) != pinned.get(field):
                errors.append(f'{integration_id}: manifest/lock {field} mismatch')
        evidence_path = ROOT/str(entry.get('evidencePath', ''))
        if not evidence_path.is_file():
            errors.append(f'{integration_id}: evidence file is missing')
        recorded = pinned.get('observedRevision')
        if recorded and recorded != pinned.get('revision'):
            mismatch = pinned.get('revisionMismatch', {})
            if mismatch.get('expected') != pinned.get('revision') or mismatch.get('observed') != recorded:
                errors.append(f'{integration_id}: checkout revision mismatch is not recorded explicitly')
            if pinned.get('revisionStatus') != 'mismatch':
                errors.append(f'{integration_id}: lock revisionStatus does not record the checkout mismatch')
        elif recorded == pinned.get('revision') and pinned.get('revisionStatus') != 'match':
            errors.append(f'{integration_id}: lock revisionStatus should be match')
        skill_trees = pinned.get('registeredSkillTrees')
        if not isinstance(skill_trees, list) or not skill_trees:
            errors.append(f'{integration_id}: lock has no registered skill integrity records')
        else:
            for skill in skill_trees:
                if not all(skill.get(field) for field in ('name', 'sourcePath', 'registeredPaths', 'skillMdSha256', 'treeSha256')):
                    errors.append(f'{integration_id}: incomplete registered skill integrity record')

        if not installed:
            continue
        checkout = pathlib.Path(pinned.get('localPath', '')).expanduser()
        try:
            result = subprocess.run(
                ['git', '-C', str(checkout), 'rev-parse', 'HEAD'],
                capture_output=True, text=True, timeout=15, check=True,
            )
            current = result.stdout.strip()
            if current != pinned.get('revision'):
                errors.append(f'{integration_id}: checkout HEAD {current} does not match lock {pinned.get("revision")}')
        except (OSError, subprocess.SubprocessError) as exc:
            errors.append(f'{integration_id}: checkout revision unavailable ({type(exc).__name__})')

        for skill in pinned.get('registeredSkillTrees', []):
            source = pathlib.Path(skill.get('sourcePath', '')).expanduser()
            if not source.is_absolute():
                source = ROOT / source
            try:
                skill_hash, tree_hash = read_tree_hash(source)
                if skill_hash != skill.get('skillMdSha256'):
                    errors.append(f'{integration_id}/{skill.get("name")}: active SKILL.md hash mismatch at {source}')
                if tree_hash != skill.get('treeSha256'):
                    errors.append(f'{integration_id}/{skill.get("name")}: active tree hash mismatch at {source}')
                resolved_source = source.resolve()
                for registered_path in skill.get('registeredPaths', []):
                    registered = pathlib.Path(registered_path).expanduser()
                    if not registered.exists():
                        errors.append(f'{integration_id}/{skill.get("name")}: registered skill path is missing: {registered}')
                    elif registered.resolve() != resolved_source:
                        errors.append(f'{integration_id}/{skill.get("name")}: registered path target differs: {registered}')
            except (OSError, ValueError) as exc:
                errors.append(f'{integration_id}/{skill.get("name")}: skill integrity unavailable ({type(exc).__name__})')
        for file_record in pinned.get('integrityFiles', []):
            path = ROOT/file_record.get('path', '')
            try:
                actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual_hash != file_record.get('sha256'):
                    errors.append(f'{integration_id}: integrity hash mismatch at {path.relative_to(ROOT)}')
            except OSError as exc:
                errors.append(f'{integration_id}: integrity file unavailable ({type(exc).__name__})')
    return errors


def integration_status():
    manifest = read_json(ROOT/'integrations/manifest.json')
    lock = read_json(ROOT/'integrations/UPSTREAM-LOCK.json')
    errors = verify_integration_records(installed=True)
    records = []
    for entry in manifest.get('integrations', []):
        integration_id = entry['id']
        pin = lock.get('upstreams', {}).get(integration_id, {})
        checkout = pathlib.Path(pin.get('localPath', entry.get('localPath', ''))).expanduser()
        if not checkout.is_absolute():
            checkout = ROOT / checkout
        current = None
        checkout_error = None
        try:
            result = subprocess.run(
                ['git', '-C', str(checkout), 'rev-parse', 'HEAD'],
                capture_output=True, text=True, timeout=15, check=True,
            )
            current = result.stdout.strip()
        except (OSError, subprocess.SubprocessError) as exc:
            checkout_error = type(exc).__name__
        records.append({
            'id': integration_id,
            'localPath': entry.get('localPath'),
            'verificationStatus': entry.get('verificationStatus'),
            'revision': pin.get('revision'),
            'checkoutRevision': current,
            'checkoutMatches': current == pin.get('revision') if current else False,
            'recordedRevisionStatus': pin.get('revisionStatus'),
            'trackedWorktree': pin.get('trackedWorktree'),
            'checkoutError': checkout_error,
            'registeredSkillTrees': len(pin.get('registeredSkillTrees', [])),
        })
    return {
        'passed': not errors,
        'errors': errors,
        'installedChecked': True,
        'integrations': records,
    }


def verify_project(project, state):
    """Validate recorded evidence, not the truth of its contents; reviewers still inspect captures/logs."""
    errors = []
    project = pathlib.Path(project).resolve()
    if state.get('mode') not in {'FAST', 'STANDARD', 'FLAGSHIP'}:
        errors.append('mode must be FAST, STANDARD or FLAGSHIP')
    for key in ('ui_changed', 'logic_changed', 'security_sensitive'):
        if not isinstance(state.get(key), bool):
            errors.append(key+' must be explicitly true or false')
    required = {'build'}
    if state.get('logic_changed'):
        required.add('tests')
    if state.get('security_sensitive'):
        required.add('security')
    if state.get('ui_changed'):
        required.update(('browser', 'accessibility', 'visual'))
        if state.get('mode') in {'STANDARD', 'FLAGSHIP'}:
            required.add('direction')
    if state.get('mode') == 'FLAGSHIP':
        required.update(('research', 'prototype', 'performance', 'independent-review'))
    checks = state.get('checks', [])
    names = [c['name'] for c in checks]
    if len(names) != len(set(names)):
        errors.append('duplicate check names')
    for name in sorted(required):
        check = next((c for c in checks if c['name'] == name), {})
        if check.get('status') != 'passed' or not check.get('evidence'):
            errors.append(name+': missing passing check and evidence')
    for check in checks:
        for file in check.get('evidence', []):
            path = (project/file).resolve()
            if not path.is_relative_to(project) or not path.is_file() or path.stat().st_size == 0:
                errors.append(check['name']+': absent, empty or escaping evidence')
    return errors


def manifest_revision(slug):
    manifest = read_json(ROOT/'integrations/manifest.json')
    entry = next((item for item in manifest['integrations'] if item['id'] == slug), None)
    if not entry or not entry.get('revision'):
        raise ValueError(slug+': no pinned revision in integrations/manifest.json')
    return entry['revision']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    routing = commands.add_parser('route', help='delegate a route request to ceos-route.py')
    routing.add_argument('task')
    routing.add_argument('--project', type=pathlib.Path)
    routing.add_argument('--secondary', action='store_true', help='explicitly request the candidate secondary')
    routing.add_argument('--mode', choices=['FAST', 'STANDARD', 'FLAGSHIP'])
    routing.add_argument('--route', dest='route_id', help='select a route ID directly')
    verify = commands.add_parser('verify')
    verify.add_argument('--installed', '--local', dest='installed', action='store_true',
                        help='also compare pinned checkouts and registered skill trees; never fetches')
    commands.add_parser('status', help='show pinned and installed integration state without changing files')
    evidence = commands.add_parser('verify-project')
    evidence.add_argument('project', type=pathlib.Path)
    evidence.add_argument('--state', default='docs/ceos-state.json')
    search = commands.add_parser('search')
    search.add_argument('query')
    search.add_argument('--limit', type=int, default=10)
    upstream = commands.add_parser('upstream-status')
    upstream.add_argument('integration', choices=list(REPOS))
    args = parser.parse_args()
    if args.command == 'route':
        result = route(args.task, args.project, args.secondary, args.mode, args.route_id)
    elif args.command == 'verify':
        errors = verify_integration_records(args.installed)
        result = {'passed': not errors, 'errors': errors, 'installed_checked': args.installed}
    elif args.command == 'status':
        result = integration_status()
    elif args.command == 'verify-project':
        project = args.project.expanduser().resolve()
        state_path = (project/args.state).resolve()
        if not state_path.is_relative_to(project):
            raise ValueError('state path must stay inside project')
        errors = verify_project(project, read_json(state_path))
        result = {'passed': not errors, 'errors': errors, 'limit': 'Validates evidence records; inspect actual logs and captures.'}
    elif args.command == 'search':
        words = args.query.casefold().split()
        if not words or not 1 <= args.limit <= 50:
            raise ValueError('query required; limit must be 1..50')
        matches = []
        for path in sorted((ROOT/'integrations/indexes').glob('*.json')):
            data = read_json(path)
            rows = data if isinstance(data, list) else next((v for v in data.values() if isinstance(v, list)), [])
            for row in rows:
                score = sum(w in json.dumps(row).casefold() for w in words)
                if score:
                    matches.append({'index': path.name, 'score': score, 'entry': row})
        result = sorted(matches, key=lambda r: -r['score'])[:args.limit]
    else:
        slug = args.integration
        pinned = manifest_revision(slug)
        response = subprocess.run(['git', 'ls-remote', 'https://github.com/'+REPOS[slug]+'.git', 'HEAD'],
                                  capture_output=True, text=True, timeout=30, check=True)
        current = response.stdout.split()[0]
        release = subprocess.run(['gh', 'api', 'repos/'+REPOS[slug]+'/releases/latest',
                                  '--jq', '{tag:.tag_name,url:.html_url,published:.published_at}'],
                                 capture_output=True, text=True, timeout=30)
        result = {'id': slug, 'pinned': pinned, 'upstream_head': current, 'different': pinned != current,
                  'latest_release': json.loads(release.stdout) if release.returncode == 0 else None,
                  'action': 'Review changes in an isolated workspace; no files or registrations changed.'}
    print(json.dumps(result, indent=2))
    return 1 if isinstance(result, dict) and result.get('passed') is False else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print('Integration check stopped:', type(exc).__name__, file=sys.stderr)
        sys.exit(2)
