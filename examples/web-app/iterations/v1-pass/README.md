# Iteration v1 — contracts PASS

Mock aplikacji webowej **zgodnej z kontraktami intencji**.

## Co tu jest

| Plik | Intent | Opis |
|------|--------|------|
| `backend/auth.py` | `auth.check_permission` | Lokalna logika RBAC, bez sieci |
| `backend/routes.py` | `api.read_profile` | Profil z pamięci, bez HTTP |
| `frontend/dashboard.ts` | `ui.render_dashboard` | View model UI bez `fetch` |
| `openapi.yaml` | `api.read_profile` | Kontrakt endpointu (x-intract) |
| `Dockerfile` | `deploy.container_image` | Non-root, pinned tag |

## Walidacja

Z katalogu repozytorium:

```bash
python -m intract validate examples/web-app/iterations/v1-pass \
  --manifest examples/web-app/intract.yaml

python -m intract graph examples/web-app/iterations/v1-pass \
  --manifest examples/web-app/intract.yaml --format mermaid

python -m intract scan examples/web-app/iterations/v1-pass --all-artifacts
```

Oczekiwane: **status pass**, graf bez `missing`, artefakty bez violation.

## W mock UI

Otwórz [`../../mock/index.html`](../../mock/index.html) i wybierz **Iteration v1 (pass)**.
