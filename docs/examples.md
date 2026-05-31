# Examples

Główne przykłady znajdują się w [`examples/`](../examples/) — indeks: [`examples/README.md`](../examples/README.md).

Uruchom integracje:

```bash
python examples/integration_tests/run_examples.py
```

## Web App (mock produktu + iteracje)

Folder:

- [`examples/web-app/`](../examples/web-app/)

Wizualny mock:

```bash
bash examples/web-app/run-demo.sh
python -m http.server 8765 --directory examples/web-app
# → http://localhost:8765/mock/index.html
```

Iteracje:

| Folder | Intract | Opis |
|--------|---------|------|
| `iterations/v1-pass/` | funkcje pass | Release candidate bez sieci |
| `iterations/v2-violation/` | violation | requests + fetch + Dockerfile |

Komendy:

```bash
python -m intract validate examples/web-app/iterations/v1-pass \
  --manifest examples/web-app/intract.yaml
python -m intract validate examples/web-app/iterations/v2-violation \
  --manifest examples/web-app/intract.yaml --planfile
python -m intract scan examples/web-app/iterations/v1-pass --all-artifacts
```

## Full-stack pipeline

- [`examples/full-stack/`](../examples/full-stack/)

## 01 — Python PASS

Folder:

- [`examples/integration_tests/01_python_pass/`](../examples/integration_tests/01_python_pass/)

Komendy:

```bash
python -m intract validate examples/integration_tests/01_python_pass --json
python -m intract scan examples/integration_tests/01_python_pass
python -m intract engine suggest examples/integration_tests/01_python_pass
```

Oczekiwane:

```text
status: pass
```

## 02 — TypeScript VIOLATION + planfile

Folder:

- [`examples/integration_tests/02_typescript_violation_planfile/`](../examples/integration_tests/02_typescript_violation_planfile/)

Komendy:

```bash
python -m intract validate examples/integration_tests/02_typescript_violation_planfile --json
python -m intract validate examples/integration_tests/02_typescript_violation_planfile --planfile
python -m intract tickets examples/integration_tests/02_typescript_violation_planfile
```

Oczekiwane:

```text
status: violation
tickets: 1+
```

Generowane:

```text
.intract/planfile-tickets.yaml
.intract/planfile-tickets.json
.intract/TODO.intract.md
```

## 03 — Watch + Engine + Drift

Folder:

- [`examples/integration_tests/03_watch_engine_drift/`](../examples/integration_tests/03_watch_engine_drift/)

Komendy:

```bash
python -m intract watch examples/integration_tests/03_watch_engine_drift --once
python -m intract engine suggest examples/integration_tests/03_watch_engine_drift
python -m intract engine drift examples/integration_tests/03_watch_engine_drift
python -m intract engine run examples/integration_tests/03_watch_engine_drift --json
```

Oczekiwane:

```text
watch_changes: 1+
engine_fragments: 1+
engine_suggestions: 1+
```

## Inne przykłady

- [`examples/python/`](../examples/python/)
- [`examples/typescript/`](../examples/typescript/)
- [`examples/csharp/`](../examples/csharp/)
- [`examples/configs/`](../examples/configs/)
