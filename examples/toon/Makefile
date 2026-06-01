.PHONY: all validate validate-uri validate-yaml help

all: validate

validate:
	@bash ./validate.sh

validate-uri:
	@echo "Uruchamianie walidacji dla płaskiego formatu URI (intract.toon)..."
	@../../venv/bin/python -m intract validate . --manifest ./intract.toon

validate-yaml:
	@echo "Uruchamianie walidacji dla formatu YAML z targetami (intract.toon.yaml)..."
	@../../venv/bin/python -m intract validate . --manifest ./intract.toon.yaml

help:
	@echo "Dostępne komendy:"
	@echo "  make validate       - Uruchamia automatyczną walidację obu manifestów"
	@echo "  make validate-uri   - Waliduje projekt tylko za pomocą płaskiego pliku intract.toon"
	@echo "  make validate-yaml  - Waliduje projekt tylko za pomocą pliku intract.toon.yaml"
