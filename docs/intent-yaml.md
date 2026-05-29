# `intent.yaml` / `intract.yaml`

A manifest allows tagging multiple files and expressing nested project contracts.

```yaml
contracts:
  - id: project.analysis
    scope: project
    intent: analyze:code_duplication
    require:
      - scan.project_files
      - extract.code_blocks
      - detect.duplicates
```
