# Intract


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.5.6-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$2.06-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-5.4h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $2.0621 (7 commits)
- 👤 **Human dev:** ~$539 (5.4h @ $100/h, 30min dedup)

Generated on 2026-05-31 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

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
# @intract.v1 scope:function intent:validate:user_permission priority:1 domain:security input:user,resource output:allowed effect:none forbid:write,network validate:input_presence,return_value,no_forbidden_effect meaning:"check whether user can modify resource without changing state"
def can_update_resource(user, resource):
    return user.is_admin or resource.owner_id == user.id
```

Run:

```bash
python -m intract scan .
python -m intract validate .
```

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
