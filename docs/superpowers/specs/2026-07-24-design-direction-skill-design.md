# design-direction skill — design

## Problem

The built-in `frontend-design` plugin skill (used for aesthetic direction on new/reshaped
UI) still tends to converge on a recognizable "Claude design style" despite its own
anti-slop warnings. Those warnings are one abstract calibration paragraph, not a
maintained, concrete reference — so the pull away from generic defaults is weak, and
there's no active pull *toward* current, distinctive, Awwwards-caliber work.

Separately, `~/.claude/skills/ui-designer` is a generic/ported skill template that
references a "context-manager" and subagents (`frontend-developer`,
`accessibility-tester`, etc.) that don't exist in this setup. Its process content
(accessibility gate, handoff notes) is useful; the rest isn't applicable.

## Goal

Replace both with a single, global, user-level skill — **`design-direction`** — that:

1. Actively steers toward current, trend-aware, distinctive design (not just away from
   slop), backed by a maintained, concrete pattern library instead of one paragraph.
2. Folds in the useful parts of `ui-designer` (accessibility/handoff checklist).
3. Coexists cleanly with `/design-system` rather than merging into it — different job,
   different trigger, different lifecycle (see "Relationship to /design-system" below).

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

To avoid drift between the two skills' anti-slop guidance:
- `design-system`'s existing `templates/anti-slop.md` is superseded — it should point at
  `design-direction`'s `trend-library.md` as the single source of truth for "what's slop
  / what's current," rather than maintaining a second, duplicate list.
- `design-direction`'s process checks for an existing `design-system/design.md` first
  (see Process, step 2) and builds within it rather than overriding it silently.

## Skill layout

```
~/.claude/skills/design-direction/
  SKILL.md
  references/
    trend-library.md
    copywriting.md
```

`~/.claude/skills/ui-designer/` is retired (deleted) once its useful content is folded
in. The `frontend-design` plugin is uninstalled.

## SKILL.md — principles & process

Core principles (carried forward from `frontend-design`, which got these right):
- Ground every design in a concrete subject, audience, and the page's single job —
  don't design in the abstract.
- Hero-as-thesis, typography-as-personality, structure-as-information: the same
  content/structure principles frontend-design already states well.
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
5. **Accessibility & handoff gate** (folded from `ui-designer`, mandatory, not
   optional) — before calling anything done, check: color contrast, visible keyboard
   focus, keyboard navigation, screen-reader-friendly structure, reduced-motion
   alternative, tap target sizing, and defined loading/empty/error/success states.
6. **Copywriting** — apply `references/copywriting.md` (ported near-verbatim from
   frontend-design's writing section — it wasn't the part causing the generic-look
   complaint).

`ui-designer`'s context-discovery step (querying a "context-manager") and
subagent-handoff section (`frontend-developer`, `accessibility-tester`, etc.) are
dropped — they reference infrastructure that doesn't exist in this setup.

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
- How AI tends to flatten it into slop

Each category ends with a **"currently overused" note** flagging patterns that have
themselves saturated into cliché (trend-chasing can become the new template), so using
one requires its own justification rather than automatic application.

The **Anti-patterns** category keeps frontend-design's three named AI-look defaults
(cream+serif+terracotta; near-black+single neon accent; broadsheet/hairline/zero-radius)
since those calibration examples remain accurate, and gets new entries added as they
emerge.

## references/copywriting.md

Ported near-verbatim from `frontend-design`'s existing writing/content section (words as
design material, active voice, end-user framing, failure/empty states as direction, tone
consistency). No changes needed here — this wasn't part of the reported problem.

## Migration steps (implementation, not part of this doc's scope beyond listing them)

1. Write the three new skill files under `~/.claude/skills/design-direction/`.
2. Delete `~/.claude/skills/ui-designer/`.
3. Update `design-system`'s `templates/anti-slop.md` reference to point at
   `design-direction`'s `trend-library.md`.
4. Uninstall the `frontend-design` plugin.
