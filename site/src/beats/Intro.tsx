import { BeatPanel } from "../components/BeatPanel";

export function Intro() {
  return (
    <BeatPanel id="intro">
      <div className="beat-intro">
        <p className="beat-eyebrow">What&rsquo;s building</p>
        <h1 id="intro-title" className="beat-intro-headline">
          AI ate GitHub.
        </h1>
        <p className="beat-intro-body">
          GitHub is where most of the world&rsquo;s open-source code lives — every
          project (a &ldquo;repo&rdquo;) that developers build and share publicly.
          We pulled 262,902 of them, every one created since 2021 and popular enough
          that real people noticed it, and had an AI read and categorize what each
          one actually does. In 2021, about one in seven of those newly-noticed
          projects was AI-related. Today, it&rsquo;s about one in two. This is that
          data, laid out so you can see exactly where that shift happened — and
          where it very much didn&rsquo;t. Scroll to start.
        </p>
      </div>
    </BeatPanel>
  );
}
