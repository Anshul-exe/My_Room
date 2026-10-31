#!/bin/sh
# One headless capture of the page, retried until the frame is more than a blank canvas.
#   sh build/shot.sh <out.png> <hash> [WxH] [budget-ms]
# Software WebGL is slow: a photo view with every pass takes 20-50 s a frame, so the budget is large
# and the result is checked for variance rather than for existing.
set -e
OUT=$1; HASH=$2; SIZE=${3:-1440x900}; BUD=${4:-20000}
W=${SIZE%x*}; H=${SIZE#*x}
for try in 1 2 3; do
  DIR=$(mktemp -d)
  rm -f "$OUT"
  perl -e 'alarm 420; exec @ARGV' google-chrome-stable --headless=new --user-data-dir="$DIR/p" \
    --disable-gpu --use-angle=swiftshader --enable-unsafe-swiftshader --disable-extensions \
    --run-all-compositor-stages-before-draw --disable-new-content-rendering-timeout \
    --window-size="$W,$H" --virtual-time-budget="$BUD" --screenshot="$OUT" \
    "http://127.0.0.1:8080/index.html#$HASH" >/dev/null 2>&1 || true
  pkill -f "user-data-dir=$DIR/p" >/dev/null 2>&1 || true
  rm -rf "$DIR"
  if [ -f "$OUT" ] && python3 -I -c "
from PIL import Image, ImageStat
import sys
s = ImageStat.Stat(Image.open('$OUT').convert('L'))
sys.exit(0 if s.stddev[0] > 12 else 1)
" 2>/dev/null; then
    echo "$(stat -c %s "$OUT") $OUT"
    exit 0
  fi
  BUD=$((BUD * 2))
done
echo "blank after 3 tries: $OUT"
exit 1
