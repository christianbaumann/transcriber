#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# ///
"""Turn whisper.json into transcript.md, or print the words of a time range.

transcript.py <whisper.json> [--slices <dir>] --out transcript.md
transcript.py <whisper.json> --excerpt HH:MM:SS-HH:MM:SS
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PARAGRAPH_PAUSE_SECONDS = 0.8
SLICE_NAME = re.compile(r"^(\d{4})_(\d{2})-(\d{2})-(\d{2})\.png$")
SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600


@dataclass(frozen=True)
class Word:
    start: float
    end: float
    text: str
    attached: bool = False


@dataclass(frozen=True)
class Slide:
    number: str
    time: float


def load_words(whisper_json: Path) -> list[Word]:
    data = json.loads(whisper_json.read_text())
    return [
        Word(w["start"], w["end"], w["word"].strip(), attached=not w["word"].startswith(" "))
        for segment in data["segments"]
        for w in segment.get("words", [])
        if w["word"].strip()
    ]


def join(parts: list[str | Word]) -> str:
    """Joins words with spaces; words whisper emitted without a leading space attach to the previous one."""
    text = ""
    for part in parts:
        if isinstance(part, Word) and part.attached and text:
            text += part.text
        else:
            text += (" " if text else "") + (part.text if isinstance(part, Word) else part)
    return text


def parse_time(text: str) -> int:
    hours, minutes, seconds = (int(part) for part in text.split(":"))
    return hours * SECONDS_PER_HOUR + minutes * SECONDS_PER_MINUTE + seconds


def format_time(seconds: float) -> str:
    total = int(seconds)
    return f"{total // SECONDS_PER_HOUR:02d}:{total % SECONDS_PER_HOUR // SECONDS_PER_MINUTE:02d}:{total % SECONDS_PER_MINUTE:02d}"


def load_slides(slices_dir: Path) -> list[Slide]:
    slides = []
    for path in sorted(slices_dir.glob("*.png")):
        match = SLICE_NAME.match(path.name)
        if match:
            number, hours, minutes, seconds = match.groups()
            slides.append(Slide(number, parse_time(f"{hours}:{minutes}:{seconds}")))
    return slides


def split_paragraphs(words: list[Word]) -> list[list[int]]:
    """Groups word indices into paragraphs, starting a new one after a long pause."""
    paragraphs: list[list[int]] = []
    for index, word in enumerate(words):
        if paragraphs and word.start - words[index - 1].end < PARAGRAPH_PAUSE_SECONDS:
            paragraphs[-1].append(index)
        else:
            paragraphs.append([index])
    return paragraphs


def place_markers(words: list[Word], slides: list[Slide]) -> dict[int, list[str]]:
    """Maps word index to the slide numbers whose timestamp is nearest to that word."""
    markers: dict[int, list[str]] = {}
    for slide in slides:
        nearest = min(range(len(words)), key=lambda i: abs(words[i].start - slide.time))
        markers.setdefault(nearest, []).append(slide.number)
    return markers


def render(words: list[Word], slides: list[Slide]) -> str:
    if not words:
        return ""
    markers = place_markers(words, slides)
    blocks = []
    for paragraph in split_paragraphs(words):
        parts = []
        for index in paragraph:
            parts += [f"→ slide {number}" for number in markers.get(index, [])]
            parts.append(words[index])
        blocks.append(f"[{format_time(words[paragraph[0]].start)}] {join(parts)}")
    return "\n\n".join(blocks) + "\n"


def excerpt(words: list[Word], start: int, end: int) -> str:
    return join([w for w in words if start <= w.start < end])


def parse_range(text: str) -> tuple[int, int]:
    start, end = text.split("-")
    return parse_time(start), parse_time(end)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("whisper_json", type=Path)
    parser.add_argument("--slices", type=Path, help="video-slicer output folder with NNNN_HH-MM-SS.png")
    parser.add_argument("--out", type=Path, help="transcript.md to write")
    parser.add_argument("--excerpt", help="HH:MM:SS-HH:MM:SS; print words starting in [start, end)")
    args = parser.parse_args()

    words = load_words(args.whisper_json)
    if args.excerpt:
        print(excerpt(words, *parse_range(args.excerpt)))
    elif args.out:
        slides = load_slides(args.slices) if args.slices else []
        args.out.write_text(render(words, slides))
    else:
        parser.error("give --out or --excerpt")


if __name__ == "__main__":
    sys.exit(main())
