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

## 0.7.x — lepsza analiza języków

Zrobione (MVP):

- Python AST (`analyzers/python_ast.py`)
- TypeScript/JavaScript block mapping (`analyzers/typescript.py`)
- C# block mapping (`analyzers/csharp.py`)
- opcjonalny tree-sitter (`pip install intract[treesitter]`)

Do zrobienia:

- Java / Go / Rust adaptery,
- pełna integracja tree-sitter w engine drift.

## 0.8.x — AST / tree-sitter

Do zrobienia:

- Python AST analyzer,
- JS/TS tree-sitter analyzer,
- C# / Java / Go / Rust adaptery,
- dokładniejsze mapowanie kontraktów do fragmentów.

## 0.9.x — ecosystem

Zrobione (MVP):

- GitHub Action [`action.yml`](../action.yml)
- VS Code extension [`extensions/vscode-intract/`](../extensions/vscode-intract/)
- Planfile HTTP adapter (`planfile push|pull|sync`)

Do zrobienia:

- publikacja VS Code extension w Marketplace,
- publikacja GitHub Action w Marketplace,
- pełny planfile API (webhooks, status sync).

## 1.0.0 — stable spec

Warunki:

- stabilny format `@intract.v1`,
- stabilny `intract.yaml`,
- pełna dokumentacja,
- schemat JSON,
- CI/pre-commit/SARIF,
- plugin API,
- examples działające jako testy integracyjne.
