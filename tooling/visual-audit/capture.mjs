#!/usr/bin/env node
// Visual-audit capture: screenshots at 1440/1024/768/390 (first screen + full page), reduced-motion set,
// console/page errors, axe-core results, and DOM measurements (type sizes, colours, h1 line count, overflow,
// outer margins, small tap targets). Uses the installed Google Chrome (no browser download).
//
// Usage: node capture.mjs --url http://localhost:5173 --out ./docs/QA/2026-10-20 [--video] [--wait 1500] [--nogl]
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs';
import path from 'node:path';

const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, arr) => {
  if (a.startsWith('--')) acc.push([a.slice(2), arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true]);
  return acc;
}, []));
if (!args.url || !args.out) { console.error('usage: capture.mjs --url <url> --out <dir> [--video] [--wait ms] [--nogl]'); process.exit(2); }
const out = path.resolve(args.out); fs.mkdirSync(out, { recursive: true });
const wait = +(args.wait || 1500);
const VIEWPORTS = [
  { name: '1440', width: 1440, height: 900 },
  { name: '1024', width: 1024, height: 768 },
  { name: '768', width: 768, height: 1024, touch: true },
  { name: '390', width: 390, height: 844, touch: true, mobile: true, dpr: 3 },
];

const MEASURE = () => {
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && +cs.opacity > 0.01; };
  const textEls = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,li,a,button,span,label,blockquote,figcaption,dd,dt,td,th')]
    .filter(el => vis(el) && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
  const sizes = {}; const families = {}; const colours = {};
  for (const el of textEls) { const cs = getComputedStyle(el); sizes[cs.fontSize] = (sizes[cs.fontSize] || 0) + 1; families[cs.fontFamily.split(',')[0].trim()] = (families[cs.fontFamily.split(',')[0].trim()] || 0) + 1; colours[cs.color] = (colours[cs.color] || 0) + 1; }
  const lines = el => { const lh = parseFloat(getComputedStyle(el).lineHeight) || parseFloat(getComputedStyle(el).fontSize) * 1.2; return Math.round(el.getBoundingClientRect().height / lh); };
  const h1s = [...document.querySelectorAll('h1')].map(h => ({ text: h.textContent.trim().slice(0, 80), fontSize: getComputedStyle(h).fontSize, lines: lines(h), visible: vis(h) }));
  const headings = [...document.querySelectorAll('h1,h2,h3')].filter(vis).map(h => ({ tag: h.tagName, text: h.textContent.trim().slice(0, 60), lines: lines(h), fontSize: getComputedStyle(h).fontSize }));
  const overflowX = document.documentElement.scrollWidth > window.innerWidth + 1;
  const small = [...document.querySelectorAll('a,button,input,select,textarea,[role=button]')].filter(vis).map(el => ({ el, r: el.getBoundingClientRect() }))
    .filter(({ r }) => r.width < 44 || r.height < 44).slice(0, 20).map(({ el, r }) => ({ tag: el.tagName, text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 40), w: Math.round(r.width), h: Math.round(r.height) }));
  const blocks = [...document.querySelectorAll('main *')].filter(el => vis(el) && el.children.length === 0 && el.getBoundingClientRect().width > 40).slice(0, 4000).map(el => el.getBoundingClientRect());
  const left = blocks.length ? Math.round(Math.min(...blocks.map(r => r.left))) : null;
  const right = blocks.length ? Math.round(window.innerWidth - Math.max(...blocks.map(r => r.right))) : null;
  const unnamed = [...document.querySelectorAll('a,button')].filter(el => vis(el) && !(el.textContent.trim() || el.getAttribute('aria-label') || el.getAttribute('title') || el.querySelector('img[alt]:not([alt=""])'))).length;
  return { title: document.title, fontSizes: sizes, fontFamilies: families, textColours: colours, h1s, headings, overflowX, smallTapTargets: small, outerMargins: { left, right }, unnamedControls: unnamed, canvases: document.querySelectorAll('canvas').length };
};

const browser = await chromium.launch({ channel: 'chrome', headless: true, args: args.nogl ? ['--disable-3d-apis'] : [] });
const report = { url: args.url, when: new Date().toISOString(), nogl: !!args.nogl, viewports: {} };
for (const reduced of [false, true]) {
  for (const vp of VIEWPORTS) {
    if (reduced && !['1440', '390'].includes(vp.name)) continue;
    const tag = vp.name + (reduced ? '-reduced' : '');
    const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, deviceScaleFactor: vp.dpr || 1, hasTouch: !!vp.touch, isMobile: !!vp.mobile,
      reducedMotion: reduced ? 'reduce' : 'no-preference', recordVideo: args.video && !reduced ? { dir: path.join(out, 'video'), size: { width: Math.min(vp.width, 1280), height: Math.round(Math.min(vp.width, 1280) * vp.height / vp.width) } } : undefined });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
    page.on('pageerror', e => errors.push('pageerror: ' + e.message.slice(0, 300)));
    const t0 = Date.now();
    await page.goto(args.url, { waitUntil: 'load', timeout: 60000 });
    const navigationMs = Date.now() - t0;
    await page.evaluate(() => document.fonts && document.fonts.ready);
    await page.waitForTimeout(wait);
    await page.screenshot({ path: path.join(out, `${tag}-first.png`) });
    const m = await page.evaluate(MEASURE);
    if (!reduced && args.video) { for (let i = 0; i < 8; i++) { await page.mouse.wheel(0, vp.height * 0.6); await page.waitForTimeout(350); } }
    await page.screenshot({ path: path.join(out, `${tag}-full.png`), fullPage: true });
    let axe = null;
    if (!reduced) {
      try { const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
        axe = r.violations.map(v => ({ id: v.id, impact: v.impact, help: v.help, nodes: v.nodes.length, sample: v.nodes[0]?.target?.join(' ') })); }
      catch (e) { axe = { error: e.message }; }
    }
    report.viewports[tag] = { navigationMs, captureElapsedMs: Date.now() - t0, consoleErrors: errors, measure: m, axe };
    await ctx.close();
    console.error(`[capture] ${tag}: ${errors.length} errors, axe ${Array.isArray(axe) ? axe.length + ' violations' : 'n/a'}, h1 lines ${m.h1s.map(h => h.lines).join('/') || '-'}, overflowX ${m.overflowX}`);
  }
}
await browser.close();
fs.writeFileSync(path.join(out, 'capture.json'), JSON.stringify(report, null, 1));
const serious = Object.values(report.viewports).flatMap(v => Array.isArray(v.axe) ? v.axe.filter(a => ['serious', 'critical'].includes(a.impact)) : []);
const errs = Object.values(report.viewports).flatMap(v => v.consoleErrors);
console.log(JSON.stringify({ out, screenshots: fs.readdirSync(out).filter(f => f.endsWith('.png')).length, consoleErrors: errs.length, axeSeriousOrCritical: serious.length }));
process.exitCode = (errs.length || serious.length) ? 1 : 0;
