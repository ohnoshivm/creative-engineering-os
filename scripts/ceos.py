#!/usr/bin/env python3
"""Portable, additive setup. Plans by default; writes require --apply. No provider/auth configuration copied."""
from __future__ import annotations
import argparse, datetime, json, os, pathlib, shutil, subprocess, sys
try:
 import tomllib
except ImportError:
 raise SystemExit('Python 3.11+ is required (stdlib TOML parser).')
ROOT=pathlib.Path(__file__).resolve().parents[1]
CLIENTS=('claude','codex','opencode','antigravity')
SKILLS={'claude':'.claude/skills','codex':'.agents/skills','opencode':'.agents/skills','antigravity':'.gemini/antigravity/skills'}
CONFIGS={'claude':'.claude.json','codex':'.codex/config.toml','opencode':'.config/opencode/opencode.json','antigravity':'.gemini/config/mcp_config.json'}
ARGS=['--yes','chrome-devtools-mcp@1.11.0','--isolated','--headless','--no-usage-statistics','--no-performance-crux']

def backup(path,user_root):
 if not path.exists():return
 directory=user_root/'.local/state/creative-engineering-os/backups'/datetime.datetime.now().strftime('%Y%m%dT%H%M%S%f')
 directory.mkdir(parents=True,mode=0o700);directory.chmod(0o700)
 target=directory/'config.before';shutil.copy2(path,target);target.chmod(0o600)
 print('  Private before-copy saved under ~/.local/state/creative-engineering-os/backups')

def atomic_text(path,text,user_root):
 path.parent.mkdir(parents=True,exist_ok=True)
 backup(path,user_root)
 # Exclusive creation avoids clobbering a stale/concurrent temporary file.
 import tempfile
 fd,name=tempfile.mkstemp(prefix='.ceos-',dir=path.parent)
 try:
  with os.fdopen(fd,'w') as out:out.write(text)
  os.chmod(name,(path.stat().st_mode&0o777) if path.exists() else 0o600)
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)

def link(source,destination,apply):
 if destination.is_symlink():
  if destination.resolve()==source.resolve():print('UNCHANGED',destination.name)
  else:print('SKIP foreign link:',destination.name)
 elif destination.exists():print('SKIP existing path:',destination.name)
 else:
  print(('LINK' if apply else 'PLAN link'),destination.name)
  if apply:destination.parent.mkdir(parents=True,exist_ok=True);destination.symlink_to(source,target_is_directory=source.is_dir())

def mcp(client,user_root,apply):
 path=user_root/CONFIGS[client]
 if path.is_symlink():raise ValueError(f'{client}: config is a symlink; configure this client manually')
 original=path.read_text() if path.exists() else ''
 if client=='codex':
  data=tomllib.loads(original);servers=data.get('mcp_servers',{})
  if 'chrome-devtools' in servers:print('SKIP existing chrome-devtools config:',client);return
  block=(ROOT/'mcp/codex.toml').read_text()
  updated=original.rstrip()+'\n\n'+block
  parsed=tomllib.loads(updated);actual=parsed.pop('mcp_servers',{});expected=data.pop('mcp_servers',{})
  assert all(actual[k]==v for k,v in expected.items()) and parsed==data
 else:
  data=json.loads(original or '{}')
  if not isinstance(data,dict):raise ValueError(f'{client}: config must be an object')
  key='mcp' if client=='opencode' else 'mcpServers';servers=data.get(key,{})
  if not isinstance(servers,dict):raise ValueError(f'{client}: server section must be an object')
  if 'chrome-devtools' in servers:print('SKIP existing chrome-devtools config:',client);return
  addition=json.loads((ROOT/'mcp'/f'{client}.json').read_text())[key]['chrome-devtools']
  data.setdefault(key,{})['chrome-devtools']=addition
  updated=json.dumps(data,indent=2)+'\n'
 print(('ADD' if apply else 'PLAN add'),'chrome-devtools to',client)
 if apply:atomic_text(path,updated,user_root)

def doctor():
 checks={}
 for executable in ['python3','node','npm','git','zsh','rsync','claude','codex','opencode','blender']:
  checks[executable]=bool(shutil.which(executable));print(('FOUND' if checks[executable] else 'OPTIONAL/MISSING'),executable)
 if checks['node']:
  r=subprocess.run(['node','--version'],capture_output=True,text=True,check=True)
  parts=tuple(int(x) for x in r.stdout.strip().lstrip('v').split('.')[:3]);print('Node',r.stdout.strip(),'; templates require >=22.22.0')
  if parts<(22,22,0):return 1
 return 0 if all(checks[x] for x in ['python3','node','npm','git','zsh','rsync']) else 1

def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['doctor','install','dependencies'])
 p.add_argument('--client',choices=[*CLIENTS,'all'],default='all');p.add_argument('--mcp',action='store_true',help='add only isolated chrome-devtools')
 p.add_argument('--apply',action='store_true',help='perform the displayed setup; otherwise plan only')
 p.add_argument('--user-root',type=pathlib.Path,default=pathlib.Path.home(),help='explicit target home for provisioning/testing; does not change HOME')
 a=p.parse_args(argv)
 if a.action=='doctor':return doctor()
 if a.action=='dependencies':
  dirs=['tooling',*[f'templates/{n}' for n in ['editorial','motion-heavy','immersive-3d','experimental-graphics']],'demo/signal-study']
  for directory in dirs:
   print(('RUN' if a.apply else 'PLAN'),'npm ci in',directory)
   if a.apply:subprocess.run(['npm','ci'],cwd=ROOT/directory,check=True)
  return 0
 root=a.user_root.expanduser().resolve();clients=CLIENTS if a.client=='all' else [a.client]
 for client in clients:
  print('CLIENT',client)
  for skill in sorted((ROOT/'skills').glob('ceos-*')):link(skill,root/SKILLS[client]/skill.name,a.apply)
  if client=='claude':link(ROOT/'agents/creative-auditor.md',root/'.claude/agents/creative-auditor.md',a.apply)
  if client=='opencode':link(ROOT/'agents/opencode/creative-auditor.md',root/'.config/opencode/agents/creative-auditor.md',a.apply)
  if a.mcp:mcp(client,root,a.apply)
 if not a.apply:print('Plan only. Re-run with --apply after review. No packages, credentials or provider routing changed.')
 return 0
if __name__=='__main__':
 try:sys.exit(main())
 except (ValueError,OSError,subprocess.CalledProcessError) as e:
  # Never print config contents or subprocess stdout on malformed/sensitive input.
  print('Setup stopped:',type(e).__name__, '(check the selected path/client manually; existing files preserved)',file=sys.stderr);sys.exit(1)
