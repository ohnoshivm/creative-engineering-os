#!/usr/bin/env python3
"""Exercise pinned isolated Chrome DevTools MCP over stdio; no client auth or logged-in browser access."""
import json,subprocess,selectors,time,sys,http.server,threading,tempfile,pathlib,os,signal,re
root=pathlib.Path(__file__).resolve().parents[1]
class Fixture(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  body=b'<!doctype html><html lang="en"><title>CEOS diagnostic fixture</title><h1>Diagnostics connected</h1><button onclick="this.textContent=\'Verified\'">Probe</button></html>'
  self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers();self.wfile.write(body)
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Fixture);threading.Thread(target=server.serve_forever,daemon=True).start()
log=tempfile.TemporaryFile(mode='w+')
p=subprocess.Popen(['npx','--yes','chrome-devtools-mcp@1.11.0','--isolated','--headless','--no-usage-statistics','--no-performance-crux'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log,text=True,bufsize=1,start_new_session=True)
sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ); seq=0

def rpc(method,params=None,notify=False):
 global seq
 seq+=1; msg={'jsonrpc':'2.0','method':method}
 if params is not None:msg['params']=params
 if not notify:msg['id']=seq
 p.stdin.write(json.dumps(msg)+'\n');p.stdin.flush()
 if notify:return
 end=time.monotonic()+70
 while time.monotonic()<end:
  if not sel.select(timeout=1):
   if p.poll() is not None:raise RuntimeError('MCP server exited')
   continue
  line=p.stdout.readline()
  try:r=json.loads(line)
  except ValueError:continue
  if r.get('id')==seq:
   if 'error' in r:raise RuntimeError(str(r['error']))
   return r['result']
 raise TimeoutError(method)

def call(name,args):
 r=rpc('tools/call',{'name':name,'arguments':args})
 if r.get('isError'):raise RuntimeError(name+': '+str(r))
 return r

try:
 init=rpc('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'ceos-verification','version':'1.0'}})
 rpc('notifications/initialized',notify=True)
 ts=rpc('tools/list')['tools'];names=[t['name'] for t in ts]
 if '--schemas' in sys.argv:
  print(json.dumps([t for t in ts if t['name'] in ['new_page','evaluate_script','performance_start_trace','take_screenshot','list_network_requests','list_console_messages']],indent=2));sys.exit()
 result={'date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'server':init['serverInfo'],'toolCount':len(ts),'isolated':True,'checks':{}}
 page_result=call('new_page',{'url':f'http://127.0.0.1:{server.server_port}/','timeout':15000})
 if '--newpage' in sys.argv: print(json.dumps(page_result));sys.exit()
 result['checks']['navigation']=True
 page_id=int(re.search(r'(?m)^(\d+):.*\[selected\]', '\n'.join(c.get('text','') for c in page_result['content'])).group(1))
 r=call('evaluate_script',{'pageId':page_id,'function':'() => { document.querySelector("button").click(); return {title:document.title,button:document.querySelector("button").textContent}; }'})
 assert 'Verified' in json.dumps(r) and 'CEOS diagnostic fixture' in json.dumps(r);result['checks']['dom-and-interaction']=True
 call('take_snapshot',{'pageId':page_id});result['checks']['snapshot']=True
 with tempfile.TemporaryDirectory(prefix='ceos-mcp-image-') as directory:
  screenshot=pathlib.Path(directory)/'fixture.png'
  call('take_screenshot',{'pageId':page_id,'filePath':str(screenshot)})
  assert screenshot.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
 result['checks']['screenshot']=True
 call('list_network_requests',{'pageId':page_id});result['checks']['network']=True
 call('list_console_messages',{'pageId':page_id});result['checks']['console']=True
 call('performance_start_trace',{'pageId':page_id,'reload':True,'autoStop':True});result['checks']['performance-trace']=True
 out=root/'docs/MCP-SMOKE.json';out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
finally:
 server.shutdown()
 p.stdin.close()
 try:p.wait(timeout=8)
 except subprocess.TimeoutExpired:
  os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL)
 log.close()
