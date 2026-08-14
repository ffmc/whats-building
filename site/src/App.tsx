import { useEffect, useRef, useState } from "react";
import Lenis from "lenis";
import { StageRail } from "./components/StageRail";
import { ControlBar } from "./components/ControlBar";
import { Intro } from "./beats/Intro";
import { Beat0 } from "./beats/Beat0";
import { Beat05 } from "./beats/Beat05";
import { loadSummary, type Summary } from "./lib/summary";

const BEATS = [
  { id: "intro", label: "Intro" },
  { id: "beat-0", label: "The bar" },
  { id: "beat-0-5", label: "The boom" },
];

export function App() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [activeId, setActiveId] = useState(BEATS[0].id);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [selectedCategories, setSelectedCategories] = useState<Set<string>>(new Set());
  const railRef = useRef<HTMLDivElement>(null);
  const lenisRef = useRef<Lenis | null>(null);

  useEffect(() => {
    loadSummary().then(setSummary).catch(console.error);
  }, []);

  useEffect(() => {
    const el = railRef.current;
    if (!el) return;

    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const isMobile = window.matchMedia("(max-width: 768px), (pointer: coarse)").matches;
    if (reduceMotion || isMobile) {
      el.style.overflowX = "auto";
      const onScroll = () => {
        const max = el.scrollWidth - el.clientWidth;
        setScrollProgress(max > 0 ? el.scrollLeft / max : 0);
      };
      el.addEventListener("scroll", onScroll);
      return () => el.removeEventListener("scroll", onScroll);
    }

    const lenis = new Lenis({
      wrapper: el,
      content: el.firstElementChild as HTMLElement,
      orientation: "horizontal",
      gestureOrientation: "vertical",
      lerp: 0.085,
    });
    lenisRef.current = lenis;
    lenis.on("scroll", ({ progress }: { progress: number }) => setScrollProgress(progress));

    function raf(time: number) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    const frame = requestAnimationFrame(raf);

    return () => {
      cancelAnimationFrame(frame);
      lenis.destroy();
    };
  }, [summary]);

  useEffect(() => {
    const el = railRef.current;
    if (!el) return;
    const sections = Array.from(el.querySelectorAll<HTMLElement>(".beat-panel"));
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) setActiveId(visible.target.id);
      },
      { root: el, threshold: 0.6 },
    );
    sections.forEach((s) => observer.observe(s));
    return () => observer.disconnect();
  }, [summary]);

  function goTo(id: string) {
    const target = document.getElementById(id);
    if (!target) return;
    if (lenisRef.current) {
      lenisRef.current.scrollTo(target, { lerp: 0.085 });
    } else {
      target.scrollIntoView({ behavior: "smooth", inline: "start" });
    }
  }

  function toggleCategory(key: string) {
    setSelectedCategories((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  }

  if (!summary) {
    return <div className="app-loading">Loading&hellip;</div>;
  }

  const categories = Object.entries(summary.by_category)
    .filter(([, count]) => count > 1)
    .sort((a, b) => b[1] - a[1])
    .map(([key, count]) => ({ key, count }));

  const filteredCount =
    selectedCategories.size === 0
      ? summary.total_repos
      : categories.filter((c) => selectedCategories.has(c.key)).reduce((sum, c) => sum + c.count, 0);

  return (
    <>
      <StageRail beats={BEATS} activeId={activeId} scrollProgress={scrollProgress} onSelect={goTo} />
      <div className="rail" ref={railRef}>
        <div className="rail-content">
          <Intro />
          <Beat0 summary={summary} />
          <Beat05 summary={summary} />
        </div>
      </div>
      <ControlBar
        contextLabel={BEATS.find((b) => b.id === activeId)?.label ?? ""}
        count={filteredCount}
        categories={categories}
        selected={selectedCategories}
        onToggle={toggleCategory}
      />
    </>
  );
}
