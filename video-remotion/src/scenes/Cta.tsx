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
 * Scene 7 — "CTA"
 *
 * Logo + kinetic headline + value props + URL
 * Clean, centered, professional close.
 */
export const Cta: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo
  const logoSpring = spring({
    frame: frame - 5,
    fps,
    config: { damping: 12, stiffness: 80, mass: 0.6 },
  });
  const logoScale = interpolate(logoSpring, [0, 1], [0.4, 1]);

  // Value pills
  const values = [
    "Real-time visibility",
    "Critical analysis",
    "Improved utilization",
  ];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLORS.navy,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Decorative glow */}
      <div
        style={{
          position: "absolute",
          width: 700,
          height: 700,
          borderRadius: "50%",
          background: `${COLORS.accent}15`,
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          filter: "blur(80px)",
        }}
      />

      {/* Logo */}
      <div
        style={{
          opacity: interpolate(logoSpring, [0, 1], [0, 1]),
          transform: `scale(${logoScale})`,
          marginBottom: 40,
        }}
      >
        <Img
          src={staticFile("logo/perismart-logo.png")}
          style={{ height: 110 }}
        />
      </div>

      {/* Headline */}
      <div style={{ marginBottom: 20 }}>
        <KineticText
          text="See what's really happening in your ORs."
          startFrame={Math.round(1.2 * fps)}
          fontSize={78}
          color="#ffffff"
          fontWeight={800}
          wordDelay={3}
          centered
          maxWidth="1300px"
        />
      </div>

      {/* Value props */}
      <div
        style={{
          display: "flex",
          gap: 20,
          marginTop: 40,
          marginBottom: 50,
        }}
      >
        {values.map((v, i) => {
          const s = spring({
            frame: frame - Math.round((3.5 + i * 0.5) * fps),
            fps,
            config: { damping: 14, stiffness: 100, mass: 0.5 },
          });
          return (
            <div
              key={i}
              style={{
                opacity: interpolate(s, [0, 1], [0, 1]),
                transform: `translateY(${interpolate(s, [0, 1], [30, 0])}px)`,
                background: i === 0 ? COLORS.accent : i === 1 ? COLORS.green : `${COLORS.accent}20`,
                color: "#ffffff",
                padding: "14px 32px",
                borderRadius: 28,
                fontSize: 24,
                fontWeight: 700,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
              }}
            >
              {v}
            </div>
          );
        })}
      </div>

      {/* URL */}
      <FadeSlide startFrame={Math.round(5 * fps)} direction="up" distance={20}>
        <div
          style={{
            fontSize: 32,
            fontWeight: 700,
            color: COLORS.accent,
            fontFamily: "'Plus Jakarta Sans', sans-serif",
          }}
        >
          peri-smart.com
        </div>
      </FadeSlide>
    </AbsoluteFill>
  );
};
