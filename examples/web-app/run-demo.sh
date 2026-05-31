#!/usr/bin/env bash
# Export Intract reports for the web-app mock dashboard.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"
MANIFEST="$ROOT/intract.yaml"
REPORTS="$ROOT/mock/reports"
mkdir -p "$REPORTS"

for label in v1-pass v2-violation; do
  target="$ROOT/iterations/$label"
  echo "==> validate $label"
  "$PYTHON" -m intract validate "$target" --manifest "$MANIFEST" --json > "$REPORTS/${label}.validate.json"
  "$PYTHON" -m intract graph "$target" --manifest "$MANIFEST" --format json > "$REPORTS/${label}.graph.json"
  "$PYTHON" -m intract scan "$target" --all-artifacts --json > "$REPORTS/${label}.artifacts.json" || true
done

echo "Reports written to $REPORTS"
echo "Open mock/index.html in a browser"
