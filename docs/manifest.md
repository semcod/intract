# Manifest `intract.yaml`

Manifest służy do opisywania wielu plików, artefaktów i relacji między intencjami.

## Minimalny przykład

```yaml
version: intract.v1

project:
  name: my-service
  intent: serve:user_api

contracts:
  - id: project.service
    scope: project
    intent: serve:user_api
    priority: 1
    domain: service
    input: [http_request]
    output: [http_response]
    require:
      - expose.user_endpoints
      - validate.user_input
      - authorize.user_access
      - package.docker_image
      - deploy.kubernetes_service
    forbid:
      - secret_leak
      - unauthenticated_write
```

## Kontrakty plików

```yaml
files:
  src/auth/permissions.py:
    - scope: file
      intent: validate:user_permission
      priority: 1
      domain: security
      input: [user, resource]
      output: [allowed]
      forbid: [network, write]
```

## Artefakty

```yaml
artifacts:
  openapi.yaml:
    kind: openapi
    provides:
      - expose.user_endpoints

  Dockerfile:
    kind: dockerfile
    provides:
      - package.docker_image
    forbid:
      - root_user
      - latest_tag
      - secret_leak

  .github/workflows/ci.yml:
    kind: github_actions
    provides:
      - validate.ci_pipeline
    require:
      - run.tests
      - run.intract
```

## Walidacja manifestu

```bash
python -m intract check-manifest intract.yaml
```

Schemat:

- [`schemas/intract.schema.json`](../schemas/intract.schema.json)

## Relacje `require`

Pole `require` pozwala sprawdzać, czy większy kontrakt jest pokryty mniejszymi kontraktami.

Przykład:

```yaml
intent: analyze:code_duplication
require:
  - scan.project_files
  - extract.code_blocks
  - detect.duplicates
  - render.report
```

Graf:

```bash
python -m intract graph . --format mermaid
```
