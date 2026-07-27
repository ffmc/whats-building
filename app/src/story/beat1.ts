import type { AiByYear } from '../lib/data';
import { renderArc, formatPct } from '../charts/arc';

export function renderBeat1(data: AiByYear[]): HTMLElement {
  const beat = document.createElement('div');
  beat.className = 'beat';

  const latest = data[data.length - 1];
  const defaultCaption = `Five years, one direction: AI's share of new popular repos has climbed
    every year since ${data[0].year}, reaching ${latest.pct}% in ${latest.year}. Hover a point for the
    exact numbers behind any year.`;

  beat.innerHTML = `
    <div class="beat-content">
      <div class="eyebrow">The arc</div>
      <h2 class="headline">Half of everything, now</h2>
      <p class="caption" id="beat1-caption">${defaultCaption}</p>
    </div>
    <div class="beat-chart" id="beat1-chart"></div>
  `;

  const chartEl = beat.querySelector('#beat1-chart') as HTMLElement;
  const caption = beat.querySelector('#beat1-caption') as HTMLElement;

  renderArc(chartEl, data, (d) => {
    caption.textContent = d ? formatPct(d) : defaultCaption;
  });

  return beat;
}
