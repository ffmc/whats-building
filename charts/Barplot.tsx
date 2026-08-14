import { useState } from "react";
import { scaleBand, scaleLinear } from "d3-scale";
import { max } from "d3-array";
import { ChartFrame } from "./primitives/ChartFrame";
import { AxisBottom } from "./primitives/AxisBottom";
import { DataTable } from "./primitives/DataTable";
import { Tooltip } from "./primitives/Tooltip";

export type BarDatum = { label: string; value: number };

/** Rounded top corners, square baseline — per dataviz mark spec. */
function barPath(x: number, y: number, width: number, height: number, radius: number): string {
  const r = Math.min(radius, width / 2, Math.max(height, 0));
  if (height <= 0) return "";
  return `M${x},${y + height} V${y + r} Q${x},${y} ${x + r},${y} H${x + width - r} Q${x + width},${y} ${x + width},${y + r} V${y + height} Z`;
}

type Props = {
  data: BarDatum[];
  ariaLabel: string;
  caption: string;
  valueLabel: string;
  height?: number;
  formatValue?: (value: number) => string;
  /** CSS custom property, e.g. "var(--chart-seq-3)" */
  fill: string;
  /** data.label of the bar to carry elevation.glow — reserve for the beat's one hero bar. */
  highlight?: string;
};

export function Barplot({
  data,
  ariaLabel,
  caption,
  valueLabel,
  height,
  formatValue = (v) => v.toLocaleString(),
  fill,
  highlight,
}: Props) {
  const margin = { left: 16, bottom: 40, top: 40, right: 16 };
  const [hover, setHover] = useState<{ label: string; value: number; x: number; y: number } | null>(
    null,
  );

  return (
    <ChartFrame
      label={ariaLabel}
      height={height}
      margin={margin}
      table={
        <DataTable
          caption={caption}
          rows={data}
          columns={[
            { key: "label", label: "Bucket" },
            { key: "value", label: valueLabel, format: (v) => formatValue(v as number) },
          ]}
        />
      }
      overlay={
        <Tooltip x={hover?.x ?? 0} y={hover?.y ?? 0} visible={hover !== null}>
          {hover && (
            <>
              <div className="chart-tooltip-value">{formatValue(hover.value)}</div>
              <div className="chart-tooltip-label">{hover.label}</div>
            </>
          )}
        </Tooltip>
      }
    >
      {({ width, height: innerHeight }) => {
        const x = scaleBand<string>()
          .domain(data.map((d) => d.label))
          .range([0, width])
          .padding(0.35);
        const y = scaleLinear()
          .domain([0, max(data, (d) => d.value) ?? 0])
          .nice()
          .range([innerHeight, 0]);
        const barWidth = Math.min(x.bandwidth(), 56);
        const barOffset = (x.bandwidth() - barWidth) / 2;

        return (
          <>
            <AxisBottom scale={x} transform={`translate(0,${innerHeight})`} />
            {data.map((d) => {
              const barHeight = innerHeight - y(d.value);
              const bandX = x(d.label) ?? 0;
              const enter = () =>
                setHover({
                  label: d.label,
                  value: d.value,
                  x: margin.left + bandX + x.bandwidth() / 2,
                  y: margin.top + y(d.value) - 8,
                });
              const leave = () => setHover(null);
              const isHovered = hover?.label === d.label;
              const isPeak = highlight === d.label;
              const filters: string[] = [];
              if (isHovered) filters.push("brightness(1.2)");
              if (isPeak) filters.push("drop-shadow(0 8px 40px rgba(250, 69, 68, 0.22))");
              return (
                <g key={d.label} className="chart-mark" data-hovered={isHovered}>
                  <path
                    d={barPath(bandX + barOffset, y(d.value), barWidth, barHeight, 4)}
                    style={{
                      fill,
                      filter: filters.length ? filters.join(" ") : undefined,
                      stroke: isPeak ? "var(--color-border-strong)" : undefined,
                      strokeWidth: isPeak ? 1 : undefined,
                    }}
                  />
                  <text
                    x={bandX + x.bandwidth() / 2}
                    y={y(d.value) - 12}
                    textAnchor="middle"
                    className="chart-bar-value"
                  >
                    {formatValue(d.value)}
                  </text>
                  <rect
                    x={bandX}
                    y={0}
                    width={x.bandwidth()}
                    height={innerHeight}
                    fill="transparent"
                    tabIndex={0}
                    role="img"
                    aria-label={`${d.label}: ${formatValue(d.value)}`}
                    onPointerEnter={enter}
                    onPointerLeave={leave}
                    onFocus={enter}
                    onBlur={leave}
                  />
                </g>
              );
            })}
          </>
        );
      }}
    </ChartFrame>
  );
}
