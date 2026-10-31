#!/bin/sh
# Open the room locally. Serves this folder on 127.0.0.1:8080 (localhost only, nothing is published)
# and opens it in your browser. Ctrl-C stops it.
#   sh room.sh [port]
PORT=${1:-8080}
HERE=$(cd "$(dirname "$0")" && pwd)
URL="http://127.0.0.1:$PORT/index.html"
if command -v curl >/dev/null && curl -s -o /dev/null --max-time 1 "$URL"; then
  echo "already serving at $URL"
  xdg-open "$URL" >/dev/null 2>&1 &
  exit 0
fi
echo "serving $HERE at $URL   (Ctrl-C to stop)"
(sleep 1; xdg-open "$URL" >/dev/null 2>&1) &
exec python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$HERE"
