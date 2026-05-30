# Missing files / project completeness checklist

This release adds the main operational files:

- `src/intract/config.py`
- `src/intract/policy.py` (+ `missing_required_p1`, `invalid_manifest` gates)
- `src/intract/git.py`
- `src/intract/coverage.py`
- `src/intract/duplicates/`
- `src/intract/graph.py`
- `src/intract/validators/registry.py`
- `src/intract/reporters/sarif.py`
- `schemas/intract.schema.json`
- `.pre-commit-hooks.yaml` (`check --staged --hunks`)
- `.github/workflows/intract.yml` (+ `full-stack-integration` job)
- `scripts/ci-full-stack.sh`
- `examples/full-stack/`
- `Dockerfile`

Integrations (sibling repos):

- reDUP: `--intent`, MCP params, Markdown/TOON intent metadata
- vallm: `--intract`, MCP tools, CLI `vallm intract`

Still missing for future releases:

- Intract MCP server (standalone)
- AST/tree-sitter analyzers for Python/TS/C#
- `intract scan . --all-artifacts`
- GitHub Action marketplace package
- real planfile API adapter, not only file export
- VS Code extension
- pyqual stage `intract_contracts`
