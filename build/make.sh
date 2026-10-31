#!/bin/sh
# Rebuild index.html (and artifact.html) from config.js: the skill's engine, then this room's engine
# extensions. Run it after every edit to config.js or build/patch.py.
#   sh build/make.sh
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd)
SKILL=${SKILL:-$HOME/.claude/plugins/cache/skylarkitchen/skylarkitchen-skills/1.4.2/skills/design/room-from-photos}
python3 "$SKILL/build.py" "$HERE" --artifact
python3 "$HERE/build/patch.py" "$HERE/index.html"
python3 "$HERE/build/patch.py" "$HERE/artifact.html"
