// Frame/CWV probe (Creative Engineering OS; adapted from the Pixelard reference-research probe) (no WebGL hooks, so no instrumentation overhead).
// Phases: load → settle → idle (no input) → pointer sweep → scripted wheel scroll → idle tail.
// Per phase: rAF frame-interval distribution, long tasks, CLS delta. Whole run: FCP, LCP, CLS, CDP metrics, bytes.
// Usage: node frame-probe.mjs --url https://… --out /abs/file.json [--vw 1440 --vh 900 --dpr 1] [--mobile] [--cpu 4]
//        [--ready "<JS expression true when the site's own loader is done>"] [--readyTimeout 90000]
//        [--touchMode events|gesture] (mobile scroll: raw CDP touch events, or Input.synthesizeScrollGesture)
//        [--settle 3000] [--idle 8000] [--scrollMs 20000] [--wheel 120] [--wheelEvery 50]
// --ready gates measurement on the site's own loader (the load event fires long before WebGL sites are interactive).
// The run records readyMs, scroll displacement (window.scrollY or #page-container translateY) and an end screenshot
// (<out>.jpg) so degraded or non-scrolling runs can be rejected.
// [--har /abs/site-config.har.zip --harMode record|replay]: record = save every response of a full scenario pass
// (slow network is fine); replay = serve only from that archive, network blocked, so frame timing measures
// rendering rather than the connection. Unmatched requests are aborted and counted (failedRequests).
import fs from 'node:fs';
import path from 'node:path';
import { mirrorFile } from '../lib/safe-mirror.mjs';

import * as pw from 'playwright';
const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, arr) => {
  if (a.startsWith('--')) acc.push([a.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]);
  return acc;
}, []));
if (!args.url || !args.out || !/^https?:$/.test(new URL(args.url).protocol)) {
  console.error('usage: frame-probe.mjs --url <http(s) URL> --out <file.json>'); process.exit(2);
}
fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
const settle = +(args.settle || 3000), idle = +(args.idle || 8000), scrollMs = +(args.scrollMs || 20000);
const wheel = +(args.wheel || 120), wheelEvery = +(args.wheelEvery || 50);

const INIT = `(() => {
  const p = window.__perf = { phase: 'load', frames: [], lt: [], lcp: null, fcp: null, cls: 0, clsByPhase: {} };
  let last = 0;
  const tick = t => { if (last) p.frames.push([p.phase, +(t - last).toFixed(2)]); last = t; requestAnimationFrame(tick); };
  requestAnimationFrame(tick);
  const po = (type, cb) => { try { new PerformanceObserver(l => l.getEntries().forEach(cb)).observe({ type, buffered: true }); } catch (e) {} };
  po('longtask', e => p.lt.push([p.phase, Math.round(e.startTime), Math.round(e.duration)]));
  po('largest-contentful-paint', e => { p.lcp = { t: Math.round(e.startTime), size: e.size, el: e.element ? e.element.tagName : null }; });
  po('paint', e => { if (e.name === 'first-contentful-paint') p.fcp = Math.round(e.startTime); });
  po('layout-shift', e => { if (!e.hadRecentInput) { p.cls += e.value; p.clsByPhase[p.phase] = (p.clsByPhase[p.phase] || 0) + e.value; } });
})();`;

const browser = await pw.chromium.launch({ channel: 'chrome', headless: true });
const ctxOpts = args.mobile ? { ...pw.devices['iPhone 15'] }
  : { viewport: { width: +(args.vw || 1440), height: +(args.vh || 900) }, deviceScaleFactor: +(args.dpr || 1) };
if (args.har && args.harMode === 'record') ctxOpts.recordHar = { path: args.har, content: 'attach', mode: 'full' };
const context = await browser.newContext(ctxOpts);
if (args.har && args.harMode === 'replay') await context.routeFromHAR(args.har, { notFound: 'abort' });
let mirrorHits = 0;
// --mirror <dir> : serve files a HAR cannot hold (e.g. bodies of Web Worker fetches) from a local mirror laid out as
// <dir>/<host>/<path>; registered after routeFromHAR so it runs first and falls back to the archive.
if (args.mirror) {
  const MIME = { jpg: 'image/jpeg', png: 'image/png', webp: 'image/webp', json: 'application/json', ktx2: 'image/ktx2' };
  await context.route(u => !u.search && !!mirrorFile(args.mirror, u), async route => {
    const u = new URL(route.request().url());
    const f = mirrorFile(args.mirror, u);
    if (f) {
      mirrorHits++;
      return route.fulfill({ status: 200, path: f, headers: { 'content-type': MIME[f.split('.').pop()] || 'application/octet-stream', 'access-control-allow-origin': '*' } });
    }
    return route.fallback();
  });
}

await context.addInitScript(INIT);
let inflight = 0;
context.on('request', () => inflight++);
context.on('requestfinished', () => inflight--);
context.on('requestfailed', () => inflight--);
const page = await context.newPage();
const failed = [];
page.on('requestfailed', r => failed.push(r.url().slice(0, 160)));
const cdp = await context.newCDPSession(page);
await cdp.send('Performance.enable');
if (args.cpu) await cdp.send('Emulation.setCPUThrottlingRate', { rate: +args.cpu });
let bytes = 0, reqs = 0;
cdp.on('Network.loadingFinished', e => { bytes += e.encodedDataLength; reqs++; });
await cdp.send('Network.enable');

const setPhase = ph => page.evaluate(x => { window.__perf.phase = x; }, ph).catch(() => {});
const W = ctxOpts.viewport.width, H = ctxOpts.viewport.height;
const t0 = Date.now();
await page.goto(args.url, { waitUntil: 'load', timeout: 120000 });
const loadMs = Date.now() - t0;
let readyMs = null, readyTimedOut = false;
if (args.ready) {
  try { await page.waitForFunction(args.ready, null, { timeout: +(args.readyTimeout || 90000), polling: 100 }); readyMs = Date.now() - t0; }
  catch (e) { readyTimedOut = true; }
}
await page.waitForTimeout(settle);
const scrollPos = () => page.evaluate(() => {
  const pc = document.getElementById('page-container');
  const ty = pc ? -new DOMMatrixReadOnly(getComputedStyle(pc).transform).m42 : 0;
  const ln = document.querySelector('.lenis > div');
  const lt = ln ? -ln.getBoundingClientRect().top : 0;
  return Math.round(Math.max(window.scrollY || 0, ty || 0, lt || 0));
}).catch(() => null);

await setPhase('idle'); await page.waitForTimeout(idle);

await setPhase('pointer');
if (args.mobile) { await page.waitForTimeout(3000); }
else { for (let k = 0; k < 3; k++) { await page.mouse.move(W * 0.1, H * 0.3, { steps: 30 }); await page.mouse.move(W * 0.9, H * 0.7, { steps: 30 }); } }

await setPhase('scroll');
const scrollStart = await scrollPos();
const tS = Date.now();
if (args.mobile && args.touchMode === 'gesture') {
  // Browser-synthesised touch scroll gesture (drives native/compositor scrolling as well as JS touch handlers).
  while (Date.now() - tS < scrollMs) {
    await cdp.send('Input.synthesizeScrollGesture', { x: W / 2, y: H * 0.7, yDistance: -Math.round(H * 0.5), speed: 1500, gestureSourceType: 'touch', repeatCount: 1 });
    await page.waitForTimeout(250);
  }
} else if (args.mobile) {
  while (Date.now() - tS < scrollMs) {
    const x = W / 2, y0 = H * 0.75, y1 = H * 0.25, n = 10;
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y: y0 }] });
    for (let i = 1; i <= n; i++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x, y: y0 + (y1 - y0) * i / n }] }); await page.waitForTimeout(16); }
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await page.waitForTimeout(250);
  }
} else {
  while (Date.now() - tS < scrollMs) { await page.mouse.wheel(0, wheel); await page.waitForTimeout(wheelEvery); }
}
await setPhase('tail'); await page.waitForTimeout(4000);
const scrollEnd = await scrollPos();
// Record mode: a site can remove its loader before all assets have arrived; keep the context open until every
// request has finished (quiet for 20 s) so the archive holds complete bodies. Max --drainMs (default 25 min).
let drainMs = null;
if (args.harMode === 'record') {
  const tD = Date.now(), maxD = +(args.drainMs || 1500000); let quietSince = Date.now();
  while (Date.now() - tD < maxD) {
    await page.waitForTimeout(2000);
    if (inflight > 0) quietSince = Date.now(); else if (Date.now() - quietSince > 20000) break;
  }
  drainMs = Date.now() - tD;
  await page.waitForTimeout(3000);
}
await page.screenshot({ path: args.out.replace(/\.json$/, '') + '.jpg', type: 'jpeg', quality: 60 }).catch(() => {});

const perf = await page.evaluate(() => window.__perf);
const m = Object.fromEntries((await cdp.send('Performance.getMetrics')).metrics.map(x => [x.name, x.value]));
await context.close();
await browser.close();

const q = (a, p) => a.length ? a[Math.min(a.length - 1, Math.floor(a.length * p))] : null;
const phases = {};
for (const ph of ['load', 'idle', 'pointer', 'scroll', 'tail']) {
  const f = perf.frames.filter(x => x[0] === ph).map(x => x[1]).sort((a, b) => a - b);
  const lt = perf.lt.filter(x => x[0] === ph);
  const sum = f.reduce((s, v) => s + v, 0);
  phases[ph] = {
    frames: f.length, fps: sum ? +(1000 * f.length / sum).toFixed(1) : null,
    p50: q(f, 0.5), p90: q(f, 0.9), p95: q(f, 0.95), p99: q(f, 0.99), max: f.at(-1) ?? null,
    over20: f.filter(v => v > 20).length, over33: f.filter(v => v > 33.4).length, over50: f.filter(v => v > 50).length,
    longtasks: lt.length, longtaskMs: lt.reduce((s, x) => s + x[2], 0), cls: +(perf.clsByPhase[ph] || 0).toFixed(4),
  };
}
const result = {
  url: args.url, when: new Date().toISOString(), mode: args.mobile ? 'mobile-emulation iPhone 15' : `${W}x${H}@${ctxOpts.deviceScaleFactor}`,
  cpuThrottle: +(args.cpu || 1), touchMode: args.mobile ? (args.touchMode || 'events') : null, loadEventMs: loadMs, readyMs, drainMs, inflightAtEnd: inflight, readyTimedOut, scrollStart, scrollEnd, fcp: perf.fcp, lcp: perf.lcp, cls: +perf.cls.toFixed(4),
  har: args.har ? { mode: args.harMode, path: args.har } : null, failedRequests: failed.length, mirrorHits, failedSample: failed.slice(0, 15),
  requests: reqs, bytesEncoded: bytes, phases,
  cdp: { JSHeapUsedMB: +(m.JSHeapUsedSize / 1048576).toFixed(1), Nodes: m.Nodes, JSEventListeners: m.JSEventListeners,
    TaskDuration: +m.TaskDuration?.toFixed(2), ScriptDuration: +m.ScriptDuration?.toFixed(2), LayoutDuration: +m.LayoutDuration?.toFixed(2),
    RecalcStyleDuration: +m.RecalcStyleDuration?.toFixed(2), LayoutCount: m.LayoutCount },
};
fs.mkdirSync(path.dirname(args.out), { recursive: true });
fs.writeFileSync(args.out, JSON.stringify(result, null, 1));
const s = phases.scroll;
console.error(`[rx-perf] ${result.mode} cpu×${result.cpuThrottle} ready=${readyTimedOut ? 'TIMEOUT' : readyMs} scrolled=${scrollStart}→${scrollEnd} failed=${failed.length} mirror=${mirrorHits} LCP=${perf.lcp?.t} scroll p50/p95/p99=${s.p50}/${s.p95}/${s.p99} fps=${s.fps} >33ms=${s.over33} LT=${s.longtasks}/${s.longtaskMs}ms -> ${args.out}`);
