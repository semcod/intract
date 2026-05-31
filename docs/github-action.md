# GitHub Action — Intract Validate

Publish this repository to the GitHub Marketplace as a **composite action**.

## Usage

```yaml
name: Intract

on: [pull_request, push]

jobs:
  contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: semcod/intract@v0.5
        with:
          path: .
          manifest: intract.yaml
          staged: "false"
          hunks: "true"
          fail-on-error: "true"
```

### Staged / pre-commit style in CI

```yaml
      - uses: semcod/intract@v0.5
        with:
          path: .
          staged: "true"
          hunks: "true"
```

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `path` | `.` | Project root |
| `manifest` | *(empty)* | Path to `intract.yaml` |
| `python-version` | `3.12` | Python runtime |
| `staged` | `false` | Validate staged files only |
| `hunks` | `true` | Hunk-level staged validation |
| `fail-on-error` | `true` | Exit non-zero on policy failure |

## Publishing checklist

1. Tag a release: `git tag v0.5.4 && git push origin v0.5.4`
2. Create GitHub Release from the tag (workflow `.github/workflows/release.yml` validates the action)
3. In repo **Settings → Actions → General**, allow GitHub Actions
4. Submit to Marketplace: **Publish this Action to GitHub Marketplace** on the release page
5. Point `action.yml` at the tagged ref (`@v0.5`, `@v0.5.4`, or `@main` for bleeding edge)

## Local verification

```bash
pip install -e .
pytest -q
# workflow job `test-composite-action` exercises uses: ./
```
