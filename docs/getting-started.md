# Getting Started

## Instalacja lokalna

Z katalogu projektu:

```bash
pip install -e .[dev]
```

Sprawdź CLI:

```bash
python -m intract --version
python -m intract --help
```

## Pierwszy kontrakt

Dodaj kontrakt nad funkcją:

```python
# @intract.v1 scope:function intent:parse:extensions priority:2 domain:cli input:raw_extensions output:extension_list effect:none forbid:network,write validate:input_presence,output_presence,return_value,no_forbidden_effect meaning:"parse raw extension string into normalized extension list"
def parse_extensions(raw_extensions: str) -> list[str]:
    extension_list = [x.strip().lower() for x in raw_extensions.split(",") if x.strip()]
    return extension_list
```

Uruchom:

```bash
python -m intract scan .
python -m intract validate .
```

## Nowy projekt

Wygeneruj manifest:

```bash
python -m intract init .
```

Powstanie:

```text
intract.yaml
```

Możesz też skopiować gotowe template’y:

- [`templates/intract.yaml`](../templates/intract.yaml)
- [`templates/pyproject-intract.toml`](../templates/pyproject-intract.toml)
- [`templates/.pre-commit-config.yaml`](../templates/.pre-commit-config.yaml)
- [`templates/.github/workflows/intract.yml`](../templates/.github/workflows/intract.yml)

## Najczęstszy workflow

```bash
python -m intract scan .
python -m intract validate .
python -m intract coverage .
python -m intract duplicates .
python -m intract graph . --format mermaid
```

## Workflow developerski w czasie rzeczywistym

```bash
python -m intract watch .
```

Z ticketami:

```bash
python -m intract watch . --planfile
```
