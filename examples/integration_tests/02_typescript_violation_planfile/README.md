# Example 02 — TypeScript VIOLATION + planfile tickets

Ten przykład celowo łamie kontrakt:

```text
forbid:network
```

Kod używa `fetch(...)`, więc Intract powinien wykryć `violation` i wygenerować tickety.

## Uruchomienie

```bash
python -m intract validate examples/integration_tests/02_typescript_violation_planfile --json
python -m intract validate examples/integration_tests/02_typescript_violation_planfile --planfile
python -m intract tickets examples/integration_tests/02_typescript_violation_planfile
```

## Oczekiwany wynik

- `validate`: `violation`
- `.intract/planfile-tickets.yaml`
- `.intract/planfile-tickets.json`
- `.intract/TODO.intract.md`
