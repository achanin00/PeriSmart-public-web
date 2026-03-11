# PeriSmart Homepage Explainer Video Generation Spec

**Level-3 Implementation Specification (L3)**  
**Version 1.0** | March 2026

---

## 1. Purpose

This document describes how the PeriSmart homepage explainer video is generated in this repository.

It covers:
- the source inputs used to generate the video
- the local rendering pipeline
- the scene and asset model
- the typography, color, and layout system used in the frames
- the narration generation process
- the audio post-processing and muxing pipeline
- the outputs written to the website

This is an implementation spec for the current generator, not only a creative brief.

---

## 2. Canonical Implementation

The canonical generator is:

- `scripts/render_homepage_video.py`

The generator creates:

- `assets/video/perismart-homepage-explainer.mp4`
- `assets/video/perismart-homepage-explainer-poster.jpg`

Temporary working files are written under:

- `.tmp_video_render/`

---

## 3. Primary Inputs

### 3.1 Narrative input

The narrative and scene intent come from:

- `spec/perismart-video-script.md`

That script defines the target story, sequence, visual intent, copy direction, and overall runtime target.

The implementation does not parse the markdown directly at runtime. Instead, the current scene copy is encoded into the Python `SCENES` list in `scripts/render_homepage_video.py`. When the script spec changes, the generator should be updated to keep the implementation aligned with the approved script.

### 3.2 Visual assets

The renderer uses local illustration and UI assets from `assets/`, including:

- product illustration assets
- privacy illustration assets
- analytics illustration assets
- schedule/context imagery
- the PeriSmart logo

The current implementation loads those assets in `load_assets()` and composes them into generated frames.

### 3.3 Typography input

The video uses the same font family as the website:

- Plus Jakarta Sans

The generator ensures local font availability by downloading the Plus Jakarta Sans variable font and instancing the weights needed for rendering.

Font files are stored in:

- `assets/fonts/PlusJakartaSans-wght.ttf`
- `assets/fonts/PlusJakartaSans-Regular.ttf`
- `assets/fonts/PlusJakartaSans-Bold.ttf`
- `assets/fonts/PlusJakartaSans-ExtraBold.ttf`

### 3.4 Website visual language

The video is styled to match the public website rather than a generic motion template. The generator uses:

- PeriSmart blue accents
- the same Plus Jakarta Sans family
- white and soft-gray card surfaces
- dark ink headline text
- rounded cards and restrained linework

This keeps the video visually continuous with the homepage.

---

## 4. Tooling and Runtime Dependencies

The current generator depends on local execution of:

- Python 3
- Pillow
- CairoSVG
- fontTools
- `ffmpeg`
- `ffprobe`
- `edge-tts`

The repository also uses:

- `.video_vendor/`

The standard invocation used in this repo is:

```bash
PYTHONPATH=.video_vendor python3 scripts/render_homepage_video.py
```

This command performs the full pipeline:

1. ensure fonts exist
2. synthesize narration
3. process the narration audio
4. concatenate all scene audio
5. render all video frames
6. mux video and audio into the final MP4
7. export a poster frame

---

## 5. Output Characteristics

Current render target:

- Resolution: `1280x720`
- Aspect ratio: `16:9`
- Frame rate: `24 fps`
- Video codec: `H.264`
- Pixel format: `yuv420p`
- Audio codec: `AAC`
- Audio sample rate: `48000 Hz`
- Audio channels: stereo

The current runtime is driven by the synthesized voiceover durations and is approximately:

- `118.8 seconds`

This is longer than the original 90-second creative target because the narration was intentionally slowed to improve intelligibility and reduce the overly synthetic feel.

---

## 6. Scene Model

The generator defines the explainer as a list of scenes in the `SCENES` array.

Each scene includes:

- `slug`: stable scene identifier
- `voiceover`: narration text for the scene
- `eyebrow`: small scene label or badge text
- `title`: primary on-screen headline
- `body`: supporting copy
- `renderer`: the function used to draw the scene

Current scene sequence:

1. `problem`
2. `intro`
3. `or-board`
4. `case-detail`
5. `analytics`
6. `privacy`
7. `cta`

Each scene’s video duration is derived from the duration of its processed narration audio rather than being hard-coded.

This means:

- copy edits can change scene length
- a slower or faster voice changes overall runtime
- the visual render adapts frame counts to the audio track

---

## 7. Frame Rendering Pipeline

### 7.1 Rendering strategy

The video is not assembled from prerecorded clips. It is rendered frame by frame in Python.

Each output frame is built by:

1. creating a fresh background canvas
2. drawing the scene composition
3. placing cards, badges, arcs, panels, and illustrations
4. rendering text with local fonts
5. applying animation timing for staggered reveals or motion
6. writing raw RGB frames into `ffmpeg`

The renderer then encodes those frames into a silent H.264 MP4.

### 7.2 Design space and scaling

The script renders from a fixed design system and outputs at:

- design space: `1920x1080`
- delivery output: `1280x720`

This allows the scene layout math to remain stable while the final output is scaled to the requested delivery resolution.

### 7.3 Motion model

Motion is implemented procedurally inside the renderer, using helper functions such as:

- easing functions
- reveal timing functions
- staggered appearance of labels and cards
- subtle transitions and position shifts

The animation style is intentionally restrained:

- no flashy transitions
- no aggressive zoom effects
- no cinematic photoreal shot generation

The result is closer to animated product storytelling than to a filmed commercial.

---

## 8. Layout and Typography Controls

### 8.1 Text fitting

The generator includes helper functions to avoid overflow:

- text wrapping
- line fitting by width
- font-size reduction when necessary
- clipping to a maximum line count in constrained areas

These helpers are used because several scenes contain compact cards and stat blocks that would otherwise overflow at 1280x720 output.

The current implementation specifically addresses:

- headline wrapping
- stat-card value fitting
- CTA layout spacing
- small process boxes in the privacy scene
- badge and chip labels

### 8.2 Colors

The frame palette is defined in code and follows the website’s visual direction. Key tokens include:

- background white
- soft gray panels
- dark ink text
- PeriSmart blue accent
- green success accent
- coral warning accent
- gold secondary highlight

These are defined in `scripts/render_homepage_video.py` so scene elements share a consistent palette.

### 8.3 Card and panel style

The generator uses:

- white card surfaces
- light borders
- large corner radii
- soft shadows
- restrained decorative arcs and blurred color fields

This styling is used across the OR board, case detail, analytics, privacy, and CTA scenes so the video feels like one system rather than a set of unrelated slides.

---

## 9. Audio Generation Pipeline

### 9.1 Source of narration

Narration is generated from the scene `voiceover` strings defined in the `SCENES` list.

Each scene’s voiceover is synthesized independently. This makes it easier to:

- regenerate only the audio assets
- inspect per-scene timing
- preserve deterministic scene ordering
- edit narration one section at a time

### 9.2 TTS engine

The current implementation uses:

- `edge-tts`

The selected voice is:

- `en-US-AvaMultilingualNeural`

The speaking rate is currently:

- `-5%`

This slower rate was chosen to reduce the fast, brittle quality heard in earlier renders.

### 9.3 Raw audio outputs

For each scene, `edge-tts` first produces a raw MP3 file under:

- `.tmp_video_render/audio/raw/`

These are intermediate assets only.

### 9.4 Audio post-processing

Each raw MP3 is processed through `ffmpeg` into a cleaned WAV file under:

- `.tmp_video_render/audio/cooked/`

The current filter chain is:

- `highpass=f=70`
- `lowpass=f=11000`
- `equalizer=f=160:t=q:w=1.2:g=2.0`
- `equalizer=f=2600:t=q:w=1.0:g=-1.6`
- `equalizer=f=5200:t=q:w=1.0:g=-1.4`
- `dynaudnorm=f=150:g=9`
- `volume=1.25`
- `pan=stereo|c0=c0|c1=c0`
- `aresample=48000`

The intent of this chain is:

- remove very low-frequency rumble
- limit overly sharp upper-end artifacts
- add some low-mid warmth
- reduce harshness in the intelligibility band
- soften the synthetic high-end edge
- stabilize loudness across scenes
- normalize delivery volume
- output a stereo track at `48 kHz`

### 9.5 Concatenation

After each scene is processed, the generator builds a concat list and joins the WAV files into one continuous voiceover file:

- `.tmp_video_render/perismart-homepage-explainer-voiceover.wav`

The concat step preserves the exact scene order defined in `SCENES`.

### 9.6 Final mux

Once the silent video has been rendered, the final voiceover WAV is muxed with the video using:

- copied H.264 video stream
- AAC audio at `256 kbps`
- `-shortest` to prevent excess trailing duration

The muxed output becomes:

- `assets/video/perismart-homepage-explainer.mp4`

---

## 10. Video Rendering and Muxing Details

### 10.1 Silent video render

The video frames are streamed into `ffmpeg` as:

- raw RGB frames
- frame size `1280x720`
- frame rate `24`

The current encoder settings are:

- `libx264`
- `-crf 18`
- `-preset medium`
- `-pix_fmt yuv420p`

This produces:

- `.tmp_video_render/perismart-homepage-explainer-silent.mp4`

### 10.2 Final assembly

The final assembly step takes:

- the silent H.264 render
- the concatenated WAV voiceover

and writes the website-facing deliverable:

- `assets/video/perismart-homepage-explainer.mp4`

### 10.3 Poster extraction

After muxing, the script extracts a still image from the finished MP4 at:

- `00:00:18`

That still becomes:

- `assets/video/perismart-homepage-explainer-poster.jpg`

---

## 11. Temporary Files and Working Directories

The generator uses `.tmp_video_render/` as a workspace.

Important temporary outputs include:

- raw per-scene MP3 files
- processed per-scene WAV files
- concat manifest
- concatenated narration WAV
- silent MP4 before audio mux

These files are useful for debugging:

- scene-level timing issues
- synthetic voice quality issues
- incorrect scene ordering
- audio clipping or loudness problems
- mismatches between narration duration and visual composition

---

## 12. Regeneration Procedure

To regenerate the current video:

```bash
PYTHONPATH=.video_vendor python3 scripts/render_homepage_video.py
```

Recommended verification after regeneration:

```bash
ffprobe -hide_banner assets/video/perismart-homepage-explainer.mp4
```

Optional contact-sheet check:

```bash
ffmpeg -y -i assets/video/perismart-homepage-explainer.mp4 -vf "fps=1/15,scale=320:-1,tile=4x2" -frames:v 1 /tmp/perismart-final-contact.jpg
```

Recommended manual review:

1. play the exported MP4 end to end
2. inspect text-heavy scenes for overflow or collisions
3. confirm badge copy and CTA URL text
4. confirm the narration pace is intelligible
5. verify that poster extraction still lands on an acceptable frame

---

## 13. Known Tradeoffs

### 13.1 Audio realism

The narration is still TTS-based. The current EQ and pacing changes improve the result, but it is not the same as professionally recorded human voice talent.

### 13.2 Runtime expansion

Because durations are tied to the synthesized narration, improving intelligibility by slowing the voice tends to increase total runtime.

### 13.3 Manual script sync

The markdown script file and the Python `SCENES` list are separate sources. They must be kept in sync manually.

### 13.4 Performance

The frame compositor renders locally and can be slow, especially because every frame is drawn procedurally before encoding.

---

## 14. Change Management Guidance

If the script changes, update the following in order:

1. `spec/perismart-video-script.md`
2. the `SCENES` list in `scripts/render_homepage_video.py`
3. any scene-specific layout or copy constraints in the renderer
4. regenerate the final MP4 and poster
5. verify the output visually and with `ffprobe`

If branding changes, review:

- font files
- color tokens
- logo assets
- CTA copy
- URL text

If narration quality needs further improvement, likely adjustment points are:

- selected TTS voice
- speech rate
- EQ bands
- normalization settings
- final AAC bitrate

---

## 15. Summary

The current PeriSmart homepage explainer video is generated entirely from local repository assets and a Python rendering pipeline.

Video generation is handled by:

- procedural scene rendering in `scripts/render_homepage_video.py`
- `ffmpeg` encoding and muxing

Audio generation is handled by:

- per-scene TTS synthesis with `edge-tts`
- `ffmpeg` cleanup and mastering
- WAV concatenation and AAC muxing

The resulting MP4 and poster are committed website assets, not placeholders.
