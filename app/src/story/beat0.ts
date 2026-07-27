import type { AiByYear } from '../lib/data';

const F = new Intl.NumberFormat('en-US');

export function renderBeat0(latest: AiByYear, base: AiByYear, totalRepos: number): HTMLElement {
  const beat = document.createElement('div');
  beat.className = 'beat';
  beat.innerHTML = `
    <div class="beat-content">
      <div class="eyebrow">What people are building on GitHub</div>
      <p class="context">Every GitHub repository created since mid-2021 that reached 50+ stars —
      ${F.format(totalRepos)} of them — classified by what it does and whether AI is part of it.
      This is a story about where that effort has gone.</p>
      <p class="hero-figure">${latest.pct}%</p>
      <p class="lede">of repositories that broke out in ${latest.year} are AI-related.</p>
      <p class="caption">In <span class="figure">${base.year}</span> that share was just
      <span class="figure">${base.pct}%</span> — about 1 in 7. Scroll to see how it climbed.</p>
    </div>
    <div class="scroll-hint">Scroll to begin &rarr;</div>
  `;
  return beat;
}
