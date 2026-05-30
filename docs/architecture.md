# Architecture

Intract składa się z kilku warstw.

## Core

Pliki:

- [`src/intract/models.py`](../src/intract/models.py)
- [`src/intract/parser.py`](../src/intract/parser.py)
- [`src/intract/signature.py`](../src/intract/signature.py)
- [`src/intract/validation.py`](../src/intract/validation.py)
- [`src/intract/normalizer.py`](../src/intract/normalizer.py)

Odpowiedzialności:

```text
contract line / manifest
  -> Contract
  -> ContractRecord
  -> ContractSignature
  -> ValidationResult
```

## CLI

Plik:

- [`src/intract/cli.py`](../src/intract/cli.py)

Komendy:

```text
scan
validate
check
check-manifest
coverage
duplicates
graph
watch
tickets
artifact
engine
```

## Watch

Plik:

- [`src/intract/watch.py`](../src/intract/watch.py)

Działa przez polling i hash plików.

```text
snapshot A
  -> zmiana pliku
snapshot B
  -> diff snapshots
  -> validate
```

## Engine

Folder:

- [`src/intract/engine/`](../src/intract/engine/)

Moduły:

```text
scanner.py    -> zbiera pliki źródłowe
analyzer.py   -> wykrywa fragmenty logiczne
assigner.py   -> sugeruje kontrakty
drift.py      -> wykrywa zmianę logiki
monitor.py    -> scala scan/suggest/drift/validate
```

## Plugins

Folder:

- [`src/intract/plugins/`](../src/intract/plugins/)

Typy pluginów:

```text
ParserPlugin
ValidatorPlugin
ReporterPlugin
IntegrationPlugin
```

## Integrations

Folder:

- [`src/intract/integrations/`](../src/intract/integrations/)

Obecnie:

```text
planfile-compatible ticket export
```

## Reporters

Folder:

- [`src/intract/reporters/`](../src/intract/reporters/)

Obecnie:

```text
SARIF
JSON przez CLI
```

## Artifact validators

Plik:

- [`src/intract/artifacts.py`](../src/intract/artifacts.py)

Obsługuje:

```text
OpenAPI x-intract
Dockerfile
GitHub Actions
Kubernetes YAML
```
