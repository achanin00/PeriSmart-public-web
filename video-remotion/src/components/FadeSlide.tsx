import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import type { ReactNode } from "react";

interface FadeSlideProps {
  children: ReactNode;
  startFrame: number;
  direction?: "up" | "down" | "left" | "right";
  distance?: number;
  style?: React.CSSProperties;
}

export const FadeSlide: React.FC<FadeSlideProps> = ({
  children,
  startFrame,
  direction = "up",
  distance = 60,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const s = spring({
    frame: frame - startFrame,
    fps,
    config: { damping: 16, stiffness: 100, mass: 0.6 },
  });

  const opacity = interpolate(s, [0, 1], [0, 1]);

  const axis = direction === "up" || direction === "down" ? "Y" : "X";
  const sign =
    direction === "down" || direction === "right" ? -distance : distance;
  const offset = interpolate(s, [0, 1], [sign, 0]);

  return (
    <div
      style={{
        opacity,
        transform: `translate${axis}(${offset}px)`,
        ...style,
      }}
    >
      {children}
    </div>
  );
};
