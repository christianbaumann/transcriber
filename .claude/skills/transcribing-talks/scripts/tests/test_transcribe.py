import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import transcribe  # noqa: E402


def test_command_requests_word_timestamps_into_whisper_json(tmp_path):
    cmd = transcribe.build_command(Path("talk.mp4"), tmp_path, None, None)
    assert cmd[cmd.index("--word-timestamps") + 1] == "True"
    assert cmd[cmd.index("--output-name") + 1] == "whisper"
    assert cmd[cmd.index("--output-dir") + 1] == str(tmp_path)
    assert "--language" not in cmd


def test_command_passes_language_and_prompt(tmp_path):
    cmd = transcribe.build_command(Path("talk.mp4"), tmp_path, "de", "Kubernetes")
    assert cmd[cmd.index("--language") + 1] == "de"
    assert cmd[cmd.index("--initial-prompt") + 1] == "Kubernetes"
