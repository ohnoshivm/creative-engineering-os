import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Decode PNG pixels: compression-byte diversity says nothing about rendering.
async function pixels(page: Page) {
  // Element screenshots include overlapping DOM. Hide the panel so text cannot fake a GPU signal.
  const png = await page.locator('#gl').screenshot({ style: '.panel { visibility: hidden !important; }' });
  return page.evaluate(async (base64) => {
    const image = new Image();
    image.src = `data:image/png;base64,${base64}`;
    await image.decode();
    const canvas = document.createElement('canvas');
    canvas.width = image.width; canvas.height = image.height;
    const ctx = canvas.getContext('2d')!;
    ctx.drawImage(image, 0, 0);
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let lit = 0, dark = 0;
    const colours = new Set<number>();
    for (let i = 0; i < data.length; i += 16) {
      const r = data[i], g = data[i + 1], b = data[i + 2];
      colours.add((r >> 3) * 1024 + (g >> 3) * 32 + (b >> 3));
      if (Math.max(r, g, b) > 70) lit++;
      if (Math.max(r, g, b) < 40) dark++;
    }
    const corner = [...ctx.getImageData(canvas.width - 8, canvas.height - 8, 1, 1).data].slice(0, 3);
    return { litFraction: lit / (data.length / 16), darkFraction: dark / (data.length / 16), colours: colours.size, corner };
  }, png.toString('base64'));
}

test('each experiment has a visible signal and dark ground, with no shader errors', async ({ page }, info) => {
  test.skip(['no-webgl', 'no-js'].includes(info.project.name));
  const errors: string[] = [];
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', (e) => errors.push(e.message));
  for (const exp of ['raymarch', 'feedback']) {
    await page.goto(`/?exp=${exp}&still`);
    await expect(page.locator('html')).toHaveAttribute('data-lab', exp);
    const sample = await pixels(page);
    expect(sample.litFraction, `${exp}: visible geometry/ink`).toBeGreaterThan(0.002);
    expect(sample.darkFraction, `${exp}: dark ground`).toBeGreaterThan(0.2);
    expect(sample.colours, `${exp}: shaded colour range`).toBeGreaterThan(30);
    if (exp === 'raymarch') {
      // RawShaderMaterial does not inject Three's output chunk. One encoding gives ~22–25;
      // missing encoding gives ~1 and double encoding gives ~84.
      [0.0045, 0.005, 0.006].forEach((linear, i) => {
        expect(Math.abs(sample.corner[i] - Math.pow(linear, 1 / 2.2) * 255)).toBeLessThan(2);
      });
    }
  }
  expect(errors).toEqual([]);
});

test('switcher works by keyboard, preserves still mode and exposes visible focus', async ({ page }, info) => {
  test.skip(['no-webgl', 'no-js', 'mobile'].includes(info.project.name));
  await page.goto('/?exp=raymarch&still');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('button', { name: 'Raymarch' })).toBeFocused();
  await page.keyboard.press('Tab');
  const feedback = page.getByRole('button', { name: 'Feedback' });
  await expect(feedback).toBeFocused();
  expect(await feedback.evaluate((b) => getComputedStyle(b).outlineStyle)).not.toBe('none');
  await page.keyboard.press('Enter');
  await expect(feedback).toHaveAttribute('aria-pressed', 'true');
  await expect(page).toHaveURL(/still/);
  expect((await pixels(page)).litFraction).toBeGreaterThan(0.002);
});

test('unknown and prototype experiment names fall back safely', async ({ page }, info) => {
  test.skip(info.project.name !== 'desktop');
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(e.message));
  for (const exp of ['missing', 'constructor', '__proto__', 'toString']) {
    await page.goto(`/?exp=${exp}&still`);
    await expect(page.locator('html')).toHaveAttribute('data-lab', 'raymarch');
    await expect(page.getByRole('button', { name: 'Raymarch' })).toHaveAttribute('aria-pressed', 'true');
  }
  expect(errors).toEqual([]);
});

test('reduced motion stays static and repaints after resize', async ({ page }, info) => {
  test.skip(info.project.name !== 'reduced-motion');
  await page.goto('/?exp=raymarch');
  await expect(page.locator('#stat')).toHaveText('Reduced motion: showing a single frame.');
  const before = await page.locator('#gl').screenshot();
  await page.waitForTimeout(250);
  expect(await page.locator('#gl').screenshot()).toEqual(before);
  await page.setViewportSize({ width: 768, height: 1024 });
  expect((await pixels(page)).litFraction).toBeGreaterThan(0.002);
});

test('capability fallback is readable and controls are disabled', async ({ page }, info) => {
  test.skip(!['no-webgl', 'no-js'].includes(info.project.name));
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(e.message));
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Graphics lab' })).toBeVisible();
  if (info.project.name === 'no-webgl') await expect(page.locator('#fallback')).toBeVisible();
  else await expect(page.locator('noscript .fallback')).toBeVisible();
  for (const button of await page.getByRole('button').all()) await expect(button).toBeDisabled();
  expect(errors).toEqual([]);
});

test('responsive layout and no serious or critical axe violations', async ({ page }, info) => {
  test.skip(info.project.name === 'no-js');
  await page.goto('/?still');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
  expect(result.violations.filter((v) => ['serious', 'critical'].includes(v.impact ?? '')).map((v) => v.id)).toEqual([]);
});

for (const exp of ['raymarch', 'feedback']) {
  test(`${exp} still frame @visual`, async ({ page }, info) => {
    test.skip(['no-webgl', 'no-js', 'reduced-motion'].includes(info.project.name));
    await page.goto(`/?exp=${exp}&still`);
    await expect(page.locator('html')).toHaveAttribute('data-lab', exp);
    await expect(page).toHaveScreenshot(`${exp}-${info.project.name}.png`, { animations: 'disabled', maxDiffPixelRatio: 0.01 });
  });
}
