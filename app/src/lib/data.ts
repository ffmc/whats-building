export interface AiByYear {
  year: string;
  total: number;
  ai: number;
  pct: number;
  partial: boolean;
}

export interface Summary {
  total_repos: number;
  boom_date: string;
  ai_by_year: AiByYear[];
  by_category: Record<string, number>;
  by_domain: Record<string, number>;
  by_language: Record<string, number>;
  created_by_month: Record<string, number>;
  star_buckets: [string, number][];
}

export async function loadSummary(): Promise<Summary> {
  const res = await fetch('/data/summary.json');
  if (!res.ok) throw new Error(`Failed to load summary.json: ${res.status}`);
  return res.json();
}
