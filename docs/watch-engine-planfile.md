# Watch, Engine and Planfile integration

## Real-time logical watch

```bash
intract watch .
intract watch . --manifest intent.yaml
intract watch . --planfile
intract watch . --once
```

`watch` polls the selected folder, computes content hashes of logical files and reruns validation when files are added, modified or deleted.

## Engine

```bash
intract engine suggest .
intract engine drift .
intract engine run . --planfile
```

The engine scans the codebase, extracts lightweight logical fragments, suggests `@intract.v1` contracts and detects logic drift between runs.

## Planfile tickets

```bash
intract tickets .
intract validate . --planfile
intract engine run . --planfile
```

Generated artifacts:

```text
.intract/planfile-tickets.yaml
.intract/planfile-tickets.json
.intract/TODO.intract.md
```

These files can be consumed by planfile or used as a fallback TODO ticket queue.
