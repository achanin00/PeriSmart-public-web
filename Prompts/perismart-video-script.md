# PeriSmart Product Overview Video — Production Script

**Target length:** 105 seconds (~1:45)
**Format:** Animated explainer with professional voiceover
**Style reference:** Apella "Avoid Rooms Running Late" (use case-driven, customer-empathy open, product demo middle, outcome close)
**Resolution:** 1920×1080, 16:9
**Recommended AI tools:** Synthesia (talking-head + screen), HeyGen, or Pictory (script-to-video); ElevenLabs for voiceover

---

## Visual Asset Inventory

These existing assets should be used for the product-demo sections (scenes 3–6). Supply them as overlays or full-frame screenshots to the AI video tool.

| Asset | File | Use in Scene |
|:---|:---|:---|
| OR Board (live timeline) | `images/ui/OR-Board.png` | Scene 3 |
| Case Detail panel | `images/ui/CaseDetails.png` | Scene 4 |
| Case Schedule (calendar) | `images/ui/Case-Schedule.png` | Scene 3 alt |
| Turnover Analysis | `images/ui/Turnover-Analysis.png` | Scene 5 |
| Block Utilization chart | `images/ui/Block-Utilization.png` | Scene 5 alt |
| Room Utilization chart | `images/ui/Room-Utilization.png` | Scene 5 alt |
| Privacy / de-identification | `images/ui/Privacy.png` | Scene 6 |
| PeriSmart logo | `images/Logo/PeriSmart logo.png` | Scene 1, Scene 7 |
| Hero illustration (OR board) | `images/public-web/illustrations/hero-or-board-illustration.svg` | Scene 1 |
| Privacy illustration | `images/public-web/illustrations/privacy-illustration.png` | Scene 6 alt |

---

## Brand Guidelines

- **Primary accent:** #1e73ff (blue)
- **Secondary accent:** #1ba966 (green)
- **Text color:** #2e3033 (ink)
- **Font:** Plus Jakarta Sans (weights 400–800)
- **Corner radius:** 26px (large panels), 16px (cards)
- **Tone:** Confident, clear, empathetic — not salesy

---

## Scene-by-Scene Script

### SCENE 1 — The Problem (0:00–0:18)

**VISUAL:** Fade in on a busy hospital corridor illustration (abstract, no real faces). Transition to animated split-screen: one side shows a whiteboard with scribbled schedule, the other shows a charge nurse on the phone. Text overlays appear as the narrator speaks. End on PeriSmart logo mark.

**ON-SCREEN TEXT (staggered reveal):**
- "Where is the surgeon?"
- "Is OR-3 ready?"
- "How long until the room turns over?"

**VOICEOVER:**
> Every day, perioperative teams manage millions of dollars in OR time — with phone calls, gut instinct, and schedules that go stale the moment the first case starts. A room runs long, turnovers drag, and the cascade hits every patient down the line. What if you could actually see what's happening — in real time — before the delays pile up?

---

### SCENE 2 — Introduce PeriSmart (0:18–0:25)

**VISUAL:** PeriSmart logo animates in (centered, clean white or light gradient background). Tagline appears below. Brief animated transition of the logo mark morphing into the OR Board view.

**ON-SCREEN TEXT:**
- "PeriSmart"
- "Real-time perioperative intelligence"

**VOICEOVER:**
> PeriSmart gives your team a live picture of every operating room — what's running, what's next, and what's at risk — all without a single phone call.

---

### SCENE 3 — The OR Board (0:25–0:42)

**VISUAL:** Full-frame screenshot of `OR-Board.png`. Animated cursor highlights key elements: the timeline with multiple ORs, the NOW line, the color-coded status indicators (green ON TRACK, red AT RISK), predicted end times, turnover bubbles. Zoom into OR-1 row to show scheduled vs. actual time comparison.

**CALLOUT ANNOTATIONS (appear as narrator mentions them):**
- Arrow to NOW line → "Live position"
- Arrow to green badge → "On Track"
- Arrow to red badge → "At Risk — 44m over"
- Arrow to turnover bubble → "Predicted turnover: 25m"

**VOICEOVER:**
> The OR Board shows every room on a single timeline. Scheduled cases sit alongside real-time progress — so you can see at a glance which rooms are on track, which are running long, and exactly when the next turnover will begin. No more walking the halls or calling into rooms.

---

### SCENE 4 — Case Detail & Milestones (0:42–0:55)

**VISUAL:** Animate the Case Detail panel (`CaseDetails.png`) sliding in from the right, as if clicking on a case from the OR Board. Highlight the milestone list (Patient In, On Table, Anesthesia Start, Time Out, etc.), the predicted end time, and the AI confidence percentages.

**CALLOUT ANNOTATIONS:**
- Arrow to "Predicted End: 8:45 AM" → "AI-predicted completion"
- Arrow to "Variance: -40 min" → "40 min ahead of schedule"
- Arrow to milestone table → "9 milestones, detected automatically"

**VOICEOVER:**
> Click any case to see the full picture — nine milestones tracked automatically from Patient In to Patient Out. PeriSmart detects each event using edge-based cameras and audio, predicts when the case will finish, and shows you the variance from the original schedule. You know exactly where every case stands.

---

### SCENE 5 — Block & Room Utilization (0:55–1:13)

**VISUAL:** Full-frame transition to the Block Utilization chart (`Block-Utilization.png`). Animated highlight sweeps across the multi-line trend chart showing utilization by block owner over time. KPI cards animate in at the top: "Overall Block Util 65.5%", "1329.5 Block Hours", "871.2 Used Hours". Then cross-fade to the Room Utilization chart (`Room-Utilization.png`) showing per-room daily trends with target line.

**CALLOUT ANNOTATIONS:**
- Arrow to overall block util KPI → "65.5% — room to grow"
- Arrow to individual block lines → "Utilization by surgeon block"
- Arrow to target dashed line → "75% target"
- Arrow to room util chart → "Per-room daily trends"

**ON-SCREEN TEXT (animated stat reveal):**
- "Every 1% gain in OR utilization = **$100K+ annual value** per room"
- "Camera-observed data — not EHR estimates"

**VOICEOVER:**
> OR time is the most expensive resource in a hospital. Every percentage point of unused block time is revenue left on the table — and most hospitals are leaving a lot. PeriSmart tracks block utilization and room utilization with camera-observed accuracy, not EHR timestamps that miss the real picture. You see exactly which blocks are underused, which rooms sit idle, and where reallocation can unlock capacity — without adding a single OR. This is the data that drives seven-figure improvements.

---

### SCENE 6 — Turnover Analytics (1:13–1:23)

**VISUAL:** Transition to the Turnover Analysis dashboard (`Turnover-Analysis.png`). Show the distribution histogram, trend line, and phase performance cards (Clean / Idle / Setup). Highlight the "Phase Over-Target Analysis" table showing actual vs. target with over-target rates.

**CALLOUT ANNOTATIONS:**
- Arrow to histogram → "Turnover distribution"
- Arrow to phase cards → "Clean 19.2m · Idle 10.1m · Setup 24.6m"
- Arrow to over-target column → "73% of turnovers exceed target"

**VOICEOVER:**
> Turnovers are the other lever. PeriSmart breaks every turnover into three phases — cleaning, idle, and setup — so you can see exactly where minutes are lost and hold the right teams accountable. Daily trends against targets, with drill-down by room and service line.

---

### SCENE 7 — Privacy-First Architecture (1:23–1:33)

**VISUAL:** Show the de-identification screenshot (`Privacy.png`) — an OR camera view with faces blurred by bounding boxes. Then animate a simple diagram: Camera → Edge Device (on-prem) → De-identified data → Cloud. Emphasize that raw video never leaves the hospital.

**CALLOUT ANNOTATIONS:**
- Arrow to blurred faces → "Faces de-identified at the edge"
- Label on edge device → "On-premise processing"
- Strike-through on cloud arrow → "Raw video never leaves the building"

**VOICEOVER:**
> Privacy is built in from the start. PeriSmart processes all video and audio on an edge device inside your hospital. Faces are de-identified before anything is stored. Raw video never touches the cloud. Designed for HIPAA and state biometric privacy laws from day one.

---

### SCENE 8 — CTA & Close (1:33–1:45)

**VISUAL:** Return to clean background. PeriSmart logo centered. Tagline below. "Request a Demo" button animates in. Fade to end card with contact info and website.

**ON-SCREEN TEXT:**
- "PeriSmart"
- "See what's really happening in your ORs."
- **[Request a Demo]** (button style, primary blue #1e73ff)

**VOICEOVER:**
> PeriSmart — real-time visibility, predicted timelines, and the utilization data that drives real financial impact. See what's really happening in your ORs. Request a demo today.

---

## Competitive Differentiation vs. Apella Video

The Apella video (2:10) uses a **customer testimonial format** — a real director of ambulatory surgery at Houston Methodist narrates a use-case scenario (rooms running late). This is effective but requires a real customer.

PeriSmart's script takes a different approach for the current stage:

| Aspect | Apella Video | PeriSmart Script |
|:---|:---|:---|
| **Format** | Customer testimonial + product walkthrough | Professional voiceover + product walkthrough |
| **Length** | 2:10 | 1:45 (tight, web-optimized) |
| **Opening hook** | Personal story (nurse can't pick up daughter) | Universal pain point (phone calls, stale schedules) |
| **Product demo** | OR board with animated cursor clicks | OR board + Case Detail + **Block/Room Utilization** + Turnover Analytics (broader scope) |
| **Key differentiator shown** | Predictive room scheduling, live video | **Block & room utilization with camera-observed accuracy**, **privacy/de-id** (Apella doesn't address this), **milestone tracking with AI confidence**, **turnover phase analytics** |
| **Closing** | Emotional callback (no disappointed kids) | Professional CTA (request a demo) |
| **Missing from Apella** | No privacy discussion, no analytics detail | PeriSmart script covers both |

### What PeriSmart's script emphasizes that Apella's does not:
1. **Block & room utilization as a value driver** — Apella's video focuses solely on day-of room scheduling; PeriSmart quantifies the financial impact of utilization improvement ("every 1% = $100K+ per room") and shows camera-observed accuracy vs. EHR estimates
2. **Camera-observed ground truth** — Apella uses cameras for event detection but doesn't contrast their data accuracy against EHR timestamps; PeriSmart explicitly positions camera-derived utilization data as more trustworthy than EHR-reported times
3. **Edge-based privacy** — Apella shows raw OR video with identifiable faces; PeriSmart leads with de-identification
4. **Milestone granularity** — 9 detected events with AI confidence %; Apella shows timeline but not the event detail
5. **Turnover phase breakdown** — Clean/Idle/Setup decomposition with over-target analysis; Apella shows turnover duration but not the phases

---

## Production Notes

### For AI Video Tools (Synthesia / HeyGen / Pictory)

1. **Voiceover:** Use a professional, warm female or male voice. Recommended: ElevenLabs "Rachel" or "Josh" voice. Pace should be conversational, ~150 words/min.

2. **Screen recordings vs. screenshots:** For scenes 3–6, static screenshots with animated annotations (arrows, highlights, zoom) are more controllable than screen recordings. Most AI video tools support "zoom into region" and "highlight area" effects.

3. **Transitions:** Use simple cross-fades between scenes. Avoid flashy transitions — the PeriSmart brand is clean and professional.

4. **Music:** Subtle background track, corporate/tech style, 80-100 BPM. Fade under during voiceover, bring up slightly during transitions. Recommended: Artlist or Epidemic Sound, search "healthcare technology" or "corporate inspiring."

5. **Total word count:** ~420 words of voiceover ≈ approximately 105 seconds at conversational pace.

### Scene Timing Summary

| Scene | Time | Duration | Content |
|:---|:---|:---|:---|
| 1 — Problem | 0:00–0:18 | 18s | Pain point, questions, chaos |
| 2 — Intro | 0:18–0:25 | 7s | Logo, tagline |
| 3 — OR Board | 0:25–0:42 | 17s | Live timeline demo |
| 4 — Case Detail | 0:42–0:55 | 13s | Milestones, predictions |
| 5 — Utilization | 0:55–1:13 | 18s | Block & room utilization value driver |
| 6 — Turnover | 1:13–1:23 | 10s | Turnover phase analytics |
| 7 — Privacy | 1:23–1:33 | 10s | Edge processing, de-id |
| 8 — CTA | 1:33–1:45 | 12s | Logo, demo request |

---

## Full Voiceover Script (Copy-Paste Ready)

> Every day, perioperative teams manage millions of dollars in OR time — with phone calls, gut instinct, and schedules that go stale the moment the first case starts. A room runs long, turnovers drag, and the cascade hits every patient down the line. What if you could actually see what's happening — in real time — before the delays pile up?
>
> PeriSmart gives your team a live picture of every operating room — what's running, what's next, and what's at risk — all without a single phone call.
>
> The OR Board shows every room on a single timeline. Scheduled cases sit alongside real-time progress — so you can see at a glance which rooms are on track, which are running long, and exactly when the next turnover will begin. No more walking the halls or calling into rooms.
>
> Click any case to see the full picture — nine milestones tracked automatically from Patient In to Patient Out. PeriSmart detects each event using edge-based cameras and audio, predicts when the case will finish, and shows you the variance from the original schedule. You know exactly where every case stands.
>
> OR time is the most expensive resource in a hospital. Every percentage point of unused block time is revenue left on the table — and most hospitals are leaving a lot. PeriSmart tracks block utilization and room utilization with camera-observed accuracy, not EHR timestamps that miss the real picture. You see exactly which blocks are underused, which rooms sit idle, and where reallocation can unlock capacity — without adding a single OR. This is the data that drives seven-figure improvements.
>
> Turnovers are the other lever. PeriSmart breaks every turnover into three phases — cleaning, idle, and setup — so you can see exactly where minutes are lost and hold the right teams accountable. Daily trends against targets, with drill-down by room and service line.
>
> Privacy is built in from the start. PeriSmart processes all video and audio on an edge device inside your hospital. Faces are de-identified before anything is stored. Raw video never touches the cloud. Designed for HIPAA and state biometric privacy laws from day one.
>
> PeriSmart — real-time visibility, predicted timelines, and the utilization data that drives real financial impact. See what's really happening in your ORs. Request a demo today.
