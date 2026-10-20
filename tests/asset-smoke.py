#!/usr/bin/env python3
"""Disposable Blender → GLB → glTF-Transform/meshopt pipeline; no user scene files or preferences touched."""
import subprocess,tempfile,pathlib,json,time
root=pathlib.Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='ceos-assets-') as directory:
 p=pathlib.Path(directory);source=p/'cube.glb';dest=p/'cube-meshopt.glb'
 commands=[['blender','--background','--factory-startup','--python-expr',f"import bpy; bpy.ops.export_scene.gltf(filepath={str(source)!r}, export_format='GLB')"],['npx','--yes','@gltf-transform/cli@4.5.1','inspect',str(source)],['npx','--yes','@gltf-transform/cli@4.5.1','optimize',str(source),str(dest),'--compress','meshopt','--texture-compress','webp','--texture-size','2048'],['npx','--yes','@gltf-transform/cli@4.5.1','inspect',str(dest)]]
 result={'date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'steps':[]}
 for command in commands:
  r=subprocess.run(command,capture_output=True,text=True,timeout=90)
  step={'tool':command[0],'operation':'export' if command[0]=='blender' else command[3],'exitCode':r.returncode};result['steps'].append(step)
  if r.returncode:print(r.stderr[-1600:]);raise SystemExit(1)
 result['sourceBytes']=source.stat().st_size;result['meshoptBytes']=dest.stat().st_size
 # meshopt uses a compressed buffer extension; parsing the GLB JSON proves it was emitted.
 raw=dest.read_bytes();length=int.from_bytes(raw[12:16],'little');gltf=json.loads(raw[20:20+length]);result['extensionsUsed']=gltf.get('extensionsUsed',[])
 assert 'EXT_meshopt_compression' in result['extensionsUsed']
 (root/'docs/ASSET-SMOKE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
