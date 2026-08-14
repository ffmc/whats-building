import { useEffect, useState } from "react";

type Props = {
  value: number;
  unit?: string;
};

const prefersReducedMotion = () =>
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

export function HeroFigure({ value, unit }: Props) {
  const [display, setDisplay] = useState(prefersReducedMotion() ? value : 0);

  useEffect(() => {
    if (prefersReducedMotion()) return;
    const duration = 1100;
    const start = performance.now();
    const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);

    let frame: number;
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      setDisplay(Math.round(easeOut(t) * value));
      if (t < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [value]);

  return (
    <p className="hero-figure" aria-label={`${value.toLocaleString()}${unit ? ` ${unit}` : ""}`}>
      {display.toLocaleString()}
      {unit && <span className="hero-figure-unit">{unit}</span>}
    </p>
  );
}
