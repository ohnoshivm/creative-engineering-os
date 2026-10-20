import {test,expect} from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
test('content, console and responsive layout',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await page.goto('/');await expect(page.getByRole('heading',{name:'Signal study.'})).toBeVisible();
 await page.waitForFunction(()=>!!document.documentElement.dataset.stage);
 await page.getByRole('link',{name:'Read the study'}).click();await expect(page.getByRole('heading',{name:'One surface. Several ways in.'})).toBeInViewport();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBeTruthy();expect(errors).toEqual([]);
});
test('stage capability and no-webgl poster',async({page},info)=>{
 await page.goto('/');await page.waitForFunction(()=>!!document.documentElement.dataset.stage);
 if(info.project.name==='no-webgl'){await expect(page.locator('html')).toHaveAttribute('data-stage','poster');await expect(page.locator('.poster')).toBeVisible();}
 else{await expect(page.locator('html')).toHaveAttribute('data-stage','live');expect(await page.locator('.stage').getAttribute('data-draws')).toBe('1');}
});
test('keyboard focus and tension control',async({page},info)=>{
 test.skip(info.project.name==='mobile');await page.goto('/');await page.keyboard.press('Tab');await expect(page.getByRole('link',{name:'Skip to content'})).toBeFocused();
 await page.keyboard.press('Tab');await page.keyboard.press('Tab');const slider=page.getByRole('slider',{name:'Surface tension'});await expect(slider).toBeFocused();await page.keyboard.press('ArrowRight');await expect(slider).toHaveValue('41');await expect(page.locator('output')).toHaveText('41%');
 expect(await slider.evaluate(el=>getComputedStyle(el).outlineStyle)).not.toBe('none');
});
test('pause stops frames and resumes',async({page},info)=>{
 test.skip(['reduced-motion','no-webgl'].includes(info.project.name));await page.goto('/');await page.waitForFunction(()=>document.documentElement.dataset.stage==='live');
 const button=page.locator('#pause');await button.click();await expect(button).toHaveAttribute('aria-pressed','true');await page.waitForTimeout(150);const before=await page.locator('canvas').screenshot();await page.waitForTimeout(350);expect(await page.locator('canvas').screenshot()).toEqual(before);await button.click();await expect(button).toHaveText('Pause motion');
});
test('native scroll and pointer change the wave',async({page},info)=>{
 test.skip(['reduced-motion','no-webgl','mobile'].includes(info.project.name));await page.goto('/');await page.waitForFunction(()=>document.documentElement.dataset.stage==='live');const stage=page.locator('.stage');await page.mouse.move(1100,450);await expect.poll(()=>stage.getAttribute('data-pointer')).not.toBe('0.000');await page.mouse.wheel(0,300);await expect.poll(async()=>Number(await stage.getAttribute('data-phase'))).toBeGreaterThan(.05);expect(await page.evaluate(()=>scrollY)).toBeGreaterThan(100);
});
test('reduced motion stays still and content remains complete',async({page},info)=>{
 test.skip(info.project.name!=='reduced-motion');await page.goto('/');await page.waitForFunction(()=>document.documentElement.dataset.stage==='live');const before=await page.locator('canvas').screenshot();await page.mouse.move(800,400);await page.waitForTimeout(350);expect(await page.locator('canvas').screenshot()).toEqual(before);await page.getByRole('slider').fill('80');await expect(page.locator('output')).toHaveText('80%');await page.locator('#reading').scrollIntoViewIfNeeded();await expect(page.locator('#reading')).toBeVisible();expect(await page.evaluate(()=>document.querySelector('#reading')&&getComputedStyle(document.querySelector('#reading')!).opacity)).toBe('1');
});
test('axe has no serious or critical violations',async({page})=>{
 await page.goto('/?still');await page.waitForFunction(()=>!!document.documentElement.dataset.stage);const result=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();expect(result.violations.filter(v=>['serious','critical'].includes(v.impact||'')).map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))).toEqual([]);
});
test('complete HTML without JavaScript',async({browser})=>{
 const context=await browser.newContext({javaScriptEnabled:false});const page=await context.newPage();await page.goto('http://localhost:4184');await expect(page.getByRole('heading',{name:'Signal study.'})).toBeVisible();await expect(page.locator('.poster')).toBeVisible();await page.getByRole('link',{name:'Read the study'}).click();await expect(page.locator('#reading')).toBeInViewport();await context.close();
});
test('instructions match input and motion preference',async({page},info)=>{await page.goto('/');if(info.project.name==='reduced-motion')await expect(page.locator('#instructions')).toHaveText('Still view. Adjust Surface tension below.',{useInnerText:true});else if(info.project.name==='mobile')await expect(page.locator('#instructions')).toHaveText('Adjust Surface tension below. Scroll to shift the phase.',{useInnerText:true});else await expect(page.locator('#instructions')).toHaveText('Move across the surface. Scroll to shift its phase.',{useInnerText:true});});
test('controls fit desktop and tablet viewports',async({page},info)=>{test.skip(info.project.name!=='desktop');for(const size of [{width:1440,height:900},{width:1024,height:768}]){await page.setViewportSize(size);await page.goto('/?still');const bounds=await page.locator('.controls').boundingBox();expect(bounds!.y+bounds!.height).toBeLessThanOrEqual(size.height);await expect(page.locator('#pause')).toBeInViewport();}});
test('first screen @visual',async({page},info)=>{test.skip(info.project.name==='no-webgl');await page.goto('/?still');await page.waitForFunction(()=>!!document.documentElement.dataset.stage);await expect(page).toHaveScreenshot(`first-${info.project.name}.png`,{animations:'disabled',maxDiffPixelRatio:.01});});
