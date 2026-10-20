#!/bin/zsh
# new-project.sh <editorial|motion-heavy|immersive-3d|experimental-graphics> <new-directory>
set -euo pipefail
OS=${0:A:h:h}
tpl=${1:-}; dest=${2:-}
case "$tpl" in editorial|motion-heavy|immersive-3d|experimental-graphics) ;;
  *) echo 'usage: new-project.sh <editorial|motion-heavy|immersive-3d|experimental-graphics> <new-directory>' >&2; exit 2;; esac
[[ -n "$dest" ]] || { echo 'destination required' >&2; exit 2; }
dest=${dest:A}
[[ ! -e "$dest" && ! -L "$dest" ]] || { echo "refusing existing destination: $dest" >&2; exit 1; }
mkdir -p "$dest"
rsync -a --exclude .git --exclude node_modules --exclude dist --exclude .astro --exclude test-results --exclude playwright-report \
  --exclude .lighthouseci --exclude docs/QA --exclude '*-snapshots' "$OS/templates/$tpl/" "$dest/"
python3 -I - "$dest" "$OS" "$tpl" <<'PY'
import json,pathlib,re,sys,shlex
p,root,tpl=pathlib.Path(sys.argv[1]),pathlib.Path(sys.argv[2]),sys.argv[3]
name=re.sub(r'[^a-z0-9-]','-',p.name.lower()).strip('-') or 'creative-project'
f=p/'package.json';d=json.loads(f.read_text());d['name']=name
for k,v in d.get('scripts',{}).items():
 d['scripts'][k]=v.replace('../../tooling/',shlex.quote(str(root/'tooling'))+'/')
f.write_text(json.dumps(d,indent=2)+'\n')
lock=p/'package-lock.json'
if lock.exists():
 l=json.loads(lock.read_text());l['name']=name
 if '' in l.get('packages',{}): l['packages']['']['name']=name
 lock.write_text(json.dumps(l,indent=2)+'\n')
(p/'docs/QA').mkdir(parents=True,exist_ok=True)
instructions=f'''# {name}

Follow `{root}/standards/STANDARD.md`. Start with `ceos-studio-workflow`.
Template: {tpl}. Architecture: README.md. Verification: CHECKLIST.md.
Use the host's native browser/delegation tools when available; load specialist roles from the shared skills.
No client claims or deployment without project authorization. Baselines are intentionally omitted: inspect fresh screenshots before creating them.
'''
for filename in ['CLAUDE.md','AGENTS.md']:(p/filename).write_text(instructions)
(p/'.gitignore').write_text('node_modules/\ndist/\n.astro/\ntest-results/\nplaywright-report/\n.lighthouseci/\n.env\n.env.*\n!.env.example\n*.log\n.DS_Store\n')
PY
# Leave committing to the project owner; creating a directory does not publish it.
git -C "$dest" init -q
echo "Created $dest from $tpl. Next: npm ci, npm run build, npm test."
