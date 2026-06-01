# Toon — Zewnętrzne adresowanie kontraktów Intract

Przykład ten demonstruje działanie systemu **Intract** w dwóch niezależnych trybach:
1. **Inline (bezpośrednio w kodzie)**: Poprzez adnotacje `@intract.v1` bezpośrednio nad funkcjami w plikach źródłowych.
2. **External (zewnętrzne pliki manifestu)**: Za pomocą precyzyjnego adresowania (targets) w plikach `.toon` oraz `.toon.yaml`, bez modyfikacji plików źródłowych.

---

## 1. Dwa sposoby adresowania

### Tryb A: Inline (w kodzie)
Adnotacja `@intract.v1` znajduje się bezpośrednio przed kodem, którego dotyczy.
*Przykład w `examples/python/parse_extensions.py`:*
```python
# @intract.v1 scope:function intent:parse:extensions priority:2 forbid:network
def parse_extensions(raw_extensions: str):
    ...
```

### Tryb B: Zewnętrzny manifest (`.toon` lub `intract.toon.yaml`)
Kontrakty są całkowicie oddzielone od kodu źródłowego i zdefiniowane w dedykowanych plikach, mapując zasady za pomocą koordynatów docelowych (target):
*   **Plik docelowy** (`file`)
*   **Nazwa funkcji** (`func` / `function`)
*   **Numer linii** (`line`)
*   **Wyrażenie XPath/XPatch** (`xpath` / `xpatch` dla plików HTML/DOM)

---

## 2. Nowy format URI linia po linii (`.toon`)

Plik `.toon` to płaski plik tekstowy, w którym każda linia reprezentuje pojedynczy kontrakt zaadresowany za pomocą standardu URI:

```text
intract://<file_path>?func=<function_name>&line=<line_number>&xpath=<xpath_expression>#id=<contract_id>&intent=<action-object>&forbid=<forbidden_effects>
```

### Przykład w `examples/toon/intract.toon`:
```text
# Płaskie adresowanie linia po linii dla calc.py, index.html oraz auth.js
intract://src/calc.py?func=add#id=pure-addition&intent=pure-add&forbid=write
intract://src/calc.py?func=write_to_log&line=13#id=log-write&intent=write-log&req=write
intract://src/index.html?xpath=//button[@id="btn-add"]#id=dom-button-check&intent=click-btn&req=auth
intract://src/auth.js?func=login#id=auth-login&intent=perform-login&forbid=network
```

---

## 3. Struktura folderu przykładowego

```text
examples/toon/
  ├── README.md               # Ta dokumentacja
  ├── Makefile                # Skróty komend (make validate, make validate-uri...)
  ├── validate.sh             # Skrypt uruchamiający automatyczną walidację
  ├── intract.toon            # Płaski manifest URI
  ├── intract.toon.yaml       # Manifest YAML z sekcją target (100% odpowiednik intract.toon)
  └── src/
      ├── calc.py             # Kod kalkulatora (Python)
      ├── auth.js             # Moduł uwierzytelniania (JavaScript)
      └── index.html          # Plik HTML z przyciskami (DOM / XPath)
```

---

## 4. Walidacja projektu przy użyciu Toon

### Sposób 1: Automatyczny skrypt (Makefile)
Możesz uruchomić pełną walidację obu manifestów za pomocą jednego polecenia:

```bash
# Walidacja obu formatów manifestu
make validate
```

### Sposób 2: Uruchomienie dedykowanych celów Makefile

*   Walidacja **tylko** za pomocą płaskiego pliku manifestu `.toon` (URI):
    ```bash
    make validate-uri
    ```
*   Walidacja **tylko** za pomocą pliku manifestu YAML z targetami:
    ```bash
    make validate-yaml
    ```

### Sposób 3: Ręczne komendy CLI

```bash
# Ręczna walidacja za pomocą płaskiego pliku .toon
python -m intract validate examples/toon --manifest examples/toon/intract.toon

# Ręczna walidacja za pomocą toon.yaml
python -m intract validate examples/toon --manifest examples/toon/intract.toon.yaml
```

