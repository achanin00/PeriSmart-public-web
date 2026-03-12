import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface KineticTextProps {
  text: string;
  startFrame: number;
  fontSize?: number;
  color?: string;
  fontWeight?: number;
  /** Delay in frames between each word */
  wordDelay?: number;
  centered?: boolean;
  maxWidth?: string;
}

export const KineticText: React.FC<KineticTextProps> = ({
  text,
  startFrame,
  fontSize = 80,
  color = "#1a1d21",
  fontWeight = 800,
  wordDelay = 3,
  centered = false,
  maxWidth = "100%",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        gap: `0 ${fontSize * 0.3}px`,
        justifyContent: centered ? "center" : "flex-start",
        maxWidth,
      }}
    >
      {words.map((word, i) => {
        const delay = startFrame + i * wordDelay;
        const s = spring({
          frame: frame - delay,
          fps,
          config: { damping: 18, stiffness: 120, mass: 0.5 },
        });
        const opacity = interpolate(s, [0, 1], [0, 1]);
        const y = interpolate(s, [0, 1], [40, 0]);

        return (
          <span
            key={i}
            style={{
              fontSize,
              fontWeight,
              color,
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              lineHeight: 1.1,
              opacity,
              transform: `translateY(${y}px)`,
              display: "inline-block",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};
