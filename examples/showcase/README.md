# Interaktywny Showcase Intract (Dashboard)

Katalog ten zawiera w pełni interaktywną, przeglądarkową aplikację demonstracyjną, która w graficzny sposób wizualizuje działanie silnika **Intract**!

---

## Co zawiera dashboard?

1.  **Edytor kodu live:** Możesz na żywo edytować kod źródłowy (Python, JavaScript, HTML).
2.  **Szybki podgląd formatów:** Posiada zakładki z kodem źródłowym, płaskim plikiem manifestu `.toon` oraz plikiem `intract.toon.yaml`.
3.  **Symulator Intract Engine:** Analizuje kod na bieżąco i wyłapuje naruszenia (np. operacje wejścia/wyjścia mimo zakazu `forbid:write`, wywołania sieciowe mimo `forbid:network`, brak elementów autoryzacyjnych na przyciskach DOM w HTML).
4.  **Interaktywna konsola logów:** Wizualizuje statyczną analizę kodu i drzewa AST w czasie rzeczywistym.
5.  **Statusy walidacji (PASS/VIOLATION):** Pokazuje dokładnie gdzie i dlaczego kod narusza zasady intencji dewelopera.

---

## Jak to uruchomić?

Możesz w prosty sposób uruchomić serwer HTTP w tym katalogu, korzystając z Pythona:

```bash
# Uruchomienie lokalnego serwera na porcie 8086
python3 -m http.server 8086 --directory examples/showcase
```

Po uruchomieniu serwera, otwórz przeglądarkę i wejdź na adres:
👉 **[http://localhost:8086](http://localhost:8086)**

---

## Scenariusze do przetestowania:

### 1. Python — Naruszenie czystej funkcji
*   **Problem:** Kontrakt `pure-addition` zabrania zapisu na dysk (`forbid:write`), ale w kodzie kalkulatora funkcja `add()` próbuje pisać logi do pliku tekstowego `log.txt`.
*   **Jak naprawić?** Usuń/zakomentuj linie 5 i 6 w edytorze kodu źródłowego kalkulatora i kliknij **Uruchom Walidację**. Status kontraktu natychmiast zmieni się na zielony **PASS**!

### 2. HTML — Bezpieczeństwo DOM i autoryzacja
*   **Problem:** Kontrakt `dom-button-check` wymaga, aby krytyczny przycisk dodawania środków (`btn-add`) posiadał atrybut lub klasę autoryzacji (`auth`).
*   **Jak naprawić?** Dodaj klasę `auth-required` do przycisku dodawania środków w edytorze kodu (linia 7: `<button id="btn-add" class="auth-required">`) i kliknij **Uruchom Walidację**!

### 3. JavaScript — Naruszenie zakazu wywołań sieciowych
*   **Problem:** Funkcja logowania `login()` deklaruje kontrakt `forbid:network`, ale w celach diagnostycznych wywołuje zapytanie HTTP za pomocą obiektu `XMLHttpRequest`.
*   **Jak naprawić?** Usuń wywołanie `XMLHttpRequest` z kodu źródłowego i kliknij **Uruchom Walidację**!
