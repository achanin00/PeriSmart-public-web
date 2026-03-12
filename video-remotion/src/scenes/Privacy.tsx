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
 * Scene 6 — "Privacy-First"
 *
 * Act A (0–3s):  Navy background with bold kinetic "Privacy-First"
 * Act B (3–end): Screenshot + animated pipeline flow + bold statement
 */
export const Privacy: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const actA_end = 3 * fps;

  const navyOpacity = interpolate(frame, [actA_end - 15, actA_end + 5], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Screenshot
  const shotSpring = spring({
    frame: frame - Math.round(2.5 * fps),
    fps,
    config: { damping: 18, stiffness: 55, mass: 0.8 },
  });

  // Pipeline stages
  const stages = [
    { icon: "🎥", label: "Camera", color: COLORS.accent },
    { icon: "🔒", label: "Edge Device", color: COLORS.green },
    { icon: "☁️", label: "Cloud Insights", color: COLORS.navy },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      {/* Main content */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          paddingTop: 24,
        }}
      >
        {/* Eyebrow */}
        <FadeSlide startFrame={Math.round(2.8 * fps)} direction="up" distance={24}>
          <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 8 }}>
            <div
              style={{
                background: COLORS.green,
                color: "#fff",
                padding: "8px 24px",
                borderRadius: 20,
                fontSize: 22,
                fontWeight: 700,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
              }}
            >
              Privacy-First
            </div>
            <span
              style={{
                fontSize: 28,
                color: COLORS.inkSoft,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
                fontWeight: 400,
              }}
            >
              Automatic In-line De-identification
            </span>
          </div>
        </FadeSlide>

        {/* Screenshot */}
        <div
          style={{
            opacity: interpolate(shotSpring, [0, 1], [0, 1]),
            transform: `scale(${interpolate(shotSpring, [0, 1], [0.85, 1])})`,
          }}
        >
          <div
            style={{
              background: "#fff",
              borderRadius: 28,
              boxShadow:
                "0 30px 90px rgba(15,23,42,0.14), 0 10px 30px rgba(15,23,42,0.08)",
              padding: 16,
              width: 1000,
            }}
          >
            <Img
              src={staticFile("illustrations/privacy-illustration.png")}
              style={{ width: "100%", borderRadius: 18 }}
            />
          </div>
        </div>

        {/* Pipeline flow */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
            marginTop: 20,
          }}
        >
          {stages.map((stage, i) => {
            const s = spring({
              frame: frame - Math.round((5.5 + i * 0.8) * fps),
              fps,
              config: { damping: 14, stiffness: 90, mass: 0.5 },
            });
            const opacity = interpolate(s, [0, 1], [0, 1]);
            const scale = interpolate(s, [0, 1], [0.7, 1]);

            return (
              <div
                key={i}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 16,
                  opacity,
                  transform: `scale(${scale})`,
                }}
              >
                <div
                  style={{
                    background: stage.color,
                    color: "#fff",
                    padding: "16px 36px",
                    borderRadius: 22,
                    fontSize: 26,
                    fontWeight: 700,
                    fontFamily: "'Plus Jakarta Sans', sans-serif",
                    display: "flex",
                    alignItems: "center",
                    gap: 12,
                  }}
                >
                  <span style={{ fontSize: 30 }}>{stage.icon}</span>
                  {stage.label}
                </div>
                {i < stages.length - 1 && (
                  <svg width="48" height="24" viewBox="0 0 48 24">
                    <path
                      d="M0 12 L38 12 M32 5 L42 12 L32 19"
                      stroke={stage.color}
                      strokeWidth="3.5"
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

        {/* Bold statement */}
        <FadeSlide startFrame={Math.round(8 * fps)} direction="up" distance={20}>
          <div
            style={{
              marginTop: 28,
              fontSize: 38,
              fontWeight: 800,
              color: COLORS.accent,
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              textAlign: "center",
            }}
          >
            Raw video is never retained.
          </div>
        </FadeSlide>
      </AbsoluteFill>

      {/* Navy color break */}
      <AbsoluteFill
        style={{
          backgroundColor: COLORS.navy,
          opacity: navyOpacity,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          gap: 30,
          zIndex: 5,
        }}
      >
        {/* Shield icon */}
        <div
          style={{
            width: 120,
            height: 120,
            borderRadius: "50%",
            background: `${COLORS.green}30`,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            fontSize: 60,
          }}
        >
          🛡️
        </div>
        <KineticText
          text="Privacy-First"
          startFrame={5}
          fontSize={130}
          color="#ffffff"
          fontWeight={800}
          wordDelay={6}
          centered
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
