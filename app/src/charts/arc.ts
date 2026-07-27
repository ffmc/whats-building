import * as d3 from 'd3';
import type { AiByYear } from '../lib/data';

const F = new Intl.NumberFormat('en-US');

export function renderArc(container: HTMLElement, data: AiByYear[], onHover: (d: AiByYear | null) => void) {
  const width = 640;
  const height = 440;
  const L = 48, R = 20, T = 24, B = 44;
  const plotW = width - L - R;
  const plotH = height - T - B;

  const x = (i: number) => L + (data.length === 1 ? plotW / 2 : (plotW * i) / (data.length - 1));
  const y = (v: number) => T + plotH * (1 - v / 60);

  const wrap = d3.select(container);
  const svg = wrap
    .append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('role', 'img')
    .style('width', '100%')
    .style('height', 'auto')
    .style('overflow', 'visible');

  // gridlines + y-axis labels
  for (let i = 0; i <= 4; i++) {
    const gy = T + (plotH * i) / 4;
    const v = 60 * (1 - i / 4);
    svg.append('line')
      .attr('x1', L).attr('y1', gy).attr('x2', width - R).attr('y2', gy)
      .attr('class', 'chart-gridline');
    svg.append('text')
      .attr('x', L - 10).attr('y', gy + 4).attr('text-anchor', 'end')
      .text(`${Math.round(v)}%`);
  }
  svg.append('line')
    .attr('x1', L).attr('y1', T + plotH).attr('x2', width - R).attr('y2', T + plotH)
    .attr('class', 'chart-baseline');

  const line = d3.line<AiByYear>()
    .x((_d, i) => x(i))
    .y((d) => y(d.pct))
    .curve(d3.curveMonotoneX);

  const path = svg.append('path')
    .datum(data)
    .attr('class', 'chart-line')
    .attr('d', line);

  // draw-on entrance: animate the line stroke from 0 to full length
  const totalLength = (path.node() as SVGPathElement).getTotalLength();
  path
    .attr('stroke-dasharray', `${totalLength} ${totalLength}`)
    .attr('stroke-dashoffset', totalLength)
    .transition()
    .duration(900)
    .ease(d3.easeCubicOut)
    .attr('stroke-dashoffset', 0);

  data.forEach((d, i) => {
    svg.append('text')
      .attr('x', x(i)).attr('y', height - 16).attr('text-anchor', 'middle')
      .text(d.year);

    const dot = svg.append('circle')
      .attr('cx', x(i)).attr('cy', y(d.pct)).attr('r', 0)
      .attr('class', `chart-dot${d.partial ? ' partial' : ''}`);

    dot.transition().delay(300 + i * 90).duration(300).ease(d3.easeBackOut).attr('r', 6);

    const hit = svg.append('circle')
      .attr('cx', x(i)).attr('cy', y(d.pct)).attr('r', 18)
      .attr('fill', 'transparent')
      .style('cursor', 'pointer');

    hit.on('mouseenter', () => {
      dot.transition().duration(120).attr('r', 8);
      onHover(d);
    });
    hit.on('mouseleave', () => {
      dot.transition().duration(120).attr('r', 6);
      onHover(null);
    });
  });

  wrap.append('div')
    .attr('class', 'axis-title')
    .text('Share of that year’s newly created, 50+ star repositories that are AI-related');

  return svg;
}

export function formatPct(d: AiByYear): string {
  const partial = d.partial ? ' (partial year)' : '';
  return `${d.year}${partial}: ${d.pct}% AI-related — ${F.format(d.ai)} of ${F.format(d.total)} repos`;
}
