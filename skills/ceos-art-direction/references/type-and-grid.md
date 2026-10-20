# Type and grid — working numbers

## Fluid type steps (example; recompute per project)

```css
:root {
  --step-small: clamp(0.8125rem, 0.78rem + 0.15vw, 0.9375rem);  /* 13–15px  captions, meta   */
  --step-body:  clamp(1.0625rem, 1rem + 0.3vw, 1.25rem);        /* 17–20px  running text     */
  --step-lead:  clamp(1.375rem, 1.1rem + 1vw, 2rem);            /* 22–32px  intro, statements*/
  --step-head:  clamp(2.25rem, 1.4rem + 3.6vw, 4.5rem);         /* 36–72px  section heads    */
  --step-display: clamp(3.5rem, 1.6rem + 8.4vw, 10rem);         /* 56–160px hero only        */
}
h1, h2, h3 { text-wrap: balance; }  p { text-wrap: pretty; }
.display { letter-spacing: -0.035em; line-height: 0.92; }
.small   { letter-spacing: 0.01em; }
```

## Measure

`max-width: 66ch` on running text; 38–45ch for captions beside images.

## Grid

```css
:root { --margin: clamp(16px, 2.5vw, 40px); --gutter: clamp(12px, 1.6vw, 24px); --cols: 12; }
.grid { display: grid; grid-template-columns: repeat(var(--cols), 1fr); column-gap: var(--gutter); padding-inline: var(--margin); }
@media (max-width: 760px) { :root { --cols: 6; } }
```

## Font loading without layout shift

```css
@font-face { font-family: "Brand"; src: url(/fonts/brand.woff2) format("woff2"); font-display: swap; }
@font-face { font-family: "Brand Fallback"; src: local("Arial"); size-adjust: 104%; ascent-override: 92%; descent-override: 24%; }
body { font-family: "Brand", "Brand Fallback", system-ui, sans-serif; }
```
Measure the overrides with a tool such as Fontaine/capsize rather than guessing.

## Contrast

WCAG 2.x: 4.5:1 normal text, 3:1 large text (≥24px or ≥18.66px bold) and UI components. Compute; don't eyeball.
