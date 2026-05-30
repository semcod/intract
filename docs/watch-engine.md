# Watch & Engine

## Watch

`watch` działa jak lokalny linter w czasie rzeczywistym.

```bash
python -m intract watch .
```

Z planfile-compatible ticketami:

```bash
python -m intract watch . --planfile
```

Jednorazowo:

```bash
python -m intract watch . --once
```

## Jak działa watch

```text
1. Skanuje folder.
2. Liczy hash plików logicznych.
3. Wykrywa added / modified / deleted.
4. Uruchamia walidację.
5. Opcjonalnie generuje tickety.
```

Kod:

- [`src/intract/watch.py`](../src/intract/watch.py)

## Engine

Silnik składa się z:

- [`src/intract/engine/scanner.py`](../src/intract/engine/scanner.py)
- [`src/intract/engine/analyzer.py`](../src/intract/engine/analyzer.py)
- [`src/intract/engine/assigner.py`](../src/intract/engine/assigner.py)
- [`src/intract/engine/drift.py`](../src/intract/engine/drift.py)
- [`src/intract/engine/monitor.py`](../src/intract/engine/monitor.py)

## Suggest

```bash
python -m intract engine suggest .
```

Proponuje kontrakty dla wykrytych fragmentów logicznych.

## Drift

```bash
python -m intract engine drift .
```

Porównuje aktualny stan logiki z poprzednim snapshotem.

Stan:

```text
.intract/engine-state.json
```

## Full engine run

```bash
python -m intract engine run .
python -m intract engine run . --planfile
python -m intract engine run . --json
```
