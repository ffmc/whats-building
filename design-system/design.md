---
version: alpha
name: Whats Building
description: Quiet, analytical, editorial design system for a horizontal-scroll data story about what people build on GitHub — big bold type with room to breathe, anchored on The Verge (type-as-graphic-device, flat, high-contrast) and Mendo (restraint, whitespace, minimal monochrome).
colors:
  primary:        { light: "#141311", dark: "#f5f2ea" }
  onPrimary:      { light: "#f7f5f0", dark: "#0d0d0e" }
  surface:        { light: "#f7f5f0", dark: "#0d0d0e" }
  surfaceRaised:  { light: "#fbf9f5", dark: "#18181a" }
  textPrimary:    { light: "#141311", dark: "#f5f2ea" }
  textSecondary:  { light: "#4a463e", dark: "#c9c3b6" }
  textMuted:      { light: "#8a8478", dark: "#8f887a" }
  border:         { light: "rgba(20,19,17,0.12)", dark: "rgba(245,242,234,0.14)" }
  focusRing:      { light: "#0058e6", dark: "#3d94ff" }
  dataBaseline:   { light: "#0058e6", dark: "#3d94ff" }
  dataAI:         { light: "#c81152", dark: "#ff4d84" }
  success:        { light: "#3f7a52", dark: "#6fae82" }
  warning:        { light: "#9c6b1f", dark: "#d9a441" }
  danger:         { light: "#a13b2e", dark: "#e2695a" }
  info:           { light: "#0058e6", dark: "#3d94ff" }
typography:
  fontFamily: { display: "IBM Plex Sans", body: "IBM Plex Sans", mono: "IBM Plex Mono" }
  ratio: "~1.4, accelerating at the top for hero-numeral drama (not a single strict multiplier)"
  scale:
    xs:  { size: 0.75rem, lineHeight: 1.5,  weight: 500, letterSpacing: "0.03em", family: body, transform: uppercase }
    sm:  { size: 0.875rem, lineHeight: 1.6, weight: 400, letterSpacing: "0em", family: body }
    base:{ size: 1rem,    lineHeight: 1.7,  weight: 400, letterSpacing: "0em", family: body }
    lg:  { size: 1.25rem, lineHeight: 1.6,  weight: 450, letterSpacing: "-0.005em", family: body }
    xl:  { size: 1.75rem, lineHeight: 1.3,  weight: 600, letterSpacing: "-0.01em", family: display }
    2xl: { size: 2.5rem,  lineHeight: 1.15, weight: 700, letterSpacing: "-0.015em", family: display }
    3xl: { size: 4rem,    lineHeight: 1.05, weight: 700, letterSpacing: "-0.02em", family: display }
    4xl: { size: "clamp(4.5rem, 10vw, 9rem)", lineHeight: 0.95, weight: 700, letterSpacing: "-0.03em", family: display }
spacing:  { xs: "4px", sm: "8px", md: "16px", lg: "32px", xl: "64px", 2xl: "96px", 3xl: "160px" }
radius:   { sm: "4px", md: "6px", lg: "0px", full: "999px" }
elevation:
  flat:   { shadow: "none", border: "1px solid {colors.border}" }
  raised: { shadow: "0 8px 24px rgba(0,0,0,0.18)", border: "1px solid {colors.border}" }
components:
  button:
    variants: [primary, secondary, ghost]
    states:   [default, hover, active, disabled, focus]
    tokens:   { radius: "{radius.sm}", elevation: "{elevation.flat}", fontFamily: "{typography.fontFamily.display}" }
  select:
    variants: [default]
    states:   [default, hover, open, disabled, focus]
    tokens:   { radius: "{radius.sm}", background: "{colors.surfaceRaised}", border: "{colors.border}" }
  segmentedToggle:
    variants: [default]
    states:   [default, selected, hover, disabled, focus]
    tokens:   { radius: "{radius.full}", background: "{colors.surfaceRaised}", selectedBackground: "{colors.dataAI}" }
  filterChip:
    variants: [lensBar, standalone]
    states:   [default, hover, focus]
    tokens:   { radius: "{radius.full}", elevation: "{elevation.raised}", background: "{colors.surfaceRaised}" }
  tag:
    variants: [ai, neutral]
    states:   [default]
    tokens:   { radius: "{radius.sm}", aiBackground: "{colors.dataAI}", neutralBackground: "{colors.border}" }
  card:
    variants: [default, compact]
    states:   [default, hover]
    tokens:   { radius: "{radius.lg}", elevation: "{elevation.flat}", background: "{colors.surfaceRaised}" }
  table:
    variants: [default]
    states:   [rowDefault, rowHover, header]
    tokens:   { border: "{colors.border}", fontFamily: "{typography.fontFamily.mono}" }
  tooltip:
    variants: [default]
    states:   [visible]
    tokens:   { radius: "{radius.sm}", elevation: "{elevation.raised}", background: "{colors.surfaceRaised}" }
  themeToggle:
    variants: [default]
    states:   [default, hover, focus]
    tokens:   { radius: "{radius.full}", border: "{colors.border}" }
---

# Whats Building Design System

## How to build with this
> Read this file before building any UI. `design-system/design.md` is the single source of truth;
> `design-system/design.html` and the token file are generated from it — edit this file, then regenerate
> them, never the reverse. Bind every visual value to a token (`var(--…)`); never hardcode a hex/px that
> has a token. Use only the variants and states listed per component — the lists are CLOSED. If a
> feature needs a token, variant, or component that isn't defined here, STOP and flag the user, then add
> it to this file deliberately — do not improvise it. Honor the Do's and Don'ts; avoid the named clichés.

## Overview

This is a data-journalism piece, not a marketing site: a horizontal-scroll interactive story about
what people build on GitHub, anchored on one claim (AI's share of new popular repos climbing from
1-in-7 to a coin-flip) and explored chart-by-chart along the way. The audience reads it once, closely,
on any device — assured, analytical, quiet is the target feeling: confident in its numbers, restrained
in its presentation, never chart-junk-cluttered and never a generic AI-product landing page. Two
anti-patterns to actively resist: the soft-shadow/rounded-everything SaaS-dashboard look, and
gradient/glassmorphism "AI product" marketing sheen.

## Colors

The neutrals are a deep, near-neutral black (dark mode) and a soft warm-off-white (light mode) —
deliberately quieter than the accents, so they stay out of the way. The accents are fully saturated,
not muted — but deliberately **not** blue/orange or indigo/mint: those pairings (along with fonts like
Inter or Space Grotesk) have become a recognizable "generated by an AI coding tool" signature, which
undercuts a system meant to feel authored and specific. Instead: `dataAI` is a vivid crimson-coral — hot, urgent, unmistakably not a safe default — and
`dataBaseline` is an electric, cyan-leaning blue (pulled toward pure blue, not violet, to stay clear of
the indigo cliché too). An earlier teal/spruce-green draft for `dataBaseline` was dropped for reading
too close to a specific reference's mint-green accent — electric blue keeps the same hot/cool contrast
against the crimson without echoing it. Same semantic logic as before (hot = AI signal, cool =
baseline), same full-saturation "graphic statement" intent. `primary` stays the ink
color itself (solid dark-on-light / light-on-dark buttons, not a branded hue) — that restraint is what
makes room for the two accents to be loud without the whole page turning gaudy. `dataBaseline` and
`dataAI` remain the *only* two saturated hues in the system and carry real meaning everywhere they
appear — never decorative, never a third hue introduced without deliberation. `focusRing` reuses
`dataBaseline`. Dark-mode accents are brightened versions of their light-mode counterparts (not the
same hex inverted), so they glow against the near-black surface the way the light-mode versions read as
deep and rich against off-white.

## Signature Device — type as graphic

The fix for "the background feels boring": oversized, bold display type is not reserved for headlines
— it doubles as background art. In hero and section-opening moments, take a single word or number
(a category name, "AI", a hero stat) and render it at a huge scale (`4xl` or larger, Space Grotesk at
its heaviest weight, 700+), often rotated 90° or bled off the edge of the viewport, in full-saturation
`dataAI` or `dataBaseline` — sitting behind or alongside the actual content rather than as the content
itself. This is the one place color is used at full graphic force rather than as a small functional
signal (a chart line, a tag) — it's what gives an otherwise-quiet, whitespace-heavy layout its
statement moment. Use it sparingly: one such device per major beat, never as a repeating background
pattern, or it stops reading as a deliberate flourish and starts reading as wallpaper.

## Typography

One designed-together type pair: **IBM Plex Sans** for everything written (headlines, body, labels,
captions) and **IBM Plex Mono** for everything counted. Both come from IBM's own type system, built
for exactly this kind of technical/editorial mixed use — a deliberate move away from Inter and Space
Grotesk, which have become the recognizable default for AI-generated interfaces and read as templated
rather than authored. Plex carries a credible, engineering/technical identity that suits a data-
journalism piece about software, without leaning on a currently-overused "modern SaaS" typeface. The
split is by content type, not by size — any standalone numeral or tabular figure (a hero percentage, a
star count, a table column) renders in Plex Mono regardless of how large or small it is; any word
renders in Plex Sans. The scale accelerates toward the top so hero numerals can dominate a full
viewport; `xs` is reserved for eyebrow/meta labels and always renders uppercase with wide tracking, a
quiet Mendo-style device for category/date labels sitting above big titles.

## Layout

Spacing is deliberately generous — the explicit brief was "plenty of room to breathe" — running from a
4px base unit up to 160px for the gaps between horizontal story beats. Don't compress this scale to fit
more on screen; if content feels cramped, the fix is fewer elements per beat, not tighter spacing.
Container widths follow the content, not a fixed grid: prose measures stay narrow (60-70ch) even inside
a full-bleed horizontal layout, so long-form captions stay readable against big chart canvases.

## Elevation & Depth

Only two real states exist, not the conventional three-tier shadow scale: **flat** (border-only, used
for every static surface — cards, panels, sections) and **raised** (one restrained shadow, reserved
exclusively for things that must visually float above chart content — tooltips, dropdowns, the
persistent filter/lens bar). Don't introduce a third shadow weight; if something needs to feel "more
raised" than `raised`, that's a signal it shouldn't be floating in the first place.

## Shapes

Radius is intentionally inverted from convention: **large surfaces stay sharp** (`radius.lg` = 0px —
cards, panels, chart containers never get rounded corners, matching both Verge and Mendo's flat,
editorial geometry), while **small interactive controls** get a slight radius (`sm`/`md`, 4-6px —
buttons, inputs, chips) just enough to read as clickable without softening the serious tone. One
deliberate exception: `full` (pill/999px) is reserved for the persistent lens/filter bar and the AI/
non-AI segmented toggle — a single recurring rounded shape that reads as a signature, not a default.

## Components

**Button** — primary is solid ink (inverted per theme), secondary is bordered/transparent, ghost is
text-only; all use `radius.sm` and stay flat.

**Select/Dropdown, Segmented Toggle, Filter Chip / Lens Bar** — these three are the "filters," and they
get the boldest treatment in the system, not the quietest: this is where a reader's own choice becomes
visible, and it should look like it matters. Their labels render in the `xs` eyebrow style (uppercase,
wide-tracked) but at higher weight (700) than a passive caption. The **segmented toggle**'s selected
state is a hard fill in `dataAI` with white/near-black text (whichever contrasts) — not a tint, not an
outline. The **filter chip / lens bar** is pill-shaped, `raised`, and once a lens is active its border
(or a leading dot/bar) uses `dataAI` or `dataBaseline` to match whatever data it's currently filtering
by — the chip should visually announce "this is live and colored," never sit as a neutral gray pill.
The **select** stays simpler (it's a raw input, not a stated choice) but its focus/open state gets a
2px `dataBaseline` border, not the default 1px neutral one every other bordered element gets.

**Tag** — small AI/neutral badges on repo cards and list rows; `sm` radius, never pill; the AI variant
is a hard `dataAI` fill, never a tint. **Card** — repo cards and leaderboard row containers; sharp
corners, flat, border-only separation. **Table** — the leaderboard; numeric columns render in Space
Mono with tabular alignment. **Tooltip** — chart hover info; the one place shadows are expected and
necessary for legibility over dense data. **Theme Toggle** — light/dark switch; pill-shaped, lives in a
persistent, unobtrusive position.

## Do's and Don'ts

**Do:**
- Bind every color/size/radius/shadow to a token — no hardcoded hex or pixel values.
- Reserve Space Mono strictly for numerals/tabular data; never set prose in it.
- Keep large surfaces sharp-cornered; keep the pill shape rare and meaningful (lens bar, toggle only).
- Let whitespace do the separating before reaching for a border or shadow.
- Use `dataAI`/`dataBaseline` consistently as the *only* meaning-carrying color pair across every chart.

**Don't:**
- Don't add a third font family, a third shadow tier, or a new accent hue without stopping to flag it.
- Don't default to rounded cards, soft drop shadows, or an indigo/violet palette — that's the generic
  SaaS-dashboard look this system exists to avoid.
- Don't use gradients, frosted-glass panels, or glow effects anywhere.
- Don't decorate with extra color, icons, or chart-junk — if a chart needs a third color to explain
  itself, the chart design is wrong, not the palette.
- Don't reproduce Beagle-style playfulness (scattered rotated cards, pastel palette, mixed serif/
  rounded-sans whimsy) — that direction was explicitly ruled out for this project.
