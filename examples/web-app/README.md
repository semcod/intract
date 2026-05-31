# Web App Demo — Intract w praktyce

Przykład dla **rozwoju aplikacji webowych**: backend (Python), frontend (TypeScript), **OpenAPI**, **Dockerfile** i manifest `intract.yaml`. Pokazuje **dwie iteracje** tego samego produktu — zgodną z intencją (v1) i z regresją (v2).

## Architektura przykładu

```text
examples/web-app/
├── README.md                 ← ten plik
├── intract.yaml              ← manifest: ship.user_dashboard + require
├── run-demo.sh               ← generuje JSON do mock UI
├── mock/
│   ├── index.html            ← wizualny mock produktu + wyniki Intract
│   └── reports/              ← v1-pass.*.json, v2-violation.*.json
└── iterations/
    ├── v1-pass/              ← iteracja 1: release candidate
    │   ├── README.md
    │   ├── backend/
    │   ├── frontend/
    │   ├── openapi.yaml
    │   └── Dockerfile
    └── v2-violation/         ← iteracja 2: sieć + zły obraz → violation
        └── …
```

## Co robi paczka Intract (w tym demo)

| Warstwa | Plik | Mechanizm Intract |
|---------|------|-------------------|
| Backend | `backend/auth.py` | `@intract.v1` + `forbid:network` |
| Backend | `backend/routes.py` | kontrakt `api.read_profile` |
| Frontend | `frontend/dashboard.ts` | kontrakt `ui.render_dashboard` |
| API spec | `openapi.yaml` | `x-intract` na endpoincie |
| DevOps | `Dockerfile` | komentarz `@intract` + `scan --all-artifacts` |
| Projekt | `intract.yaml` | `require:` auth, api, deploy — **graf intencji** |

Reguły sprawdzane m.in.: obecność input/output, `return`, wykryte efekty (`requests`, `fetch`), polityka manifestu.

## Uruchomienie krok po kroku

### 1. Walidacja iteracji v1 ( funkcje OK )

```bash
python -m intract validate examples/web-app/iterations/v1-pass \
  --manifest examples/web-app/intract.yaml

python -m intract graph examples/web-app/iterations/v1-pass \
  --manifest examples/web-app/intract.yaml --format mermaid

python -m intract scan examples/web-app/iterations/v1-pass --all-artifacts
```

**Oczekiwane:** brak `violation` na funkcjach; graf bez `missing` dla `auth`, `api`, `deploy`.

### 2. Walidacja iteracji v2 (blokada release)

```bash
python -m intract validate examples/web-app/iterations/v2-violation \
  --manifest examples/web-app/intract.yaml

python -m intract validate examples/web-app/iterations/v2-violation \
  --manifest examples/web-app/intract.yaml --planfile
```

**Oczekiwane:** `violation` na `auth.check_permission` (requests) i `ui.render_dashboard` (fetch); opcjonalnie tickety w `.intract/`.

### 3. Mock UI (wizualizacja)

```bash
bash examples/web-app/run-demo.sh

cd examples/web-app
python -m http.server 8765
```

Otwórz: [http://localhost:8765/mock/index.html](http://localhost:8765/mock/index.html)

Przełącz **Iteration v1** / **v2**:

- **Lewy panel** — mock ekranu dashboardu (kolejna wersja aplikacji)
- **Prawy panel** — status Intract i kontrakty funkcji
- **Dół** — graf `ship.user_dashboard → require *`

## Iteracje jako „mock aplikacji”

| | v1-pass | v2-violation |
|---|---------|--------------|
| **Historia** | MVP zgodny z architekturą | Sprint: „szybkie” API auth + metryki z sieci |
| **auth.py** | lokalna logika RBAC | `requests.get(...)` |
| **dashboard.ts** | view model z danych | `fetch(...)` |
| **Dockerfile** | `3.12-slim`, `USER app` | `python:latest`, root |
| **Intract** | funkcje **pass** | **violation** → CI / pre-commit fail |

To model pracy: **kod wygląda jak działająca apka**, a Intract weryfikuje **zadeklarowaną intencję**, nie tylko składnię.

## Pre-commit / CI (web team)

```yaml
# fragment .github/workflows lub lokalnie
- run: |
    python -m intract validate examples/web-app/iterations/v1-pass \
      --manifest examples/web-app/intract.yaml
    python -m intract check . --staged --hunks
```

Composite action: [`action.yml`](../../action.yml) — [`docs/github-action.md`](../../docs/github-action.md).

## Powiązane przykłady

- [`../integration_tests/02_typescript_violation_planfile/`](../integration_tests/02_typescript_violation_planfile/) — sam TypeScript + planfile
- [`../full-stack/`](../full-stack/) — duplikaty intencji w pipeline
- [`../README.md`](../README.md) — indeks wszystkich examples

## Rozszerzenia

- Dodaj `.github/workflows/ci.yml` z kontraktem na workflow (artifact validator).
- Podłącz `intract planfile sync` po `--planfile` w v2.
- Użyj `intract watch` podczas lokalnego dev serwera frontendu.
