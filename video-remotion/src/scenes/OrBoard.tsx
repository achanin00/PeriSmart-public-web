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
 * Scene 3 — "OR Board"
 *
 * Act A (0–3s):  Blue color break with kinetic section title
 * Act B (3–end): Full-bleed screenshot with animated NOW marker + callout cards
 */
export const OrBoard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const actA_end = 3 * fps;

  // Blue overlay fades out
  const blueOpacity = interpolate(frame, [actA_end - 15, actA_end + 5], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Screenshot
  const boardSpring = spring({
    frame: frame - Math.round(2.5 * fps),
    fps,
    config: { damping: 18, stiffness: 55, mass: 0.8 },
  });
  const boardScale = interpolate(boardSpring, [0, 1], [0.85, 1]);
  const boardOpacity = interpolate(boardSpring, [0, 1], [0, 1]);

  // NOW indicator pulse
  const pulse = 1 + Math.sin(frame * 0.08) * 0.06;

  // Callout cards
  const callouts = [
    { title: "Live position", body: "Current timeline anchor", color: COLORS.accent },
    { title: "On Track", body: "Green rooms stay visible", color: COLORS.green },
    { title: "At Risk", body: "44m over projected plan", color: COLORS.coral },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: "#ffffff" }}>
      {/* === Act B: Full-bleed screenshot === */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          paddingTop: 40,
        }}
      >
        {/* Eyebrow + title row */}
        <FadeSlide startFrame={Math.round(2.8 * fps)} direction="up" distance={30}>
          <div style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 24 }}>
            <div
              style={{
                background: COLORS.accent,
                color: "#fff",
                padding: "8px 24px",
                borderRadius: 20,
                fontSize: 22,
                fontWeight: 700,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
              }}
            >
              OR Board
            </div>
            <span
              style={{
                fontSize: 28,
                color: COLORS.inkSoft,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
                fontWeight: 400,
              }}
            >
              One timeline for planned, actual, and predicted flow.
            </span>
          </div>
        </FadeSlide>

        {/* Screenshot */}
        <div
          style={{
            opacity: boardOpacity,
            transform: `scale(${boardScale})`,
            position: "relative",
          }}
        >
          {/* NOW badge */}
          <div
            style={{
              position: "absolute",
              top: -18,
              left: "52%",
              transform: `scale(${pulse})`,
              zIndex: 10,
              background: COLORS.navy,
              color: "#fff",
              padding: "8px 22px",
              borderRadius: 16,
              fontSize: 20,
              fontWeight: 700,
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              boxShadow: "0 4px 16px rgba(15,23,42,0.3)",
            }}
          >
            NOW
          </div>

          <div
            style={{
              background: "#fff",
              borderRadius: 28,
              boxShadow:
                "0 30px 90px rgba(15,23,42,0.14), 0 10px 30px rgba(15,23,42,0.08)",
              padding: 16,
              width: 1700,
            }}
          >
            <Img
              src={staticFile("illustrations/or-board-screenshot.png")}
              style={{ width: "100%", borderRadius: 18 }}
            />
          </div>
        </div>

        {/* Callout cards */}
        <div
          style={{
            display: "flex",
            gap: 28,
            marginTop: 36,
          }}
        >
          {callouts.map((c, i) => {
            const s = spring({
              frame: frame - Math.round((5 + i * 0.8) * fps),
              fps,
              config: { damping: 14, stiffness: 90, mass: 0.5 },
            });
            return (
              <div
                key={i}
                style={{
                  opacity: interpolate(s, [0, 1], [0, 1]),
                  transform: `translateY(${interpolate(s, [0, 1], [40, 0])}px)`,
                  background: "#fff",
                  border: `2px solid ${c.color}30`,
                  borderRadius: 20,
                  padding: "22px 32px",
                  width: 340,
                  boxShadow: "0 4px 16px rgba(0,0,0,0.04)",
                }}
              >
                <div
                  style={{
                    display: "inline-block",
                    background: c.color,
                    color: "#fff",
                    padding: "5px 16px",
                    borderRadius: 12,
                    fontSize: 20,
                    fontWeight: 700,
                    fontFamily: "'Plus Jakarta Sans', sans-serif",
                    marginBottom: 8,
                  }}
                >
                  {c.title}
                </div>
                <p
                  style={{
                    fontSize: 20,
                    color: COLORS.inkSoft,
                    fontFamily: "'Plus Jakarta Sans', sans-serif",
                    margin: 0,
                  }}
                >
                  {c.body}
                </p>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>

      {/* === Act A: Blue color break overlay === */}
      <AbsoluteFill
        style={{
          backgroundColor: COLORS.accent,
          opacity: blueOpacity,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 5,
        }}
      >
        <KineticText
          text="OR Board"
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
