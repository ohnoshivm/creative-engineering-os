import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('smoke', () => {
  test('loads with content, no console errors, h1 visible', async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(e.message));
    await page.goto('/');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Start a project' })).toBeVisible();
    await page.waitForTimeout(1500);
    expect(errors).toEqual([]);
  });

  test('stage state matches capability', async ({ page }, info) => {
    await page.goto('/');
    if (info.project.name === 'no-js') {
      await expect(page.locator('.poster')).toBeVisible();
      await expect(page.locator('[data-stage] canvas')).toHaveCount(0);
      return;
    }
    await page.waitForFunction(() => !!document.documentElement.dataset.stage, null, { timeout: 10_000 });
    const state = await page.evaluate(() => document.documentElement.dataset.stage);
    if (info.project.name === 'no-webgl') {
      expect(state).toBe('poster');
      await expect(page.locator('.poster')).toBeVisible();
    } else {
      expect(state).toBe('live');
      await expect(page.locator('[data-stage] canvas')).toHaveCount(1);
    }
  });

  test('primary action reachable by keyboard with visible focus', async ({ page }, info) => {
    test.skip(info.project.name === 'mobile', 'keyboard path tested on desktop projects');
    await page.goto('/');
    await page.keyboard.press('Tab'); // skip link
    await expect(page.getByRole('link', { name: 'Skip to content' })).toBeFocused();
    for (let i = 0; i < 6; i++) {
      await page.keyboard.press('Tab');
      if (await page.getByRole('link', { name: 'Start a project' }).evaluate((el) => el === document.activeElement)) break;
    }
    const focused = page.getByRole('link', { name: 'Start a project' });
    await expect(focused).toBeFocused();
    const outline = await focused.evaluate((el) => getComputedStyle(el).outlineStyle);
    expect(outline).not.toBe('none');
  });

  test('no serious or critical axe violations', async ({ page }, info) => {
    test.skip(info.project.name === 'no-js', 'axe injects JavaScript; other projects cover the same HTML');
    await page.goto('/');
    await page.waitForTimeout(1200);
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
    const serious = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
    expect(serious.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).slice(0, 5).join(', ')}`)).toEqual([]);
  });

  test('reduced motion shows all content without travel', async ({ page }, info) => {
    test.skip(info.project.name !== 'reduced-motion');
    await page.goto('/');
    await page.locator('#system').scrollIntoViewIfNeeded();
    const hidden = await page.$$eval('main p, main li, main h2', (els) => els.filter((e) => +getComputedStyle(e).opacity < 0.99).length);
    expect(hidden).toBe(0);
  });
});

test('scrolling reveals all section copy', async ({ page }, info) => {
  test.skip(info.project.name !== 'desktop');
  await page.goto('/');
  for (const section of await page.locator('main section:not(.hero)').all()) {
    await section.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1100);
    for (const copy of await section.locator('h2, p, li').all()) {
      expect(await copy.evaluate((el) => +getComputedStyle(el).opacity)).toBeGreaterThan(0.99);
    }
  }
});

test('reduced-motion ribbon remains drawn after resizing', async ({ page }, info) => {
  test.skip(info.project.name !== 'reduced-motion');
  await page.goto('/');
  await expect(page.locator('html')).toHaveAttribute('data-stage', 'live');
  const colourCount = async () => {
    const png = await page.locator('.stage').screenshot();
    return page.evaluate(async (base64) => {
      const image = new Image(); image.src = `data:image/png;base64,${base64}`; await image.decode();
      const canvas = document.createElement('canvas'); canvas.width = image.width; canvas.height = image.height;
      const ctx = canvas.getContext('2d')!; ctx.drawImage(image, 0, 0);
      const rgba = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
      const colours = new Set<number>();
      for (let i = 0; i < rgba.length; i += 16) colours.add((rgba[i] >> 3) * 1024 + (rgba[i + 1] >> 3) * 32 + (rgba[i + 2] >> 3));
      return colours.size;
    }, png.toString('base64'));
  };
  expect(await colourCount()).toBeGreaterThan(100);
  await page.setViewportSize({ width: 768, height: 1024 });
  await page.waitForTimeout(200);
  expect(await colourCount()).toBeGreaterThan(100);
});

test('first screen @visual', async ({ page }, info) => {
  test.skip(['no-webgl', 'no-js'].includes(info.project.name));
  await page.goto('/?still');
  await page.waitForFunction(() => !!document.documentElement.dataset.stage);
  await page.waitForTimeout(800);
  await expect(page).toHaveScreenshot(`first-${info.project.name}.png`, { animations: 'disabled', maxDiffPixelRatio: 0.02 });
});
