# Executed next stage

Implemented in this package:

- manifest schema validation: `intract check-manifest`
- selected path validation helpers for staged/changed mode
- unified diff hunk parser
- policy fail/warn decisions
- coverage report: `intract coverage`
- duplicate intent report: `intract duplicates`
- graph builder: `intract graph`
- SARIF reporter: `intract check --format sarif`
- artifact validators:
  - OpenAPI `x-intract`
  - Dockerfile safety checks
  - GitHub Actions workflow checks
  - Kubernetes manifest checks
- pre-commit hook file
- GitHub Actions workflow
- Dockerfile
