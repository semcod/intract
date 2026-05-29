# Example 03 — Watch + Engine + Drift

Ten przykład pokazuje tryby:

```bash
intract watch
intract engine suggest
intract engine drift
intract engine run
```

## Uruchomienie jednorazowe

```bash
python -m intract watch examples/integration_tests/03_watch_engine_drift --once
python -m intract engine suggest examples/integration_tests/03_watch_engine_drift
python -m intract engine drift examples/integration_tests/03_watch_engine_drift
python -m intract engine run examples/integration_tests/03_watch_engine_drift --json
```

## Test drift

1. Uruchom:

```bash
python -m intract engine drift examples/integration_tests/03_watch_engine_drift
```

2. Zmień logikę w `scanner.py`, np. dodaj `.lower()` albo dodatkowy warunek.
3. Uruchom ponownie:

```bash
python -m intract engine drift examples/integration_tests/03_watch_engine_drift
```

Powinien pojawić się `logic_changed`.

## Watch real-time

```bash
python -m intract watch examples/integration_tests/03_watch_engine_drift --planfile
```

Następnie zmień plik `scanner.py`. Intract wykryje zmianę i uruchomi walidację.
