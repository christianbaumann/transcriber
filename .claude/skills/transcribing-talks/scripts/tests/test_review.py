import json
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import review  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "review"
SCRIPT = Path(review.__file__)


@pytest.fixture
def items():
    return review.list_items(FIXTURE / "notes", FIXTURE)


@pytest.fixture
def info():
    return json.loads((FIXTURE / "info.json").read_text())


def test_parse_note_reads_frontmatter_and_body():
    meta = review.parse_note(FIXTURE / "notes" / "0007.md")
    assert meta["slide"] == 7
    assert meta["kind"] == "diagram"
    assert meta["body"] == "Gateway box"


def test_list_items_come_from_assets_and_note_body(items):
    assert [i["key"] for i in items] == [
        "7/diagrams/0007-architecture.svg",
        "12/code-1",
        "30/formula-1",
        "30/table-1",
        "30/code-1",
    ]
    assert items[0]["original"] == FIXTURE / "slices" / "0007_00-12-34.png"


def test_formula_png_is_shown_with_the_formula_not_as_own_item(items):
    formula = items[2]
    assert formula["images"] == [FIXTURE / "diagrams" / "0030-throughput.png"]
    assert "30/diagrams/0030-throughput.png" not in [i["key"] for i in items]


def test_code_dollars_do_not_become_formulas(items):
    assert "12/formula-1" not in [i["key"] for i in items]
    assert "costs $5 and $6" in items[1]["text"]


def test_page_shows_original_next_to_each_recreated_item(items, info):
    page = review.render_page(info, items, lambda p: f"/f/{p.name}")
    assert page.count('class="item"') == 5
    for item in items:
        block = page.split(f'data-key="{item["key"]}"')[1].split("</section>")[0]
        assert block.index("Original") < block.index("Re-created")
        assert f'/f/{item["original"].name}' in block
    assert "/f/0007-architecture.svg" in page
    formula = page.split('data-key="30/formula-1"')[1].split("</section>")[0]
    assert "$$\\mathrm{Throughput}" in formula
    assert "/f/0030-throughput.png" in formula
    assert "<td>8000</td>" in page
    assert "&lt;ok&gt;" in page


def test_missing_info_fields_are_marked_as_gaps(items, info):
    page = review.render_page(info, items, str)
    for field in ("event", "source", "speaker"):
        assert f"<span>{field} (gap" in page
    for field in ("title", "date", "duration"):
        assert f"<span>{field}</span>" in page


def start(items, info, tmp_path):
    done = threading.Event()
    server = review.make_server(info, items, tmp_path, done)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, done, f"http://127.0.0.1:{server.server_address[1]}"


def post(url, payload):
    req = urllib.request.Request(url + "/answers", json.dumps(payload).encode(),
                                 {"Content-Type": "application/json"})
    return urllib.request.urlopen(req)


def test_server_serves_page_and_files(items, info, tmp_path):
    server, _, url = start(items, info, tmp_path)
    try:
        assert b"Info area" in urllib.request.urlopen(url + "/").read()
        png = urllib.request.urlopen(url + "/file?id=0")
        assert png.headers["Content-Type"] == "image/png"
        with pytest.raises(urllib.error.HTTPError):
            urllib.request.urlopen(url + "/file?id=999")
    finally:
        server.shutdown()


def test_post_writes_answers_in_documented_format(items, info, tmp_path):
    server, done, url = start(items, info, tmp_path)
    answers = {"info": {"title": "Talk", "event": None},
               "items": {i["key"]: {"status": "ok", "comment": ""} for i in items}}
    answers["items"]["30/formula-1"] = {"status": "fix", "comment": "c"}
    try:
        assert post(url, answers).read() == b"saved"
    finally:
        server.shutdown()
    assert done.is_set()
    assert json.loads((tmp_path / "answers.json").read_text()) == answers


def test_post_rejects_unknown_items_and_statuses(items, info, tmp_path):
    server, done, url = start(items, info, tmp_path)
    good = {i["key"]: {"status": "ok", "comment": ""} for i in items}
    bad_status = {**good, items[0]["key"]: {"status": "maybe", "comment": ""}}
    try:
        for payload in ({"info": {}, "items": {}}, {"info": {}, "items": bad_status}):
            with pytest.raises(urllib.error.HTTPError) as e:
                post(url, payload)
            assert e.value.code == 400
    finally:
        server.shutdown()
    assert not done.is_set()
    assert not (tmp_path / "answers.json").exists()


def run_cli(tmp_path, timeout):
    return subprocess.Popen(
        [sys.executable, "-I", str(SCRIPT), "--notes", str(FIXTURE / "notes"),
         "--info", str(FIXTURE / "info.json"), "--out", str(tmp_path),
         "--timeout", str(timeout), "--no-open"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_cli_exits_nonzero_on_timeout_without_answers(tmp_path):
    proc = run_cli(tmp_path, 1)
    _, err = proc.communicate(timeout=30)
    assert proc.returncode == 1
    assert "No answers" in err
    assert not (tmp_path / "answers.json").exists()


def test_cli_exits_zero_after_submission(tmp_path, items):
    proc = run_cli(tmp_path, 30)
    url = proc.stdout.readline().split("Review page: ")[1].strip().rstrip("/")
    post(url, {"info": {}, "items": {i["key"]: {"status": "ok", "comment": ""}
                                     for i in items}})
    proc.communicate(timeout=30)
    assert proc.returncode == 0
    assert (tmp_path / "answers.json").exists()
