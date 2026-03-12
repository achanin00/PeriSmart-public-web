import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { Problem } from "./scenes/Problem";
import { Intro } from "./scenes/Intro";
import { OrBoard } from "./scenes/OrBoard";
import { CaseDetail } from "./scenes/CaseDetail";
import { Analytics } from "./scenes/Analytics";
import { Privacy } from "./scenes/Privacy";
import { Cta } from "./scenes/Cta";

/**
 * Full PeriSmart explainer video.
 *
 * Scene durations (in seconds) are driven by voiceover length.
 * Update SCENE_DURATIONS after generating new audio.
 */
const SCENE_DURATIONS: number[] = [
  27,   // 1 – Problem
  14,   // 2 – Intro
  17,   // 3 – OR Board
  18,   // 4 – Case Detail
  20,   // 5 – Analytics
  20,   // 6 – Privacy
  12,   // 7 – CTA
];

const SCENES = [Problem, Intro, OrBoard, CaseDetail, Analytics, Privacy, Cta];

export const PeriSmartVideo: React.FC = () => {
  const { fps } = useVideoConfig();

  let cumulativeFrames = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      <Audio src={staticFile("video/voiceover.wav")} />
      {SCENES.map((SceneComponent, i) => {
        const durationFrames = Math.round(SCENE_DURATIONS[i] * fps);
        const from = cumulativeFrames;
        cumulativeFrames += durationFrames;
        return (
          <Sequence key={i} from={from} durationInFrames={durationFrames}>
            <SceneComponent />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
