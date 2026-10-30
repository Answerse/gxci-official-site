#!/bin/bash
# 一次性：起 Chrome → 跑 cdp_shot → 关 Chrome
# 用法: bash tools/shot_pages.sh <width> <prefix> <page...>
set -e
W=$1; P=$2; shift 2
PORT=9336
TMPD=/tmp/cdp-shot-$$
("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --no-sandbox --in-process-gpu --no-proxy-server \
  --remote-debugging-port=$PORT "--remote-allow-origins=*" \
  --user-data-dir=$TMPD --hide-scrollbars about:blank >/tmp/cdp-shot.log 2>&1 &)
sleep 4
cd "$(dirname "$0")/.."
NO_PROXY=127.0.0.1 no_proxy=127.0.0.1 \
  /Users/answerose/.workbuddy/binaries/python/envs/default/bin/python tools/cdp_shot.py "$W" "$P" "$@"
pkill -f "user-data-dir=$TMPD" || true
