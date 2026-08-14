import type { ReactNode } from "react";

type Props = {
  id: string;
  children: ReactNode;
};

export function BeatPanel({ id, children }: Props) {
  return (
    <section id={id} className="beat-panel" aria-labelledby={`${id}-title`}>
      {children}
    </section>
  );
}
