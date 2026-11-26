#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Serve a local review page for the info area and re-created slide items.

review.py --notes <slides dir> --info <info.json> --out <dir>
          [--article <dir>] [--timeout SECONDS] [--no-open]

--notes    directory with slide notes (NNNN.md: YAML frontmatter + body)
--info     JSON object with the keys title, event, date, source, duration,
           speaker. A missing key or null marks a gap the user must fill.
--out      directory that receives answers.json
--article  base for relative `assets` and `image` paths in the notes
           (default: parent of --notes)

The page shows the info fields, then every re-created item next to its
original slide image, with ok / fix and a comment. Items: each image in
`assets` (.drawio sources excluded) and, from the note body, each fenced
code block, Markdown table and $$...$$ formula (keys <slide>/code-N,
table-N, formula-N). When the body has a formula, the slide's asset images
are shown with the first formula instead of as own items. Submitting writes <out>/answers.json and the script
exits 0:

  {"info": {field: value|null},
   "items": {"<slide>/<asset>": {"status": "ok"|"fix", "comment": "..."}}}

Without a submission within --timeout the script exits 1 and writes nothing.
Formulas are typeset by KaTeX loaded from a CDN; offline, the LaTeX source
is shown as text.
"""
import argparse
import html
import json
import re
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import yaml

INFO_FIELDS = ["title", "event", "date", "source", "duration", "speaker"]
DEFAULT_TIMEOUT_S = 1800
STATUSES = ("ok", "fix")
SOURCE_ONLY_SUFFIXES = {".drawio"}
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.S)


def parse_note(path: Path) -> dict:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"{path}: no frontmatter")
    meta = yaml.safe_load(match.group(1)) or {}
    meta["body"] = match.group(2).strip()
    return meta


FENCE = re.compile(r"^```[^\n]*\n(.*?)^```[ \t]*$", re.S | re.M)
DISPLAY_FORMULA = re.compile(r"\$\$(.+?)\$\$", re.S)
TABLE = re.compile(r"(?:^[ \t]*\|.*(?:\n|\Z))+", re.M)


def body_items(body: str) -> list[tuple[str, str]]:
    """(type, text) for each display formula, table and code block."""
    prose = FENCE.sub("", body)
    formulas = [("formula", m.group(1).strip()) for m in DISPLAY_FORMULA.finditer(prose)]
    tables = [("table", m.group(0).strip()) for m in TABLE.finditer(prose)]
    code = [("code", m.group(1).rstrip("\n")) for m in FENCE.finditer(body)]
    return formulas + tables + code


def list_items(notes_dir: Path, article_dir: Path) -> list[dict]:
    """One item per re-created diagram asset and per code block, table or
    formula in the note body, each with the slide's original image."""
    items = []
    for note in sorted(notes_dir.glob("*.md")):
        meta = parse_note(note)
        slide = meta["slide"]
        common = {"slide": slide, "time": meta.get("time", ""),
                  "kind": meta.get("kind", ""),
                  "original": resolve(meta.get("image"), article_dir)}
        from_body = body_items(meta["body"])
        assets = [a for a in meta.get("assets") or []
                  if Path(a).suffix.lower() not in SOURCE_ONLY_SUFFIXES]
        has_formula = any(kind == "formula" for kind, _ in from_body)
        if not has_formula:
            items += [{**common, "key": f"{slide}/{a}", "type": "asset",
                       "label": a, "images": [article_dir / a], "text": ""}
                      for a in assets]
        counts: dict[str, int] = {}
        for kind, text in from_body:
            counts[kind] = counts.get(kind, 0) + 1
            first_formula = kind == "formula" and counts[kind] == 1
            items.append({**common, "key": f"{slide}/{kind}-{counts[kind]}",
                          "type": kind, "label": f"{kind} {counts[kind]}",
                          "images": [article_dir / a for a in assets] if first_formula else [],
                          "text": text})
    return items


def resolve(path: str | None, base: Path) -> Path | None:
    if not path:
        return None
    p = Path(path)
    return p if p.is_absolute() else base / p


def table_html(markdown: str) -> str:
    rows = [[c.strip() for c in line.strip().strip("|").split("|")]
            for line in markdown.splitlines() if line.strip().startswith("|")]
    rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", c) for c in r)]
    if not rows:
        return f"<pre>{html.escape(markdown)}</pre>"
    head, *body = rows
    th = "".join(f"<th>{html.escape(c)}</th>" for c in head)
    trs = "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r)
                  + "</tr>" for r in body)
    return f"<table><tr>{th}</tr>{trs}</table>"


def asset_html(item: dict, file_url) -> str:
    images = "".join(f'<img src="{file_url(p)}" alt="{html.escape(p.name)}">'
                     for p in item["images"])
    if item["type"] == "formula":
        return f'<div class="latex">$${html.escape(item["text"])}$$</div>{images}'
    if item["type"] == "table":
        return table_html(item["text"])
    if item["type"] == "code":
        return f"<pre><code>{html.escape(item['text'])}</code></pre>"
    return images


def info_html(info: dict) -> str:
    rows = []
    for field in INFO_FIELDS:
        value = info.get(field)
        gap = value in (None, "")
        rows.append(
            f'<label class="{"gap" if gap else ""}"><span>{field}'
            f'{" (gap: please fill in)" if gap else ""}</span>'
            f'<input name="info.{field}" value="{html.escape(str(value or ""))}">'
            "</label>")
    return "<section><h2>Info area</h2>" + "".join(rows) + "</section>"


def item_html(index: int, item: dict, file_url) -> str:
    original = (f'<img src="{file_url(item["original"])}" alt="original">'
                if item["original"] else '<p class="missing">no original</p>')
    key = html.escape(item["key"], quote=True)
    return f"""<section class="item" data-key="{key}">
<h3>Slide {item["slide"]} ({html.escape(str(item["time"]))}, {html.escape(item["kind"])}): {html.escape(item["label"])}</h3>
<div class="pair"><figure><figcaption>Original</figcaption>{original}</figure>
<figure><figcaption>Re-created</figcaption>{asset_html(item, file_url)}</figure></div>
<label><input type="radio" name="status.{index}" value="ok" checked> ok</label>
<label><input type="radio" name="status.{index}" value="fix"> fix</label>
<input class="comment" name="comment.{index}" placeholder="comment">
</section>"""


SCRIPT = """
document.querySelector('form').addEventListener('submit', async e => {
  e.preventDefault();
  const info = {};
  document.querySelectorAll('[name^="info."]').forEach(i =>
    info[i.name.slice(5)] = i.value.trim() || null);
  const items = {};
  document.querySelectorAll('.item').forEach((s, n) => {
    items[s.dataset.key] = {
      status: s.querySelector('input[type=radio]:checked').value,
      comment: s.querySelector('.comment').value};
  });
  const r = await fetch('/answers', {method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({info, items})});
  document.getElementById('state').textContent =
    r.ok ? 'saved' : 'error: ' + await r.text();
});
"""

STYLE = """
body{font:15px system-ui;max-width:1200px;margin:1rem auto;padding:0 1rem}
.pair{display:flex;gap:1rem}.pair figure{flex:1;margin:0;min-width:0}
img{max-width:100%;border:1px solid #ccc}
label{display:block;margin:.3rem 0}label span{display:inline-block;width:8rem}
.gap input{background:#fff3cd;border:1px solid #d39e00}.gap span{color:#a06600}
.comment{width:60%}.missing{color:#a00}pre{overflow:auto;background:#f6f6f6}
.item{border-top:1px solid #aaa;margin-top:1rem}
td,th{border:1px solid #ccc;padding:.2rem .5rem}
"""


def render_page(info: dict, items: list[dict], file_url) -> str:
    blocks = "".join(item_html(i, it, file_url) for i, it in enumerate(items))
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Review</title><style>{STYLE}</style>
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}}]}})"></script>
</head><body><h1>Review</h1><form>{info_html(info)}
<h2>Re-created items ({len(items)})</h2>{blocks}
<p><button type="submit">Submit</button> <span id="state"></span></p></form>
<script>{SCRIPT}</script></body></html>"""


def validate_answers(data: dict, expected_keys: set[str]) -> None:
    if set(data.get("items", {})) != expected_keys:
        raise ValueError("items do not match the review page")
    for key, answer in data["items"].items():
        if answer.get("status") not in STATUSES:
            raise ValueError(f"invalid status for {key}")
    if not isinstance(data.get("info"), dict):
        raise ValueError("info missing")


def make_server(info: dict, items: list[dict], out_dir: Path,
                done: threading.Event, port: int = 0) -> ThreadingHTTPServer:
    files: dict[str, Path] = {}

    def file_url(path: Path) -> str:
        token = str(len(files))
        files[token] = path
        return f"/file?id={token}"

    page = render_page(info, items, file_url).encode()
    expected = {it["key"] for it in items}

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, body=b"", ctype="text/plain"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            url = urlparse(self.path)
            if url.path == "/":
                return self._send(200, page, "text/html; charset=utf-8")
            if url.path == "/file":
                path = files.get(parse_qs(url.query).get("id", [""])[0])
                if path and path.is_file():
                    import mimetypes
                    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
                    return self._send(200, path.read_bytes(), ctype)
            self._send(404, b"not found")

        def do_POST(self):
            if self.path != "/answers":
                return self._send(404, b"not found")
            try:
                data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                validate_answers(data, expected)
            except (ValueError, KeyError, TypeError, AttributeError) as e:
                return self._send(400, str(e).encode())
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "answers.json").write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            self._send(200, b"saved")
            done.set()

        def log_message(self, *args):
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def run(notes: Path, info_path: Path, out_dir: Path, article: Path,
        timeout: float, open_browser: bool = True) -> int:
    info = json.loads(info_path.read_text(encoding="utf-8"))
    items = list_items(notes, article)
    done = threading.Event()
    server = make_server(info, items, out_dir, done)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Review page: {url}", flush=True)
    if open_browser:
        webbrowser.open(url)
    saved = done.wait(timeout)
    server.shutdown()
    if not saved:
        print(f"No answers submitted within {timeout:g} s", file=sys.stderr)
        return 1
    print(f"Answers written to {out_dir / 'answers.json'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--notes", type=Path, required=True)
    ap.add_argument("--info", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--article", type=Path)
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_S)
    ap.add_argument("--no-open", action="store_true")
    a = ap.parse_args()
    article = a.article or a.notes.resolve().parent
    return run(a.notes, a.info, a.out, article, a.timeout, not a.no_open)


if __name__ == "__main__":
    sys.exit(main())
