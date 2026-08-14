---
version: alpha
name: Signal
description: A dark, bold, instrument-grade system for a horizontally-scrolling data story about what GitHub paid attention to.
theme: dark-only
colors:
  ground:        { dark: "#0A0A0F" }
  groundSunken:  { dark: "#06060A" }
  surface:       { dark: "#14141B" }
  surfaceRaised: { dark: "#1D1D26" }
  textPrimary:   { dark: "#F2F4F7" }
  textSecondary: { dark: "#C0C6CF" }
  textMuted:     { dark: "#8B94A0" }
  border:        { dark: "#26262F" }
  borderStrong:  { dark: "#3A3A47" }
  focusRing:     { dark: "#FDB1A9" }
  primary:       { dark: "#FA4544" }
  onPrimary:     { dark: "#0A0A0F" }
  accent:        { dark: "#B9FA31" }
  onAccent:      { dark: "#0A0A0F" }
  success:       { dark: "#10A8A3" }
  warning:       { dark: "#D68A00" }
  danger:        { dark: "#B267E4" }
  info:          { dark: "#048FF4" }
charts:
  categorical:    ["#FA4544", "#2A92BB", "#769F26", "#B5297B", "#A98C35"]
  sequential:     ["#C2D3E8", "#9CB3D1", "#7A94B7", "#5A769A", "#415A79"]
  divergingAI:    ["#B1C4EC", "#6D95EE", "#4B70C6", "#264698"]
  divergingNotAI: ["#FCDD60", "#C7A92A", "#967F1C", "#6B5A10"]
  divergingMid:   "#74747A"
  gridline:       "#1D1D26"
  axis:           "#3A3A47"
  deemphasis:     "#4A4A57"
typography:
  fontFamily:
    text: Geist
    numeric: Martian Mono
  ratio: "fluid (clamp), ~1.5 at display sizes"
  scale:
    hero:      { size: "clamp(64px, 9.5vw, 168px)", lineHeight: 0.9,  weight: 700, letterSpacing: "-0.055em", family: numeric }
    figureLg:  { size: "clamp(36px, 4.5vw, 72px)",  lineHeight: 1.0,  weight: 700, letterSpacing: "-0.04em",  family: numeric }
    display1:  { size: "clamp(52px, 7vw, 120px)",   lineHeight: 0.94, weight: 600, letterSpacing: "-0.035em", family: text }
    display2:  { size: "clamp(38px, 4.5vw, 72px)",  lineHeight: 1.0,  weight: 600, letterSpacing: "-0.03em",  family: text }
    headline:  { size: "clamp(26px, 2.6vw, 40px)",  lineHeight: 1.1,  weight: 600, letterSpacing: "-0.02em",  family: text }
    bodyLg:    { size: "clamp(17px, 1.3vw, 21px)",  lineHeight: 1.5,  weight: 400, letterSpacing: "-0.01em",  family: text }
    body:      { size: "16px",                      lineHeight: 1.6,  weight: 400, letterSpacing: "0",        family: text }
    bodySm:    { size: "14px",                      lineHeight: 1.5,  weight: 400, letterSpacing: "0",        family: text }
    label:     { size: "12px",                      lineHeight: 1.2,  weight: 500, letterSpacing: "0.08em",   family: numeric }
    figure:    { size: "inherit",                   lineHeight: 1,    weight: 500, letterSpacing: "-0.01em",  family: numeric }
    micro:     { size: "11px",                      lineHeight: 1.2,  weight: 400, letterSpacing: "0.04em",   family: numeric }
spacing: { xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 40px, 2xl: 64px, 3xl: 104px }
radius:  { sm: 3px, md: 6px, lg: 12px, pill: 999px, none: 0 }
elevation:
  sm: "0 1px 2px rgba(0,0,0,0.55)"
  md: "0 6px 20px rgba(0,0,0,0.6)"
  lg: "0 18px 56px rgba(0,0,0,0.7)"
  glow: "0 0 0 1px #26262F, 0 8px 40px rgba(250,69,68,0.22)"
motion:
  easeOut:    "cubic-bezier(0.22, 1, 0.36, 1)"
  easeInOut:  "cubic-bezier(0.65, 0, 0.35, 1)"
  duration:   { instant: 120ms, fast: 240ms, base: 420ms, slow: 720ms, beat: 1100ms }
  scrollLerp: 0.085
components:
  stageRail:
    variants: [ default ]
    states:   [ rest, active, visited, hover, focus ]
  controlBar:
    variants: [ narrative, explorer ]
    states:   [ rest, expanded ]
  beatPanel:
    variants: [ statement, chart, split, board ]
    states:   [ offscreen, entering, active, leaving ]
  chartFrame:
    variants: [ default, wide, full ]
    states:   [ loading, ready, empty, error ]
  heroFigure:
    variants: [ default, withUnit ]
    states:   [ rest, counting ]
  repoCard:
    variants: [ default, compact, feature ]
    states:   [ rest, hover, focus ]
  filterChip:
    variants: [ default, poleAI, poleNotAI ]
    states:   [ rest, hover, selected, focus, disabled ]
  button:
    variants: [ primary, ghost, quiet ]
    states:   [ rest, hover, active, focus, disabled ]
  statusMessage:
    variants: [ info, success, warning, danger ]
    states:   [ visible ]
  tooltip:
    variants: [ point, crosshair ]
    states:   [ hidden, visible ]
  dataTable:
    variants: [ inline, virtualized ]
    states:   [ loading, ready, empty ]
---

# Signal Design System

## How to build with this
> Read this file before building any UI. `design-system/design.md` is the single source of truth; `design.html`
> and the token file are generated from it — edit this file, then regenerate them, never the reverse.
> Bind every visual value to a token (`var(--…)`); never hardcode a hex/px that has a token. Use only the
> variants and states listed per component — the lists are CLOSED. If a feature needs a token, variant, or
> component that isn't defined here, STOP and flag the user, then add it to this file deliberately — do not
> improvise it. Honor the Do's and Don'ts; avoid the named clichés.

**This system is dark-only.** A deliberate deviation from the usual light+dark requirement, taken
because the story is designed as a single cinematic surface. No light theme is defined. Do not invent
one — if a light theme is ever wanted, it must be re-stepped from these ramps and re-validated against
a light surface, never derived by inverting these values.

## Overview

The subject is 262,902 GitHub repositories that all cleared 50 stars — a record of what people
*paid attention to*, not what they merely published. The system's job is to make a five-year
argument legible while scrolling sideways, then hand the reader an instrument to check it.

Two ideas organize everything:

**The palette and the argument are the same thing.** The story's central finding is a polarity —
repos are overwhelmingly AI-related or overwhelmingly not, with almost nothing in between. That
polarity is the brand: signal red reads as hot, urgent, alarm-adjacent — the AI pole; neon
chartreuse reads as radioactive, organic-but-synthetic — the not-AI pole. Both are used at full
saturation everywhere the polarity itself needs to show: buttons, chips, prose.

**The diverging chart is deliberately not brand-colored.** Red and chartreuse sit close enough on
the deuteranopia confusion axis that the `dataviz` validator collapses them to ΔE 1.4 (floor is 6,
target 8) — a red-green colorblind reader cannot tell the two arms of the Sankey apart by hue at
any lightness step; re-lightening one arm doesn't fix it; the hues themselves have to differ. So the
one chart that literally *is* the AI/not-AI polarity — `divergingAI` / `divergingNotAI` — runs its
own validated indigo/gold pair instead (worst cross-arm ΔE 21.6 deutan, 22.1 normal-vision). Brand
red and chartreuse still carry the polarity everywhere else — chip, button, prose — just not in
this one diverging scale.

**The numbers are the display face.** Text is set in Geist, which recedes and does the reading work.
Every number is set in Martian Mono — including the hero figures at 168px. This inverts the usual
hierarchy: on most sites the headline shouts and the data whispers. Here `50.2%` is the loudest
object on the screen and the sentence around it is quiet. For a page whose entire argument is
quantitative, that is the honest arrangement.

The reference points were Capital and Driftime, taken for *behaviour* — long decelerating motion,
oversized display type, a persistent bottom control bar — and explicitly not for appearance. Both
are warm-black with a green accent and a light geometric sans, which is this genre's current default
and the thing being avoided.

## Colors

Ground is a cool, blue-shifted near-black (`#0A0A0F`), deliberately opposite the warm-tinted blacks
both references use.

| Role | Value | Contrast on ground |
|---|---|---|
| `ground` | `#0A0A0F` | — |
| `surface` | `#14141B` | 1.08:1 |
| `textPrimary` | `#F2F4F7` | **17.93:1** |
| `textSecondary` | `#C0C6CF` | **11.49:1** |
| `textMuted` | `#8B94A0` | **6.43:1** |
| `primary` — AI | `#FA4544` | **5.64:1** |
| `accent` — not AI | `#B9FA31` | **15.78:1** |
| `danger` | `#B267E4` | **5.60:1** |
| `focusRing` | `#FDB1A9` | **11.32:1** |

Both poles are bright enough to read as running text directly on `ground` — no lighter step needed
the way the previous purple/lime pair required one. Both are too light for white-on-fill text,
though: a white label on `primary` or `accent` fills clears only 3.50:1 / 1.25:1. Use `onPrimary` /
`onAccent` (`#0A0A0F`, matching `ground`) as the fill text colour instead — 5.64:1 / 15.78:1,
comfortably AA even at body size.

All chart colours were generated in OKLCH and verified with the `dataviz` validator against the
`#0A0A0F` surface. Do not substitute a hex by eye — re-run the validator.

- **Categorical (5 slots, fixed order):** `#FA4544` `#2A92BB` `#769F26` `#B5297B` `#A98C35`.
  Worst *adjacent* CVD ΔE 17.6 (this order — red, blue, green, magenta, gold — keeps the two brand
  poles non-adjacent; red directly next to the accent's green step collapses to ΔE 2.0 under
  deuteranopia, which is why the order matters here more than in the old palette). All in the dark
  lightness band, all ≥3:1. This order is validated for **adjacent-pair use only** (bars, ribbons,
  chips) — re-validate with `--pairs all` before using it in a scatter, bubble, or choropleth form.
  Five is the ceiling — there is no sixth slot. A sixth series folds into "Other," facets into small
  multiples, or the chart changes form. Never generate a new hue.
- **Sequential — steel (magnitude):** `#C2D3E8 → #415A79`, one low-chroma hue, monotone lightness,
  darkest step still 2.79:1 on ground. Untouched by the brand-colour change — deliberately its own
  neutral hue, independent of both poles.
  **Why steel and not the primary red:** magnitude bars appear in beats that have nothing to do
  with AI. If counts were drawn in the AI pole's hue, every bar chart would imply an AI reading it
  doesn't carry. Desaturated steel says "this is just a count" and keeps saturated red and
  chartreuse meaning one thing only.
- **Diverging — AI share (the Sankey scale):** this is the one place the brand poles are *not* used
  directly. `#FA4544` (AI) and `#B9FA31` (not-AI) collapse to ΔE 1.4 under deuteranopia — a
  red-green colorblind reader cannot tell the arms apart at any lightness step, which fails the
  validator's hard floor (6.0) by a wide margin and can't be fixed by re-lightening. So this chart
  runs a decoupled, validated pair instead: indigo arm `#B1C4EC → #264698` (AI), gold arm
  `#FCDD60 → #6B5A10` (not-AI), neutral midpoint `#74747A`. Worst cross-arm ΔE 21.6 deutan / 22.1
  normal-vision — both comfortably clear. Each arm validated independently as a single-hue ramp; the
  midpoint is a true desaturated grey — never a third hue. Every other component (button, chip,
  prose) still uses brand red/chartreuse directly — only this chart's arms differ, and only because
  the validator forced it.

Colour carries exactly one variable at a time. In the Sankey, node identity comes from direct labels
and ribbon colour carries AI share alone; this is what keeps a 13→27 node diagram inside the
five-slot categorical ceiling.

### Checked against the status colours — no collision

`danger` (`#B267E4`, OKLCH H309.8°) sits clear of `primary` (H25.8°, ΔE 25.9 deutan / 27.8 normal)
and of the categorical set's magenta slot (`#B5297B`, H350°, ΔE 16.1 deutan / 17.7 normal) — both
comfortably above the 15 normal-vision floor. `warning` (H70.8°) and `success` (H191.0°) remain far
from both brand poles. The general rule still stands regardless: **no status state may rely on
colour alone.** Every `statusMessage` ships with an icon and a text label regardless.

## Typography

Two families, one job each.

- **Geist** — all text. Headlines, prose, UI labels, descriptions. Weights 400/500/600. It is
  deliberately the quieter of the two: it sets the sentence, the number carries the moment.
- **Martian Mono** — every number, plus repo slugs, category codes, axis ticks, and eyebrow labels.
  Weights 500/700. Wide, geometric, and built to hold up at display sizes, which is why it takes the
  `hero` and `figureLg` roles rather than a display sans.

Rules:

- `font-variant-numeric: tabular-nums` everywhere numbers appear, so counts don't jitter when they
  animate or update.
- Martian Mono is wide by construction. At `hero` size, tracking goes to `-0.055em` to stop long
  figures like `262,902` from breaking the panel; always test the *longest* number in a slot, not a
  short one.
- Never set running prose in Martian Mono — it is a display and data face here, not a body face.
- Never set a headline figure in Geist. If it is a number the argument depends on, it is Martian Mono.

Display line-height goes to `0.9` at hero — intended; give those blocks explicit padding rather than
relying on line-box spacing.

## Layout

The page is a horizontal rail. Beats are full-viewport panels laid left to right.

- **Beat panel:** `100dvh` tall, `100vw` wide by default; the Sankey beat is deliberately wider than
  the viewport and is the one place horizontal overflow inside a beat is allowed.
- **Panel padding:** `3xl` (104px) desktop, `lg` (24px) mobile, with the bottom `2xl` reserved so
  content never sits under the control bar.
- **Content column:** max `72ch` for prose; charts take the remaining width.
- **Stage rail** pins to the top, **control bar** pins to the bottom, both fixed across the whole
  experience. Reserve their heights as layout padding, never as overlay.
- **Grid:** 12 columns within a beat, `md` (16px) gutter.

Breakpoints: `sm` 480px, `md` 768px, `lg` 1080px, `xl` 1440px. The layout stays horizontal at every
breakpoint — on mobile the beats are swiped, and the Sankey beat swaps to its heatmap form rather
than shrinking.

## Elevation & Depth

Depth comes from **surface steps and hairline borders**, not heavy shadows — on a near-black ground,
large soft shadows read as smudges. Cards sit on `surface` with a 1px `border`; only floating things
(tooltip, expanded control bar, filter sheet) take a real shadow.

`elevation.glow` is the one expressive treatment: a hairline border plus a wide, very low-opacity
red bloom. Reserved for the active beat's primary chart and the hero figure. Using it anywhere else
spends the system's one bold move on something that doesn't deserve it.

## Shapes

- `none` — chart marks, table cells, stage rail, full-bleed panels.
- `sm` (3px) — bar/ribbon data-ends, filter chips, tags.
- `md` (6px) — buttons, inputs, tooltips.
- `lg` (12px) — cards, control bar, sheets.
- `pill` — stage-rail indicator and toggles only.

Chart marks are square-cornered except a 4px rounded cap on the data-end, anchored to the baseline.

## Motion

Specified rather than left to taste, since motion is what the references were chosen for.

- **Scroll:** Lenis in `orientation: 'horizontal'`, lerp `0.085`. A normal vertical wheel or
  trackpad gesture moves the rail sideways; the reader should never think about it.
- **Easing:** `easeOut` `cubic-bezier(0.22, 1, 0.36, 1)` for everything entering or settling.
  `easeInOut` only for things that reverse. Never `linear`, never `ease`.
- **Durations:** `fast` 240ms hover/state, `base` 420ms element transitions, `slow` 720ms beat
  content settling, `beat` 1100ms chart draw-on.
- **Properties:** animate `transform` and `opacity` only. Never `width`, `height`, `top`, `left`;
  never colour on scroll.
- **Beat entry:** content rises `24px` and fades in, staggered `60ms`, capped at five staggered
  items — past that everything arrives together.
- **Chart draw-on:** once, when a beat first becomes active; never again on re-entry.

**Reduced motion is a first-class path, not a fallback.** Under `prefers-reduced-motion: reduce`:
Lenis smoothing is disabled and native scrolling takes over, draw-on is skipped (charts render final
state), staggers collapse to zero, and the counting hero figure renders its final value. Nothing
becomes unreachable and no information is lost.

## Components

### stageRail
The top progress indicator: where the reader is in the story.
- **Variants:** `default`. **States:** `rest, active, visited, hover, focus`.
- Fixed top, full width, 44px tall. One segment per beat, numbered, labelled in `micro`.
- `border` at rest, `textMuted` when visited, `primary` when active; the active segment carries a
  `pill` underline that slides between positions with `easeOut`/`base`.
- Segments are **buttons**, not decoration — they jump to their beat, sit in the tab order, and show
  a visible `focusRing`.

### controlBar
The persistent bottom bar: filters, current-selection readout, navigation.
- **Variants:** `narrative`, `explorer`. **States:** `rest, expanded`.
- Fixed bottom, `lg` radius on top corners, `surface` background, 1px top `border`, `elevation.md`.
  64px at rest; `expanded` grows to at most 45dvh and scrolls internally.
- One row: left = context label, centre = filters, right = counts and beat navigation. On mobile the
  centre collapses to a "Filters" button opening the expanded state as a sheet.
- **Always shows the live record count in Martian Mono** — the reader should always know how many
  repos the current view represents.

### beatPanel
- **Variants:** `statement`, `chart`, `split`, `board`. **States:** `offscreen, entering, active, leaving`.
- Only the `active` beat runs animations or fetches data. `offscreen` beats are
  `content-visibility: auto` and must not hold chart instances alive.
- Every beat has an `id` and is deep-linkable; entering updates the URL hash without adding a
  history entry per intermediate beat.

### chartFrame
- **Variants:** `default`, `wide`, `full` (Sankey only). **States:** `loading, ready, empty, error`.
- Legend present whenever there are ≥2 series; a single series is named by the title instead.
- **Every chart frame must offer a table view.** Not optional — it serves the weak-tritan pair,
  screen-reader users, and anyone wanting to copy numbers.
- `loading` is a skeleton at final height (no layout shift); `empty` names the filter that caused it
  and offers a reset; `error` offers retry and is never a blank box.

### heroFigure
- **Variants:** `default`, `withUnit`. **States:** `rest, counting`.
- `hero` scale, Martian Mono, `textPrimary`, unit in `textMuted` at 0.4em.
- `counting` animates from 0 over `beat` with `easeOut`; skipped under reduced motion. The final
  value is always in the DOM for assistive tech regardless of animation state.

### repoCard
- **Variants:** `default`, `compact`, `feature`. **States:** `rest, hover, focus`.
- Slug in Martian Mono `bodySm`, description in Geist `body` `textSecondary` clamped to 2 lines,
  stars in Martian Mono with tabular figures, category and domain as `filterChip`s.
- The whole card is one link, `rel="noopener noreferrer"`; the star count is announced as "N stars"
  rather than a bare number.
- `hover` raises to `surfaceRaised` and shifts border to `borderStrong` — no scale transform.

### filterChip
- **Variants:** `default`, `poleAI` (red), `poleNotAI` (chartreuse). **States:** `rest, hover, selected, focus, disabled`.
- `sm` radius, `label` type, 32px tall with a ≥44px hit area via padding.
- `selected` fills with the variant colour; selection is never colour-alone — a check glyph accompanies it.

### button
- **Variants:** `primary`, `ghost`, `quiet`. **States:** `rest, hover, active, focus, disabled`.
- 44px minimum height, `md` radius, `label` type.
- `focus` always shows a 2px `focusRing` at 2px offset — never removed, never replaced by a colour change alone.

### statusMessage
- **Variants:** `info`, `success`, `warning`, `danger`. **States:** `visible`.
- Icon + text label + `surface` background with a 2px left border in the status colour.
- **Colour is never the only signal** — the general status rule, kept even though this palette has
  no accent/danger collision to resolve.
- `danger` uses `#B267E4`, distinct from both the primary and accent hues.

### tooltip
- **Variants:** `point`, `crosshair`. **States:** `hidden, visible`.
- `surfaceRaised`, 1px `border`, `md` radius, `elevation.md`, `bodySm` text with Martian Mono figures.
- Appears within `instant`; never animates position while following the cursor; flips side near the
  viewport edge so it never covers the mark it describes.
- Tooltips are an enhancement — the same information must be reachable in the table view.

### dataTable
- **Variants:** `inline`, `virtualized`. **States:** `loading, ready, empty`.
- Real `<table>` semantics with `<caption>`, `<th scope>`, Martian Mono tabular figures,
  right-aligned numerics.
- `virtualized` renders a window of rows, keeps header semantics, supports keyboard paging, and uses
  a fixed row height so the scrollbar is honest.

## Do's and Don'ts

**Do**
- Bind every value to a token; re-run the `dataviz` validator after any colour change.
- Let red and chartreuse mean AI and not-AI *everywhere* — chart, chip, and prose.
- Set every number in Martian Mono with tabular figures; set every sentence in Geist.
- Use the steel ramp for plain magnitude so counts never imply an AI reading.
- Reserve `elevation.glow` for the active beat's primary chart and the hero figure.
- Keep the record count visible in the control bar at all times.
- Ship every status message with an icon and a label.
- Give every chart a table view and every beat a deep link.

**Don't**
- Don't add a sixth categorical hue. Fold into "Other" or change the form.
- Don't put a hue at the diverging midpoint — it is grey `#74747A`.
- Don't use the primary red for plain magnitude bars; that is what the steel ramp is for.
- Don't use red or chartreuse for UI emphasis unrelated to the AI polarity.
- Don't use brand red/chartreuse directly in the diverging Sankey scale — use `divergingAI` /
  `divergingNotAI`, the validator-forced decoupled pair.
- Don't signal an error with colour alone — always pair with an icon and label.
- Don't set prose in Martian Mono or headline figures in Geist.
- Don't animate anything but `transform` and `opacity`.
- Don't let the stage rail or control bar overlap content — reserve their height.
- Don't use warm near-black, a green accent, or a light-weight geometric sans — the references'
  signatures and this genre's default.
- Don't add gradient text, glassmorphism, or a glowing grid backdrop. The one bold move is the
  numeric display type at scale, and it is already spent.
- Don't scale cards on hover or fake elevation with shadow on `ground` — use surface steps.
