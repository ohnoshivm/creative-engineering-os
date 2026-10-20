---
name: ceos-interaction-architecture
description: Designs information architecture, user journeys and the interaction model of a website — navigation and route transitions, pointer, touch, gesture and keyboard behaviour, focus management, semantic structure, state machines for complex UI, and spatial/3D interfaces — with accessibility built in. Use when planning a sitemap or journey, designing menus, transitions, drag/scroll/gesture interactions, interactive 3D navigation, forms and enquiry flows, or when an interaction feels confusing or breaks for keyboard/touch users.
---

# UX and interaction architecture

## Purpose

Make an ambitious experience *operable and understandable* by everyone, on every input, without diluting it.

## Expert knowledge to apply

- **Journey first**: arrive → understand what this is (≤5 s) → feel the point of view → see proof → find fit →
  act. Every page has one primary action, visible without needing to discover a gesture.
- **IA**: navigation labels named by what users want, 3–6 top-level items, one persistent primary CTA. Every important
  piece of content is reachable by a normal link and crawlable HTML.
- **Input parity**: pointer, touch, keyboard and assistive tech each have a complete path. Hover only *enhances*;
  nothing essential is hover-only. Touch targets ≥ 44×44 CSS px (WCAG 2.5.8 minimum 24×24).
- **Keyboard**: logical DOM order = visual order; visible `:focus-visible` style with ≥3:1 contrast; skip link;
  Escape closes overlays and returns focus to the trigger; closed menus are `inert`/hidden (no tabbing into invisible
  links); focus moves into dialogs and is contained; custom scrollers scroll the focused element into view.
- **Scroll**: never hijack native scroll semantics. If smoothing, keep wheel/keys/PageUp/Down/Home/End/Space,
  anchor links and find-in-page working. Snapping only where content is genuinely paged. Back/forward restores place.
- **Transitions**: preserve spatial continuity (the thing you clicked becomes the thing you see); route changes
  update `<title>`, focus the new `<h1>` or main, announce via the router, and work with Back. Use the View
  Transitions API where supported, with a plain navigation fallback.
- **Gestures**: discoverable (affordance or hint), bounded (springs back), cancellable, never the only path.
  Distinguish drag vs. scroll on touch with `touch-action`.
- **Spatial / 3D UI**: give users orientation (where am I, what can I do), make 3D hotspots real buttons in the DOM
  (positioned over canvas) with names, and provide a list view of the same content.
- **State machines**: model complex UI (menus with sub-states, loaders, multi-step forms, scene modes) as explicit
  states + events (statecharts). Impossible states impossible; every state has enter/exit and an interrupt path.
- **Forms**: labels always visible, inline validation on blur, errors that say how to fix, success that says what
  happens next, works without JS where possible, spam protection that doesn't punish humans.

## Inputs

Approved concept, content inventory, art direction draft, conversion goal.

## Decision procedure

1. Sitemap + primary journeys (as lists or a Mermaid flow).
2. Per page: sections in order with the claim each makes and the action available.
3. Interaction inventory table: element · input (pointer/touch/keyboard/AT) · behaviour · states · feedback ·
   reduced-motion behaviour · no-JS/no-WebGL behaviour.
4. State charts for any component with more than 3 states.
5. Accessibility plan: landmarks, heading outline, focus order, live regions, contrast owner.

## Verification

- Keyboard-only walkthrough of every journey (record tab order; screenshot focus states).
- Screen-reader smoke test (VoiceOver: rotor headings/landmarks/links read sensibly).
- axe-core: 0 serious/critical. Touch run at 390 px with emulated touch.
- Back/forward and reload preserve position on long pages and route transitions.

## Failure criteria

Essential content inside canvas only; gesture-only navigation; invisible focus; focus trapped in hidden menus;
scroll hijacked; route change without focus management; hover-only reveals; form errors that only turn red.

## Output

`docs/UX.md`: sitemap, journeys, interaction inventory, state charts, accessibility plan.
