#!/bin/bash
# Zautomatyzowany skrypt walidacji dla Toon przykładów
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$DIR/../.."

echo -e "\033[1;34m=== Uruchamianie walidacji dla przykładu Toon ===\033[0m"

# Wykrywanie Pythona z venv
if [ -d "$ROOT_DIR/venv" ]; then
    PYTHON="$ROOT_DIR/venv/bin/python"
else
    PYTHON="python3"
fi

echo -e "\033[1;32m1. Walidacja przy użyciu płaskiego manifestu URI (intract.toon):\033[0m"
$PYTHON -m intract validate "$DIR" --manifest "$DIR/intract.toon"

echo -e "\n\033[1;32m2. Walidacja przy użyciu manifestu YAML z targetami (intract.toon.yaml):\033[0m"
$PYTHON -m intract validate "$DIR" --manifest "$DIR/intract.toon.yaml"

echo -e "\n\033[1;36m=== Walidacja zakończona! ===\033[0m"
