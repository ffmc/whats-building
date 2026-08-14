import type { ReactNode } from "react";

type Props = {
  x: number;
  y: number;
  visible: boolean;
  children: ReactNode;
};

export function Tooltip({ x, y, visible, children }: Props) {
  return (
    <div
      className="chart-tooltip"
      data-visible={visible}
      style={{ transform: `translate(calc(${x}px - 50%), calc(${y}px - 100%))` }}
      role="status"
      aria-live="polite"
    >
      {children}
    </div>
  );
}
