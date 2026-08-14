import { useState } from "react";
import { scaleLog, scaleLinear } from "d3-scale";
import { max as d3max } from "d3-array";
import { ChartFrame } from "./primitives/ChartFrame";
import { AxisBottom } from "./primitives/AxisBottom";
import { DataTable } from "./primitives/DataTable";
import { Tooltip } from "./primitives/Tooltip";

export type HistogramBin = { starsMin: number; starsMax: number; count: number };

type Props = {
  data: HistogramBin[];
  ariaLabel: string;
  caption: string;
  height?: number;
  /** CSS custom property, e.g. "var(--chart-seq-3)" */
  fill: string;
  peakLabel?: (d: HistogramBin) => string;
};

const formatStars = (v: number) =>
  v >= 1000 ? `${Math.round(v / 1000)}k` : String(Math.round(v));

/** Rounded top corners, square baseline — per dataviz mark spec. */
function barPath(x: number, y: number, width: number, height: number, radius: number): string {
  const r = Math.min(radius, width / 2, Math.max(height, 0));
  if (height <= 0) return "";
  return `M${x},${y + height} V${y + r} Q${x},${y} ${x + r},${y} H${x + width - r} Q${x + width},${y} ${x + width},${y + r} V${y + height} Z`;
}

export function Histogram({ data, ariaLabel, caption, height, fill, peakLabel }: Props) {
  const peak = data.reduce((best, d) => (d.count > best.count ? d : best), data[0]);
  const margin = { left: 16, bottom: 40, top: 48, right: 16 };
  const [hover, setHover] = useState<HistogramBin & { x: number; y: number } | null>(null);

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
            { key: "starsMin", label: "From (stars)", format: (v) => (v as number).toLocaleString() },
            { key: "starsMax", label: "To (stars)", format: (v) => (v as number).toLocaleString() },
            { key: "count", label: "Repos", format: (v) => (v as number).toLocaleString() },
          ]}
        />
      }
      overlay={
        <Tooltip x={hover?.x ?? 0} y={hover?.y ?? 0} visible={hover !== null}>
          {hover && (
            <>
              <div className="chart-tooltip-value">{hover.count.toLocaleString()} repos</div>
              <div className="chart-tooltip-label">
                {formatStars(hover.starsMin)}–{formatStars(hover.starsMax)}★
              </div>
            </>
          )}
        </Tooltip>
      }
    >
      {({ width, height: innerHeight }) => {
        const x = scaleLog()
          .domain([data[0].starsMin, data[data.length - 1].starsMax])
          .range([0, width]);
        const y = scaleLinear()
          .domain([0, d3max(data, (d) => d.count) ?? 0])
          .nice()
          .range([innerHeight, 0]);

        const [xMin, xMax] = x.domain();
        const tickValues = [50, 100, 1000, 10000, 100000].filter((v) => v >= xMin && v <= xMax);
        const gap = 2;

        return (
          <>
            <AxisBottom
              scale={x}
              transform={`translate(0,${innerHeight})`}
              tickValues={tickValues}
              format={(v) => `${formatStars(v as number)}★`}
            />
            {data.map((d) => {
              const left = x(d.starsMin);
              const right = x(d.starsMax);
              const barWidth = Math.max(1, right - left - gap);
              const barHeight = innerHeight - y(d.count);
              const isPeak = d === peak;
              const isHovered = hover?.starsMin === d.starsMin;
              const enter = () =>
                setHover({ ...d, x: margin.left + left + barWidth / 2, y: margin.top + y(d.count) - 8 });
              const leave = () => setHover(null);
              const filters: string[] = [];
              if (isHovered) filters.push("brightness(1.2)");
              if (isPeak) filters.push("drop-shadow(0 8px 40px rgba(250, 69, 68, 0.22))");
              return (
                <g key={d.starsMin} className="chart-mark" data-hovered={isHovered}>
                  <path
                    d={barPath(left, y(d.count), barWidth, barHeight, 2)}
                    style={{
                      fill,
                      opacity: isPeak ? 1 : 0.65,
                      filter: filters.length ? filters.join(" ") : undefined,
                      stroke: isPeak ? "var(--color-border-strong)" : undefined,
                      strokeWidth: isPeak ? 1 : undefined,
                    }}
                  />
                  <rect
                    x={left}
                    y={0}
                    width={right - left}
                    height={innerHeight}
                    fill="transparent"
                    tabIndex={0}
                    role="img"
                    aria-label={`${formatStars(d.starsMin)} to ${formatStars(d.starsMax)} stars: ${d.count.toLocaleString()} repos`}
                    onPointerEnter={enter}
                    onPointerLeave={leave}
                    onFocus={enter}
                    onBlur={leave}
                  />
                </g>
              );
            })}
            {peakLabel && (
              <text
                x={x(peak.starsMin)}
                y={y(peak.count) - 14}
                textAnchor={x(peak.starsMin) < width * 0.7 ? "start" : "end"}
                className="chart-bar-value"
              >
                {peakLabel(peak)}
              </text>
            )}
          </>
        );
      }}
    </ChartFrame>
  );
}
