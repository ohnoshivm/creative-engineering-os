#!/usr/bin/env python3
"""No account/config dumps. Verify skill schema, links, starter contracts and secret exclusions."""
import json,pathlib,re,subprocess
root=pathlib.Path(__file__).resolve().parents[1]; skills=sorted((root/'skills').glob('ceos-*'));assert len(skills)==13
for p in skills:
 text=(p/'SKILL.md').read_text();fm=text.split('---',2)[1]
 n=re.search(r'^name: (.+)$',fm,re.M).group(1);assert n==p.name and re.fullmatch(r'[a-z0-9-]{1,64}',n)
 desc=re.search(r'^description: (.+)$',fm,re.M).group(1);assert 0<len(desc)<=1024
 for directory in ['.claude/skills','.agents/skills','.gemini/antigravity/skills']:
  link=pathlib.Path.home()/directory/n;assert link.is_symlink() and link.resolve()==p.resolve(),link
for tpl in ['editorial','motion-heavy','immersive-3d','experimental-graphics']:
 p=root/'templates'/tpl;d=json.loads((p/'package.json').read_text());lock=json.loads((p/'package-lock.json').read_text())
 assert lock['name']==d['name'];assert {'build','test','test:visual'}<=d['scripts'].keys()
 for f in ['README.md','CHECKLIST.md','playwright.config.ts']:assert (p/f).is_file()
for f in ['standards/STANDARD.md','standards/QA-REPORT.md','agents/TEAM.md','architecture/ARCHITECTURE.md']:assert (root/f).is_file()
assert subprocess.run(['git','-C',str(root),'check-ignore','backups/example'],capture_output=True).returncode==0
print('PASS: 13 skill schemas, 39 owned links, 4 locked template contracts, standard/team docs, backup exclusion')
