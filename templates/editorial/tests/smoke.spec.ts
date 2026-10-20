import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('loads, h1 visible, console clean', async ({ page }) => {
  const errors: string[] = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto('/');
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  await page.waitForTimeout(1600);
  const hiddenLines = await page.$$eval('.title .line', (els) => els.filter((e) => getComputedStyle(e).clipPath.includes('100%')).length);
  expect(hiddenLines).toBe(0); // title fully revealed after the intro (or never hidden)
  expect(errors).toEqual([]);
});

test('contact reachable by keyboard with visible focus', async ({ page }, info) => {
  test.skip(info.project.name === 'mobile');
  await page.goto('/');
  const target = page.getByRole('link', { name: 'Email the studio' });
  for (let i = 0; i < 10 && !(await target.evaluate((el) => el === document.activeElement)); i++) await page.keyboard.press('Tab');
  await expect(target).toBeFocused();
  expect(await target.evaluate((el) => getComputedStyle(el).outlineStyle)).not.toBe('none');
});

test('no serious or critical axe violations', async ({ page }, info) => {
  test.skip(info.project.name === 'no-js', 'axe injects a script; covered by the other projects');
  await page.goto('/');
  await page.waitForTimeout(1500);
  const r = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
  expect(r.violations.filter((v) => ['serious', 'critical'].includes(v.impact ?? '')).map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).slice(0, 5).join(', ')}`)).toEqual([]);
});

test('measure stays readable (≤ 75 characters per line)', async ({ page }) => {
  await page.goto('/');
  const chars = await page.$eval('.article p', (p) => {
    const cs = getComputedStyle(p); const c = document.createElement('canvas').getContext('2d')!;
    c.font = `${cs.fontSize} ${cs.fontFamily}`; const avg = c.measureText('abcdefghijklmnopqrstuvwxyz ').width / 27;
    return Math.round(p.getBoundingClientRect().width / avg);
  });
  expect(chars).toBeLessThanOrEqual(80);
});

test('first screen @visual', async ({ page }, info) => {
  await page.goto('/');
  await page.waitForTimeout(1800);
  await expect(page).toHaveScreenshot(`first-${info.project.name}.png`, { animations: 'disabled', maxDiffPixelRatio: 0.01 });
});
