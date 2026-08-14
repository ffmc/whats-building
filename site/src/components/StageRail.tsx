type Beat = { id: string; label: string };

type Props = {
  beats: Beat[];
  activeId: string;
  scrollProgress: number;
  onSelect: (id: string) => void;
};

export function StageRail({ beats, activeId, scrollProgress, onSelect }: Props) {
  const activeIndex = Math.max(0, beats.findIndex((b) => b.id === activeId));
  const progress = scrollProgress * 100;

  return (
    <nav className="stage-rail" aria-label="Story progress">
      <div className="stage-rail-track">
        <div className="stage-rail-progress" style={{ width: `${progress}%` }} />
        <div className="stage-rail-playhead" style={{ left: `${progress}%` }} aria-hidden="true" />
      </div>
      <ol className="stage-rail-nodes">
        {beats.map((beat, i) => (
          <li key={beat.id}>
            <button
              type="button"
              className="stage-rail-node"
              data-active={beat.id === activeId}
              data-visited={i <= activeIndex}
              onClick={() => onSelect(beat.id)}
            >
              <span className="stage-rail-dot" aria-hidden="true" />
              <span className="stage-rail-label">{beat.label}</span>
            </button>
          </li>
        ))}
      </ol>
    </nav>
  );
}
