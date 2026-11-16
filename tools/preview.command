#!/bin/bash
# Local preview of the website. Double-click in Finder, or run: ./tools/preview.command
# - If Jekyll is installed (see README), it rebuilds from content/ and reloads on every save.
# - Otherwise it serves the last built copy in _site/.
cd "$(dirname "$0")/.." || exit 1
PORT=4000
BASEURL=$(grep -E '^baseurl:' _config.yml | sed -E 's/baseurl:[[:space:]]*"?([^"]*)"?.*/\1/')
URL="http://localhost:$PORT$BASEURL/"
if command -v bundle >/dev/null 2>&1 && bundle exec jekyll -v >/dev/null 2>&1; then
  echo "Starting Jekyll at $URL  (Ctrl+C to stop)"
  bundle exec jekyll serve --port $PORT --livereload
else
  echo "Jekyll is not installed on this Mac: serving the pre-built site in _site/"
  ROOT="${TMPDIR:-/tmp}/siam-site-preview"
  mkdir -p "$ROOT$(dirname "${BASEURL:-/x}")"
  if [ -n "$BASEURL" ]; then ln -sfn "$PWD/_site" "$ROOT$BASEURL"; SERVE="$ROOT"; else SERVE="$PWD/_site"; fi
  echo "Open $URL  (Ctrl+C to stop)"
  (sleep 1; open "$URL") &
  python3 -m http.server $PORT --directory "$SERVE"
fi
