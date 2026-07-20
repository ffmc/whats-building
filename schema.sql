-- whats-building schema. SQLite for dev; kept Postgres-compatible for later migration.

CREATE TABLE dim_repo (
    repo_id        INTEGER PRIMARY KEY,   -- GitHub numeric id
    node_id        TEXT,                  -- GraphQL global id (rename-proof metric lookups)
    full_name      TEXT,
    owner          TEXT,                  -- owner.login
    owner_type     TEXT,                  -- owner.type: User | Organization
    name           TEXT,
    description    TEXT,
    homepage       TEXT,
    language       TEXT,
    license        TEXT,                  -- license.spdx_id
    is_fork        INTEGER,
    is_template    INTEGER,
    default_branch TEXT,
    size_kb        INTEGER,               -- repo size in KB
    created_at     TEXT,
    pushed_at      TEXT,                  -- latest push; refreshed daily
    archived       INTEGER,               -- latest; refreshed daily
    first_seen_at  TEXT                   -- when we first pulled it
);

CREATE TABLE dim_topic (
    topic_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT UNIQUE
);

CREATE TABLE bridge_repo_topic (
    repo_id  INTEGER REFERENCES dim_repo(repo_id),
    topic_id INTEGER REFERENCES dim_topic(topic_id),
    PRIMARY KEY (repo_id, topic_id)
);

-- Append-only time-series, keyed (repo_id, snapshot_date). Never overwrite a prior snapshot.
CREATE TABLE fact_repo_metrics (
    repo_id           INTEGER REFERENCES dim_repo(repo_id),
    snapshot_date     TEXT,
    tier              TEXT,   -- anchor | weekly | monthly (drives retention)
    stargazers_count  INTEGER,
    forks_count       INTEGER,
    watchers_count    INTEGER,   -- REAL watchers (GraphQL watchers.totalCount), not REST's stars-duplicate
    open_issues_count INTEGER,
    PRIMARY KEY (repo_id, snapshot_date)
);

-- Retention: delete WHERE tier='weekly' AND snapshot_date older than 90d; never touch anchor/monthly.
CREATE INDEX idx_metrics_tier_date ON fact_repo_metrics (tier, snapshot_date);

-- One row per repo (not time-series). Re-classify only if description_hash changed.
CREATE TABLE fact_repo_classification (
    repo_id                INTEGER PRIMARY KEY REFERENCES dim_repo(repo_id),
    category               TEXT,
    domain                 TEXT,
    is_ai_built_or_related INTEGER,
    confidence             TEXT,
    description_hash       TEXT,
    classified_at          TEXT
);
