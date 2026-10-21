#!/usr/bin/env python3
"""Generate the CEOS integration manifest from the specialist evidence records."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / 'integrations/evidence'
MANIFEST_PATH = ROOT / 'integrations/manifest.json'
INTEGRATION_IDS = (
    'impeccable', 'ui-ux-pro-max', 'react-bits', 'pmndrs-examples',
    'gsap-skills', 'superpowers', 'shadcn-ui', 'router',
)
UPSTREAM_IDS = set(INTEGRATION_IDS) - {'router'}
INTEGRATION_TYPES = {
    'impeccable': 'native-skill',
    'ui-ux-pro-max': 'native-skill',
    'react-bits': 'reference-only',
    'pmndrs-examples': 'reference-only',
    'gsap-skills': 'native-skill',
    'superpowers': 'native-skill',
    'shadcn-ui': 'project-level CLI',
    'router': 'project-level CLI',
}
AGENT_ALIASES = {
    'claude': 'claude', 'claude code': 'claude',
    '.agents': 'codex', 'codex': 'codex',
    'opencode': 'opencode', 'open code': 'opencode',
    'antigravity': 'antigravity',
}


def read_json(path):
    return json.loads(path.read_text())


def upstream_record(evidence):
    if isinstance(evidence.get('source'), dict):
        return evidence['source']
    if isinstance(evidence.get('upstream'), dict):
        return evidence['upstream']
    return evidence


def first_value(*values):
    return next((value for value in values if value not in (None, '')), None)


def normalize_license(value):
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return first_value(value.get('name'), value.get('spdx'), value.get('repository_spdx')) or json.dumps(value, sort_keys=True)
    return value


def walk(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def supported_agents(evidence, global_install=None, global_skill_names=()):
    candidates = []
    for key, value in walk(evidence):
        if key in {'clients', 'provider', 'agent'} or ('agent' in key.casefold() and 'support' in key.casefold()):
            if isinstance(value, (str, list)):
                candidates.append(value)
    for key, value in walk(evidence):
        if key in {'path', 'links', 'linkLocations'}:
            if isinstance(value, (str, list)):
                candidates.append(value)
    if global_install:
        for skill in global_install.get('skills', []):
            if skill.get('name') in global_skill_names:
                candidates.extend(skill.get('links', []))

    result = set()
    for candidate in candidates:
        values = candidate if isinstance(candidate, list) else [candidate]
        for value in values:
            if not isinstance(value, str):
                continue
            folded = value.casefold()
            for alias, agent in AGENT_ALIASES.items():
                if alias in folded:
                    result.add(agent)
    return [agent for agent in ('claude', 'codex', 'opencode', 'antigravity') if agent in result]


def technologies(evidence, integration_id):
    values = evidence.get('technologies') or evidence.get('supportedTech')
    if isinstance(values, list):
        return values
    if isinstance(values, dict):
        result = list(values.get('interfaceScope', []))
        extensions = values.get('detectorSourceExtensions', [])
        if extensions:
            result.append('Source formats: ' + ', '.join(extensions))
        return result
    if integration_id == 'gsap-skills':
        return ['GSAP', 'JavaScript', 'React', 'Vue', 'Svelte', 'ScrollTrigger']
    if integration_id == 'router':
        return ['Python 3.9+ standard library', 'JSON']
    return []


def triggers(evidence, integration_id):
    values = evidence.get('triggers')
    if isinstance(values, list):
        return [item if isinstance(item, str) else f"{item.get('skill')}: {item.get('description')}"
                for item in values]
    if integration_id == 'gsap-skills':
        return [item.get('trigger_summary') for item in evidence.get('skills', []) if item.get('trigger_summary')]
    if integration_id == 'router':
        return ['Choose one primary capability for a website task; request a secondary only when its recorded contribution is useful.']
    return []


def verification_status(evidence, integration_id):
    if integration_id in {'impeccable', 'superpowers'}:
        return 'partial'
    if integration_id == 'router':
        return 'passed_with_limitations'
    value = evidence.get('verification', {})
    raw = value.get('status') if isinstance(value, dict) else None
    if isinstance(raw, str) and 'partial' in raw.casefold():
        return 'partial'
    return 'passed_with_limitations'


def evidence_status(evidence):
    value = evidence.get('status')
    if isinstance(value, str):
        return value
    if isinstance(evidence.get('verification'), dict):
        return evidence['verification'].get('status')
    return None


def build_upstream_entry(integration_id, global_install):
    path = EVIDENCE_DIR / f'{integration_id}.json'
    evidence = read_json(path)
    source = upstream_record(evidence)
    repository = first_value(source.get('repository'), source.get('repositoryUrl'), evidence.get('repository'))
    revision = first_value(source.get('revision'), source.get('pinned_revision'), source.get('pinnedRevision'),
                           source.get('commit'), evidence.get('revision'))
    local_path = first_value(source.get('localPath'), source.get('checkoutPath'), source.get('checkout_path'),
                             evidence.get('localPath'))
    license_value = first_value(source.get('license'), evidence.get('license'))
    update = first_value(evidence.get('updateMethod'), evidence.get('update_method'), evidence.get('update'),
                         evidence.get('installUpdateRollback'), evidence.get('install_update_rollback'))
    rollback = first_value(evidence.get('rollbackMethod'), evidence.get('rollback_method'),
                           evidence.get('rollback'), evidence.get('installUpdateRollback'),
                           evidence.get('install_update_rollback'))
    if rollback is None and isinstance(evidence.get('update'), dict):
        rollback = evidence['update'].get('rollback')
    if isinstance(update, dict):
        update = first_value(update.get('method'), update.get('update'), update.get('steps'), update)
    if isinstance(rollback, dict):
        rollback = first_value(rollback.get('rollback'), rollback.get('details'), rollback.get('restoreInstructions'),
                               rollback.get('restore_instructions'), rollback)
    if integration_id == 'gsap-skills' and update is None:
        update = 'Review a pinned upstream commit and license, back up only files to change, then update skill links and rerun source, link, and discovery checks.'
    if integration_id == 'router':
        raise ValueError('router is generated separately')
    if not all((repository, revision, local_path, license_value, update, rollback)):
        raise ValueError(f'{integration_id}: evidence is missing a required manifest field')
    return {
        'id': integration_id,
        'repository': repository.removesuffix('.git'),
        'revision': revision,
        'localPath': local_path,
        'license': normalize_license(license_value),
        'integrationType': INTEGRATION_TYPES[integration_id],
        'supportedAgents': supported_agents(
            evidence,
            global_install if integration_id in {'react-bits', 'pmndrs-examples'} else None,
            (integration_id,) if integration_id in {'react-bits', 'pmndrs-examples'} else ()),
        'technologies': technologies(evidence, integration_id),
        'triggers': triggers(evidence, integration_id),
        'dependencies': evidence.get('dependencies', {}),
        'verificationStatus': verification_status(evidence, integration_id),
        'evidenceStatus': evidence_status(evidence),
        'evidencePath': path.relative_to(ROOT).as_posix(),
        'updateMethod': update,
        'rollbackMethod': rollback,
    }


def build_router_entry():
    evidence = read_json(EVIDENCE_DIR / 'router.json')
    audit = read_json(ROOT / 'docs/integrations/pre-install-state.json')
    return {
        'id': 'router',
        'repository': 'https://github.com/ohnoshivm/creative-engineering-os',
        'revision': audit['head'],
        'localPath': '.',
        'license': 'MIT',
        'integrationType': INTEGRATION_TYPES['router'],
        'supportedAgents': ['claude', 'codex', 'opencode', 'antigravity'],
        'technologies': technologies(evidence, 'router'),
        'triggers': triggers(evidence, 'router'),
        'dependencies': {'runtime': 'Python 3.9+ standard library; no network or installed packages.'},
        'verificationStatus': verification_status(evidence, 'router'),
        'evidenceStatus': evidence_status(evidence),
        'evidencePath': 'integrations/evidence/router.json',
        'updateMethod': 'Review changes to scripts/ceos-route.py and integrations/routes.json together, then run the routing and integration suites.',
        'rollbackMethod': 'Revert only the intended router files and integration records; preserve unrelated working-tree changes.',
        'revisionScope': 'Base checkout commit recorded by pre-install-state.json; router changes are uncommitted and are not represented by this SHA.',
    }


def render():
    global_install = read_json(EVIDENCE_DIR / 'global-install.json')
    records = [build_upstream_entry(item, global_install) for item in INTEGRATION_IDS if item != 'router']
    records.append(build_router_entry())
    data = {'schemaVersion': 2, 'integrations': records}
    return (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare generated bytes with manifest.json')
    args = parser.parse_args(argv)
    expected = render()
    if args.check:
        if MANIFEST_PATH.read_bytes() != expected:
            print('integrations/manifest.json differs from generated output', file=sys.stderr)
            return 1
        print('integrations/manifest.json matches specialist evidence')
        return 0
    MANIFEST_PATH.write_bytes(expected)
    print(f'Wrote integrations/manifest.json ({len(json.loads(expected)["integrations"])} integrations)')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f'integration manifest generation stopped: {type(exc).__name__}: {exc}', file=sys.stderr)
        raise SystemExit(2)
