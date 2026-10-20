---
name: design-system-builder
description: >
  Builds a new design system from scratch from one of four inputs: a product brief, inspiration screenshots, a brand color palette, or a mix. Produces design tokens (color scales, typography, spacing, shape, elevation, motion), light and dark themes, component specs, and a contrast-verified output. Use when the user asks to "create a design system", "create a color palette", "define a spacing/typography scale", "set up theming/dark mode", "design tokens" or "style guide" for a new product. Not for changing the tokens of an existing codebase, and not for single-component or one-off page work (e.g. "build a landing page", "style this button").
license: MIT
---

# Design System Builder

Builds a new design system from the input the user gives. Every run follows the same path: **identify the input mode → confirm a direction → build tokens → spec components → verify → deliver.**

## 1. Identify the input mode

| Mode | The user gives you | Direction comes from |
|---|---|---|
| **Autonomous** | A brief or nothing visual: "playful fintech app", a product type, an audience | You decide, from product type, audience and platform |
| **Screenshots** | Images of sites, apps or mockups they like | What you extract from the images |
| **Palette** | Hex/RGB/HSL values, a palette image, a logo, or brand colors | The palette is fixed; you design everything else around it |
| **Mixed** | Screenshots plus a palette | Palette wins for color. Screenshots drive type, spacing, shape, elevation and tone |

Edge inputs:

- **Text-only brief** (no colors, no images) → Autonomous.
- **Logo image** → treat as Palette: pull the dominant brand colors from it.
- **URL or Figma link** you cannot open or view → say so, and ask for screenshots or exported colors. Never invent what the page looks like.
- **A single brand color or a font name only** → Palette mode with a sparse input (see §3).
- **Screenshots of a named competitor or product with "make it like this"** → extract tone and structure, but build original tokens. Do not reproduce their exact palette or branding.

## 2. Minimum inputs, then ask once

You need these before building. Take whatever the user already stated and ask for the rest **in a single batch**, never one question at a time:

- Product type and audience (needed for Autonomous; helpful for all modes)
- Platform: web, native iOS/Android, or both. This decides the output format (§6).
- Accessibility target. **Default to WCAG 2.2 AA** if unstated.
- Light only, dark only, or both. **Default to both.**
- Anything fixed that you must keep: brand colors, fonts, an existing logo.

If the user says "just do it" or the session cannot be interactive, apply the defaults and list them as assumptions in the direction summary.

## 3. Establish and confirm the direction

Produce a **Direction Summary** before writing any tokens. It states, with concrete values: the color roles and brand hues (hex), neutral temperature, typeface choices, type scale ratio, spacing base and density, corner radius, elevation style, motion feel, and overall tone. Say why for each choice. Then **wait for the user to confirm or redirect.** The checkpoint applies to every mode. Skip the wait only if the user has said to proceed without confirming; in that case state the summary and continue.

Mode-specific rules:

**Autonomous.** Pick a direction that fits the product and audience, and justify it in a sentence each. Avoid defaulting to a generic blue-and-gray palette without a reason.

**Screenshots.**
- Extract palette, type style, spacing density, corner radius, elevation and tone. Do not copy layout or branding.
- Colors read from images are **approximations**. Say so, and round to clean values.
- If screenshots disagree (e.g. one light, one dark, or two unrelated palettes), report the conflict in the summary and propose which signal wins, rather than averaging them.
- JPEG artifacts, gradients and photos distort sampling. Use flat UI regions and note low confidence where relevant.

**Palette.**
- Brand colors are fixed inputs. Build tonal scales and semantic roles around them.
- Check every text/background pairing at the target contrast level (default AA). **Never silently change a brand color.** When a pair fails: report it, propose the nearest passing alternative (a darker or lighter step, or a different pairing), and keep the original brand value available for logos and decorative use.
- **Sparse palettes.** With only one brand color, derive the neutrals, the secondary/accent (if needed) and the success/warning/error roles yourself, and mark them as derived in the summary. If the palette has no neutrals or feedback colors, derive those the same way.
- Match the palette's temperature when deriving neutrals: tint them slightly toward the brand hue.

**Mixed.** Palette defines brand colors. Screenshots define type, spacing, shape, elevation and tone. Neutrals and feedback colors come from the palette if present; otherwise derive them to suit the screenshots' tone.

## 4. Build

### Token architecture (three layers)

1. **Primitive**: raw values. `--primitive-{category}-{name}`. Never used by components directly.
2. **Semantic**: purpose-based, pointing at primitives. `--color-text-primary`, `--space-section-gap`, `--radius-control`. This is the layer product code uses.
3. **Component**: per-component decisions pointing at semantic tokens. `--button-primary-bg`, `--input-border-focus`.

See [references/tokens.example.css](references/tokens.example.css) for a complete, checker-verified example of all three layers, both themes, and the accessibility media queries. It shows structure and completeness, **not a palette to reuse.**

### Token rules

- **No raw values in the semantic or component layers.** Everything points at a token one layer down (e.g. no literal `white`).
- **Every fill that carries text gets an `on-*` partner** (`--color-primary` / `--color-on-primary`, the same for success, warning, error, info). No hardcoded `white` or `black` for text on color.
- **Define every primitive you reference.** Each hue used gets a full 50–950 scale (the example abbreviates green/amber/red for brevity; real output should not).
- **Complete categories.** Color, spacing, typography (family, size, weight, line-height, letter-spacing), radius, shadow/elevation, z-index, motion (duration, easing), focus ring. Document breakpoints too, in comments or the docs, since `var()` cannot be used inside `@media`.
- **Scales must be derivable.** Type: a modular ratio (state it). Spacing: a base unit (state it) with deliberate gaps. Color: even lightness steps tuned per hue, not one chroma value for all steps.
- **Color in OKLCH, in sRGB gamut.** The checker warns on out-of-gamut values. Lower the chroma, or state explicitly that you are targeting Display-P3. Provide hex fallbacks (`check_contrast.py --hex` prints them) when supporting browsers without `oklch()`.
- **Sizes in `rem`** so user font-size settings and zoom work.
- **Consistent naming**: kebab-case, same word order everywhere. Figma maps by replacing `-` with `/` at role boundaries (`--color-text-primary` ↔ `color/text/primary`).

### Theming and dark mode

- Build light and dark unless told otherwise. A dark theme **overrides every color token whose value should change**, not a handful. This includes surfaces, borders, brand, feedback, shadows and on-colors.
- Dark themes use lighter, less saturated brand and feedback colors. **Hover and active states get lighter on dark surfaces**, not darker.
- Support both an explicit toggle (`[data-theme="dark"]`) and the OS preference (`@media (prefers-color-scheme: dark)`). The toggle wins: `:root:not([data-theme="light"])` inside the media query. Set `color-scheme` on each theme.

### Components

Pick the inventory from the product. A typical set: Button, Input, Select, Checkbox/Radio/Switch, Card, Badge, Alert/Toast, Modal, Tabs, Tooltip. **Fully specify at least Button, Input, Card and Alert**, and list the rest with their variants and states.

Each spec covers: variants, sizes, states (default, hover, active, focus-visible, disabled, loading, error where applicable), component tokens used, composition rules, accessibility requirements, and a do/don't.

Accessibility requirements that apply to every interactive component:
- Visible focus indicator (`:focus-visible`) with ≥3:1 contrast against its surroundings, via a focus-ring token.
- Pointer targets ≥44px (WCAG 2.5.8 requires 24px minimum, platforms recommend 44px). If the visual size is smaller, grow the hit area or switch to 44px on `(pointer: coarse)`. Specs must not contradict this (e.g. a 32px button with a "44px target" line and no mechanism).
- Disabled and loading states use `aria-disabled` / `aria-busy` where the element must stay focusable.
- Feedback states (success/warning/error) never rely on color alone: include an icon or text.
- Respect `prefers-reduced-motion` (collapse durations) and `forced-colors` (fall back to system colors for focus and borders).

## 5. Verify before delivering

1. Run the contrast checker on the generated CSS:
   ```
   python3 -I scripts/check_contrast.py design-system/tokens.css
   ```
   It resolves `var()` chains, checks both themes, tests the standard text/surface, on-color/fill, border and focus-ring pairs (text 4.5:1, non-text UI 3:1), and warns about out-of-gamut colors. Add custom pairs with `--pair FG BG MIN` for any extra tokens (e.g. a secondary accent).
2. Fix every FAIL by adjusting the **derived** tokens or step choice. For Palette-mode brand colors, follow the failure rule in §3 instead of editing the brand value.
3. Confirm no `var()` references an undefined token (the checker errors on these) and that both themes pass.
4. Paste the final checker summary into the contrast report deliverable. If you could not run it, say so plainly instead of claiming the pairs pass.

## 6. Deliverables and output format

Write files to `design-system/` in the working directory, unless the user names a location:

| File | Contents |
|---|---|
| `tokens.css` | All three layers, light and dark themes, accessibility media queries |
| `components.md` | Component specs (§4) |
| `README.md` | Direction summary and rationale, token naming guide, usage with do/don't examples, Figma naming map, short versioning notes |
| `contrast-report.txt` | The checker's output |

Format by platform:
- **Web (default)**: CSS custom properties.
- **Tailwind**: also emit a v4 `@theme` block (or a theme config for earlier versions) that maps to the semantic tokens.
- **Other tooling or multi-platform**: also emit W3C DTCG JSON (`tokens.json`), which Style Dictionary and Figma plugins consume.
- **Native iOS/Android**: emit the DTCG JSON plus a short mapping to platform primitives (Color/Font assets, `MaterialTheme`). Use dp/pt, not rem. Note that CSS-only pieces (media queries, `color-scheme`) don't apply.

Versioning notes (kept to a few lines in the README): semantic versioning for the token set, renaming or removing a token is a major change, and deprecate with a note for one release before removal.

## 7. Reply style

Chat replies stay short: the direction summary, the assumptions you made, the checker result, and the list of files written. The detail lives in the files. Explain the reasoning behind each major choice in a sentence, and flag anything derived or approximated.
