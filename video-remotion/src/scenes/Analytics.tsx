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
 * Scene 5 — "Analytics"
 *
 * Act A (0–3s):  Navy color break with kinetic title
 * Act B (3–end): Turnover (left) with info cards below it.
 *                Block + Room utilization (right, large, stacked).
 */
export const Analytics: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const actA_end = 3 * fps;

  const navyOpacity = interpolate(frame, [actA_end - 15, actA_end + 5], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Info panels (go under turnover)
  const panels = [
    { title: "Turnover trend", body: "Daily vs target", color: COLORS.accent },
    { title: "Clean / Idle / Setup", body: "Phase breakdown", color: COLORS.green },
    { title: "CSV export", body: "Board reporting ready", color: COLORS.navy },
  ];

  // Turnover spring
  const turnoverSpring = spring({
    frame: frame - Math.round(3 * fps),
    fps,
    config: { damping: 18, stiffness: 55, mass: 0.8 },
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      {/* Main content */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          paddingTop: 28,
        }}
      >
        {/* Eyebrow row */}
        <FadeSlide startFrame={Math.round(2.8 * fps)} direction="up" distance={24}>
          <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 16 }}>
            <div
              style={{
                background: COLORS.navy,
                color: "#fff",
                padding: "8px 24px",
                borderRadius: 20,
                fontSize: 22,
                fontWeight: 700,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
              }}
            >
              Analytics
            </div>
            <span
              style={{
                fontSize: 28,
                color: COLORS.inkSoft,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
                fontWeight: 400,
              }}
            >
              Turnover, idle time, room use, and block use.
            </span>
          </div>
        </FadeSlide>

        {/* Two-column layout */}
        <div style={{ display: "flex", gap: 24, alignItems: "flex-start", width: 1520 }}>
          {/* Left column: Turnover + info cards below */}
          <div style={{ display: "flex", flexDirection: "column", width: 780 }}>
            {/* Turnover dashboard */}
            <div
              style={{
                opacity: interpolate(turnoverSpring, [0, 1], [0, 1]),
                transform: `translateY(${interpolate(turnoverSpring, [0, 1], [80, 0])}px)`,
              }}
            >
              <div
                style={{
                  background: "#fff",
                  borderRadius: 22,
                  boxShadow: "0 16px 50px rgba(15,23,42,0.12), 0 5px 18px rgba(15,23,42,0.06)",
                  padding: 12,
                }}
              >
                <Img
                  src={staticFile("illustrations/turnover-analytics-illustration.svg")}
                  style={{ width: "100%", borderRadius: 14 }}
                />
              </div>
              <div
                style={{
                  textAlign: "center",
                  marginTop: 10,
                  fontSize: 22,
                  fontWeight: 700,
                  color: COLORS.ink,
                  fontFamily: "'Plus Jakarta Sans', sans-serif",
                }}
              >
                Turnover Analysis
              </div>
            </div>

            {/* Info cards row — below turnover */}
            <div style={{ display: "flex", gap: 14, marginTop: 16 }}>
              {panels.map((p, i) => {
                const s = spring({
                  frame: frame - Math.round((6 + i * 0.5) * fps),
                  fps,
                  config: { damping: 14, stiffness: 90, mass: 0.5 },
                });
                return (
                  <div
                    key={i}
                    style={{
                      opacity: interpolate(s, [0, 1], [0, 1]),
                      transform: `translateY(${interpolate(s, [0, 1], [24, 0])}px)`,
                      background: "#fff",
                      border: `2px solid ${COLORS.line}`,
                      borderRadius: 18,
                      padding: "14px 18px",
                      flex: 1,
                      boxShadow: "0 4px 12px rgba(0,0,0,0.04)",
                    }}
                  >
                    <div
                      style={{
                        fontSize: 19,
                        fontWeight: 700,
                        color: COLORS.ink,
                        fontFamily: "'Plus Jakarta Sans', sans-serif",
                        marginBottom: 2,
                      }}
                    >
                      {p.title}
                    </div>
                    <div
                      style={{
                        fontSize: 16,
                        color: p.color,
                        fontFamily: "'Plus Jakarta Sans', sans-serif",
                        fontWeight: 600,
                      }}
                    >
                      {p.body}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right column: Block + Room utilization — large, stacked */}
          <div style={{ display: "flex", flexDirection: "column", gap: 12, width: 700 }}>
            {[
              "illustrations/block-utilization-illustration.svg",
              "illustrations/room-utilization-illustration.svg",
            ].map((src, i) => {
              const s = spring({
                frame: frame - Math.round((3.5 + i * 0.7) * fps),
                fps,
                config: { damping: 16, stiffness: 60, mass: 0.6 },
              });
              return (
                <div
                  key={i}
                  style={{
                    opacity: interpolate(s, [0, 1], [0, 1]),
                    transform: `translateX(${interpolate(s, [0, 1], [60, 0])}px)`,
                  }}
                >
                  <div
                    style={{
                      background: "#fff",
                      borderRadius: 22,
                      boxShadow: "0 16px 50px rgba(15,23,42,0.12), 0 5px 18px rgba(15,23,42,0.06)",
                      padding: 12,
                    }}
                  >
                    <Img
                      src={staticFile(src)}
                      style={{ width: "100%", borderRadius: 14 }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </AbsoluteFill>

      {/* Navy color break */}
      <AbsoluteFill
        style={{
          backgroundColor: COLORS.navy,
          opacity: navyOpacity,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 5,
        }}
      >
        <KineticText
          text="Analytics"
          startFrame={5}
          fontSize={140}
          color="#ffffff"
          fontWeight={800}
          wordDelay={5}
          centered
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
