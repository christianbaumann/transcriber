#!/usr/bin/env bash
# Copies the gitignored reference talk videos and decks from ~/Downloads into testdata/talks/.
set -euo pipefail

SRC="${1:-$HOME/Downloads}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/testdata/talks"

copy() { # <talk dir> <source file name> <target file name>
  cp -v "$SRC/$2" "$DEST/$1/$3"
}

FOOL=fool-with-a-tool
copy $FOOL "Don’t be a fool with a tool ‒ fundamental knowledge for proper test automation (720p_24fps_H264-192kbit_AAC).mp4" video.mp4
copy $FOOL "Don’t be a fool with a tool - askui Hackathon 2023-03.pptx" deck.pptx
copy $FOOL "Don’t be a fool with a tool - askui Hackathon 2023-03.pdf" deck.pdf

ECLIPSE=extreme-learning-eclipsecon
copy $ECLIPSE "2020 EclipseCon.mp4" video.mp4
copy $ECLIPSE "Extreme learning situations as testers EclipseCon.pptx" deck.pptx
copy $ECLIPSE "Extreme learning situations as testers EclipseCon.pdf" deck.pdf

DRAGONS=dragons-agiletd
copy $DRAGONS "Dragons biases and other things you shouldnt ignore AgileTD 2025.mp4" video.mp4
copy $DRAGONS "Dragons, biases, and other things you shouldn’t ignore.pptx" deck.pptx
copy $DRAGONS "Dragons, biases, and other things you shouldn’t ignore.pdf" deck.pdf
