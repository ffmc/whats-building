import './style.css';
import { loadSummary } from './lib/data';
import { renderBeat0 } from './story/beat0';
import { renderBeat1 } from './story/beat1';

const app = document.querySelector<HTMLDivElement>('#app')!;

async function boot() {
  const summary = await loadSummary();
  const ai = summary.ai_by_year;
  const latest = ai[ai.length - 1];
  const base = ai[0];

  const track = document.createElement('div');
  track.className = 'story-track';
  track.append(renderBeat0(latest, base, summary.total_repos), renderBeat1(ai));
  app.appendChild(track);

  const themeToggle = document.createElement('button');
  themeToggle.className = 'theme-toggle';
  themeToggle.textContent = 'Dark';
  themeToggle.onclick = () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    themeToggle.textContent = isDark ? 'Dark' : 'Light';
  };
  document.body.appendChild(themeToggle);

  setupHorizontalScroll(track);
}

function setupHorizontalScroll(track: HTMLElement) {
  let target = 0;
  let current = 0;
  const maxScroll = () => track.scrollWidth - window.innerWidth;

  window.addEventListener('wheel', (e) => {
    e.preventDefault();
    target += e.deltaY + e.deltaX;
    target = Math.max(0, Math.min(maxScroll(), target));
  }, { passive: false });

  function tick() {
    current += (target - current) * 0.12;
    track.style.transform = `translateX(${-current}px)`;
    requestAnimationFrame(tick);
  }
  tick();

  window.addEventListener('resize', () => {
    target = Math.max(0, Math.min(maxScroll(), target));
  });
}

boot().catch((e) => {
  app.innerHTML = `<div class="beat"><p class="lede">Could not load data: ${e.message}</p></div>`;
});
