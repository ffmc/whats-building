export type Summary = {
  total_repos: number;
  boom_date: string;
  by_category: Record<string, number>;
  by_domain: Record<string, number>;
  cohort: { pre_boom: number; post_boom: number };
  ai_related_by_cohort: { pre_boom: number; post_boom: number };
  star_buckets: [string, number][];
  star_histogram: { starsMin: number; starsMax: number; count: number }[];
};

let cached: Promise<Summary> | null = null;

export function loadSummary(): Promise<Summary> {
  if (!cached) {
    cached = fetch("/data/summary.json").then((res) => {
      if (!res.ok) throw new Error(`summary.json ${res.status}`);
      return res.json() as Promise<Summary>;
    });
  }
  return cached;
}
