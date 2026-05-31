# Integrations

## Monorepo CI (Intract + vallm + reDUP)

Local full-stack check:

```bash
bash scripts/ci-full-stack.sh
```

Installs sibling repos when present (`../vallm`, `../redup`) and runs:

```bash
intract validate examples/full-stack
intract duplicates examples/full-stack
vallm intract examples/full-stack
redup scan examples/full-stack --intent
```

GitHub Actions job `full-stack-integration` runs the intract-only subset by default. For full integration in CI, checkout sibling repos and unset `SKIP_VALLM` / `SKIP_REDUP`.

## planfile

Intract generuje planfile-compatible tickety i może synchronizować je z HTTP API.

Komendy:

```bash
python -m intract tickets .
python -m intract validate . --planfile
python -m intract planfile push . --url https://planfile.example/api
python -m intract planfile pull .
python -m intract planfile sync .
```

Zmienne środowiskowe: `PLANFILE_URL`, `PLANFILE_TOKEN`, `PLANFILE_PROJECT`, `PLANFILE_WEBHOOK_URL`, `PLANFILE_WEBHOOK_SECRET`.

Webhook:

```bash
intract planfile webhook-test --url https://hooks.example/intract
intract planfile webhook-apply . event.json
```

Outbound events: `tickets.exported`, `tickets.pushed`, `tickets.synced`. Inbound: `ticket.updated` / `tickets.updated` aktualizuje status w `.intract/planfile-tickets.json`.

Pliki:

```text
.intract/planfile-tickets.yaml
.intract/planfile-tickets.json
.intract/TODO.intract.md
```

Kod:

- [`src/intract/integrations/planfile.py`](../src/intract/integrations/planfile.py)
- [`src/intract/integrations/planfile_adapter.py`](../src/intract/integrations/planfile_adapter.py)

## GitHub Action (Marketplace-ready)

Composite action w repozytorium:

```yaml
- uses: semcod/intract@v0
  with:
    path: .
    manifest: intract.yaml
    staged: "false"
```

Plik: [`action.yml`](../action.yml)

## VS Code

Extension: [`extensions/vscode-intract/`](../extensions/vscode-intract/)

- podświetlanie `@intract.v1` w komentarzach
- komendy Validate Project / Check Staged

## pre-commit

Pliki:

- [`.pre-commit-hooks.yaml`](../.pre-commit-hooks.yaml)
- [`templates/.pre-commit-config.yaml`](../templates/.pre-commit-config.yaml)

Użycie w projekcie:

```yaml
repos:
  - repo: local
    hooks:
      - id: intract
        name: intract intent contracts
        entry: intract check --staged --hunks
        language: system
        pass_filenames: false
```

`--hunks` waliduje tylko kontrakty dotknięte staged diffem.

## GitHub Actions

Workflow:

- [`.github/workflows/intract.yml`](../.github/workflows/intract.yml)

Generuje SARIF:

```bash
python -m intract check . --format sarif --output intract.sarif
```

## Docker

Dockerfile:

- [`Dockerfile`](../Dockerfile)

Walidacja:

```bash
python -m intract artifact Dockerfile
```

## OpenAPI

Kontrakty w OpenAPI używają `x-intract`.

Przykład:

- [`templates/openapi.intract.yaml`](../templates/openapi.intract.yaml)

Walidacja:

```bash
python -m intract artifact openapi.yaml
```

## Kubernetes

Walidacja:

```bash
python -m intract artifact k8s/deployment.yaml
```

## vallm

Zainstalowanie:

```bash
pip install -e ../intract
pip install -e "../vallm[intract]"
```

CLI:

```bash
vallm validate --file app.py --intract
vallm batch src --recursive --intract
vallm intract .
vallm intract . --staged
vallm intract . --changed --base main
```

MCP tools (`mcp/server/_tools_vallm.py`):

- `validate_intent_contracts` — snippet z `@intract`
- `validate_intract_project` — walidacja projektu
- `validate_intract_staged` — staged check przed commitem

Adapter:

- [`src/intract/integrations/vallm.py`](../src/intract/integrations/vallm.py)

## reDUP

Zainstalowanie:

```bash
pip install -e ../intract
pip install -e "../redup[intent]"
```

CLI:

```bash
redup scan . --intent --intent-threshold 0.84
redup scan . --intent --intent-manifest intract.yaml
```

MCP scan params: `intent`, `intent_threshold`, `intent_manifest`.

Adapter:

- [`src/intract/integrations/redup.py`](../src/intract/integrations/redup.py)
- [`../redup/src/redup/integrations/intract/adapter.py`](../../redup/src/redup/integrations/intract/adapter.py)

Intent duplicate groups are tagged with `engine: intract` in JSON/Markdown/TOON reporters.

## Intract MCP server

Standalone JSON-RPC MCP server:

```bash
intract-mcp
# or
python -m intract.mcp.server
```

Tools: `validate_project`, `validate_staged`, `validate_intent_snippet`, `find_duplicates`, `build_graph`, `scan_artifacts`, `project_info`.

Kod: [`src/intract/mcp/`](../src/intract/mcp/)

## Policy gates

Domyślne `fail_on`:

```yaml
fail_on: ["violation", "invalid_manifest"]
```

Stopniowe zaostrzanie:

```yaml
fail_on: ["violation", "missing_required_p1", "invalid_manifest"]
```

`missing_required_p1` sprawdza brakujące `require` wymagane przez kontrakty manifestu z `priority: 1`.
