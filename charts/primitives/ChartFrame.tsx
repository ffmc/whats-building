import { useEffect, useState, type ReactNode } from "react";
import { useDimensions } from "./useDimensions";

export type Margin = { top: number; right: number; bottom: number; left: number };

export const defaultMargin: Margin = { top: 8, right: 16, bottom: 32, left: 48 };

export type Inner = { width: number; height: number };

type Props = {
  label: string;
  /** Fixed pixel height. Omit to fill the available height of the parent (parent must have a definite height). */
  height?: number;
  margin?: Partial<Margin>;
  legend?: ReactNode;
  overlay?: ReactNode;
  table?: ReactNode;
  children: (inner: Inner) => ReactNode;
};

export function ChartFrame({
  label,
  height,
  margin,
  legend,
  overlay,
  table,
  children,
}: Props) {
  const { ref, dimensions } = useDimensions<HTMLDivElement>();
  const m = { ...defaultMargin, ...margin };
  const fill = height === undefined;
  const svgHeight = fill ? dimensions.height : height;
  const inner: Inner = {
    width: Math.max(0, dimensions.width - m.left - m.right),
    height: Math.max(0, svgHeight - m.top - m.bottom),
  };

  const [drawn, setDrawn] = useState(false);
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setDrawn(true);
      return;
    }
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setDrawn(true);
          observer.disconnect();
        }
      },
      { threshold: 0.4 },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [ref]);

  return (
    <figure className="chart-root" data-fill={fill} data-drawn={drawn}>
      {legend}
      <div ref={ref} className="chart-plot">
        {dimensions.width > 0 && svgHeight > 0 && (
          <svg width={dimensions.width} height={svgHeight} role="img" aria-label={label}>
            <g transform={`translate(${m.left},${m.top})`}>{children(inner)}</g>
          </svg>
        )}
        {overlay}
      </div>
      {table}
    </figure>
  );
}
