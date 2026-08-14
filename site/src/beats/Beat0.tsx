import { BeatPanel } from "../components/BeatPanel";
import { HeroFigure } from "../components/HeroFigure";
import { Histogram } from "@charts/Histogram";
import type { Summary } from "../lib/summary";

export function Beat0({ summary }: { summary: Summary }) {
  return (
    <BeatPanel id="beat-0">
      <div className="beat-split">
        <div className="beat-text">
          <p className="beat-eyebrow">The data</p>
          <h2 id="beat-0-title" className="beat-headline">
            Here&rsquo;s what we&rsquo;re actually looking at.
          </h2>
          <HeroFigure value={summary.total_repos} unit="GitHub repos" />
          <p className="beat-body">
            A &ldquo;star&rdquo; is GitHub&rsquo;s bookmark button — one click from
            anyone who found a project worth remembering. We kept only repos with at
            least 50 of them: real, repeated attention, not something only its
            author ever saw. Here&rsquo;s the catch — most repos barely clear that
            bar. A rare few go viral. The gap between them is enormous.
          </p>
        </div>
        <div className="beat-chart-col">
          <Histogram
            data={summary.star_histogram}
            ariaLabel="Histogram of star counts across all repos, sharply concentrated near the 50-star floor with a long tail toward viral projects"
            caption="Repos by star count (log scale)"
            fill="var(--chart-seq-3)"
            peakLabel={(d) => `most repos land right here, ${d.starsMin}–${d.starsMax}★`}
          />
        </div>
      </div>
    </BeatPanel>
  );
}
