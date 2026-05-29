.PHONY: install test lint format

install:
	pip install -e .[dev]

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .
