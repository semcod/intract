#!/usr/bin/env bash
# Run Intract demo plus optional vallm/reDUP intent integration checks.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
DEMO="${DEMO:-$ROOT/examples/full-stack}"
VALLM_ROOT="${VALLM_ROOT:-$ROOT/../vallm}"
REDUP_ROOT="${REDUP_ROOT:-$ROOT/../redup}"
WEB_APP="${WEB_APP:-$ROOT/examples/web-app}"
WEB_MANIFEST="${WEB_MANIFEST:-$WEB_APP/intract.yaml}"

echo "==> Installing intract"
"$PYTHON" -m pip install -q -e "$ROOT[dev]"

install_extra() {
  local name=$1
  local path=$2
  local extra=$3
  if [[ -f "$path/pyproject.toml" || -f "$path/setup.py" ]]; then
    echo "==> Installing ${name} from ${path}[${extra}]"
    "$PYTHON" -m pip install -q -e "${path}[${extra}]"
    return 0
  fi
  echo "==> Installing ${name}[${extra}] from PyPI"
  "$PYTHON" -m pip install -q "${name}[${extra}]"
}

if [[ "${SKIP_VALLM:-0}" != "1" ]]; then
  install_extra vallm "$VALLM_ROOT" intract || echo "WARN: vallm[intract] not available"
fi

if [[ "${SKIP_REDUP:-0}" != "1" ]]; then
  install_extra redup "$REDUP_ROOT" intent || echo "WARN: redup[intent] not available"
fi

echo "==> intract validate ${DEMO}"
"$PYTHON" -m intract validate "$DEMO" --manifest "$DEMO/intract.yaml"

echo "==> intract duplicates ${DEMO}"
"$PYTHON" -m intract duplicates "$DEMO" --threshold 0.5

echo "==> intract graph ${DEMO}"
"$PYTHON" -m intract graph "$DEMO" --manifest "$DEMO/intract.yaml" --format json >/dev/null

if [[ -f "$WEB_MANIFEST" ]]; then
  echo "==> intract validate web-app v1-pass"
  "$PYTHON" -m intract validate "$WEB_APP/iterations/v1-pass" --manifest "$WEB_MANIFEST"
  echo "==> intract validate web-app v2-violation (expect violation)"
  if "$PYTHON" -m intract check "$WEB_APP/iterations/v2-violation" --manifest "$WEB_MANIFEST"; then
    echo "ERROR: v2-violation should fail policy check"
    exit 1
  fi
  if "$PYTHON" -m vallm intract --help >/dev/null 2>&1; then
    echo "==> vallm intract web-app v1-pass"
    "$PYTHON" -m vallm intract "$WEB_APP/iterations/v1-pass" --manifest "$WEB_MANIFEST"
  fi
fi

if "$PYTHON" -m vallm intract --help >/dev/null 2>&1; then
  echo "==> vallm intract ${DEMO}"
  "$PYTHON" -m vallm intract "$DEMO" --manifest "$DEMO/intract.yaml"
else
  echo "SKIP: vallm not installed"
fi

if "$PYTHON" -m redup scan --help >/dev/null 2>&1; then
  echo "==> redup scan ${DEMO} --intent"
  "$PYTHON" -m redup scan "$DEMO" --intent --intent-threshold 0.5 --format json >/dev/null
else
  echo "SKIP: redup not installed"
fi

echo "OK: full-stack CI checks passed"
