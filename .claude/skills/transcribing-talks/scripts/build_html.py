#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Build a self-contained HTML file from an article Markdown file with pandoc.

Images and SVGs, the stylesheet and KaTeX (script, CSS, fonts) are embedded.
KaTeX is fetched from pandoc's default CDN at build time, so the build needs
network access; the resulting file does not.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

CSS = Path(__file__).with_name("article.css")
PANDOC_RESOURCE_WARNING = "Could not fetch resource"


class BuildError(Exception):
    pass


def page_title(markdown: str, fallback: str) -> str:
    heading = re.search(r"^#\s+(.+)$", markdown, re.M)
    return heading.group(1).strip() if heading else fallback


def build(article: Path, out: Path) -> None:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise BuildError("pandoc not found on PATH; install it (e.g. brew install pandoc)")
    if not article.is_file():
        raise BuildError(f"article not found: {article}")
    markdown = article.read_text(encoding="utf-8")
    cmd = [
        pandoc, str(article), "--from=markdown", "--standalone", "--embed-resources",
        "--math-method=katex", f"--css={CSS}", f"--resource-path={article.parent}",
        f"--metadata=pagetitle:{page_title(markdown, article.stem)}",
        "--output", str(out),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    unresolved = [line for line in result.stderr.splitlines() if PANDOC_RESOURCE_WARNING in line]
    if unresolved:
        raise BuildError("image not found: " + "; ".join(l.split(PANDOC_RESOURCE_WARNING)[1].strip() for l in unresolved))
    if result.returncode != 0:
        raise BuildError(f"pandoc failed:\n{result.stderr.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        build(args.article, args.out)
    except BuildError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
