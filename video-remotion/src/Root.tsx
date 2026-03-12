import { Composition } from "remotion";
import { Problem } from "./scenes/Problem";
import { Intro } from "./scenes/Intro";
import { OrBoard } from "./scenes/OrBoard";
import { CaseDetail } from "./scenes/CaseDetail";
import { Analytics } from "./scenes/Analytics";
import { Privacy } from "./scenes/Privacy";
import { Cta } from "./scenes/Cta";
import { PeriSmartVideo } from "./PeriSmartVideo";
import { WIDTH, HEIGHT, FPS } from "./constants";

/**
 * Scene durations in seconds — update after generating new audio.
 */
const SCENE_DURATIONS = [27, 14, 17, 18, 20, 20, 12];
const TOTAL_FRAMES = SCENE_DURATIONS.reduce((a, b) => a + b, 0) * FPS;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Full video */}
      <Composition
        id="PeriSmartVideo"
        component={PeriSmartVideo}
        durationInFrames={TOTAL_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />

      {/* Individual scene previews */}
      <Composition id="Scene1" component={Problem} durationInFrames={27 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="Scene2" component={Intro} durationInFrames={14 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="Scene3" component={OrBoard} durationInFrames={17 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="Scene4" component={CaseDetail} durationInFrames={18 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="Scene5" component={Analytics} durationInFrames={20 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="Scene6" component={Privacy} durationInFrames={20 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} />
      <Composition id="Scene7" component={Cta} durationInFrames={12 * FPS} fps={FPS} width={WIDTH} height={HEIGHT} />
    </>
  );
};
