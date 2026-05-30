# Missing files / project completeness checklist

This release adds the main missing operational files:

- `src/intract/config.py`
- `src/intract/policy.py`
- `src/intract/git.py`
- `src/intract/coverage.py`
- `src/intract/duplicates.py`
- `src/intract/graph.py`
- `src/intract/reporters/sarif.py`
- `schemas/intract.schema.json`
- `.pre-commit-hooks.yaml`
- `.github/workflows/intract.yml`
- `Dockerfile`

Still missing for future releases:

- full JSON Schema validation command
- true `check --staged` hunk-level validation
- AST/tree-sitter analyzers
- OpenAPI parser plugin
- Dockerfile validator plugin
- Kubernetes validator plugin
- GitHub Action marketplace package
- real planfile API adapter, not only file export
- VS Code extension
- MCP server
