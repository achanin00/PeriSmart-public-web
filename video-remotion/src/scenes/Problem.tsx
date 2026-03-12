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
 * Scene 1 — "The Problem"
 *
 * Three acts:
 *   A (0–4s):   Navy background, large kinetic headline
 *   B (4–10s):  Transition to white, OR board screenshot fills ~85% of frame
 *   C (10–18s): Three outcome cards slide up from bottom, screenshot shrinks slightly
 */
export const Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // --- Act timing (frames) ---
  const actA_end = 4 * fps; // 120
  const actB_start = 3.5 * fps; // overlap for crossfade
  const actB_end = 10 * fps;
  const actC_start = 9 * fps;

  // --- Act A: Navy background with kinetic headline ---
  const navyOpacity = interpolate(frame, [actA_end - 20, actA_end + 10], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Pulsing circle decoration
  const pulseScale = 1 + Math.sin(frame * 0.05) * 0.08;

  // --- Act B: Screenshot entrance ---
  const screenshotSpring = spring({
    frame: frame - actB_start,
    fps,
    config: { damping: 20, stiffness: 60, mass: 0.8 },
  });
  const screenshotY = interpolate(screenshotSpring, [0, 1], [300, 0]);
  const screenshotOpacity = interpolate(screenshotSpring, [0, 1], [0, 1]);

  // Screenshot scale: starts large, shrinks slightly when cards appear
  const shrinkSpring = spring({
    frame: frame - actC_start,
    fps,
    config: { damping: 22, stiffness: 80, mass: 0.6 },
  });
  const screenshotScale = interpolate(shrinkSpring, [0, 1], [1, 0.78]);
  const screenshotTranslateY = interpolate(shrinkSpring, [0, 1], [0, -80]);

  // --- Act C: Outcome cards ---
  const cards = [
    {
      title: "Reduce Turnovers",
      body: "Actual phase data cuts avg turnover time.",
      color: COLORS.accent,
      bg: "#eef4ff",
    },
    {
      title: "Allocate Block Time",
      body: "Real utilization drives smarter scheduling.",
      color: COLORS.green,
      bg: "#edfcf4",
    },
    {
      title: "Optimize Utilization",
      body: "Room efficiency improves with real-time tracking.",
      color: COLORS.coral,
      bg: "#fef3f0",
    },
  ];

  // Eyebrow label
  const eyebrowSpring = spring({
    frame: frame - 5,
    fps,
    config: { damping: 14, stiffness: 100, mass: 0.4 },
  });

  // White bg
  const whiteBgOpacity = interpolate(
    frame,
    [actB_start, actB_start + 20],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: COLORS.navy }}>
      {/* White background layer that fades in for Act B */}
      <AbsoluteFill
        style={{
          backgroundColor: "#ffffff",
          opacity: whiteBgOpacity,
        }}
      />

      {/* === ACT A: Navy kinetic headline === */}
      <AbsoluteFill
        style={{
          opacity: navyOpacity,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 2,
        }}
      >
        {/* Decorative circles */}
        <div
          style={{
            position: "absolute",
            width: 500,
            height: 500,
            borderRadius: "50%",
            border: `3px solid ${COLORS.accent}40`,
            top: -100,
            right: -80,
            transform: `scale(${pulseScale})`,
          }}
        />
        <div
          style={{
            position: "absolute",
            width: 300,
            height: 300,
            borderRadius: "50%",
            background: `${COLORS.accent}18`,
            bottom: -60,
            left: -40,
            transform: `scale(${pulseScale * 1.1})`,
          }}
        />

        {/* Eyebrow pill */}
        <div
          style={{
            opacity: eyebrowSpring,
            transform: `translateY(${interpolate(eyebrowSpring, [0, 1], [20, 0])}px)`,
            marginBottom: 40,
          }}
        >
          <div
            style={{
              background: COLORS.accent,
              color: "#fff",
              padding: "12px 32px",
              borderRadius: 30,
              fontSize: 28,
              fontWeight: 700,
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              letterSpacing: 1,
            }}
          >
            The Problem
          </div>
        </div>

        {/* Main kinetic headline */}
        <div style={{ padding: "0 140px", textAlign: "center" }}>
          <KineticText
            text="The schedule gets stale the moment the first case moves."
            startFrame={15}
            fontSize={88}
            color="#ffffff"
            fontWeight={800}
            wordDelay={3}
            centered
            maxWidth="1400px"
          />
        </div>

        {/* Subtext */}
        <FadeSlide startFrame={50} direction="up" distance={30}>
          <p
            style={{
              fontSize: 32,
              color: `${COLORS.accent}cc`,
              fontFamily: "'Plus Jakarta Sans', sans-serif",
              fontWeight: 400,
              marginTop: 36,
              textAlign: "center",
              maxWidth: 900,
            }}
          >
            Phone calls and status chasing create delay before the board even
            shows it.
          </p>
        </FadeSlide>
      </AbsoluteFill>

      {/* === ACT B: Large OR Board screenshot === */}
      <AbsoluteFill
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 1,
        }}
      >
        <div
          style={{
            opacity: screenshotOpacity,
            transform: `translateY(${screenshotY + screenshotTranslateY}px) scale(${screenshotScale})`,
          }}
        >
          {/* "Accurate OR time" floating badge */}
          <FadeSlide startFrame={actB_start + 25} direction="right" distance={40}>
            <div
              style={{
                position: "absolute",
                top: -24,
                right: 40,
                background: COLORS.accent,
                color: "#fff",
                padding: "10px 28px",
                borderRadius: 24,
                fontSize: 24,
                fontWeight: 700,
                fontFamily: "'Plus Jakarta Sans', sans-serif",
                boxShadow: "0 8px 30px rgba(30,107,235,0.3)",
                zIndex: 10,
              }}
            >
              Accurate OR time
            </div>
          </FadeSlide>

          {/* Screenshot card */}
          <div
            style={{
              background: "#fff",
              borderRadius: 28,
              boxShadow:
                "0 25px 80px rgba(15,23,42,0.12), 0 8px 24px rgba(15,23,42,0.08)",
              padding: 16,
              width: 1600,
            }}
          >
            <Img
              src={staticFile("illustrations/hero-or-board-illustration.svg")}
              style={{
                width: "100%",
                borderRadius: 18,
              }}
            />
          </div>
        </div>
      </AbsoluteFill>

      {/* === ACT C: Three outcome cards === */}
      <div
        style={{
          position: "absolute",
          bottom: 50,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          gap: 30,
          zIndex: 3,
        }}
      >
        {cards.map((card, i) => {
          const cardSpring = spring({
            frame: frame - (actC_start + i * 6),
            fps,
            config: { damping: 14, stiffness: 90, mass: 0.5 },
          });
          const cardY = interpolate(cardSpring, [0, 1], [120, 0]);
          const cardOpacity = interpolate(cardSpring, [0, 1], [0, 1]);

          return (
            <div
              key={i}
              style={{
                opacity: cardOpacity,
                transform: `translateY(${cardY}px)`,
                background: card.bg,
                border: `2px solid ${card.color}30`,
                borderRadius: 22,
                padding: "28px 36px",
                width: 460,
              }}
            >
              <div
                style={{
                  display: "inline-block",
                  background: card.color,
                  color: "#fff",
                  padding: "6px 18px",
                  borderRadius: 14,
                  fontSize: 22,
                  fontWeight: 700,
                  fontFamily: "'Plus Jakarta Sans', sans-serif",
                  marginBottom: 12,
                }}
              >
                {card.title}
              </div>
              <p
                style={{
                  fontSize: 22,
                  color: COLORS.inkSoft,
                  fontFamily: "'Plus Jakarta Sans', sans-serif",
                  fontWeight: 400,
                  margin: 0,
                  lineHeight: 1.4,
                }}
              >
                {card.body}
              </p>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
