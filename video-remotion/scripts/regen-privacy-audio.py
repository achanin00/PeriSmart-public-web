#!/usr/bin/env python3
"""Regenerate only the privacy scene (06) audio and re-concatenate."""

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

PRIVACY_TEXT = (
    "Privacy is core to our mission and is built in. PeriSmart processes "
    "all video on an edge device inside your hospital. Faces are always "
    "de-identified. Raw video is never retained. Monitor and TV screens "
    "are automatically obfuscated. It\u2019s designed for privacy and "
    "regulatory compliance from day one."
)

SCENE_SLUGS = [
    "01-problem", "02-intro", "03-or-board", "04-case-detail",
    "05-analytics", "06-privacy", "07-cta",
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

    raw_mp3 = raw_dir / "06-privacy.mp3"
    cooked_wav = cooked_dir / "06-privacy.wav"

    print("  TTS [6/7] 06-privacy ...")
    tts(PRIVACY_TEXT, raw_mp3)

    # Normalize loudness, stereo, 48kHz (same settings as main script)
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
    print(f"    → {dur:.2f}s")

    # Re-concatenate all scene audio
    concat_list = AUDIO_DIR / "concat.txt"
    with concat_list.open("w") as f:
        for slug in SCENE_SLUGS:
            wav_path = cooked_dir / f"{slug}.wav"
            if not wav_path.exists():
                raise RuntimeError(f"Missing cooked WAV: {wav_path}")
            f.write(f"file '{wav_path}'\n")

    voiceover_out = PUBLIC_DIR / "voiceover.wav"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy", str(voiceover_out),
    ], check=True)

    # Print all durations for reference
    print("\nAll scene durations:")
    for slug in SCENE_SLUGS:
        wav_path = cooked_dir / f"{slug}.wav"
        d = ffprobe_duration(wav_path)
        print(f"  {slug}: {d:.1f}s")

    total = sum(ffprobe_duration(cooked_dir / f"{s}.wav") for s in SCENE_SLUGS)
    print(f"\nTotal runtime: {total:.2f}s")
    print(f"Voiceover: {voiceover_out}")


if __name__ == "__main__":
    main()
