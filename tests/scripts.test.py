#!/usr/bin/env python3
import unittest,tempfile,pathlib,subprocess,json
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Scripts(unittest.TestCase):
 def run_script(self,name,*args):return subprocess.run([str(ROOT/'scripts'/name),*map(str,args)],capture_output=True,text=True)
 def test_create_spaces_and_lock(self):
  with tempfile.TemporaryDirectory(prefix='ceos script test ') as t:
   dest=pathlib.Path(t)/'A new site';r=self.run_script('new-project.sh','editorial',dest);self.assertEqual(r.returncode,0,r.stderr)
   self.assertEqual(json.loads((dest/'package.json').read_text())['name'],'a-new-site')
   self.assertEqual(json.loads((dest/'package-lock.json').read_text())['name'],'a-new-site')
   self.assertTrue((dest/'AGENTS.md').is_file());self.assertTrue((dest/'.gitignore').is_file());self.assertFalse((dest/'node_modules').exists())
   self.assertEqual(list((dest/'tests').glob('*-snapshots')),[])
   sentinel=dest/'keep';sentinel.write_text('user data');r=self.run_script('new-project.sh','editorial',dest);self.assertNotEqual(r.returncode,0);self.assertEqual(sentinel.read_text(),'user data')
 def test_reject_template_traversal(self):
  with tempfile.TemporaryDirectory() as t:
   dest=pathlib.Path(t)/'no';r=self.run_script('new-project.sh','../tooling',dest);self.assertEqual(r.returncode,2);self.assertFalse(dest.exists())
 def test_refuse_dangling_destination(self):
  with tempfile.TemporaryDirectory() as t:
   dest=pathlib.Path(t)/'link';dest.symlink_to(pathlib.Path(t)/'missing');r=self.run_script('new-project.sh','editorial',dest);self.assertNotEqual(r.returncode,0);self.assertTrue(dest.is_symlink())
 def test_link_idempotency_foreign_protection(self):
  with tempfile.TemporaryDirectory() as t:
   target=pathlib.Path(t)/'skills';target.mkdir();foreign=target/'ceos-art-direction';foreign.symlink_to('/nonexistent/foreign');real=target/'ceos-creative-direction';real.mkdir()
   for _ in range(2):
    r=self.run_script('link-skills.sh',target);self.assertEqual(r.returncode,0,r.stderr)
   self.assertEqual(str(foreign.readlink()),'/nonexistent/foreign');self.assertFalse(real.is_symlink());self.assertEqual(len(list(target.iterdir())),14)
   self.assertEqual((target/'ceos-realtime-3d').resolve(),ROOT/'skills/ceos-realtime-3d')
if __name__=='__main__':unittest.main()
