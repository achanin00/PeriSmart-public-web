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
 * Scene 4 — "Case Detail"
 *
 * Act A (0–3s):  Green color break with kinetic title
 * Act B (3–end): Tight header + full screenshot + animated stat counters
 */
export const CaseDetail: React.FC = () => {
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
  const shotY = interpolate(shotSpring, [0, 1], [200, 0]);
  const shotOpacity = interpolate(shotSpring, [0, 1], [0, 1]);

  // Stats
  const stats = [
    { label: "Predicted End", value: "8:45 AM", color: COLORS.accent },
    { label: "Variance", value: "40 min ahead", color: COLORS.green },
    { label: "Milestones", value: "auto-detected", color: COLORS.coral },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      {/* Main content — tighter spacing */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          paddingTop: 24,
        }}
      >
        {/* Eyebrow — reduced bottom margin */}
        <FadeSlide startFrame={Math.round(2.8 * fps)} direction="up" distance={24}>
          <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 10 }}>
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
              Case Detail
            </div>
            <span
              style={{
                fontSize: 28,
                color: COLORS.inkSoft,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
                fontWeight: 400,
              }}
            >
              Milestones and finish-time predictions in one panel.
            </span>
          </div>
        </FadeSlide>

        {/* Full screenshot — immediately below header */}
        <div
          style={{
            opacity: shotOpacity,
            transform: `translateY(${shotY}px)`,
          }}
        >
          <div
            style={{
              background: "#fff",
              borderRadius: 28,
              boxShadow:
                "0 30px 90px rgba(15,23,42,0.14), 0 10px 30px rgba(15,23,42,0.08)",
              padding: 16,
              width: 1600,
            }}
          >
            <Img
              src={staticFile("illustrations/case-detail-illustration.svg")}
              style={{ width: "100%", borderRadius: 18 }}
            />
          </div>
        </div>

        {/* Stat cards — tighter margin */}
        <div style={{ display: "flex", gap: 30, marginTop: 24 }}>
          {stats.map((stat, i) => {
            const s = spring({
              frame: frame - Math.round((5.5 + i * 0.7) * fps),
              fps,
              config: { damping: 14, stiffness: 100, mass: 0.5 },
            });
            return (
              <div
                key={i}
                style={{
                  opacity: interpolate(s, [0, 1], [0, 1]),
                  transform: `translateY(${interpolate(s, [0, 1], [50, 0])}px)`,
                  background: "#fff",
                  border: `2px solid ${COLORS.line}`,
                  borderRadius: 22,
                  padding: "24px 40px",
                  minWidth: 280,
                  textAlign: "center",
                  boxShadow: "0 4px 16px rgba(0,0,0,0.04)",
                }}
              >
                <div
                  style={{
                    fontSize: 20,
                    color: COLORS.inkSoft,
                    fontFamily: "'Plus Jakarta Sans', sans-serif",
                    fontWeight: 400,
                    marginBottom: 8,
                  }}
                >
                  {stat.label}
                </div>
                <div
                  style={{
                    fontSize: 36,
                    color: stat.color,
                    fontFamily: "'Plus Jakarta Sans', sans-serif",
                    fontWeight: 800,
                  }}
                >
                  {stat.value}
                </div>
              </div>
            );
          })}
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
          text="Case Detail"
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
