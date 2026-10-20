#!/usr/bin/env python3
"""Bounded source checks; reports paths/counts only, never matched secret values."""
import pathlib,re,sys,urllib.parse
root=pathlib.Path(__file__).resolve().parents[1]
excluded={'node_modules','dist','.git','.astro','test-results','playwright-report','backups','.playwright-cli','.lighthouseci','__pycache__'}
patterns=[re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),re.compile(r'\b(?:sk-proj-|sk-ant-api\d+-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}')]
links=[];secrets=[];count=0
for p in root.rglob('*'):
 if any(part in excluded for part in p.relative_to(root).parts) or not p.is_file() or p.suffix not in {'.md','.py','.ts','.mjs','.json','.toml','.sh','.html','.css','.astro','.frag','.vert','.glsl'}:continue
 try:s=p.read_text()
 except (UnicodeError,OSError):continue
 count+=1
 if any(rx.search(s) for rx in patterns):secrets.append(str(p.relative_to(root)))
 if p.suffix=='.md':
  for href in re.findall(r'\]\(([^)]+)\)',s):
   href=href.strip('<>');u=urllib.parse.urlsplit(href)
   if u.scheme or not u.path or any(c in href for c in ['<','>','*']):continue
   target=p.parent/urllib.parse.unquote(u.path)
   if not target.exists():links.append((str(p.relative_to(root)),href))
print('Text source files checked:',count,'secret-pattern findings:',len(secrets),'broken local Markdown links:',len(links))
for p in secrets:print('REVIEW secret pattern in',p)
for p,link in links:print('BROKEN',p,link)
if secrets or links:sys.exit(1)
