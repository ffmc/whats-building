import { BeatPanel } from "../components/BeatPanel";
import { Barplot } from "@charts/Barplot";
import type { Summary } from "../lib/summary";

export function Beat05({ summary }: { summary: Summary }) {
  const preShare = (summary.ai_related_by_cohort.pre_boom / summary.cohort.pre_boom) * 100;
  const postShare = (summary.ai_related_by_cohort.post_boom / summary.cohort.post_boom) * 100;
  const bootYear = new Date(summary.boom_date).getFullYear() - 1;
  const boomMonth = new Date(summary.boom_date).toLocaleDateString(undefined, {
    month: "long",
    year: "numeric",
  });

  const data = [
    { label: "Pre-boom", value: preShare },
    { label: "Post-boom", value: postShare },
  ];

  return (
    <BeatPanel id="beat-0-5">
      <div className="beat-split">
        <div className="beat-text">
          <p className="beat-eyebrow">The dividing line</p>
          <h2 id="beat-0-5-title" className="beat-headline">
            The five years in this dataset weren&rsquo;t a random window — they were
            picked to catch the moment it changed.
          </h2>
          <p className="beat-body">
            Every repo here was created after {bootYear}, which means the set splits
            cleanly in two: {summary.cohort.pre_boom.toLocaleString()} repos from
            before ChatGPT&rsquo;s launch in {boomMonth}, and{" "}
            {summary.cohort.post_boom.toLocaleString()} after. Before, {preShare.toFixed(1)}%
            of what people noticed was AI. After,{" "}
            <strong>{postShare.toFixed(1)}%</strong> — a {(postShare / preShare).toFixed(1)}×
            jump. That&rsquo;s the shift this whole story is about.
          </p>
        </div>
        <div className="beat-chart-col">
          <Barplot
            data={data}
            ariaLabel={`AI share of pre-boom repos, ${preShare.toFixed(1)} percent, versus post-boom repos, ${postShare.toFixed(1)} percent`}
            caption="AI share by cohort"
            valueLabel="AI share (%)"
            formatValue={(v) => `${v.toFixed(1)}%`}
            fill="var(--chart-seq-3)"
            highlight="Post-boom"
          />
        </div>
      </div>
    </BeatPanel>
  );
}
