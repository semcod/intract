# Missing files / project completeness checklist

Operational files:

- core validation, policy, git, graph, duplicates, MCP server
- `scripts/ci-full-stack.sh`, `pyqual.yaml`, `action.yml`
- `examples/full-stack/`, language analyzers under `src/intract/analyzers/`
- VS Code extension under `extensions/vscode-intract/`
- planfile HTTP adapter in `integrations/planfile_adapter.py`

Integrations (sibling repos):

- reDUP: `--intent`, MCP params, Markdown/TOON intent metadata
- vallm: `--intract`, MCP tools, CLI `vallm intract`

Still missing for future releases:

- Marketplace publication (GitHub Action + VS Code)
- Java / Go / Rust language adapters
- planfile webhooks and bidirectional status sync
- artifact plugins split into separate packages
