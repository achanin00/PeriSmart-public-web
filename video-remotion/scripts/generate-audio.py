#!/usr/bin/env python3
"""
Generate voiceover audio for all scenes using ElevenLabs TTS.
Uses Jessica Anne Bogart voice. Outputs individual scene WAVs + concatenated voiceover.

Usage:
  python scripts/generate-audio.py

Requires ELEVENLABS_API_KEY in ../.env
"""

import json
import os
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
PUBLIC_DIR = ROOT / "public" / "video"
AUDIO_DIR = ROOT / ".audio_tmp"

VOICE_ID = "lxYfHSkYm1EzQzGhdbfc"  # Jessica Anne Bogart
MODEL = "eleven_multilingual_v2"

SCENES = [
    {
        "slug": "01-problem",
        "text": (
            "Every day, perioperative teams manage millions of dollars in O.R. time "
            "\u2014 with phone calls, gut instinct, and schedules that go stale the moment "
            "the first case starts. A room runs long, turnovers drag, and the cascade "
            "hits every patient down the line. What if you could see and analyze "
            "what\u2019s happening \u2014 in real time \u2014 before the delays pile up "
            "and use that data to improve turnovers, better allocate block time, "
            "and optimize room utilization?"
        ),
    },
    {
        "slug": "02-intro",
        "text": (
            "PeriSmart gives your team a live picture of every operating room "
            "\u2014 what\u2019s running, what\u2019s next, and what\u2019s at risk "
            "\u2014 all without a single phone call. The actual case and turnover "
            "times are used to improve analysis and make better projections."
        ),
    },
    {
        "slug": "03-or-board",
        "text": (
            "The O.R. Board shows every room on a single timeline. Scheduled cases "
            "sit alongside real-time progress \u2014 so you can see at a glance which "
            "rooms are on track, which are running long, and exactly when the next "
            "turnover will begin. No more walking the halls or calling into rooms."
        ),
    },
    {
        "slug": "04-case-detail",
        "text": (
            "Click any case to see the full picture \u2014 nine milestones tracked "
            "automatically from Patient In to Patient Out. PeriSmart detects each "
            "event using computer vision, predicts when the case will finish, and "
            "shows you the variance from the original schedule. You know exactly "
            "where every case stands."
        ),
    },
    {
        "slug": "05-analytics",
        "text": (
            "Beyond the day-of board, PeriSmart gives your leadership team the "
            "analytics to drive lasting improvement. Turnover times broken down by "
            "phase \u2014 cleaning, idle, and setup \u2014 so you can pinpoint where "
            "minutes are lost. Room and block utilization trends, tracked daily, "
            "weekly, and monthly, with export to CSV for analysis."
        ),
    },
    {
        "slug": "06-privacy",
        "text": (
            "Privacy is core to our mission and is built in. PeriSmart processes "
            "all video on an edge device inside your hospital. Faces are always "
            "de-identified. Raw video is never retained. Monitor and TV screens "
            "are automatically obfuscated. It\u2019s designed for privacy and "
            "regulatory compliance from day one."
        ),
    },
    {
        "slug": "07-cta",
        "text": (
            "PeriSmart \u2014 real-time visibility, critical analysis, "
            "improved utilization, and privacy-first deployment. "
            "Make your operating rooms more efficient. Request a demo today."
        ),
    },
]


def load_env():
    env_file = PROJECT_ROOT / ".env"
    if not env_file.exists():
        raise RuntimeError(f".env not found at {env_file}")
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def tts(text: str, out_path: Path) -> None:
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY not set")

    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.60,
            "similarity_boost": 0.80,
            "style": 0.30,
            "use_speaker_boost": True,
        },
    }).encode()

    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        data=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
    )
    with urllib.request.urlopen(req) as resp:
        out_path.write_bytes(resp.read())


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def main():
    load_env()

    raw_dir = AUDIO_DIR / "raw"
    cooked_dir = AUDIO_DIR / "cooked"
    raw_dir.mkdir(parents=True, exist_ok=True)
    cooked_dir.mkdir(parents=True, exist_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    durations = []

    for i, scene in enumerate(SCENES, 1):
        raw_mp3 = raw_dir / f"{scene['slug']}.mp3"
        cooked_wav = cooked_dir / f"{scene['slug']}.wav"

        print(f"  TTS [{i}/{len(SCENES)}] {scene['slug']} ...")
        tts(scene["text"], raw_mp3)

        # Normalize loudness, stereo, 48kHz
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_mp3),
            "-af", (
                "highpass=f=55,"
                "loudnorm=I=-16:TP=-1.5:LRA=11,"
                "volume=1.05,"
                "atempo=1.08,"
                "pan=stereo|c0=c0|c1=c0,"
                "aresample=48000"
            ),
            "-ar", "48000",
            str(cooked_wav),
        ], check=True)

        dur = ffprobe_duration(cooked_wav)
        durations.append(dur)
        print(f"    → {dur:.2f}s")

    # Concatenate all scene audio
    concat_list = AUDIO_DIR / "concat.txt"
    with concat_list.open("w") as f:
        for scene in SCENES:
            slug = scene["slug"]
            wav_path = cooked_dir / f"{slug}.wav"
            f.write(f"file '{wav_path}'\n")

    voiceover_out = PUBLIC_DIR / "voiceover.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy", str(voiceover_out),
    ], check=True)

    total = sum(durations)
    print(f"\nDone! Total runtime: {total:.2f}s")
    print(f"Voiceover: {voiceover_out}")
    print(f"\nScene durations (update in PeriSmartVideo.tsx + Root.tsx):")
    print(f"  [{', '.join(f'{d:.0f}' for d in durations)}]")
    print(f"\nIndividual durations:")
    for scene, dur in zip(SCENES, durations):
        print(f"  {scene['slug']}: {dur:.1f}s")


if __name__ == "__main__":
    main()
