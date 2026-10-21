#!/usr/bin/env python3
import unittest,tempfile,pathlib,subprocess,json,tomllib
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Installer(unittest.TestCase):
 def run_setup(self,d,*args):return subprocess.run(['python3',str(ROOT/'scripts/ceos.py'),'install','--user-root',str(d),*args],capture_output=True,text=True)
 def test_plan_has_no_writes(self):
  with tempfile.TemporaryDirectory() as t:
   d=pathlib.Path(t)/'new-home';r=self.run_setup(d,'--client','all','--mcp');self.assertEqual(r.returncode,0,r.stderr);self.assertFalse(d.exists())
 def test_merge_preserves_settings_and_is_idempotent(self):
  with tempfile.TemporaryDirectory(prefix='ceos user root ') as t:
   d=pathlib.Path(t);claude=d/'.claude.json';before={'provider':{'keep':'private-value'},'mcpServers':{'existing':{'command':'keep','env':{'PRIVATE':'private-value'}}}};claude.write_text(json.dumps(before))
   codex=d/'.codex/config.toml';codex.parent.mkdir();original='model = "unchanged"\n[mcp_servers.existing]\ncommand = "keep"\nargs = []\n';codex.write_text(original)
   for _ in range(2):
    r=self.run_setup(d,'--client','all','--mcp','--apply');self.assertEqual(r.returncode,0,r.stderr);self.assertNotIn('private-value',r.stdout+r.stderr)
   actual=json.loads(claude.read_text());actual['mcpServers'].pop('chrome-devtools');self.assertEqual(actual,before)
   self.assertTrue(codex.read_text().startswith(original));parsed=tomllib.loads(codex.read_text());self.assertEqual(parsed['model'],'unchanged');self.assertEqual(parsed['mcp_servers']['existing']['args'],[])
   self.assertEqual(codex.read_text().count('[mcp_servers.chrome-devtools]'),1)
   self.assertEqual(len(list((d/'.agents/skills').iterdir())),14)
   self.assertTrue((d/'.config/opencode/agents/creative-auditor.md').is_symlink())
   copies=list((d/'.local/state/creative-engineering-os/backups').glob('*/config.before'));self.assertEqual(len(copies),2)
   for p in copies:self.assertEqual(p.stat().st_mode&0o777,0o600);self.assertEqual(p.parent.stat().st_mode&0o777,0o700)
 def test_existing_entries_and_foreign_links_untouched(self):
  with tempfile.TemporaryDirectory() as t:
   d=pathlib.Path(t);p=d/'.claude.json';data={'mcpServers':{'chrome-devtools':{'command':'custom'}}};p.write_text(json.dumps(data));target=d/'.claude/skills';target.mkdir(parents=True);link=target/'ceos-art-direction';link.symlink_to('/foreign/skill')
   r=self.run_setup(d,'--client','claude','--mcp','--apply');self.assertEqual(r.returncode,0);self.assertEqual(json.loads(p.read_text()),data);self.assertEqual(str(link.readlink()),'/foreign/skill')
 def test_invalid_and_symlinked_configs_refused(self):
  with tempfile.TemporaryDirectory() as t:
   d=pathlib.Path(t);p=d/'.claude.json';p.write_text('{bad private-value')
   r=self.run_setup(d,'--client','claude','--mcp','--apply');self.assertNotEqual(r.returncode,0);self.assertEqual(p.read_text(),'{bad private-value');self.assertNotIn('private-value',r.stderr)
   p.unlink();other=d/'outside';other.write_text('{}');p.symlink_to(other)
   r=self.run_setup(d,'--client','claude','--mcp','--apply');self.assertNotEqual(r.returncode,0);self.assertEqual(other.read_text(),'{}')
 def test_public_export_contains_core_no_private_state(self):
  with tempfile.TemporaryDirectory() as t:
   dest=pathlib.Path(t)/'bundle';r=subprocess.run(['python3',str(ROOT/'scripts/build-bundle.py'),'--out',str(dest)],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr)
   for rel in ['skills/ceos-studio-workflow/SKILL.md','agents/creative-auditor.md','agents/opencode/creative-auditor.md','.claude-plugin/plugin.json','mcp/codex.toml','tooling/package-lock.json','templates/editorial/package-lock.json','scripts/ceos.py','README.md','LICENSE']:self.assertTrue((dest/rel).is_file(),rel)
   for rel in ['backups','.git','node_modules','CLAUDE.md','docs/CONFIG-PRESERVATION.json','docs/01-audit-2026-10-20.md','demo/signal-study/docs/QA']:self.assertFalse((dest/rel).exists(),rel)
   self.assertIn('ohnoshivm/creative-engineering-os',(dest/'README.md').read_text())
   for p in dest.rglob('*'):
    self.assertFalse(p.is_symlink(),p)
    if p.is_file() and p.suffix in {'.md','.json','.py','.toml','.ts','.mjs','.sh'}:self.assertNotRegex(p.read_text(),r'/' + r'Users/[A-Za-z0-9._-]+/',str(p))
if __name__=='__main__':unittest.main()
