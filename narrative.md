# The narrative and the charts

Source of truth for the story, the data findings, the chart specs, and the technical
constraints that shape them. Supersedes `docs/superpowers/specs/2026-07-29-narrative-and-charts.md`
(deleted — this doc absorbed everything from it still valid, including payload sizing
and the verification checklist). Visual system (palette, type, motion, components)
lives in `design-system/design.md` — this doc references it, doesn't repeat it.

## The reframe

The dataset is filtered to repos with **≥50 stars**. Every repo in it already cleared an
attention bar. The page is not "what exists on GitHub" — it is **what people paid
attention to on GitHub**. The star filter is not a caveat buried in a footer; it is the
premise, stated up front in beat 0.

A second premise sits beside it: the 5-year discovery window (2021-07-19 → today) was
chosen to **straddle the AI boom** (ChatGPT, Nov 2022) on purpose, so the dataset
contains a real pre-boom-created cohort to compare against post-boom-created repos —
not an arbitrary lookback. This is stated as premise too, in beat 0.5, with a number
attached (see Findings).

Within that already-filtered set, the page shows: the categories and domains people
built in, the fact that most of what's attention-worthy now is AI-focused, named
recognizable repos, and then hands the reader the full 262,902-repo set to check the
argument themselves.

## The two AI axes — and which one this page tells

There are two distinct questions people mean when they say "was this built with AI":

1. **Built WITH AI** — was the *code itself* authored using AI tooling (Copilot,
   Claude Code, Cursor, etc.)?
2. **Built FOR AI** — is the repo's *subject matter* AI/agents/MCP — what the
   `ai-agents-mcp`, `llm-genai-apps` domains already capture?

**This page tells axis 2 only.** `fact_repo_classification.is_ai_built_or_related`
(`sql/schema.sql:67`) and the domain taxonomy (`scripts/classify.py:48`) were always
built to answer "is this repo about AI," never "was AI used to write it." GitHub's API
exposes no signal for axis 1, and inferring it (commit patterns, README mentions,
`.cursor`/`.claude` directories, co-author trailers) is a materially harder, noisier
classification task than the one already running.

**Decision:** axis 2 is the fully-charted story. Axis 1 is named as a known,
stated limitation — one honest sentence in the narrative ("we can tell you what people
built, not yet whether AI helped build it") — not faked with a weak proxy signal.
Revisiting axis 1 is a separate project (new classifier pass, new cost, uncertain
accuracy), out of scope here.

## Format, decided

- **Horizontal scroll**, driven by a normal vertical wheel/trackpad gesture (native
  scroll semantics, not a hijacked one-beat-per-scroll snap). Mobile swipes
  right-to-left instead, since there's no wheel — see Scroll mechanics below.
- **Every beat is explorable in place.** No separate "story mode" vs. "explore mode" —
  each beat states its claim and lets the reader drill into the chart that proves it.
  The final beat is the full explorer, not a different app bolted on the end.
- Story that also lets the reader explore — a hybrid of "one argument, told well" and
  "a reference dashboard," not a pure instance of either.

## Findings that ground the narrative

Pulled directly from `whats_building.db`, not assumed:

- **262,902 repos**, created 2021-07-19 → 2026-07-21, all ≥50 stars, `fork:false`.
- **Pre/post-boom split** (boom date 2022-11-30, ChatGPT launch — already computed by
  `aggregate.py`'s `BOOM_DATE` constant and `summary.json`'s `ai_related_by_cohort`):
  **76,810 pre-boom repos, 14.8% AI** vs. **186,092 post-boom repos, 35.7% AI** — a
  2.4× jump in AI share between cohorts, the number that grounds beat 0.5.
- **AI share of new repos by year:** 14.1% (2021, partial) → 15.7% → 28.6% → 31.5% →
  40.2% → **50.2%** (2026, partial).
- **`ai-agents-mcp` is the real story, not just the AI-share headline:** 275 repos
  created in 2022 → **9,072 in 2026** (33×). It is now the largest domain in the 2026
  cohort, past `devops-infra` (1,557), which used to dwarf it. Of the 20,383 repos in
  this domain, **3,640 (17.9%)** explicitly mention "mcp" or "model context protocol"
  in their description — the sharpest sub-slice of the story, not the whole of it (the
  domain also includes generic agent frameworks; `ai-agents-mcp` is one bundled
  taxonomy value, MCP is not separable at the classifier level — see Pipeline changes).
- **AI did not spread evenly — it built new territory.** By domain: `llm-genai-apps`
  99.4% AI, `ai-agents-mcp` 99.0%, `computer-vision` 91.2%, `ml-dl-research` 89.9% — but
  `ui-frontend` 1.1%, `compilers-languages` 1.4%, `gaming-entertainment` 3.1%,
  `devops-infra` 3.7%.
- **The category×domain flows are bimodal**, and this is the single most interesting
  fact in the dataset:

  | AI-share band | flows (≥300 repos) | repos | % of repos |
  |---|---|---|---|
  | 0–10% | 84 | 118,522 | 57.4% |
  | 10–80% | 26 | 23,793 | **11.5%** |
  | 80–100% | 27 | 64,248 | 31.1% |

  Almost no middle ground. Repos are overwhelmingly AI-related or overwhelmingly not.
  This is *why* the brand palette is a diverging pair rather than an arbitrary choice —
  the polarity in the data and the polarity in the colour system are the same thing.

- **Named, recognizable repos** (by stars): `openclaw/openclaw` 383,687 · `ollama/ollama`
  176,566 · `open-webui` 146,188 · `AUTOMATIC1111/stable-diffusion-webui` 164,269 ·
  `anthropics/claude-code` 138,554 · `openai/whisper` 105,328.
  *Wispr Flow* (the dictation product) is closed-source and not in the dataset — beat 6
  uses repos recognizable **as products**, not that specific one.

## The eight beats

Each beat: a claim, one primary chart, and an in-place drill.

| # | Beat | Claim | Form | Colour job | Explore in place |
|---|---|---|---|---|---|
| 0 | **The bar** | 262,902 repos, every one ≥50★. Nothing here is obscure. | Hero figure + star-bucket bars | sequential (steel) | static premise; no live star-floor slider (cut, see below) |
| 0.5 | **The boom** | Pre-boom 14.8% AI vs. post-boom 35.7% AI — the window was chosen to straddle this. | Two-bar cohort comparison | sequential (steel) | — |
| 1 | **What people build** | library-sdk 65,952 · web-app 30,934 · docs-reference 25,362 · cli-tool 25,331 | left-node bar (see Beat 1/2/5 unification) | sequential (steel) | Click a category → its top repos |
| 2 | **What it's about** | ai-agents-mcp 20,383 · devops-infra 19,183 · ml-dl-research 17,129 · security 16,658 | right-node bar (same object as beat 1) | sequential (steel) | Click a domain → its top repos |
| 3 | **The shift** | 14.1% → 50.2% AI over five years | line/area over time | AI-accent | Hover a year → that cohort's mix |
| 4 | **The new territory** | ai-agents-mcp: 275 → 9,072 (33×); 17.9% MCP-labeled | single large line, same AI-accent as beat 3 | AI-accent (reused from beat 3) | Toggle "compare to other domains" → demotes to small multiples, emphasis (accent + grey) |
| 5 | **Form meets subject** | *(the centerpiece)* | **Sankey**, same object as beats 1/2, ribbons revealed | diverging on AI share | Hover node → highlight flows; click ribbon → its repos; mobile: heatmap/table is primary |
| 6 | **You know these** | openclaw · ollama · open-webui · stable-diffusion-webui · claude-code · whisper | repo cards | none (categorical chips only) | Links out to GitHub |
| 7 | **The whole board** | All 262,902, yours to filter | beeswarm (primary) + virtualized table (fallback) | AI-share / category, per facet | Facet toggle, hover tooltip, click → repo |

Caveats (trending-sample bias, survivorship inflation on recent years, 2026/2021
partial-year data, and the axis-1 "built WITH AI" gap) live in **beat 0 / 0.5 as
premise**, not a disclaimer footer.

## Why beat 4 moved, and why it shares beat 3's colour

Beat 4 (`ai-agents-mcp` growth) used to sit after the Sankey, as one of several toggle-able
small multiples. Now that "built FOR AI" is the confirmed thesis rather than one theme
among several, it moves to sit **right after beat 3**: macro shift ("AI share went
14%→50%," which can feel abstract) immediately followed by the concrete catalyst
("here's the specific new territory driving it — 275 → 9,072 in four years"). The pair
reads as one abstract/concrete rhyme rather than two disconnected facts.

Beat 4 also **reuses beat 3's AI-accent colour** for its single line, rather than the
old emphasis (accent + grey) treatment. `ai-agents-mcp` is 99% AI — the same hue beat 3
used for "the AI share" is literally correct here, not just visually convenient. The
emphasis (accent + grey) scheme is kept for the *demoted* small-multiples drill-down,
where beat 4's domain gets picked out against several greyed-out others.

**Deliberately not seeded:** beats 1 and 2 stay strictly neutral/sequential, no AI
colour hint. `design-system/design.md`'s colour-job discipline (sequential for raw
counts, diverging/accent only once AI is the variable being measured) is a
signal-per-chart rule; breaking it early to foreshadow the thesis would blur the one
place colour actually means something. Beat 3 stays the clean narrative "turn."

## Beats 1, 2, 5 — one chart, three progressive reveals

Sankey node totals **are** the category and domain bar charts: summing ribbon widths by
left node reproduces beat 1's category counts exactly; summing by right node reproduces
beat 2's domain counts. There's no data reason to build three separate charts.

**Decision:** one `d3-sankey` layout, computed once, rendered in three states:

- **Beat 1** — only left nodes shown, as a bar (no ribbons). Category totals.
- **Beat 2** — only right nodes shown, as a bar (no ribbons). Domain totals.
- **Beat 5** — same nodes, **ribbons revealed**. The full flow.

Node positions and colours stay visually continuous across 1 → 2 → 5, so the reader
feels the chart unfold rather than encountering three unrelated visualizations. This is
also cheaper to build than three independent chart components.

## Beat 5 — the Sankey, specified

The chart that was explicitly requested, and the load-bearing one. Implementation:
**`d3-sankey`** (the standard d3 layout module), locked in now rather than left open —
it's layout-only (computes node/link positions, no rendering opinions), matching the
stack's "d3 for calculation, React for rendering" split, and it's the de facto standard
so there's no research detour at build time. Build with `/d3-charts`.

- **Left nodes:** 13 categories. **Right nodes:** 27 domains. `unknown` / `other` /
  `unclassified` excluded from the diagram — `unknown→unknown` alone is 26,030 repos
  and would dominate an uninformative slab. Their count is disclosed in a note beside
  the chart, never silently dropped.
- **Ribbons:** 383 flows exist; the top ~40 are drawn (top 30 ≈ 53.6% of repos, top 40
  ≈ 61.4%) and each category's tail bundles into a muted "other" ribbon.
- **Ribbon height** = repo count. **Ribbon colour = AI share**, on the diverging scale
  (`--chart-div-ai-*` / `--chart-div-not-ai-*` / `--chart-div-mid`).
- **Why diverging, and why this doesn't blow the categorical ceiling.** 13→27 nodes far
  exceeds the `dataviz` skill's ~5-slot categorical cap. The resolution: **colour does
  not carry node identity** here. Identity comes from direct node labels; colour carries
  exactly one variable, AI share. Diverging is the right form because the data is
  genuinely bipolar — see the bimodality table above — and the near-empty grey middle
  band *is* the finding, visible directly rather than stated in prose.
- **What it shows that a bar chart cannot:** `library-sdk` fans out into
  `ai-agents-mcp` (98.6% AI) and `ui-frontend` (1.0% AI) side by side — same form, same
  builders, two disjoint worlds.
- **Horizontal-scroll payoff:** the Sankey is deliberately wider than the viewport
  (`beatPanel` variant `full`, the one place a beat may exceed 100vw). The page's
  scroll gesture is the reading gesture for this beat.
- **Table/heatmap view is mandatory** (per `dataviz` and `chartFrame`'s closed states),
  not optional: the same data as a 13×27 heatmap and a sortable table, reachable from
  the beat. On mobile this heatmap/table *is* the primary form — a full Sankey doesn't
  fit a ~390px viewport.

## Beat 7 — the explorer, all 262,902 rows

**Primary form: a beeswarm, Canvas-rendered.** Sliceable/facetable, highlightable by
category/domain/AI-share, hover tooltips, click-through to the GitHub repo. A
virtualized table remains as the **mandatory accessible fallback** (per `dataviz` and
`chartFrame`'s closed states — every chart needs a table view), and is what mobile and
screen-reader users get primarily, same as beat 5's heatmap/table pattern.

**Why Canvas, not SVG:** 262,902 DOM/SVG nodes is a non-starter — same limit that
already ruled out one-row-per-repo table rendering. Canvas has no per-point DOM
elements, so hover/click hit-testing needs a **quadtree spatial index** built over the
rendered positions.

**Why swarm layouts are precomputed at build time, not simulated client-side.** A
beeswarm needs collision-resolved positions (`d3.forceSimulation` + `forceCollide`
territory). Running that live over 262k nodes on every facet change would take seconds
per re-layout — real jank, not frames. **Decision: precompute 2–3 fixed layouts in
`aggregate.py`** at build time — grouped by category, by domain, by AI-share — matching
the facets the rest of the narrative already uses (category in beat 1, domain in beat
2, AI-share throughout). Shipped as extra x/y float coordinate columns alongside the
existing tier-1 index. This keeps every interaction instant and avoids introducing Web
Workers as new infrastructure. Tradeoff accepted: the reader can't invent an arbitrary
new facet — consistent with how every other beat in the narrative works (fixed,
curated views, not an open-ended pivot table).

**Rejected: a live Postgres/Supabase backend for this beat.** Considered and rejected —
the beeswarm's cost is layout *computation*, not data retrieval, and a live DB doesn't
solve that; the compute still has to happen somewhere. `README.md:223-225` already
reasoned through this exact tradeoff for the whole project ("Supabase alone does not
solve this. It is storage, not compute") and chose static JSON + $0 hosting explicitly,
rejecting Supabase Pro. A DB round-trip per hover/facet-change would also be *slower*
than the already-planned local scan over a typed array (10–30ms). Nothing here reopens
that decision.

Sized with real measurements, not estimates (brotli -q9, actual DB data):

| Column | Raw | Brotli |
|---|---|---|
| `full_name` | 6.70 MB | **2.98 MB** |
| `description` | 22.71 MB | **7.25 MB** |
| stars (u32) | 1.05 MB | 0.38 MB |
| created month (u16) | 0.53 MB | ~0.00 MB |
| category (u8, 15 vals) | 0.26 MB | 0.13 MB |
| domain (u8, 30 vals) | 0.26 MB | 0.16 MB |
| language (u16, >256 vals) | 0.53 MB | ~0.20 MB |
| ai flag (u8) | 0.26 MB | ~0.03 MB |
| swarm x/y per layout (2× f32) | ~2.10 MB/layout | ~0.8–1.2 MB/layout (est., floats compress worse than ints) |

**Two-tier design:**

- **Tier 1 — the index, ~3.9 MB brotli + ~2–3.5 MB for 2–3 precomputed swarm layouts.**
  Every one of the 262,902 rows: name, stars, created month, category, domain,
  language, AI flag, plus swarm x/y per precomputed facet. Columnar typed arrays, not
  JSON. Powers all filtering, sorting, counting, name-substring search, and beeswarm
  rendering. Fetched once, cacheable. Gated behind entering beat 7 — never loaded up
  front (mobile data cost).
- **Tier 2 — descriptions, 7.25 MB brotli, sharded** into ~64 chunks of ~4k rows
  (~110 KB each), fetched only for rows scrolled/hovered into view (tooltip content).

**Consequences accepted up front:**

- Name + facet search is effectively instant (linear scan over a ~6.7 MB
  `Uint8Array` is ~10–30 ms).
- **Full-text search across descriptions is not free** — needs all of tier 2. Ship as
  explicit opt-in ("search descriptions too — loads 7 MB"), not pretend-instant.
- Rendering requires Canvas + quadtree hit-testing for the beeswarm, and a
  **virtualized** list for the table fallback — 262k DOM rows isn't viable either way.
- Rows sorted by creation date on disk so the month column delta-compresses to
  ~nothing (confirmed — that's why it measures ~0.00 MB).
- On mobile, the table fallback drops to a single-column card list; filters collapse
  into a sheet off the `controlBar`'s `expanded` state.

**Star floor:** the beat-0 idea of a live slider that re-cuts the 50★ threshold and
recomputes every downstream beat was **cut**. It's the most expensive interaction in
the design (forces the whole tier-1 index to load before the first screen is
interactive, plus live aggregation over 262k rows per drag) and the argument doesn't
depend on the reader re-cutting it. Beat 0 states the 50★ bar statically. The
capability still exists, scoped to **beat 7's explorer only**, where the index is
already loaded and the cost is already paid.

## Scroll mechanics — decided

**Desktop:** a normal vertical wheel/trackpad gesture moves the page **sideways** via
Lenis in `orientation: 'horizontal'` mode (`--scroll-lerp: 0.085`, see
`design-system/design.md` § Motion). It should feel like scrolling a vertical page —
the reader never thinks about the mechanism. Non-negotiable regardless:

- Keyboard: arrows, PageUp/PageDown, Home/End all navigate beats.
- `prefers-reduced-motion: reduce`: Lenis disabled, native scrolling takes over, no
  smoothing or easing.
- Browser find-in-page and deep-linked beats (`beatPanel`'s per-beat `id`) still land
  correctly.
- Scroll position survives resize and back-navigation.

**Mobile:** stays horizontal — beats sit side by side, swiped right-to-left. A
persistent affordance (arrow / progress rail, i.e. `stageRail`) makes this obvious,
since the format isn't self-evident on a phone. This is why beats 5 and 7 need
dedicated mobile forms rather than simply scaling down (heatmap for the Sankey, card
list for the explorer) — the horizontal layout doesn't relax into a vertical one at
small sizes the way it would in a simpler responsive design.

**Stage rail** (top, fixed) shows which beat the reader is on — `stageRail` component,
one segment per beat, clickable, keyboard-reachable. **Control bar** (bottom, fixed)
carries filters and the live record count — `controlBar` component, `narrative` variant
for beats 0–6, `explorer` variant for beat 7.

## Pipeline changes needed

- `scripts/aggregate.py`'s `top_lists()` (`scripts/aggregate.py:135-154`) still doesn't
  select or emit `is_ai_built_or_related` per repo — every entry lacks an AI flag.
  Beats 1, 2, 6, and the explorer all need this fixed before they can render/filter by
  AI correctly.
- New emitters needed: tier-1 binary/columnar index, tier-2 description shards, and the
  2–3 precomputed beeswarm swarm-layout coordinate columns described above.
- **Already done, no action needed:** the pre/post-boom split (`BOOM_DATE` constant,
  `ai_related_by_cohort` in `summary.json`, `scripts/aggregate.py:17,65-74,108`) —
  beat 0.5 can use this directly.
- **Not pursued:** re-classifying to split `ai-agents-mcp` into separate MCP vs.
  generic-agent domains. The cheap alternative — a `LIKE '%mcp%' OR LIKE '%model
  context protocol%'` substring pass over already-classified data, zero LLM cost — is
  sufficient for beat 4's sub-stat (17.9% MCP-labeled) and was run directly against
  `whats_building.db` to produce the number above. No new classifier pass needed.

## Stack

React + TypeScript (a change from the torn-out prototype's vanilla TS/Vite), because
`/d3-charts` — the chart-building approach settled on for this project, and the one to
use for every chart build in this narrative — is built on "React for rendering, d3 for
calculation only" and binds chart colour/type to a React design system. `tokens.css`
(generated from `design-system/design.md`) is framework-agnostic CSS custom properties
either way. Beeswarm layout computation is the one exception to "d3 in the browser" —
it runs at build time in Python (`aggregate.py`), not client-side d3-force, per the
Beat 7 reasoning above.

## Sequencing

1. ~~Design system~~ — done: `design-system/design.md` (Signal), `design.html`,
   `tokens.css` generated and accepted.
2. Fix `aggregate.py`'s AI-flag bug in `top_lists()`; add the tier-1/tier-2 explorer
   emitters plus the precomputed beeswarm layouts; regenerate data.
3. Feed the tokens into `dataviz` as palette parameters and confirm
   `scripts/validate_palette.js` still passes for the final in-app usage (it already
   passed in isolation during system-mode — see `design-system/design.md` § Colors).
4. Build beats 0, 0.5, 1, 2, 3, 6 first (cheapest) to validate the horizontal-scroll
   shell, Lenis integration, and the shared Sankey-object node rendering.
5. Build beat 4 (the promoted single-line chart, reusing beat 3's colour).
6. Build beat 5 (Sankey ribbons revealed + heatmap/table).
7. Build beat 7 (beeswarm + table fallback) last — highest risk, most isolated, largest
   payload.

## Verification

- **Payload:** assert tier 1 ≤ 7 MB brotli (index + swarm layouts), each description
  shard ≤ 150 KB, and the server actually serves `content-encoding: br`.
- **Explorer:** load with network throttled to Fast 3G; first interactive filter under
  5 s; beeswarm hover/click hit-testing correct at all 262,902 points; scroll the table
  fallback to row 262,000 with no dropped shard or memory blowup.
- **Charts:** `dataviz`'s `validate_palette.js` passes for every palette actually used
  in-app; every chart has a table view and a hover layer (per `chartFrame`'s closed
  states in `design-system/design.md`); beats 1/2/5 confirmed to share one Sankey
  layout object, not three independent computations.
- **Numbers:** rendered figures match direct SQL — AI share by year, pre/post-boom
  split (14.8% vs 35.7%), the 33× `ai-agents-mcp` growth, the 17.9% MCP substring
  share, the three bimodality bands. Charts must never restate a number the DB
  disagrees with.
- **Accessibility gate:** WCAG AA contrast (already verified for every token — see
  `design-system/design.md` § Colors), visible keyboard focus, intact heading order,
  reduced-motion alternative for the scroll, ≥44px tap targets, defined
  loading/empty/error states — the explorer especially.
