import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { COLORS } from "../constants";
import { KineticText } from "../components/KineticText";
import { FadeSlide } from "../components/FadeSlide";

/**
 * Scene 2 — "PeriSmart Intro"
 *
 * No logo. Headline at top, full-screen board below, data-flow strip at bottom.
 */
export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Board screenshot
  const boardDelay = 2.5 * fps;
  const boardSpring = spring({
    frame: frame - boardDelay,
    fps,
    config: { damping: 18, stiffness: 50, mass: 0.8 },
  });
  const boardY = interpolate(boardSpring, [0, 1], [300, 0]);
  const boardOpacity = interpolate(boardSpring, [0, 1], [0, 1]);

  // Flow strip
  const flowDelay = 8 * fps;
  const steps = [
    { label: "Actual Times", color: COLORS.accent },
    { label: "Better Analysis", color: COLORS.green },
    { label: "Improved Utilization", color: COLORS.navy },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      {/* Subtle gradient top */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 300,
          background: `linear-gradient(180deg, ${COLORS.accent}08 0%, transparent 100%)`,
        }}
      />

      {/* Headline — at the top */}
      <div
        style={{
          position: "absolute",
          top: 40,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <KineticText
          text="Real-time perioperative intelligence."
          startFrame={Math.round(0.5 * fps)}
          fontSize={72}
          color={COLORS.ink}
          fontWeight={800}
          wordDelay={4}
          centered
          maxWidth="1200px"
        />
        <FadeSlide startFrame={Math.round(2 * fps)} direction="up" distance={24}>
          <p
            style={{
              fontSize: 30,
              color: COLORS.inkSoft,
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              fontWeight: 400,
              marginTop: 16,
              textAlign: "center",
            }}
          >
            What's running. What's next. What's at risk.
          </p>
        </FadeSlide>
      </div>

      {/* Full-width board screenshot — positioned to fit */}
      <div
        style={{
          position: "absolute",
          top: 280,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          opacity: boardOpacity,
          transform: `translateY(${boardY}px)`,
        }}
      >
        <div
          style={{
            background: "#fff",
            borderRadius: 24,
            boxShadow:
              "0 25px 80px rgba(15,23,42,0.12), 0 8px 24px rgba(15,23,42,0.08)",
            padding: 14,
            width: 1600,
          }}
        >
          <Img
            src={staticFile("illustrations/hero-or-board-illustration.svg")}
            style={{ width: "100%", borderRadius: 16 }}
          />
        </div>
      </div>

      {/* Data-flow strip */}
      <div
        style={{
          position: "absolute",
          bottom: 40,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 12,
        }}
      >
        {steps.map((step, i) => {
          const s = spring({
            frame: frame - (flowDelay + i * 8),
            fps,
            config: { damping: 14, stiffness: 100, mass: 0.5 },
          });
          const opacity = interpolate(s, [0, 1], [0, 1]);
          const y = interpolate(s, [0, 1], [30, 0]);

          return (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 12,
                opacity,
                transform: `translateY(${y}px)`,
              }}
            >
              <div
                style={{
                  background: step.color,
                  color: "#fff",
                  padding: "14px 36px",
                  borderRadius: 30,
                  fontSize: 26,
                  fontWeight: 700,
                  fontFamily: "'Plus Jakarta Sans', sans-serif",
                }}
              >
                {step.label}
              </div>
              {i < steps.length - 1 && (
                <svg width="36" height="20" viewBox="0 0 36 20">
                  <path
                    d="M0 10 L28 10 M22 4 L30 10 L22 16"
                    stroke={step.color}
                    strokeWidth="3"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              )}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
