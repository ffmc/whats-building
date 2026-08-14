export type LegendItem = { label: string; color: string };

type Props = {
  items: LegendItem[];
  active?: string | null;
  onToggle?: (label: string) => void;
};

export function Legend({ items, active, onToggle }: Props) {
  const interactive = Boolean(onToggle);

  return (
    <ul className="chart-legend">
      {items.map((item) => {
        const dimmed = active != null && active !== item.label;
        const swatch = <span className="chart-legend-swatch" style={{ background: item.color }} />;

        return (
          <li key={item.label} data-dimmed={dimmed}>
            {interactive ? (
              <button type="button" onClick={() => onToggle?.(item.label)} aria-pressed={!dimmed}>
                {swatch}
                {item.label}
              </button>
            ) : (
              <>
                {swatch}
                {item.label}
              </>
            )}
          </li>
        );
      })}
    </ul>
  );
}
