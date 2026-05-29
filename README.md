# Intract


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.3.1-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$0.44-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-2.0h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $0.4398 (1 commits)
- 👤 **Human dev:** ~$200 (2.0h @ $100/h, 30min dedup)

Generated on 2026-05-29 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---



**Intract** is a lightweight intent-contract system for codebases.

Intract is not primarily a programming language. It is a **contract layer** for code intent.
A contract may be a single line, an inline comment, or a multi-file `intent.yaml` manifest.

## Inline contract

```python
# @intract.v1 scope:function intent:validate:user_permission priority:1 domain:security input:user,resource output:allowed effect:none forbid:write,network require:none validate:input_presence,return_value,no_forbidden_effect meaning:"check whether user can modify resource without changing state"
def can_update_resource(user, resource):
    return user.is_admin or resource.owner_id == user.id
```

## Multi-file manifest

```yaml
project:
  name: redup

contracts:
  - id: project.analysis
    scope: project
    intent: analyze:code_duplication
    priority: 1
    domain: project
    input: [source_tree]
    output: [DuplicationMap, RefactorSuggestion]
    effect: [read]
    forbid: [network]
    require:
      - scan.project_files
      - extract.code_blocks
      - detect.duplicates
      - group.duplicates
      - render.report
    validate:
      - required_intents
      - no_forbidden_effect
    meaning: "Project should analyze source code duplication and produce refactoring guidance."

files:
  src/redup/core/scanner/__init__.py:
    - scope: file
      intent: scan:project_files
      priority: 1
      domain: scanner
      input: [ScanConfig]
      output: [file_list]
      effect: [read]
      forbid: [network]
      meaning: "Scanner file should collect project source files."
```

## CLI

```bash
pip install -e .[dev]

intract scan .
intract validate .
intract validate . --manifest intent.yaml --json
intract init .
```

## Validation statuses

| Status | Meaning |
|---|---|
| `pass` | Contract is satisfied. |
| `partial` | Contract is partly satisfied but missing evidence or sub-intents. |
| `fail` | Contract is not satisfied. |
| `violation` | Contract matches but violates a forbidden constraint. |
| `unknown` | Not enough information to decide. |

## Contract fields

| Field | Example | Meaning |
|---|---|---|
| `scope` | `function` | Level: `line`, `block`, `function`, `class`, `file`, `module`, `project`. |
| `intent` | `validate:user_permission` | Main action and object. |
| `priority` | `1` | Importance from 1 to 5. |
| `domain` | `security` | Architectural/business domain. |
| `input` | `user,resource` | Expected inputs. |
| `output` | `allowed` | Expected output. |
| `effect` | `read` | Allowed/declared side effects. |
| `forbid` | `write,network` | Forbidden effects. |
| `require` | `scan.project_files` | Required sub-intents. |
| `validate` | `input_presence,no_forbidden_effect` | Validation rules to apply. |
| `meaning` | `"..."` | Human-readable explanation. |


## Plugins and SDKs

This package now includes a plugin registry and SDK templates for:

- Python plugin packages through `project.entry-points`
- TypeScript / Node SDK
- Go SDK
- Rust SDK
- Java SDK
- C# SDK
- config templates for `intract.yaml`, pre-commit, GitHub Actions, Dockerfile, OpenAPI

See:

```text
docs/plugins.md
docs/quick-enable.md
templates/
sdks/
```


## Watch and engine

Intract can now behave like a logical linter running during development:

```bash
intract watch .
intract watch . --planfile
intract engine suggest .
intract engine drift .
intract engine run . --planfile
intract tickets .
```

`watch` observes logical file changes in real time using content hashes and reruns validation.
`engine` scans the codebase, extracts logical fragments, suggests Intract contracts and detects drift.
`tickets` exports failed, partial or violating results as planfile-compatible ticket files.


## License

Licensed under Apache-2.0.
