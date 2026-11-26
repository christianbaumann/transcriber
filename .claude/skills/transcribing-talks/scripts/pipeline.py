#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Mechanical inputs for the orchestrator's subagent briefs.

pipeline.py slide-excerpts <whisper.json> <slices dir> --out <dir>
    writes <dir>/NNNN.txt: the transcript from a slide's appearance to the next slide's
pipeline.py chapter-excerpts <whisper.json> <outline.md> --out <dir>
    writes <dir>/NN.txt: the transcript of each chapter's time range in the outline
pipeline.py reference <notes dir> <article dir>
    copies the original slide image of every slide with a review item to <article dir>/reference/
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

import review
import transcript

OPEN_END = "end"
CHAPTER_HEADING = re.compile(r"^## (\d+)\. .*?\[(\d\d:\d\d:\d\d)-(\d\d:\d\d:\d\d|end)\]", re.M)
REFERENCE_DIR = "reference"


def slide_excerpts(whisper_json: Path, slices_dir: Path, out: Path) -> list[Path]:
    words = transcript.load_words(whisper_json)
    slides = transcript.load_slides(slices_dir)
    out.mkdir(parents=True, exist_ok=True)
    ends = [s.time for s in slides[1:]] + [float("inf")]
    written = []
    for slide, end in zip(slides, ends):
        path = out / f"{slide.number}.txt"
        path.write_text(transcript.excerpt(words, slide.time, end) + "\n", encoding="utf-8")
        written.append(path)
    return written


def chapter_excerpts(whisper_json: Path, outline: Path, out: Path) -> list[Path]:
    words = transcript.load_words(whisper_json)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for number, start, end in CHAPTER_HEADING.findall(outline.read_text(encoding="utf-8")):
        stop = float("inf") if end == OPEN_END else transcript.parse_time(end)
        path = out / f"{int(number):02d}.txt"
        path.write_text(transcript.excerpt(words, transcript.parse_time(start), stop) + "\n",
                        encoding="utf-8")
        written.append(path)
    return written


def copy_reference(notes_dir: Path, article_dir: Path) -> list[Path]:
    originals = {item["original"] for item in review.list_items(notes_dir, article_dir)
                 if item["original"]}
    target = article_dir / REFERENCE_DIR
    target.mkdir(parents=True, exist_ok=True)
    return [Path(shutil.copy2(src, target / src.name)) for src in sorted(originals)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("slide-excerpts", "chapter-excerpts"):
        p = sub.add_parser(name)
        p.add_argument("whisper_json", type=Path)
        p.add_argument("source", type=Path)
        p.add_argument("--out", type=Path, required=True)
    p = sub.add_parser("reference")
    p.add_argument("notes", type=Path)
    p.add_argument("article", type=Path)
    args = ap.parse_args()

    if args.command == "slide-excerpts":
        files = slide_excerpts(args.whisper_json, args.source, args.out)
    elif args.command == "chapter-excerpts":
        files = chapter_excerpts(args.whisper_json, args.source, args.out)
    else:
        files = copy_reference(args.notes, args.article)
    print(f"{len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
