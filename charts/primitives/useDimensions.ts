import { useLayoutEffect, useRef, useState } from "react";

export type Dimensions = { width: number; height: number };

export function useDimensions<T extends HTMLElement = HTMLDivElement>() {
  const ref = useRef<T>(null);
  const [dimensions, setDimensions] = useState<Dimensions>({ width: 0, height: 0 });

  useLayoutEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new ResizeObserver(([entry]) => {
      const { width, height } = entry.contentRect;
      setDimensions({ width, height });
    });

    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return { ref, dimensions };
}
