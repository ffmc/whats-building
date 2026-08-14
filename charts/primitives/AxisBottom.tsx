import type { ScaleBand, ScaleLinear, ScaleLogarithmic, ScaleTime } from "d3-scale";

export type BottomScale =
  | ScaleLinear<number, number>
  | ScaleLogarithmic<number, number>
  | ScaleTime<number, number>
  | ScaleBand<string>;

type Props = {
  scale: BottomScale;
  transform: string;
  tickCount?: number;
  /** Explicit tick values — bypasses scale.ticks(), needed for log scales
   * whose default tick generation ignores the count hint and returns every
   * integer multiple per decade. */
  tickValues?: number[];
  format?: (value: any) => string;
  tickSize?: number;
};

type Tick = { key: string; label: string; offset: number };

function isBand(scale: BottomScale): scale is ScaleBand<string> {
  return "bandwidth" in scale;
}

export function ticksFor(
  scale: BottomScale,
  tickCount: number,
  format: (value: any) => string,
  tickValues?: number[],
): Tick[] {
  if (isBand(scale)) {
    return scale.domain().map((value) => ({
      key: value,
      label: format(value),
      offset: (scale(value) ?? 0) + scale.bandwidth() / 2,
    }));
  }
  const values = tickValues ?? (scale.ticks(tickCount) as any[]);
  return values.map((value) => ({
    key: String(value),
    label: format(value),
    offset: (scale as (v: any) => number)(value),
  }));
}

export function AxisBottom({
  scale,
  transform,
  tickCount = 5,
  tickValues,
  format = String,
  tickSize = 6,
}: Props) {
  const [start, end] = scale.range();
  const ticks = ticksFor(scale, tickCount, format, tickValues);

  return (
    <g className="chart-axis" transform={transform}>
      <line x1={start} x2={end} />
      {ticks.map((tick) => (
        <g key={tick.key} transform={`translate(${tick.offset},0)`}>
          <line y2={tickSize} />
          <text dy="0.71em" y={tickSize + 4} textAnchor="middle">
            {tick.label}
          </text>
        </g>
      ))}
    </g>
  );
}
