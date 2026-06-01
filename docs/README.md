# Intract Docs

Dokumentacja projektu **Intract** — warstwy kontraktów intencji dla kodu, endpointów, artefaktów DevOps i CI/CD.

## Start

- [Getting Started](getting-started.md) — instalacja, pierwsze uruchomienie, podstawowy workflow.
- [Contract Format](contract-format.md) — format jednej linijki `@intract.v1`.
- [Manifest: `intract.yaml`](manifest.md) — kontrakty wielu plików, relacje `require`, graf intencji.
- [Commands Reference](commands.md) — pełna lista komend CLI.
- [Examples Guide](examples.md) — opis przykładów testowych i jak je uruchomić.
- [SUMD Descriptor](../SUMD.md) — metadata projektu, workflow, quality pipeline (`pyqual.yaml`), env i release.

## Główne obszary

- [Architecture](architecture.md) — jak działa core, pluginy, engine, walidatory i raporty.
- [Validation Model](validation.md) — statusy, reguły, `fail_on`, `warn_on`, policy.
- [Watch & Engine](watch-engine.md) — `intract watch`, drift, auto-suggest kontraktów.
- [Integrations](integrations.md) — pre-commit, GitHub Actions, Docker, OpenAPI, planfile, vallm, reDUP.
- [Plugins](plugins.md) — system pluginów i SDK.
- [Roadmap](roadmap.md) — co dalej rozwijać.

## Istotne miejsca w projekcie

- [`src/intract/`](../src/intract/) — kod źródłowy paczki.
- [`src/intract/engine/`](../src/intract/engine/) — analiza codebase, sugestie kontraktów, drift.
- [`src/intract/plugins/`](../src/intract/plugins/) — plugin registry i wbudowane pluginy.
- [`src/intract/integrations/`](../src/intract/integrations/) — integracje, m.in. planfile-compatible export.
- [`src/intract/reporters/`](../src/intract/reporters/) — raporty, m.in. SARIF.
- [`examples/integration_tests/`](../examples/integration_tests/) — 3 gotowe przykłady testowe.
- [`templates/`](../templates/) — gotowe konfiguracje do nowych projektów.
- [`sdks/`](../sdks/) — SDK/template’y dla różnych języków.
- [`schemas/intract.schema.json`](../schemas/intract.schema.json) — JSON Schema manifestu.
