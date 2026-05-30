# Full-stack Intract demo

Minimal project showing manifest graph, inline contracts, and intent duplicates.

## Run locally

```bash
cd examples/full-stack

intract validate .
intract graph . --format mermaid
intract duplicates . --threshold 0.5
intract coverage .
```

## Staged / pre-commit

```bash
git init
git add .
git commit -m "baseline"

# change only parser_a body
echo "# edit" >> src/parser_a.py
git add src/parser_a.py

intract check --staged
intract check --staged --hunks
```

`--hunks` validates only contracts whose function body was touched by staged diff.

## Expected results

- `validate` — project require intents satisfied (`scan`, `parse`, `detect`)
- `duplicates` — `parse.extensions` vs `read.extension_list` (similar intents)
- `graph` — missing edges only if you remove a required intent from code
