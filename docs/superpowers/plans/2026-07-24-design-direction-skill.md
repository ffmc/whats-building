# design-direction Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a new global skill, `design-direction`, that governs aesthetic direction for UI work, replacing the plugin/skill previously used for this role, and retire the other skill that overlapped with it.

**Architecture:** Three markdown files under `~/.claude/skills/design-direction/` (`SKILL.md` + two `references/` files), plus a small cross-reference edit in `~/.claude/skills/design-system/templates/anti-slop.md`, a deletion of `~/.claude/skills/ui-designer/`, and one `enabledPlugins` flip in `~/.claude/settings.json`. All file changes live in the `~/.claude` git repo (confirmed a repo, clean working tree, branch `main`) and are committed there — separate from the `whats-building` repo that holds this plan.

**Tech Stack:** Markdown + YAML frontmatter skill files (no build/test tooling — verification is structural: frontmatter parses, required sections present).

## Global Constraints

- Skill lives at `~/.claude/skills/design-direction/` (global, user-level — not project-scoped).
- Skill name/frontmatter `name` field: `design-direction`.
- `references/trend-library.md` frontmatter must include `last_reviewed: <ISO date>`.
- No content in any new file may frame itself as "replacing," "carried over from," or otherwise reference the prior skill/plugin by name — state every principle directly (per prior explicit instruction).
- Commits for `~/.claude` changes happen in that repo, not `whats-building`.

---

### Task 1: Create `design-direction/SKILL.md`

**Files:**
- Create: `/home/franciscocardoso/.claude/skills/design-direction/SKILL.md`

**Interfaces:**
- Produces: a skill file with frontmatter `name: design-direction`, `description: ...`, referencing `references/trend-library.md` and `references/copywriting.md` by relative path — later tasks (2, 3) must create files at exactly those paths.

- [ ] **Step 1: Create the directory and write SKILL.md**

```bash
mkdir -p /home/franciscocardoso/.claude/skills/design-direction/references
```

Write `/home/franciscocardoso/.claude/skills/design-direction/SKILL.md`:

```markdown
---
name: design-direction
description: Use whenever building or reshaping any UI/UX surface — new pages, redesigns, components, marketing sites. Grounds design decisions in the specific brief, pulls toward current Awwwards-caliber patterns via a maintained trend library, and enforces an accessibility/handoff gate before anything is called done. Trigger on "design this", "redesign", "build a landing page/UI", "make this look better/more modern", or any request to create or improve a visual interface.
---

# Design Direction

Approach this as the design lead at a small studio known for giving every client a
visual identity that could not be mistaken for anyone else's. Make deliberate,
opinionated choices about palette, typography, and layout that are specific to this
brief, and take one real aesthetic risk you can justify.

## Principles

- **Ground every design in a concrete subject.** If the brief doesn't pin down what the
  product or subject is, pin it yourself: name one concrete subject, its audience, and
  the page's single job, and state your choice. The subject's own world — its
  materials, instruments, artifacts, vernacular — is where distinctive choices come
  from.
- **The hero is a thesis.** Open with the most characteristic thing in the subject's
  world, in whatever form fits: a headline, an image, an animation, a live demo, an
  interactive moment.
- **Typography carries personality.** Pair display and body faces deliberately, set a
  clear type scale with intentional weights/widths/spacing, and make the type
  treatment itself memorable rather than a neutral delivery vehicle.
- **Structure is information.** Numbering, eyebrows, dividers, and labels should encode
  something true about the content, not decorate it. A numbered sequence (01/02/03) is
  only appropriate when the content really is a sequence.
- **Spend boldness in one place.** Pick a single signature element the design will be
  remembered by; keep everything around it quiet and disciplined. Not taking a risk can
  be a risk itself.
- **Match complexity to the vision.** Maximalist directions need elaborate execution;
  minimal directions need precision in spacing, type, and detail.

## Process

1. **Ground it in the subject.** Before designing anything, name the concrete subject,
   audience, and the page's single job.

2. **Check for an existing system.** If `design-system/design.md` exists in the
   project, read it and build strictly within its tokens and closed variant/state
   lists — flag conflicts to the user rather than overriding silently. If no system
   exists, proceed with open aesthetic direction, and once the direction is set, mention
   that running `/design-system draft` would lock it in for reuse.

3. **Consult `references/trend-library.md`.** Pull 2-3 patterns relevant to this
   brief's category (layout, typography, color/material, or motion) — not a random
   grab-bag. For each candidate pattern, read its "wrong for" note and the category's
   "currently overused" note before committing to it. Check the Anti-patterns section
   and actively steer away from every entry there.

4. **Plan, critique, build, critique again.**
   - First pass: write a compact plan — a 4-6 named-hex color palette, 2+ typefaces by
     role, a one-sentence-plus-ASCII-wireframe layout concept, and the one signature
     element.
   - Review that plan against the brief: if any part reads like the generic default you
     would produce for any similar brief, revise it and state what changed and why.
   - Only then write code, deriving every color/type/layout decision from the revised
     plan.
   - After building, self-critique again (take a screenshot if the environment supports
     it) before presenting to the user.

5. **Accessibility & handoff gate — mandatory, not optional.** Before calling anything
   done, verify:
   - Color contrast meets WCAG AA in every theme the design supports.
   - Keyboard focus is visible on every interactive element.
   - The page is fully keyboard-navigable.
   - Structure is screen-reader-friendly (heading order intact, no skipped levels).
   - A reduced-motion alternative exists for any non-trivial animation.
   - Tap targets meet a ≥44px minimum hit area.
   - Loading, empty, error, and success states are all defined, not just the happy path.

6. **Copywriting.** Apply `references/copywriting.md` to any words the design needs —
   headlines, labels, button text, empty/error states.

## Restraint and self-critique

Spend your boldness in one place. Let the signature element be the one memorable
thing; cut any decoration that doesn't serve the brief. Build to a quality floor
without announcing it: responsive down to mobile, visible keyboard focus, reduced
motion respected. Consider Chanel's advice: before leaving the house, take a look in
the mirror and remove one accessory.
```

- [ ] **Step 2: Verify frontmatter parses and required sections exist**

Run:
```bash
python3 -c "
import re
text = open('/home/franciscocardoso/.claude/skills/design-direction/SKILL.md').read()
fm = re.match(r'^---\n(.*?)\n---\n', text, re.S).group(1)
import yaml
data = yaml.safe_load(fm)
assert data['name'] == 'design-direction'
assert 'references/trend-library.md' in text
assert 'references/copywriting.md' in text
for heading in ['## Principles', '## Process', '## Restraint and self-critique']:
    assert heading in text, heading
print('OK')
"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd /home/franciscocardoso/.claude
git add skills/design-direction/SKILL.md
git commit -m "Add design-direction skill: SKILL.md"
```

---

### Task 2: Create `design-direction/references/trend-library.md`

**Files:**
- Create: `/home/franciscocardoso/.claude/skills/design-direction/references/trend-library.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: a file with frontmatter `last_reviewed: <date>` and five `##` category
  headings (`Layout`, `Typography`, `Color & material`, `Motion & interaction`,
  `Anti-patterns`), each containing named `###` pattern entries and ending in a
  `**Currently overused:**` line. Task 1's SKILL.md step 3 already references this
  path.

- [ ] **Step 1: Write the file**

Write `/home/franciscocardoso/.claude/skills/design-direction/references/trend-library.md`:

```markdown
---
last_reviewed: 2026-07-24
---

# Trend Library

Current, concrete design patterns worth pulling from, and the recognizable AI-look
defaults to actively avoid. If `last_reviewed` above is more than ~90 days old, tell
the user this library may be stale and offer to refresh it (re-research current
Awwwards Site-of-the-Day / trend write-ups) before relying on it for a high-stakes
design.

## Layout

### Broken / asymmetric grid
- **Looks like:** content blocks intentionally offset from a baseline grid; some
  elements bleed past column edges on purpose.
- **Why it reads as intentional:** signals a considered layout hierarchy rather than a
  centered 12-column template.
- **Wrong for:** dense data/dashboard UIs where predictability matters more than
  expression.
- **Flattens into slop when:** asymmetry is applied randomly without an underlying grid
  discipline — reads as broken, not broken-on-purpose.

### Bento grid
- **Looks like:** a modular grid of variously-sized cards with distinct bordered cells,
  akin to product-feature pages.
- **Why it reads as intentional:** gives a feature list or dashboard an interesting
  rhythm instead of uniform tiles.
- **Wrong for:** content that isn't genuinely modular or comparable in importance.
- **Flattens into slop when:** every cell is the same size with an icon+title+paragraph,
  just wrapped in a bento label.

### Full-bleed editorial section
- **Looks like:** a section that ignores the container and runs to the viewport edge,
  often for a single large image, quote, or stat.
- **Why it reads as intentional:** creates a deliberate beat/pause in an otherwise
  contained layout.
- **Wrong for:** short pages where every section already feels large — it loses its
  contrast.
- **Flattens into slop when:** used on every section, so nothing is actually
  full-bleed *by contrast*.

### Horizontal-scroll section
- **Looks like:** a sub-section (cards, a timeline) that scrolls sideways within an
  otherwise vertical page.
- **Why it reads as intentional:** apt for browseable, collection-like content.
- **Wrong for:** primary, navigation-critical content that needs to be scannable at a
  glance.
- **Flattens into slop when:** there's no visual affordance that it scrolls, hiding
  content from users (especially on desktop, without a scroll cue).

**Currently overused:** bento grids on generic SaaS marketing pages, regardless of
whether the content is actually modular.

## Typography

### Oversized expressive display type
- **Looks like:** headline type well beyond body-scale (often 8rem+), tight tracking,
  sometimes overflowing its frame.
- **Why it reads as intentional:** gives a strong, confident hierarchy signal.
- **Wrong for:** text-dense, reading-first content where the headline should cede
  space to body copy.
- **Flattens into slop when:** done with a generic grotesque instead of a distinct
  display face — big size alone isn't a typographic choice.

### Variable-font weight play
- **Looks like:** a single variable font, animating or varying weight/width for
  emphasis instead of switching families.
- **Why it reads as intentional:** creates a coherent visual voice with real expressive
  range.
- **Wrong for:** briefs that need a strong two-voice contrast (e.g. editorial serif vs.
  utility sans).
- **Flattens into slop when:** the variable axis is chosen but never actually exploited
  — defeats the point of picking the font.

### Kinetic / animated type
- **Looks like:** headline letters or words animate in on scroll or load (stagger,
  slide, blur-in).
- **Why it reads as intentional:** choreographs attention on a hero moment.
- **Wrong for:** content-heavy pages with many headings — becomes noisy if repeated
  everywhere.
- **Flattens into slop when:** bounce/elastic easing is used on every letter — a
  recognizable "AI motion" tell.

### Deliberate serif+grotesque pairing
- **Looks like:** a display/body pairing chosen for what it references about the
  subject matter, not the safe default combination.
- **Why it reads as intentional:** gives the page a subject-specific typographic
  identity.
- **Wrong for:** briefs with an existing brand typeface already specified.
- **Flattens into slop when:** it's a generic humanist sans + generic slab with no
  stated rationale for either.

**Currently overused:** giant oversized hero type — now extremely common on
Awwwards-style sites; using it needs a reason beyond "it looks like an awards site."

## Color & material

### Grain / noise texture overlay
- **Looks like:** subtle film-grain noise layered over flat color fields.
- **Why it reads as intentional:** adds tactility and depth without reaching for a
  gradient.
- **Wrong for:** data-dense UI where texture would reduce legibility.
- **Flattens into slop when:** it's the *only* differentiator — texture standing in for
  an actual design decision.

### Duotone imagery
- **Looks like:** photography mapped to two brand colors instead of rendered in full
  color.
- **Why it reads as intentional:** unifies photography with the palette; feels
  art-directed rather than stock.
- **Wrong for:** photography where accurate color is functionally important (product
  shots, e-commerce).
- **Flattens into slop when:** applied to generic stock photography that still reads as
  stock underneath the color treatment.

### Gradient mesh
- **Looks like:** organic, multi-point gradients rather than a flat two-stop linear
  gradient.
- **Why it reads as intentional:** painterly, considered quality vs. the generic
  linear-gradient hero background.
- **Wrong for:** minimal/austere briefs where any gradient reads as excess.
- **Flattens into slop when:** it still defaults to purple/blue/pink hues just rendered
  as a mesh instead of a line.

### Monochrome + single accent
- **Looks like:** a near-single-hue palette with one sharp, deliberate accent color
  reserved for actions/emphasis.
- **Why it reads as intentional:** disciplined — lets the one accent do real
  signaling work.
- **Wrong for:** content that needs multiple simultaneous status colors (dashboards,
  data states).
- **Flattens into slop when:** the "one" accent chosen is indigo/violet by default
  rather than a deliberate pick.

**Currently overused:** grain texture — now common enough on portfolio/agency sites to
verge on self-parody; using it needs its own justification.

## Motion & interaction

### Scroll-triggered reveals
- **Looks like:** elements fade or slide in as they enter the viewport, staggered by
  group.
- **Why it reads as intentional:** paces content and rewards scrolling.
- **Wrong for:** long, content-heavy pages, where it delays reading and becomes
  tedious.
- **Flattens into slop when:** every single element gets the same fade-up with no
  variation or purpose.

### Magnetic / cursor-reactive elements
- **Looks like:** buttons or elements that shift toward the cursor within a radius.
- **Why it reads as intentional:** adds tactile feedback and a signature feel to key
  CTAs.
- **Wrong for:** touch-primary interfaces, where there's no cursor to react to.
- **Flattens into slop when:** applied to every interactive element instead of the one
  signature moment — dilutes the "spend boldness in one place" principle.

### Pinned / sticky sections
- **Looks like:** a section pins in place while adjacent content scrolls past or over
  it (scrollytelling).
- **Why it reads as intentional:** strong for a genuinely sequential narrative (steps,
  before/after).
- **Wrong for:** content with no real sequence to walk through.
- **Flattens into slop when:** arbitrary sections are pinned purely for effect, with no
  narrative reason.

### Orchestrated page-load sequence
- **Looks like:** a one-time intro animation (logo reveal, mask wipe) before the page
  settles into its resting state.
- **Why it reads as intentional:** memorable first impression when the brief supports
  theatricality.
- **Wrong for:** return visitors and utility apps, where speed matters more than
  ceremony, and repeat viewings turn ceremony into friction.
- **Flattens into slop when:** added to a plain SaaS marketing page with no narrative
  reason and no skip option.

**Currently overused:** WebGL shader/blob-gradient hero backgrounds — now a
recognizable "creative agency site" cliché in their own right.

## Anti-patterns

Recognizable AI-look defaults. These are not neutral starting points — treat them as
choices you'd have to defend, not defaults you fall into.

### Cream + serif + terracotta
- **Looks like:** a warm cream background (near `#F4F1EA`), a high-contrast serif
  display face, and a terracotta/rust accent.
- **Why it reads as templated:** it's the "tasteful AI editorial" default — it appears
  regardless of subject.
- **Only defensible when:** the brief explicitly specifies this exact palette/mood.
- **Compounding risk:** paired with numbered-marker structure or a broadsheet layout,
  it reads as fully generic rather than merely familiar.

### Near-black + single neon accent
- **Looks like:** a near-black background with one bright acid-green or vermilion
  accent color.
- **Why it reads as templated:** the "AI dev-tool" default — again appears regardless
  of subject.
- **Only defensible when:** the brief is genuinely a dev tool and this look is
  explicitly requested.
- **Compounding risk:** combined with a colored glow/halo shadow, compounds into a
  fully generic "AI dashboard" look.

### Broadsheet / hairline / zero-radius
- **Looks like:** hairline rules, zero border-radius everywhere, dense
  newspaper-style columns.
- **Why it reads as templated:** used as a default aesthetic rather than a deliberate
  editorial choice tied to the content actually being newspaper-like.
- **Only defensible when:** the subject is genuinely editorial/journalistic and the
  brief calls for that register.
- **Compounding risk:** paired with Inter/system-ui for both display and body, it reads
  as having made no typographic choice at all.

### Unmodified indigo/violet + purple→blue gradient
- **Looks like:** Tailwind-default indigo or violet as the brand hue, often with a
  purple→blue gradient hero or button.
- **Why it reads as templated:** it's the strongest "no one chose this" signal in
  current AI-generated UI.
- **Only defensible when:** never — if this is genuinely the brand's hue, modify it
  (shift temperature, adjust saturation) so it reads as a choice.
- **Compounding risk:** combined with a 3-across feature-card grid below, reads as a
  fully unedited AI-default page.

### 3-across icon+title+paragraph feature grid
- **Looks like:** three (or four) identical cards, each with a centered icon, a title,
  and a short paragraph, uniform radius throughout.
- **Why it reads as templated:** it's the default "features section" regardless of
  what the features actually are.
- **Only defensible when:** the features are genuinely parallel and equally weighted,
  and the card design itself carries a specific, non-default treatment.
- **Compounding risk:** combined with emoji-as-icons or inflated placeholder stats
  ("10x faster," "Trusted by 10,000+ teams"), reads as fully unedited filler content.

**Currently overused:** all five entries above remain the most common recognizable AI
defaults — the bar for using any of them deliberately is a specific, stated reason tied
to the brief, not familiarity or convenience.
```

- [ ] **Step 2: Verify frontmatter and structure**

Run:
```bash
python3 -c "
import re, yaml
text = open('/home/franciscocardoso/.claude/skills/design-direction/references/trend-library.md').read()
fm = re.match(r'^---\n(.*?)\n---\n', text, re.S).group(1)
data = yaml.safe_load(fm)
assert 'last_reviewed' in data
for heading in ['## Layout', '## Typography', '## Color & material', '## Motion & interaction', '## Anti-patterns']:
    assert heading in text, heading
assert text.count('Currently overused') == 5
print('OK')
"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd /home/franciscocardoso/.claude
git add skills/design-direction/references/trend-library.md
git commit -m "Add design-direction skill: trend-library.md"
```

---

### Task 3: Create `design-direction/references/copywriting.md`

**Files:**
- Create: `/home/franciscocardoso/.claude/skills/design-direction/references/copywriting.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: a file with the headings referenced by SKILL.md step 6 ("Copywriting").

- [ ] **Step 1: Write the file**

Write `/home/franciscocardoso/.claude/skills/design-direction/references/copywriting.md`:

```markdown
# Copywriting for Design

Words appear in a design for one reason: to make it easier to understand and use.
They are design material, not decoration — bring the same intentionality to copy that
you'd bring to spacing and color.

## Write from the end user's side of the screen

Name things by what people control and recognize, never by how the system is built. A
person manages notifications, not webhook config. Describe what something does in
plain terms rather than selling it. Being specific is always better than being clever.

## Use active voice as the default

A control should say exactly what happens when it's used: "Save changes," not
"Submit." An action keeps the same name through the whole flow — the button that says
"Publish" produces a toast that says "Published." The vocabulary of an interface is the
signposting for someone navigating the product; cohesion and consistency are how
people learn their way around.

## Treat failure and emptiness as moments for direction, not mood

Explain what went wrong and how to fix it, in the interface's voice rather than a
person's. Errors don't apologize, and they are never vague about what happened. An
empty screen is an invitation to act, not a dead end.

## Keep the register conversational and tuned

Plain verbs, sentence case, no filler, tone matched to the brand and the audience. Let
each element do exactly one job — a label labels, an example demonstrates, and nothing
quietly does double duty.

## Before writing anything

Ask what the design needs to say, and how it can best be said to help the person
navigate the experience. If the brief has no real content, write copy as carefully as
you'd design layout — generic placeholder copy ("10x faster," "Trusted by 10,000+
teams") makes a design feel as templated as reused layout does.
```

- [ ] **Step 2: Verify structure**

Run:
```bash
python3 -c "
text = open('/home/franciscocardoso/.claude/skills/design-direction/references/copywriting.md').read()
for heading in ['# Copywriting for Design', '## Write from the end user', '## Use active voice', '## Treat failure and emptiness', '## Keep the register conversational', '## Before writing anything']:
    assert heading in text, heading
print('OK')
"
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd /home/franciscocardoso/.claude
git add skills/design-direction/references/copywriting.md
git commit -m "Add design-direction skill: copywriting.md"
```

---

### Task 4: Remove the `ui-designer` skill

**Files:**
- Delete: `/home/franciscocardoso/.claude/skills/ui-designer/SKILL.md`
- Delete directory: `/home/franciscocardoso/.claude/skills/ui-designer/`

**Interfaces:**
- Consumes: nothing (independent of Tasks 1-3).
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Remove the directory**

```bash
git -C /home/franciscocardoso/.claude rm -r skills/ui-designer
```

- [ ] **Step 2: Verify it's gone**

```bash
test ! -e /home/franciscocardoso/.claude/skills/ui-designer && echo OK
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd /home/franciscocardoso/.claude
git commit -m "Remove ui-designer skill"
```

---

### Task 5: Cross-reference the trend library from `design-system`'s anti-slop check

**Files:**
- Modify: `/home/franciscocardoso/.claude/skills/design-system/templates/anti-slop.md`

**Interfaces:**
- Consumes: the path `~/.claude/skills/design-direction/references/trend-library.md`
  created in Task 2 (must exist before this task, or point to a path that will exist).
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Add a cross-reference line**

Current top of the file reads:

```markdown
# Anti-Slop Check

Run this before presenting a draft, and whenever revising. A direction that trips a **reject** item goes back for revision — not to the user with a caveat. All **require** items must hold, not just most.
```

Edit it to:

```markdown
# Anti-Slop Check

Run this before presenting a draft, and whenever revising. A direction that trips a **reject** item goes back for revision — not to the user with a caveat. All **require** items must hold, not just most.

For what's currently trending vs. currently overused — beyond the fixed reject list
below — also check `~/.claude/skills/design-direction/references/trend-library.md`,
the maintained source for current pattern judgment.
```

- [ ] **Step 2: Verify the edit**

```bash
grep -q "design-direction/references/trend-library.md" /home/franciscocardoso/.claude/skills/design-system/templates/anti-slop.md && echo OK
```
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd /home/franciscocardoso/.claude
git add skills/design-system/templates/anti-slop.md
git commit -m "Cross-reference design-direction trend library from anti-slop check"
```

---

### Task 6: Uninstall the `frontend-design` plugin

**Files:**
- Modify: `/home/franciscocardoso/.claude/settings.json`

**Interfaces:**
- Consumes: nothing from other tasks (independent).
- Produces: nothing consumed by later tasks.

- [ ] **Step 1: Read current state**

```bash
grep -n "frontend-design" /home/franciscocardoso/.claude/settings.json
```
Expected output (line number may vary):
```
27:    "frontend-design@claude-plugins-official": true,
```

- [ ] **Step 2: Flip the flag to false**

Change the line found in Step 1 from:
```json
    "frontend-design@claude-plugins-official": true,
```
to:
```json
    "frontend-design@claude-plugins-official": false,
```

- [ ] **Step 3: Verify**

```bash
grep -n "frontend-design" /home/franciscocardoso/.claude/settings.json
```
Expected:
```
27:    "frontend-design@claude-plugins-official": false,
```

- [ ] **Step 4: Commit**

```bash
cd /home/franciscocardoso/.claude
git add settings.json
git commit -m "Disable frontend-design plugin"
```

---

## Post-implementation note

`SKILL.md` files are picked up by the harness at session start / skill-list refresh —
the new `design-direction` skill and the `frontend-design` disable will apply starting
in a fresh session (or after whatever reload mechanism this harness uses). No action
needed beyond the commits above.
