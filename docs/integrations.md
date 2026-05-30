# Integrations

## planfile

Intract generuje planfile-compatible tickety.

Komendy:

```bash
python -m intract tickets .
python -m intract validate . --planfile
python -m intract watch . --planfile
python -m intract engine run . --planfile
```

Pliki:

```text
.intract/planfile-tickets.yaml
.intract/planfile-tickets.json
.intract/TODO.intract.md
```

Kod:

- [`src/intract/integrations/planfile.py`](../src/intract/integrations/planfile.py)

## pre-commit

Plik:

- [`.pre-commit-hooks.yaml`](../.pre-commit-hooks.yaml)

Użycie w projekcie:

```yaml
repos:
  - repo: local
    hooks:
      - id: intract
        name: intract intent contracts
        entry: intract check --staged
        language: system
        pass_filenames: false
```

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

Docelowa integracja:

```bash
vallm validate --enable-intract
vallm intract --staged
```

Intract ma odpowiadać na pytanie:

```text
czy kod realizuje zadeklarowaną intencję?
```

## reDUP

Docelowa integracja:

```bash
redup scan . --intent
```

Intract ma dostarczać sygnatury kontraktów do wykrywania duplikacji intencji.
