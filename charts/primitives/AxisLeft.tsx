import { ticksFor, type BottomScale } from "./AxisBottom";

export type LeftScale = BottomScale;

type Props = {
  scale: LeftScale;
  width: number;
  tickCount?: number;
  format?: (value: any) => string;
  grid?: boolean;
};

export function AxisLeft({
  scale,
  width,
  tickCount = 5,
  format = String,
  grid = true,
}: Props) {
  const ticks = ticksFor(scale, tickCount, format);

  return (
    <g className="chart-axis">
      {ticks.map((tick) => (
        <g key={tick.key} transform={`translate(0,${tick.offset})`}>
          {grid && <line className="chart-grid" x2={width} />}
          <line x2={-6} />
          <text dy="0.32em" x={-10} textAnchor="end">
            {tick.label}
          </text>
        </g>
      ))}
    </g>
  );
}
