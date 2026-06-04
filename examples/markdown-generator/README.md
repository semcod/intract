# Markdown generator + Intract

Ten przykład pokazuje generator dokumentu Markdown, który ma wygenerować treść na zadany temat i utrzymać stały format:

- `# <temat>` jako H1,
- sekcje `## Cel`, `## Kontekst`, `## Kluczowe punkty`, `## Następne kroki`,
- czysty Markdown bez HTML,
- brak pobierania treści z sieci i brak zapisu plików.

Intract pilnuje tego na dwóch poziomach:

1. Manifest [`intract.yaml`](intract.yaml) opisuje kontrakt projektu: generator ma dostać `topic`, zwrócić `markdown_document`, nie używać `network/write` i wymagać kroków `transform.topic`, `build.markdown_outline`, `render.markdown_section`, `validate.markdown_contract`.
2. Kod w [`pass/generator.py`](pass/generator.py) ma inline kontrakty `@intract.v1` oraz funkcję `guard_markdown_contract()`, która w runtime sprawdza temat w H1, wymagane nagłówki i brak HTML.

## Poprawna wersja

Najkrótsza ścieżka demo:

```bash
bash examples/markdown-generator/run-demo.sh
```

Skrypt wypisuje wygenerowany Markdown, wynik runtime guardu oraz statusy walidacji Intract dla wariantu `pass` i `violation`.

Ręczna walidacja poprawnego wariantu:

```bash
python -m intract validate examples/markdown-generator/pass \
  --manifest examples/markdown-generator/intract.yaml
```

Oczekiwane:

```text
Status: pass
```

Możesz też uruchomić sam generator:

```bash
python examples/markdown-generator/pass/generator.py
```

## Wersja naruszająca

[`violation/generator.py`](violation/generator.py) celowo łamie kontrakt:

- pobiera treść przez `requests.get(...)`,
- zapisuje `generated.md`,
- renderuje HTML zamiast Markdown,
- zmienia temat dokumentu na promocję.

```bash
python -m intract validate examples/markdown-generator/violation \
  --manifest examples/markdown-generator/intract.yaml
```

Oczekiwane:

```text
Status: violation
Declared forbid:network
Declared forbid:write
```

To jest celowo prosty przykład: Intract statycznie pilnuje obecności zakontraktowanych kroków, wejść/wyjść i zakazanych efektów, a domenowy strażnik `guard_markdown_contract()` pilnuje samego kształtu wygenerowanego Markdowna.
