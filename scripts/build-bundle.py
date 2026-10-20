#!/usr/bin/env python3
"""Export a public source bundle by allowlist into a new directory, without private history or machine reports."""
import argparse,pathlib,re,shutil,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
FILES={'.gitignore','AGENTS.md','LICENSE','THIRD_PARTY_NOTICES.md','Brewfile','.mcp.json','START-HERE.md','llms.txt'}
TREES={'.github','.claude-plugin','skills','standards','references','mcp','manifests','scripts','tooling','templates','demo','tests','library'}
DOCS={'INSTALL.md','USE.md','PLUGINS.md','SECURITY.md','ECOSYSTEM.md','RELEASE-VALIDATION.md','OPTIONAL-TOOLING.md'}
EXCLUDED={'.git','node_modules','dist','.astro','test-results','playwright-report','.lighthouseci','backups','.playwright-cli','__pycache__','release','publication'}
TEXT={'.md','.py','.mjs','.sh','.ts','.astro','.html','.css','.json','.toml','.glsl','.frag','.vert','.yml','.yaml'}

# Pattern fragments are split so this file never matches itself.
SECRET=re.compile(rb'(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|thk' rb'_live_|xox[bp]-[A-Za-z0-9-]{10,}|AKIA(?!IOSFODNN7EXAMPLE)[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIV' rb'ATE KEY)')
ROOT_ONLY={'release','publication'}

def sensitive_name(rel):
 # Credential-looking file names outside the third-party library are never exported. Library files are judged by
 # content instead (design-token files are legitimate there): see has_secret().
 return rel.parts[0]!='library' and any(k in rel.name.lower() for k in ('token','api-key','apikey'))

def has_secret(path):
 try:return bool(SECRET.search(path.read_bytes()))
 except OSError:return True

def include(rel):
 if any(p in EXCLUDED for p in rel.parts[:-1] if rel.parts[0]!='library' or p not in ROOT_ONLY):return False
 if rel.parts[0] in ROOT_ONLY:return False
 if sensitive_name(rel):return False
 if rel.parts[0]=='library':return True
 if rel.name.startswith('.env') or rel.name in {'auth.json','.credentials.json','service.json'}:return False
 if rel.parts[0]=='docs':return len(rel.parts)==2 and rel.name in DOCS
 if len(rel.parts)==1:return rel.name in FILES
 if rel.parts[0]=='agents':return rel.as_posix() in {'agents/creative-auditor.md','agents/opencode/creative-auditor.md'}
 if rel.parts[0] not in TREES:return False
 if 'docs' in rel.parts:return rel.as_posix()=='demo/signal-study/docs/ART_DIRECTION.md'
 if rel.as_posix()=='agents/TEAM.md':return False
 return True

def clean(s):
 return re.sub(r"/Users/[A-Za-z0-9._-]+(?=/)","~",s).replace('agents/TEAM.md','docs/AGENT-TEAM.md')

def export(destination):
 if destination.exists() or destination.is_symlink():raise ValueError('destination already exists')
 destination.mkdir(parents=True)
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if not p.is_file() or p.is_symlink() or not include(rel):continue
  if has_secret(p):print('SKIPPED (secret pattern):',rel);continue
  target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True)
  if p.suffix in TEXT:
   try:text=p.read_bytes().decode('utf-8')
   except UnicodeDecodeError:shutil.copy2(p,target)  # non-UTF-8 upstream file: keep the bytes unchanged
   else:target.write_bytes(clean(text).encode('utf-8'))
  else:shutil.copy2(p,target)
  target.chmod(p.stat().st_mode&0o777)
 for source,target in [('distribution/README.md','README.md'),('distribution/SYSTEM.md','SYSTEM.md'),('distribution/AGENT-TEAM.md','docs/AGENT-TEAM.md')]:
  origin=ROOT/source
  if not origin.exists():origin=ROOT/target
  (destination/target).write_text(clean(origin.read_text()))
 (destination/'architecture').mkdir(exist_ok=True)
 (destination/'architecture/ARCHITECTURE.md').write_text((destination/'SYSTEM.md').read_text())
 # The reusable project instructions are AGENTS.md; CLAUDE.md isn't loaded by a plugin and triggers a validator warning.
 # This demo README is public-facing and doesn't refer to omitted machine-local reports.
 (destination/'demo/signal-study/README.md').write_text('# Signal study\n\nOriginal shader + GSAP capability study. Run npm ci, npm run dev, npm run build and npm test here. See docs/ART_DIRECTION.md for concept/tokens and ../../docs/RELEASE-VALIDATION.md for original evidence and limitations. The preview uses port4184.\n')
 asset=ROOT/'demo/signal-study/docs/QA/final/1440-first.png'
 if not asset.exists():asset=ROOT/'docs/assets/signal-study.png'
 if asset.exists():
  out=destination/'docs/assets/signal-study.png';out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(asset,out)
 # Keep generated local verification outputs and release artifacts out of future commits.
 with (destination/'.gitignore').open('a') as out:out.write('\n/release/\n/publication/\ndocs/*-SMOKE.json\ndocs/CONFIG-PRESERVATION.json\n')
 print('Exported public bundle to',destination)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args()
 try:export(a.out.expanduser().absolute())
 except (ValueError,OSError) as e:raise SystemExit(str(e))
