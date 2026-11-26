#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pillow", "scipy"]
# ///
"""Grade one run of transcribing-talks against a reference talk.

grade.py <article dir> <ground truth dir> [--slices DIR] [--out grading.json]

<article dir>: the run's `<video>-article/`. <ground truth dir>: `testdata/talks/<name>/`
(`slides/NN.png`, `slides.md`). --slices defaults to the article dir with `-article`
replaced by `-slices`. Exits 1 if a check fails.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.optimize import linear_sum_assignment

EVALS_JSON = Path(__file__).with_name("evals.json")
THUMB_SIZE = (96, 54)
PIXEL_TOLERANCE = 24
MIN_SIMILARITY = 0.65
MIN_WORD_LENGTH = 3
MIN_LINE_WORDS = 2
LINE_MATCH_RATIO = 0.8
FOOTER_MARKERS = ("@chrissbaumann", "#eclipsecon")
NOTES_HEADING = "### Notes"
SLIDE_HEADING = re.compile(r"^# Slide (\d+)\b.*$", re.M)
HEADING = re.compile(r"^(#{1,6})\s+\S", re.M)
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
DRAWIO_VALUE = re.compile(r'\bvalue="([^"]*)"')


def load_config(path: Path = EVALS_JSON) -> dict:
    return json.loads(path.read_text())


def expectation_texts(config: dict) -> list[str]:
    t = config["thresholds"]
    return [
        f"All required files are present: {', '.join(config['required_files'])}",
        f"Slide recall is at least {t['slide_recall']}",
        f"Unspoken slide content reaches the article: coverage is at least {t['unspoken_coverage']}",
        f"The article has headings at least {t['min_heading_depth']} levels below the title",
    ]


def thumbnail(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("L").resize(THUMB_SIZE, Image.BILINEAR), dtype=float)


def similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean(np.abs(a - b) < PIXEL_TOLERANCE))


def match_slides(slices: list[Path], deck: list[Path]) -> dict[int, int]:
    """1:1 assignment, deck index -> slice index, of pairs at or above MIN_SIMILARITY."""
    if not slices or not deck:
        return {}
    a = [thumbnail(p) if p else np.full(THUMB_SIZE[::-1], -1e6) for p in deck]
    b = [thumbnail(p) for p in slices]
    sim = np.array([[similarity(x, y) for y in b] for x in a])
    rows, cols = linear_sum_assignment(-sim)
    return {int(r): int(c) for r, c in zip(rows, cols) if sim[r, c] >= MIN_SIMILARITY}


def build_steps(texts: dict[int, list[str]]) -> set[int]:
    """Slides whose text is a proper subset of the next slide's: earlier steps of a build."""
    steps = set()
    for n, lines in texts.items():
        current, following = {ln.strip() for ln in lines}, {ln.strip() for ln in texts.get(n + 1, [])}
        if current and current < following:
            steps.add(n)
    return steps


def slide_recall(slices: list[Path], deck: list[Path], skip: set[int] = frozenset()) -> tuple[float, list[int], dict[int, int]]:
    """Recall over deck slides that are not build steps (numbers in `skip`)."""
    matched = match_slides(slices, [None if i + 1 in skip else p for i, p in enumerate(deck)])
    counted = [i for i in range(len(deck)) if i + 1 not in skip]
    missed = [i + 1 for i in counted if i not in matched]
    hits = len(counted) - len(missed)
    return (hits / len(counted) if counted else 0.0), missed, matched


def words(text: str) -> list[str]:
    return [w for w in re.findall(r"\w+", text.lower()) if len(w) >= MIN_WORD_LENGTH]


def slide_texts(slides_md: str) -> dict[int, list[str]]:
    """Slide number -> text lines without notes and social-handle footers."""
    parts = SLIDE_HEADING.split(slides_md)
    texts = {}
    for number, body in zip(parts[1::2], parts[2::2]):
        body = body.split(NOTES_HEADING)[0].split("\n---")[0]
        lines = [ln for ln in body.splitlines() if ln.strip()]
        texts[int(number)] = [ln for ln in lines if not any(m in ln.lower() for m in FOOTER_MARKERS)]
    return texts


def line_in(line_words: list[str], vocabulary: set[str]) -> bool:
    return sum(w in vocabulary for w in line_words) / len(line_words) >= LINE_MATCH_RATIO


def unspoken_coverage(texts: dict[int, list[str]], slide_numbers, transcript: str, article: str) -> tuple[float, list[str]]:
    spoken, written = set(words(transcript)), set(words(article))
    unspoken, missing = 0, []
    for n in slide_numbers:
        for line in texts.get(n, []):
            lw = words(line)
            if len(lw) < MIN_LINE_WORDS or line_in(lw, spoken):
                continue
            unspoken += 1
            if not line_in(lw, written):
                missing.append(f"slide {n}: {line.strip()}")
    return ((unspoken - len(missing)) / unspoken if unspoken else 1.0), missing


def article_text(article_dir: Path) -> str:
    text = (article_dir / "article.md").read_text() if (article_dir / "article.md").is_file() else ""
    for drawio in sorted(article_dir.glob("diagrams/*.drawio")):
        text += "\n" + "\n".join(html.unescape(v) for v in DRAWIO_VALUE.findall(drawio.read_text()))
    return text


def heading_depth(markdown: str) -> int:
    levels = [len(m.group(1)) for m in HEADING.finditer(FENCE.sub("", markdown))]
    return max(levels) - 1 if levels else 0


def check_files(article_dir: Path, required: list[str]) -> tuple[bool, str]:
    missing = [f for f in required if not (article_dir / f).is_file()]
    return not missing, f"missing: {', '.join(missing)}" if missing else "all present"


def read(path: Path) -> str:
    return path.read_text() if path.is_file() else ""


def grade(article_dir: Path, truth_dir: Path, slices_dir: Path, config: dict) -> dict:
    t = config["thresholds"]
    deck = sorted((truth_dir / "slides").glob("*.png"))
    slices = sorted(slices_dir.glob("*.png")) if slices_dir.is_dir() else []
    texts = slide_texts(read(truth_dir / "slides.md"))
    skipped = build_steps(texts)
    recall, missed, matched = slide_recall(slices, deck, skipped)
    matched_numbers = [i + 1 for i in sorted(matched)]
    coverage, uncovered = unspoken_coverage(texts, matched_numbers,
                                            read(article_dir / "transcript.md"), article_text(article_dir))
    depth = heading_depth(read(article_dir / "article.md"))
    results = [
        check_files(article_dir, config["required_files"]),
        (recall >= t["slide_recall"], f"recall {recall:.2f} ({len(deck) - len(skipped) - len(missed)}/{len(deck) - len(skipped)} deck slides without build steps {sorted(skipped)}, {len(slices)} kept); missed {missed}"),
        (coverage >= t["unspoken_coverage"], f"coverage {coverage:.2f}; not in article: {uncovered[:10]}"),
        (depth >= t["min_heading_depth"], f"depth {depth}"),
    ]
    expectations = [{"text": text, "passed": passed, "evidence": evidence}
                    for text, (passed, evidence) in zip(expectation_texts(config), results)]
    passed = sum(e["passed"] for e in expectations)
    return {"expectations": expectations,
            "metrics": {"slide_recall": round(recall, 3), "unspoken_coverage": round(coverage, 3),
                        "heading_depth": depth, "missed_slides": missed, "uncovered_lines": uncovered},
            "summary": {"passed": passed, "failed": len(expectations) - passed, "total": len(expectations)}}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("article_dir", type=Path)
    parser.add_argument("truth_dir", type=Path)
    parser.add_argument("--slices", type=Path)
    parser.add_argument("--out", type=Path, default=Path("grading.json"))
    args = parser.parse_args(argv[1:])
    article_dir = args.article_dir.resolve()
    slices = args.slices or article_dir.with_name(re.sub(r"-article$", "-slices", article_dir.name))
    grading = grade(article_dir, args.truth_dir, slices, load_config())
    args.out.write_text(json.dumps(grading, indent=2, ensure_ascii=False))
    for e in grading["expectations"]:
        print(("PASS" if e["passed"] else "FAIL"), e["text"], "|", e["evidence"][:200])
    return 1 if grading["summary"]["failed"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
