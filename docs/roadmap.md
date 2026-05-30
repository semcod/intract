# Roadmap

## 0.5.x — aktualny etap

Zrobione:

- `check --staged` + `--hunks`
- manifest schema validation
- OpenAPI x-intract parser
- Dockerfile / GitHub Actions / Kubernetes validators
- SARIF reporter
- coverage, duplicates, graph, watch, engine
- planfile-compatible export
- integrations: reDUP `--intent`, vallm `--intract`
- rule registry z raportem per reguła
- demo `examples/full-stack/`
- CI script `scripts/ci-full-stack.sh`
- MCP: vallm (`validate_intent_contracts`, `validate_intract_project`, `validate_intract_staged`), reDUP intent params

## 0.6.x — stabilizacja staged/hunk validation

Do zrobienia:

- ostrzejsze policy dla P1/P2 (`missing_required_p1` — częściowo),
- pełna obsługa `fail_on` / `warn_on` w vallm/redup,
- AST mapowanie hunk → kontrakt (Python).

## 0.7.x — pluginy artefaktów

Do zrobienia:

- wydzielenie `artifacts.py` do pluginów:
  - `intract-openapi`
  - `intract-docker`
  - `intract-kubernetes`
  - `intract-github-actions`
- plugin discovery przez entry points,
- testy pluginów.

## 0.8.x — AST / tree-sitter

Do zrobienia:

- Python AST analyzer,
- JS/TS tree-sitter analyzer,
- C# / Java / Go / Rust adaptery,
- dokładniejsze mapowanie kontraktów do fragmentów.

## 0.9.x — ecosystem

Do zrobienia:

- prawdziwy planfile API adapter,
- vallm validator,
- reDUP detector,
- MCP server,
- VS Code extension,
- GitHub Action marketplace.

## 1.0.0 — stable spec

Warunki:

- stabilny format `@intract.v1`,
- stabilny `intract.yaml`,
- pełna dokumentacja,
- schemat JSON,
- CI/pre-commit/SARIF,
- plugin API,
- examples działające jako testy integracyjne.
