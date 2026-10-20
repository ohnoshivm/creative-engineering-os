#!/usr/bin/env python3
"""Vendor every installed third-party skill whose licence clearly permits redistribution into library/skills/,
with its upstream licence file, and write a catalogue + install manifest for everything else.

Selection rule (conservative):
  - at least one licence label in PERMISSIVE, none in BLOCKING, and
  - a real licence file (LICENSE/LICENCE/COPYING, any extension) found at the skill folder or an ancestor
    inside the same package root. Plugin-manifest-only evidence is not enough.
Skills that fail the rule are listed in library/UPSTREAM.md (name + upstream repository when known) and are
never copied. Re-run safely: library/ is rebuilt from scratch each time.

Usage: python3 scripts/vendor-library.py [--dry-run]
"""
import json, pathlib, re, shutil, sys, collections

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOME = pathlib.Path.home()
LIB = ROOT / 'library'
PERMISSIVE = {'MIT', 'MIT-style notice', 'Apache-2.0', 'ISC', 'BSD-2-Clause', 'BSD-3-Clause', '0BSD', 'Unlicense', 'CC0-1.0'}
BLOCKING = re.compile(r'proprietary|gpl|agpl|lgpl|cc-by-nc|all rights reserved', re.I)
SKIP_DIRS = {'node_modules', '.git', '__pycache__', 'dist', 'build', '.venv', 'venv', '.next', '.cache'}
MAX_FILE = 2 * 1024 * 1024        # skip single files over 2 MB
MAX_SKILL = 12 * 1024 * 1024      # skip whole skills over 12 MB
LICENSE_RE = re.compile(r'^(LICEN[CS]E|COPYING)(\.[A-Za-z]+)?$', re.I)

CATEGORIES = [  # first match wins; order matters
    ('Creative direction & concept', r'creative-direction|concept|moodboard|brainstorm|art-direction|brand|identity|taste|originality|creative'),
    ('Visual design & typography', r'typograph|font|palette|colou?r|layout|grid|visual|design-system|tokens|theme|impeccable|aesthetic|minimal|brutalist|editorial|glass|gradient|shadow|skeuomorph|style'),
    ('UX & interaction', r'\bux\b|user-experience|interaction|accessib|a11y|navigation|form|onboarding|usability|journey|keyboard|interface'),
    ('Motion & animation', r'gsap|motion|animat|scroll|transition|easing|lenis|marquee|reveal|parallax|kinetic|lottie|rive|theatre'),
    ('3D, WebGL & shaders', r'three|webgl|webgpu|shader|glsl|3d|r3f|particle|globe|raymarch|postprocess|blender|gltf|vantajs|unicorn'),
    ('Frontend engineering', r'react|next|vercel|vite|astro|tailwind|css|frontend|component|typescript|shadcn|svelte|vue|html'),
    ('Quality, performance & testing', r'test|qa|playwright|performance|vitals|lighthouse|audit|review|debug|verif|lint|security|semgrep|codeql'),
    ('Content, SEO & growth', r'seo|copy|content|marketing|social|linkedin|instagram|twitter|\bx-|facebook|ads|growth|email|newsletter'),
    ('Media: image, video & audio', r'image|video|audio|photo|voice|music|tts|render|recording|clip'),
    ('Workflow & agents', r'plan|workflow|agent|skill|mcp|git|deploy|ship|release|docs|spec|office-hours|gstack|superpowers'),
]

def expand(p): return pathlib.Path(p.replace('~', str(HOME), 1))

def frontmatter(md):
    m = re.match(r'^---\n(.*?)\n---', md, re.S)
    if not m: return {}
    out = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(':')
        if k.strip() in ('name', 'description') and v.strip(): out[k.strip()] = v.strip().strip('"\'')
    return out

def find_license(skill_dir: pathlib.Path):
    """Nearest licence file at the skill folder or an ancestor, stopping at the package root (a dir with a
    plugin manifest, package.json, .git, or the skills container's parent)."""
    d = skill_dir
    for _ in range(6):
        for f in sorted(d.iterdir()) if d.is_dir() else []:
            if f.is_file() and LICENSE_RE.match(f.name): return f
        if any((d / m).exists() for m in ('.claude-plugin', 'package.json', '.git')) and d != skill_dir: break
        if d.parent == d or d == HOME: break
        d = d.parent
    return None

def size_ok(skill_dir):
    total = 0
    for f in skill_dir.rglob('*'):
        if any(p in SKIP_DIRS for p in f.relative_to(skill_dir).parts): continue
        if f.is_file() and not f.is_symlink(): total += f.stat().st_size
    return total <= MAX_SKILL, total

def categorise(name, desc):
    text = f'{name} {desc}'.lower()
    for cat, pat in CATEGORIES:
        if re.search(pat, text): return cat
    return 'Other'

def repo_of(rec):
    for s in rec.get('sources') or []:
        if s.get('repository'): return s['repository']
    return None

UPSTREAM_SPDX = {'pbakaus/impeccable': 'Apache-2.0', 'greensock/gsap-skills': 'MIT', 'Leonxlnx/taste-skill': 'MIT',
    'nextlevelbuilder/ui-ux-pro-max-skill': 'MIT', 'emilkowalski/skills': 'MIT', 'Dammyjay93/interface-design': 'MIT',
    'microsoft/playwright-cli': 'Apache-2.0', 'obra/superpowers': 'MIT'}  # verified via GitHub API, 20 Oct 2026
UPSTREAM_REPOS = [  # official public repos with permissive licences, cloned at HEAD and pinned by commit
    'pbakaus/impeccable', 'greensock/gsap-skills', 'Leonxlnx/taste-skill', 'nextlevelbuilder/ui-ux-pro-max-skill',
    'emilkowalski/skills', 'Dammyjay93/interface-design', 'microsoft/playwright-cli', 'obra/superpowers',
]

def upstream_skills(tmp):
    """Shallow-clone each repo; yield (skill_dir, licence_file, repo_url, commit) for every SKILL.md folder."""
    import subprocess
    for slug in UPSTREAM_REPOS:
        dest = tmp / slug.replace('/', '__')
        url = f'https://github.com/{slug}'
        r = subprocess.run(['git', 'clone', '--depth', '1', '--quiet', url + '.git', str(dest)], capture_output=True, text=True)
        if r.returncode: print('  clone failed', slug, r.stderr.strip()[:120]); continue
        commit = subprocess.run(['git', '-C', str(dest), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
        lic = next((f for f in sorted(dest.iterdir()) if f.is_file() and LICENSE_RE.match(f.name)), None)
        if lic is None: print('  no licence file, skipped', slug); continue
        for md in dest.rglob('SKILL.md'):
            rel = md.relative_to(dest).parts
            if any(p in SKIP_DIRS or p.startswith('.') and p not in ('.claude', '.agents') for p in rel[:-1]): continue
            if any(p in ('test', 'tests', 'fixtures', 'examples', 'evals') for p in rel[:-1]): continue
            yield md.parent, lic, url, commit

def main(dry):
    core = {p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()}
    recs = json.loads((ROOT / 'manifests/ecosystem-skills.json').read_text())['skills']
    # Prefer records with a declared upstream, then the first discovery.
    recs.sort(key=lambda r: (r['status'] != 'upstream_install', r['name']))
    vendored, upstream, seen = [], [], set(core)
    for r in recs:
        name = r['name']
        if name in seen or r['status'] == 'bundled_core': continue
        if all('/.trash/' in c for c in r['canonical_sources']): continue  # deleted local skills: never publish
        labels = {e['label'] for e in r['license_evidence']}
        src = next((expand(c) for c in r['canonical_sources'] if expand(c).exists()), None)
        reason = None
        if src is None: reason = 'source not on disk'
        elif any(BLOCKING.search(l) for l in labels): reason = 'licence not permissive (' + ', '.join(sorted(l for l in labels if BLOCKING.search(l))) + ')'
        elif not labels & PERMISSIVE: reason = 'no permissive licence evidence'
        lic = None
        if reason is None:
            lic = find_license(src.parent)
            if lic is None: reason = 'licence file not found'
            else:
                ok, total = size_ok(src.parent)
                if not ok: reason = f'too large ({total // 1048576} MB)'
        fm = frontmatter(src.read_text(errors='replace')) if src else {}
        desc = fm.get('description', '')
        entry = {'name': name, 'description': desc[:300], 'category': categorise(name, desc), 'repository': repo_of(r),
                 'licence': sorted(labels & PERMISSIVE) or sorted(labels)}
        seen.add(name)
        if reason:
            entry['reason'] = reason; upstream.append(entry); continue
        entry['path'] = f'library/skills/{name}/SKILL.md'
        entry['licence_file'] = lic.name
        entry['_src'] = src.parent; entry['_lic'] = lic
        vendored.append(entry)

    import tempfile
    tmp = pathlib.Path(tempfile.mkdtemp(prefix='ceos-upstream-'))
    by_name = {e['name']: e for e in vendored}
    up_names = {e['name'] for e in upstream}
    added = replaced = 0
    for d, lic, url, commit in upstream_skills(tmp):
        fm = frontmatter((d / 'SKILL.md').read_text(errors='replace'))
        name = fm.get('name') or d.name
        if name in core: continue
        ok, total = size_ok(d)
        if not ok: continue
        desc = fm.get('description', '')
        entry = {'name': name, 'description': desc[:300], 'category': categorise(name, desc), 'repository': url,
                 'commit': commit, 'licence': [UPSTREAM_SPDX.get(url.removeprefix('https://github.com/'), lic.name)], 'path': f'library/skills/{name}/SKILL.md', 'licence_file': lic.name,
                 '_src': d, '_lic': lic, 'origin': 'upstream-clone'}
        if name in by_name and by_name[name].get('origin') == 'upstream-clone': continue  # first repo wins
        if name in by_name: vendored.remove(by_name[name]); replaced += 1
        else: added += 1
        if name in up_names: upstream[:] = [u for u in upstream if u['name'] != name]; up_names.discard(name)
        by_name[name] = entry; vendored.append(entry)
    print(f'upstream clones: +{added} new, {replaced} replaced by official copies')
    print(f'vendor: {len(vendored)} skills · upstream-only: {len(upstream)}')
    print(' reasons:', collections.Counter(e['reason'].split(' (')[0] for e in upstream).most_common())
    if dry:
        shutil.rmtree(tmp, ignore_errors=True); return

    if LIB.exists(): shutil.rmtree(LIB)
    (LIB / 'skills').mkdir(parents=True)
    for e in vendored:
        dst = LIB / 'skills' / e['name']
        def ignore(d, names):
            out = []
            for n in names:
                p = pathlib.Path(d) / n
                if n in SKIP_DIRS or p.is_symlink() or (p.is_file() and p.stat().st_size > MAX_FILE): out.append(n)
            return out
        shutil.copytree(e['_src'], dst, ignore=ignore)
        if not any(LICENSE_RE.match(f.name) for f in dst.iterdir()):
            shutil.copy2(e['_lic'], dst / ('LICENSE.upstream' + (e['_lic'].suffix or '')))
        # scrub absolute home paths from text files
        for f in dst.rglob('*'):
            if f.is_file() and f.suffix.lower() in {'.md', '.txt', '.json', '.py', '.js', '.mjs', '.ts', '.sh', '.yml', '.yaml', '.toml', '.csv', '.html', '.css'}:
                try:
                    t = f.read_text()
                    t2 = re.sub(r'/Users/[A-Za-z0-9._-]+/', '~/', t)
                    if t2 != t: f.write_text(t2)
                except (UnicodeDecodeError, PermissionError): pass

    clean = lambda e: {k: v for k, v in e.items() if not k.startswith('_')}
    (LIB / 'catalog.json').write_text(json.dumps({'vendored': [clean(e) for e in vendored], 'upstream_only': upstream}, indent=1) + '\n')

    by = collections.defaultdict(list)
    for e in vendored: by[e['category']].append(e)
    lines = ['# Skill library catalogue', '',
             f'{len(vendored)} third-party skills bundled here (permissive licences, upstream licence file kept in each folder),',
             f'plus {len(upstream)} skills that are **not** redistributed — see [UPSTREAM.md](UPSTREAM.md) for where to get them.',
             '', 'These are **not auto-loaded**. Read the one you need: open its `SKILL.md` and follow it. The 14 core `ceos-*` skills',
             'in `../skills/` are the studio method; this library is the reference shelf they point to.', '']
    order = [c for c, _ in CATEGORIES] + ['Other']
    lines.append('## Sections\n')
    lines += [f'- [{c}](#{re.sub(r"[^a-z0-9 -]", "", c.lower()).replace(" ", "-")}) — {len(by[c])}' for c in order if by[c]]
    for c in order:
        if not by[c]: continue
        lines += ['', f'## {c}', '', '| Skill | Use it for | Licence | Upstream |', '|---|---|---|---|']
        for e in sorted(by[c], key=lambda e: e['name']):
            d = (e['description'] or '—').replace('|', '\\|').replace('\n', ' ')
            d = d[:180] + ('…' if len(d) > 180 else '')
            up = f'[repo]({e["repository"]})' if e['repository'] else '—'
            lines.append(f'| [`{e["name"]}`](skills/{e["name"]}/SKILL.md) | {d} | {", ".join(e["licence"])} | {up} |')
    (LIB / 'CATALOG.md').write_text('\n'.join(lines) + '\n')

    ul = ['# Skills not bundled', '', 'These skills exist in the author\'s environment but are not redistributed here, because their licence is',
          'proprietary/copyleft/unclear or no licence file was found. Install them from their own source if you need them.', '',
          '| Skill | Category | Why not bundled | Upstream |', '|---|---|---|---|']
    for e in sorted(upstream, key=lambda e: (e['category'], e['name'])):
        ul.append(f'| `{e["name"]}` | {e["category"]} | {e["reason"]} | {e["repository"] or "unknown"} |')
    (LIB / 'UPSTREAM.md').write_text('\n'.join(ul) + '\n')

    notes = ['# Third-party skills in library/', '', 'Each folder keeps its upstream licence file. Copyright remains with the original authors.', '',
             '| Skill | Licence | Upstream |', '|---|---|---|']
    notes += [f'| {e["name"]} | {", ".join(e["licence"])} ({e["licence_file"]}) | {e["repository"] or "see licence file"} |' for e in sorted(vendored, key=lambda e: e['name'])]
    (LIB / 'NOTICES.md').write_text('\n'.join(notes) + '\n')
    shutil.rmtree(tmp, ignore_errors=True)
    print('wrote', LIB)

if __name__ == '__main__':
    main('--dry-run' in sys.argv)
