# Examples — Intract

Katalog `examples/` pokazuje jak używać paczki **intract** w realistycznych scenariuszach.

## Mapa przykładów

| Folder | Dla kogo | Co pokazuje |
|--------|----------|-------------|
| [`web-app/`](web-app/) | **Aplikacje webowe** | Dwie iteracji produktu (pass vs violation), mock UI, OpenAPI, Dockerfile |
| [`full-stack/`](full-stack/) | Pipeline / analiza | Manifest `require`, duplikaty intencji, graf |
| [`integration_tests/`](integration_tests/) | CI / QA | 3 automatyczne scenariusze (`run_examples.py`) |
| [`python/`](python/) | Pojedynczy kontrakt | Minimalny `@intract.v1` w Pythonie |
| [`typescript/`](typescript/) | Frontend / API | TypeScript + `forbid:network` |
| [`csharp/`](csharp/) | .NET | Kontrakt na metodzie C# |
| [`configs/`](configs/) | Konfiguracja | Przykładowy `intent.yaml` |

## Szybki start

```bash
pip install -e .

# Demo web (mock + walidacja)
bash examples/web-app/run-demo.sh
python -m http.server 8765 --directory examples/web-app
# → http://localhost:8765/mock/index.html

# Integracje
python examples/integration_tests/run_examples.py

# Full-stack
python -m intract validate examples/full-stack --manifest examples/full-stack/intract.yaml
```

## Struktura (konwencja)

Każdy większy przykład ma:

```text
examples/<name>/
  README.md          ← jak uruchomić, co oczekiwać
  intract.yaml       ← manifest projektu (opcjonalnie)
  …                  ← kod, artefakty, mock
```

Przykład **web-app** rozszerza to o `iterations/<v1|v2>/` — symulacja kolejnych sprintów.

## Powiązanie z komendami CLI

| Komenda | Przykład |
|---------|----------|
| `intract validate` | `web-app/iterations/v1-pass` |
| `intract graph` | `full-stack`, `web-app` |
| `intract scan --all-artifacts` | `web-app` (OpenAPI + Dockerfile) |
| `intract check --staged --hunks` | `full-stack/README.md` |
| `intract planfile push` | `integration_tests/02_*` |
| `intract duplicates` | `full-stack` |

Więcej: [docs/commands.md](../docs/commands.md), [docs/examples.md](../docs/examples.md).
