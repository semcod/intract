# Intract

## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.5.14-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$4.75-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-15.4h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $4.7470 (22 commits)
- 👤 **Human dev:** ~$1537 (15.4h @ $100/h, 30min dedup)

Generated on 2026-07-06 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

**Intract** is an intent-contract layer for codebases and software delivery artifacts.

It lets you describe, validate and monitor intent across:

```text
code
functions
classes
files
project manifests
API endpoints
Dockerfiles
CI/CD workflows
Kubernetes manifests
DevOps artifacts
```

Intract is not primarily a programming language. It is a **contract system** for short, portable intent declarations.

## Quick example

```python
# Comment form (all supported languages)
# @intract.v1 scope:function intent:validate:user_permission priority:1 domain:security input:user,resource output:allowed effect:none forbid:write,network validate:input_presence,return_value,no_forbidden_effect meaning:"check whether user can modify resource without changing state"
def can_update_resource(user, resource):
    return user.is_admin or resource.owner_id == user.id
```

Decorator form (same contract model, no comment prefix):

```rust
@intract.v1 id:safe-decoder scope:function intent:decode:header domain:security forbid:unsafe
pub fn decode_header(raw_data: &[u8]) -> Header {
    // ...
}
```

Rust attributes are also accepted: `#[intract.v1 id:safe-decoder intent:decode:header forbid:unsafe]`.

Run:

```bash
python -m intract scan .
python -m intract validate .
```

## Practical usage (small and large projects)

Poniżej gotowe wzorce użycia, które możesz pokazać zespołowi jako „jak to działa w praktyce”.

### 1) Mały projekt (1 repo, 1-3 usług)

Cel: szybko pilnować intencji funkcji i nie spowalniać developmentu.

Przykładowe technologie:

- Python API (`@intract.v1` nad funkcjami serwisowymi)
- TypeScript frontend (kontrakty `ui.*`, `validate.*`)
- Dockerfile (kontrakty deploy, np. `forbid:root_user`)

Workflow:

```bash
# lokalnie podczas developmentu
python -m intract validate .
python -m intract check --staged --hunks

# szybki podgląd pokrycia i duplikatów intencji
python -m intract coverage .
python -m intract duplicates . --threshold 0.8
```

### 2) Duży projekt (monorepo, wiele zespołów)

Cel: rozdzielić intencje na domeny i mieć osobne bramki jakości.

Przykładowe technologie w 1 monorepo:

- Backend: Python + Java + Go
- Frontend: TypeScript
- Platforma: Dockerfile, Kubernetes, GitHub Actions/OpenAPI

Workflow:

```bash
# pełna walidacja release branch
python -m intract validate . --manifest intract.yaml

# raport do security/code scanning
python -m intract check . --format sarif --output intract.sarif

# graf zależności intencji i braków require
python -m intract graph . --format mermaid
```

## Fokus na kategorie intencji (dev vs CI/CD)

Najpraktyczniej mieć osobne manifesty lub sekcje dla różnych etapów pracy:

- `intract.dev.yaml` → fokus na poprawność funkcji (`domain:app`, `domain:logic`)
- `intract.ci.security.yaml` → fokus na bezpieczeństwo (`domain:security`, `forbid:network/write/unsafe`)

Przykład uruchamiania:

```bash
# development: sprawdzamy głównie intencje funkcji
python -m intract validate . --manifest intract.dev.yaml

# CI/CD: sprawdzamy głównie bezpieczeństwo i artefakty dostarczeniowe
python -m intract validate . --manifest intract.ci.security.yaml
python -m intract scan . --all-artifacts --json
```

W praktyce daje to możliwość „przełączania radaru”:

- dev: czy funkcja robi to, co obiecuje (`intent`, `input/output`, `return`)
- CI/CD: czy release spełnia polityki bezpieczeństwa (network, secrets, root, workflow)

## Automatyczne generowanie intencji

Intract wspiera generowanie kontraktów automatycznie (LLM i engine):

```bash
# 1) propozycje kontraktów z konkretnego pliku (LLM)
python -m intract propose llm --file src/auth.py --goal "RBAC without network side effects"

# 2) sugestie engine dla projektu
python -m intract engine suggest .

# 3) walidacja po zaakceptowaniu propozycji
python -m intract validate .
```

Wskazówka: zacznij od małej liczby kontraktów (kluczowe funkcje), potem rozszerzaj obszary.

## Greenfield demo: NLP -> Intract -> Code

Poniższy scenariusz pokazuje start od zera dla nowej aplikacji.

### Krok 1: Nowy projekt

```bash
mkdir my-app && cd my-app
python -m venv .venv
source .venv/bin/activate
pip install intract
python -m intract init .
```

### Krok 2: Opis celu językiem naturalnym (NLP)

Przykład celu:

> "Zbuduj API do zarządzania zadaniami. Endpoint create-task ma walidować input, nie może robić zewnętrznych wywołań sieciowych i ma zwracać jawny status."

### Krok 3: Wygeneruj kontrakty z NLP na kod

Tworzysz szkic pliku (`src/tasks.py`) i prosisz Intract/LLM o propozycje:

```bash
python -m intract propose llm --file src/tasks.py --goal "task API: validate input, no network, explicit status"
```

Wynik to linie `@intract.v1 ...`, które możesz wkleić nad funkcje lub przenieść do manifestu Toon/YAML.

### Krok 4: Implementuj kod pod kontrakty

Implementujesz funkcje zgodnie z intencją, np.:

- `intent:create:task`
- `forbid:network`
- `validate:input_presence,return_value`

### Krok 5: Pętla deweloperska i CI

```bash
# lokalnie
python -m intract check --staged --hunks

# w CI
python -m intract validate .
python -m intract check . --format sarif --output intract.sarif
```

Efekt: flow przechodzi od wymagań NLP, przez kontrakty intencji, do kodu i automatycznej walidacji jakości.

## External Target Addressing (Toon Manifests)

In addition to inline annotations, Intract supports **two ways** of defining quality gates and intent contracts:

1. **Inline Comments**: Using `@intract.v1` in source files (with `#`, `//`, `--`, or HTML comment prefixes).
2. **Inline Decorators**: Bare `@intract.v1 ...` lines or Rust `#[intract.v1 ...]` attributes on the line above the governed block.
3. **External manifests (Toon Manifests)**: Decoupled files (`.toon` or `intract.toon.yaml`) that specify precise coordinates (targets) for files, functions, lines, and XPaths.

### 1. Płaski format URI linia po linii (`.toon`)

Pliki `.toon` używają struktury URI do prostego i przejrzystego przypisywania kontraktów na poziomie konkretnych linii, funkcji lub selektorów:

```text
# Flat target-based URI rules
intract://src/calc.py?func=add#id=pure-addition&intent=pure-add&forbid=write
intract://src/calc.py?func=write_to_log&line=13#id=log-write&intent=write-log&require=write
```

### 2. Manifest YAML z targetowaniem (`intract.toon.yaml`)

Możesz również zdefiniować zasady w formacie YAML, podając sekcję `target`:

```yaml
version: intract.v1
contracts:
  - id: addition-check
    intent: pure:addition
    forbid: [write]
    target:
      file: src/calc.py
      function: add
```

Więcej informacji i pełne przykłady znajdziesz w katalogu [`examples/toon/`](examples/toon/).

## Documentation

Start here:

- [Docs index](docs/README.md)
- [Getting Started](docs/getting-started.md)
- [Commands Reference](docs/commands.md)
- [Contract Format](docs/contract-format.md)
- [Manifest `intract.yaml`](docs/manifest.md)
- [Architecture](docs/architecture.md)
- [Validation Model](docs/validation.md)
- [Watch & Engine](docs/watch-engine.md)
- [Plugins](docs/plugins.md)
- [Integrations](docs/integrations.md)
- [Roadmap](docs/roadmap.md)
- [SUMD Descriptor](SUMD.md)

## SUMD-based operational view

Dokument `SUMD.md` jest źródłem opisu operacyjnego projektu (workflow, pipeline jakości, interfejsy, env).

Architecture flow:

```text
SUMD (description) -> DOQL/source (code) -> taskfile (automation) -> testql (verification)
```

Interfaces:

- CLI entry points: `intract`, `intract-mcp`
- testql scenarios: `testql-scenarios/generated-cli-tests.testql.toon.yaml`

Quality pipeline (`pyqual.yaml`) — najważniejsze etapy:

- `test` (`python -m pytest -q --tb=short`)
- `intract_contracts` (`validate`, `check`, `duplicates` na `examples/full-stack`)
- `intract_artifacts` (`scan --all-artifacts --json` do `.pyqual/artifacts.json`)
- `intract_web_app` (`validate` i `scan` dla `examples/web-app/iterations/v1-pass` + `run-demo.sh`)
- `intract_demo_ci` (`bash scripts/ci-full-stack.sh`)

Environment variables (`.env.example`) używane w automatyzacji:

- `OPENROUTER_API_KEY`
- `LLM_MODEL`
- `PFIX_AUTO_APPLY`, `PFIX_AUTO_INSTALL_DEPS`, `PFIX_AUTO_RESTART`
- `PFIX_MAX_RETRIES`, `PFIX_DRY_RUN`, `PFIX_ENABLED`
- `PFIX_GIT_COMMIT`, `PFIX_GIT_PREFIX`, `PFIX_CREATE_BACKUPS`

Release and build references:

- `goal.yaml` (semver, conventional commits, changelog)
- `Makefile` targets: `install`, `test`, `lint`, `format`
- analysis artifacts: `project/map.toon.yaml`, `project/context.md`, `project/prompt.txt`

## Important project locations

Core:

- [`src/intract/`](src/intract/)
- [`src/intract/models.py`](src/intract/models.py)
- [`src/intract/parser.py`](src/intract/parser.py)
- [`src/intract/signature.py`](src/intract/signature.py)
- [`src/intract/validation.py`](src/intract/validation.py)

Operational modules:

- [`src/intract/cli.py`](src/intract/cli.py)
- [`src/intract/config.py`](src/intract/config.py)
- [`src/intract/policy.py`](src/intract/policy.py)
- [`src/intract/git.py`](src/intract/git.py)
- [`src/intract/watch.py`](src/intract/watch.py)

Analysis engine:

- [`src/intract/engine/`](src/intract/engine/)
- [`src/intract/engine/scanner.py`](src/intract/engine/scanner.py)
- [`src/intract/engine/analyzer.py`](src/intract/engine/analyzer.py)
- [`src/intract/engine/assigner.py`](src/intract/engine/assigner.py)
- [`src/intract/engine/drift.py`](src/intract/engine/drift.py)
- [`src/intract/engine/monitor.py`](src/intract/engine/monitor.py)

Plugins and integrations:

- [`src/intract/plugins/`](src/intract/plugins/)
- [`src/intract/integrations/`](src/intract/integrations/)
- [`src/intract/integrations/planfile.py`](src/intract/integrations/planfile.py)
- [`src/intract/artifacts.py`](src/intract/artifacts.py)
- [`src/intract/reporters/sarif.py`](src/intract/reporters/sarif.py)

Schemas and templates:

- [`schemas/intract.schema.json`](schemas/intract.schema.json)
- [`templates/`](templates/)
- [`templates/intract.yaml`](templates/intract.yaml)
- [`templates/pyproject-intract.toml`](templates/pyproject-intract.toml)
- [`templates/openapi.intract.yaml`](templates/openapi.intract.yaml)
- [`templates/Dockerfile.intract`](templates/Dockerfile.intract)

Examples:

- [`examples/README.md`](examples/README.md) — indeks wszystkich przykładów
- [`examples/web-app/`](examples/web-app/) — **aplikacja webowa**: iteracje v1/v2 + mock UI
- [`examples/full-stack/`](examples/full-stack/) — graf, duplikaty intencji
- [`examples/integration_tests/`](examples/integration_tests/)

SDKs:

- [`sdks/python/`](sdks/python/)
- [`sdks/typescript/`](sdks/typescript/)
- [`sdks/go/`](sdks/go/)
- [`sdks/rust/`](sdks/rust/)
- [`sdks/java/`](sdks/java/)
- [`sdks/csharp/`](sdks/csharp/)

CI / packaging:

- [`.pre-commit-hooks.yaml`](.pre-commit-hooks.yaml)
- [`.github/workflows/intract.yml`](.github/workflows/intract.yml)
- [`Dockerfile`](Dockerfile)
- [`pyproject.toml`](pyproject.toml)

## Installation

```bash
pip install -e .[dev]
```

## Main commands

```bash
python -m intract scan .
python -m intract validate .
python -m intract check .
python -m intract check --staged
python -m intract check --changed --base main
python -m intract check . --format sarif --output intract.sarif
python -m intract check-manifest intract.yaml
python -m intract coverage .
python -m intract duplicates .
python -m intract graph . --format mermaid
python -m intract watch .
python -m intract tickets .
python -m intract artifact Dockerfile
python -m intract artifact openapi.yaml
python -m intract engine suggest .
python -m intract engine drift .
python -m intract engine run .
```

## Run examples

```bash
python examples/integration_tests/run_examples.py
```

Expected:

```text
example_01: pass
example_02: violation + planfile-compatible ticket
example_03: watch/engine/drift works
```

## Project manifest

Generate:

```bash
python -m intract init .
```

Validate:

```bash
python -m intract check-manifest intract.yaml
python -m intract validate . --manifest intract.yaml
```

## Pre-commit

Example `.pre-commit-config.yaml`:

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

## SARIF / GitHub Code Scanning

```bash
python -m intract check . --format sarif --output intract.sarif
```

GitHub workflow:

- [`.github/workflows/intract.yml`](.github/workflows/intract.yml)

## License

Licensed under Apache-2.0.
