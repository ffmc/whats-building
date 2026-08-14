export type CategoryFilter = { key: string; count: number };

type Props = {
  contextLabel: string;
  count: number;
  categories: CategoryFilter[];
  selected: Set<string>;
  onToggle: (key: string) => void;
};

function formatLabel(key: string) {
  return key.replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function ControlBar({ contextLabel, count, categories, selected, onToggle }: Props) {
  return (
    <div className="control-bar" data-variant="narrative">
      <span className="control-bar-context">{contextLabel}</span>
      <div className="control-bar-filters" role="group" aria-label="Filter by category">
        {categories.map((c) => (
          <button
            key={c.key}
            type="button"
            className="control-bar-chip"
            data-active={selected.has(c.key)}
            onClick={() => onToggle(c.key)}
          >
            {formatLabel(c.key)}
          </button>
        ))}
      </div>
      <span className="control-bar-count">{count.toLocaleString()} repos</span>
    </div>
  );
}
