import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('loads, h1 readable, console clean', async ({ page }) => {
  const errors: string[] = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1, name: 'Every word arrives on the beat.' })).toBeVisible();
  await page.waitForTimeout(1500);
  expect(errors).toEqual([]);
});

test('read-along lights words as you scroll and the tempo run moves horizontally', async ({ page }, info) => {
  test.skip(info.project.name !== 'desktop');
  await page.goto('/');
  await page.waitForTimeout(800);
  const litBefore = await page.$$eval('[data-readalong] .w', (ws) => ws.filter((w) => +getComputedStyle(w).opacity > 0.9).length);
  await page.evaluate(() => window.scrollTo(0, document.querySelector<HTMLElement>('.read')!.offsetTop + innerHeight * 1.2));
  await page.waitForTimeout(1200);
  const litAfter = await page.$$eval('[data-readalong] .w', (ws) => ws.filter((w) => +getComputedStyle(w).opacity > 0.9).length);
  expect(litAfter).toBeGreaterThan(litBefore);
  const x0 = await page.$eval('.tempo-track', (t) => new DOMMatrix(getComputedStyle(t).transform).m41);
  await page.evaluate(() => { const s = document.querySelector<HTMLElement>('.tempos')!; window.scrollTo(0, s.getBoundingClientRect().top + scrollY + innerHeight); });
  await page.waitForTimeout(1200);
  const x1 = await page.$eval('.tempo-track', (t) => new DOMMatrix(getComputedStyle(t).transform).m41);
  expect(x1).toBeLessThan(x0 - 100);
});

test('reduced motion and no-JS show every word at full strength', async ({ page }, info) => {
  test.skip(!['reduced-motion', 'no-js'].includes(info.project.name));
  await page.goto('/');
  const faint = await page.$$eval('main p, main h1, main li', (els) => els.filter((e) => +getComputedStyle(e).opacity < 0.99).length);
  expect(faint).toBe(0);
  expect(await page.$eval('html', (h) => h.classList.contains('js-motion'))).toBe(false);
});

test('keyboard reaches the action with visible focus', async ({ page }, info) => {
  test.skip(info.project.name === 'mobile');
  await page.goto('/');
  const target = page.getByRole('link', { name: 'Book a session' });
  for (let i = 0; i < 6 && !(await target.evaluate((el) => el === document.activeElement)); i++) await page.keyboard.press('Tab');
  await expect(target).toBeFocused();
  expect(await target.evaluate((el) => getComputedStyle(el).outlineStyle)).not.toBe('none');
});

test('no serious or critical axe violations', async ({ page }, info) => {
  test.skip(info.project.name === 'no-js');
  await page.goto('/');
  await page.waitForTimeout(1200);
  const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
  expect(r.violations.filter((v) => ['serious', 'critical'].includes(v.impact ?? '')).map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).slice(0, 5).join(', ')}`)).toEqual([]);
});

test('first screen @visual', async ({ page }, info) => {
  await page.goto('/');
  await page.waitForTimeout(1800);
  await expect(page).toHaveScreenshot(`first-${info.project.name}.png`, { animations: 'disabled', maxDiffPixelRatio: 0.01 });
});
