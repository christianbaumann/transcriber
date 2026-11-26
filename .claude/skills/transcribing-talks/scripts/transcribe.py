#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""Transcribe a video with mlx_whisper large-v3 and word timestamps.

Writes <out>/whisper.json and prints the detected language.
Uses the `mlx_whisper` on PATH, else `uvx --from mlx-whisper`.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

MODEL = "mlx-community/whisper-large-v3-mlx"
OUTPUT_NAME = "whisper"


def whisper_command() -> list[str]:
    if shutil.which("mlx_whisper"):
        return ["mlx_whisper"]
    return ["uvx", "--from", "mlx-whisper", "mlx_whisper"]


def build_command(video: Path, out: Path, language: str | None, initial_prompt: str | None) -> list[str]:
    cmd = whisper_command() + [
        str(video),
        "--model", MODEL,
        "--word-timestamps", "True",
        "--output-format", "json",
        "--output-name", OUTPUT_NAME,
        "--output-dir", str(out),
        "--condition-on-previous-text", "False",
        "--verbose", "False",
    ]
    if language:
        cmd += ["--language", language]
    if initial_prompt:
        cmd += ["--initial-prompt", initial_prompt]
    return cmd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--language", help="spoken language code, e.g. en or de; auto-detected if omitted")
    parser.add_argument("--initial-prompt", help="names and technical terms to bias recognition")
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    subprocess.run(build_command(args.video, args.out, args.language, args.initial_prompt), check=True)
    output = args.out / f"{OUTPUT_NAME}.json"
    if not output.exists():
        sys.exit(f"mlx_whisper produced no {output}; see its output above")
    result = json.loads(output.read_text())
    print(f"language: {result['language']}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        sys.exit(error.returncode)
