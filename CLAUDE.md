# whats-building — project instructions

Full context: `README.md` in this directory. Read it before making changes here.

## Non-obvious rules

- `fact_repo_metrics` is **append-only** (time-series, keyed on `repo_id` +
  `snapshot_date`). Never overwrite a prior snapshot — insert a new row per daily pull.
- `fact_repo_classification` is **not** time-series — one row per repo. Before
  calling the LLM to classify a repo, check `description_hash`; only re-classify if
  the description changed or the repo has no row yet. Classification costs money;
  metrics pulls don't.
- The trending filter (`created:>{rolling window}` + `stars:>=N`) is a deliberate
  choice, not a placeholder — it structurally overrepresents AI-tooling-about-AI-tooling.
  That bias is accepted scope, not a bug to fix by broadening the sample.
- `dim_topic` / GitHub topic tags are sparse (~52% of repos untagged in the initial
  sample) — don't rely on them as the sole classification signal.

## When adding to this project

Update the "Status / where we left off" checklist in `README.md` as steps complete.
