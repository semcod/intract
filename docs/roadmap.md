# Roadmap

## 0.5.x — aktualny etap

Zrobione:

- `check --staged`
- hunk parser
- manifest schema validation
- OpenAPI x-intract parser
- Dockerfile validator
- GitHub Actions validator
- Kubernetes validator
- SARIF reporter
- coverage
- duplicates
- graph
- watch
- engine
- planfile-compatible export

## 0.6.x — stabilizacja staged/hunk validation

Do zrobienia:

- mapowanie hunków na funkcje/metody/kontrakty,
- walidacja tylko dotkniętych fragmentów,
- ostrzejsze policy dla P1/P2,
- config `fail_on` / `warn_on` z pełną obsługą.

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
