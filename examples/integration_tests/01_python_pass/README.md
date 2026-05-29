# Example 01 — Python PASS

Ten przykład pokazuje prostą funkcję z kontraktem `Intract v1`, która powinna przejść walidację.

## Uruchomienie

Z katalogu głównego paczki:

```bash
python -m intract validate examples/integration_tests/01_python_pass --json
python -m intract scan examples/integration_tests/01_python_pass
python -m intract engine suggest examples/integration_tests/01_python_pass
```

## Oczekiwany wynik

- `validate`: `pass`
- `scan`: wykrywa 1 kontrakt
- `engine suggest`: wykrywa fragment logiczny i proponuje kontrakt
