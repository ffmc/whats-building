# design-direction skill — design

## Goal

A single, global, user-level skill — **`design-direction`** — that governs aesthetic
direction whenever new or reshaped UI is being built. It actively steers toward current,
trend-aware, distinctive design choices grounded in the specific brief, backed by a
maintained, concrete pattern library, and enforces accessibility/handoff as a mandatory
gate rather than an afterthought.

## Relationship to /design-system

Kept as two separate skills:

- **`/design-system`** extracts and locks down a system from references you already have
  (screenshots, a live site, a brief) into an enforceable token contract
  (`design.md`/`tokens.css`) meant to stay stable and be reused across features. It runs
  once (or rarely, on resync).
- **`design-direction`** originates or reshapes a specific UI surface using live taste
  and trend judgment. It runs every time UI work happens.

Merging them would blur two different processes (image→token extraction vs. open
aesthetic direction) into one skill — an unclear-boundary smell.

`design-direction`'s process checks for an existing `design-system/design.md` first (see
Process, step 2) and builds within it rather than overriding it silently.

## Skill layout

```
~/.claude/skills/design-direction/
  SKILL.md
  references/
    trend-library.md
    copywriting.md
```

## SKILL.md — principles & process

Core principles:
- Ground every design in a concrete subject, audience, and the page's single job —
  don't design in the abstract.
- The hero is a thesis: open with the most characteristic thing in the subject's world.
- Typography carries personality; structural devices (numbering, dividers, labels)
  should encode something true about the content, not decorate it.
- Spend boldness in one place (a single signature element); keep everything else
  disciplined. Match execution complexity to the chosen vision.

Process (numbered, non-negotiable order):

1. **Ground it in the subject** — pin the concrete subject, audience, and the page's job
   before designing anything.
2. **Check for an existing system** — if `design-system/design.md` exists in the
   project, read it and build within its tokens; flag conflicts rather than overriding
   silently. If it doesn't exist, proceed with open aesthetic direction, and mention
   `/design-system draft` as a follow-up once the direction is set.
3. **Consult `trend-library.md`** — pull 2-3 patterns relevant to this brief's category
   (not a random grab-bag). Check each pattern's "currently overused" note before
   committing to it.
4. **Plan → critique → build → critique** — first pass: a compact token/pattern plan
   (color, type, layout, signature element). Review that plan against the brief:
   if any part reads like the generic default for a similar brief, revise it and say
   what changed and why. Only then write code, deriving every decision from the
   revised plan. Self-critique again after building (screenshot if possible).
5. **Accessibility & handoff gate** (mandatory, not optional) — before calling anything
   done, check: color contrast, visible keyboard focus, keyboard navigation,
   screen-reader-friendly structure, reduced-motion alternative, tap target sizing, and
   defined loading/empty/error/success states.
6. **Copywriting** — apply `references/copywriting.md`.

## references/trend-library.md

Front matter: `last_reviewed: <date>`. SKILL.md instructs: if `last_reviewed` is more
than ~90 days old, tell the user the library may be stale and offer to refresh it
(re-research current Awwwards Site-of-the-Day / trend write-ups) before relying on it
for a high-stakes design.

Content organized by category — Layout, Typography, Color & material, Motion &
interaction, Anti-patterns. Each named pattern entry has four parts:

- What it looks like
- Why it currently reads as intentional rather than templated
- When it's the wrong call for a brief
- How it gets flattened into slop when applied carelessly

Each category ends with a **"currently overused" note** flagging patterns that have
themselves saturated into cliché (trend-chasing can become the new template), so using
one requires its own justification rather than automatic application.

The **Anti-patterns** category names the current recognizable AI-look defaults to
actively avoid (e.g. cream background + high-contrast serif + terracotta accent;
near-black background + single neon accent; broadsheet/hairline-rule/zero-radius
layouts), and gets new entries added as new defaults emerge.

## references/copywriting.md

Guidance for content as design material: words as design material (not decoration),
active voice, end-user framing (name things by what people control/recognize, not
system internals), failure/empty states as direction rather than mood, and tone
consistency across a flow.

## Migration steps

1. Write the three new skill files under `~/.claude/skills/design-direction/`.
2. Remove `~/.claude/skills/ui-designer/`.
3. Update `design-system`'s `templates/anti-slop.md` reference to point at
   `design-direction`'s `trend-library.md` as the single source of truth for
   slop/current-pattern judgment.
4. Uninstall the `frontend-design` plugin.
