# Iteration v2 — contracts VIOLATION (następny sprint)

Ta iteracja symuluje **kolejny krok produktu**: developer dodał wywołania sieciowe i „szybki” Dockerfile. Intract blokuje release zanim mock trafi na produkcję.

## Różnice względem v1

| Plik | Problem | Reguła |
|------|---------|--------|
| `backend/auth.py` | `requests.get(...)` | `forbid:network` |
| `frontend/dashboard.ts` | `fetch(...)` | `forbid:network` |
| `Dockerfile` | `python:latest`, brak `USER` | artefakt: latest_tag, root_user |

## Walidacja

```bash
python -m intract validate examples/web-app/iterations/v2-violation \
  --manifest examples/web-app/intract.yaml

python -m intract validate examples/web-app/iterations/v2-violation \
  --manifest examples/web-app/intract.yaml --planfile

python -m intract scan examples/web-app/iterations/v2-violation --all-artifacts
```

Oczekiwane: **status violation**, tickety planfile, artefakty Dockerfile z violation.

## Naprawa → powrót do v1

Usuń sieć z `auth.py` / `dashboard.ts` i przywróć Dockerfile z v1 — walidacja wraca do **pass**.

## W mock UI

Otwórz [`../../mock/index.html`](../../mock/index.html) i wybierz **Iteration v2 (violation)**.
