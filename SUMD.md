# Intract

Intent contract tagging, validation and semantic mapping for codebases.

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Quality Pipeline (`pyqual.yaml`)](#quality-pipeline-pyqualyaml)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `intract`
- **version**: `0.5.12`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, pyqual.yaml, goal.yaml, .env.example, Dockerfile, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: intract;
  version: 0.5.12;
}

dependencies {
  runtime: "pyyaml>=6.0, typer>=0.12.0, rich>=13.0";
  dev: "pytest>=7.0, ruff>=0.4, mypy>=1.8, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="intract"] {

}

workflow[name="install"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Installing sumd...";
  step-2: run cmd=if command -v uv > /dev/null 2>&1; then \;
  step-3: run cmd=uv pip install -e .; \;
  step-4: run cmd=else \;
  step-5: run cmd=pip install -e .; \;
  step-6: run cmd=fi;
  step-7: run cmd=echo "✅ Installation completed!";
}

workflow[name="install-dev"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Installing sumd with dev dependencies...";
  step-2: run cmd=if command -v uv > /dev/null 2>&1; then \;
  step-3: run cmd=uv pip install -e ".[dev]"; \;
  step-4: run cmd=else \;
  step-5: run cmd=pip install -e ".[dev]"; \;
  step-6: run cmd=fi;
  step-7: run cmd=echo "✅ Dev installation completed!";
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 Running tests...";
  step-2: run cmd=.venv/bin/python -m pytest tests/ -v --tb=short;
}

workflow[name="test-cov"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 Running tests with coverage...";
  step-2: run cmd=.venv/bin/python -m pytest tests/ -v --cov=sumd --cov-report=term-missing --cov-report=json;
}

workflow[name="lint"] {
  trigger: manual;
  step-1: run cmd=echo "🔍 Running linting with ruff...";
  step-2: run cmd=.venv/bin/python -m ruff check sumd/;
  step-3: run cmd=.venv/bin/python -m ruff check tests/;
}

workflow[name="format"] {
  trigger: manual;
  step-1: run cmd=echo "📝 Formatting code with ruff...";
  step-2: run cmd=.venv/bin/python -m ruff format sumd/;
  step-3: run cmd=.venv/bin/python -m ruff format tests/;
}

workflow[name="clean"] {
  trigger: manual;
  step-1: run cmd=echo "🧹 Cleaning temporary files...";
  step-2: run cmd=find . -type f -name "*.pyc" -delete;
  step-3: run cmd=find . -type d -name "__pycache__" -delete;
  step-4: run cmd=find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true;
  step-5: run cmd=rm -rf build/ dist/ .coverage htmlcov/ coverage.json;
  step-6: run cmd=echo "✅ Clean completed!";
}

workflow[name="publish"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Publishing to PyPI...";
  step-2: run cmd=command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build);
  step-3: run cmd=rm -rf dist/ build/ *.egg-info/;
  step-4: run cmd=.venv/bin/python -m build;
  step-5: run cmd=.venv/bin/twine check dist/*;
  step-6: run cmd=echo "⚡ Ready to upload. Run: make publish-confirm to upload to PyPI";
}

workflow[name="publish-confirm"] {
  trigger: manual;
  step-1: run cmd=echo "🚀 Uploading to PyPI...";
  step-2: run cmd=.venv/bin/twine upload dist/*;
}

workflow[name="publish-test"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Publishing to TestPyPI...";
  step-2: run cmd=command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build);
  step-3: run cmd=rm -rf dist/ build/ *.egg-info/;
  step-4: run cmd=.venv/bin/python -m build;
  step-5: run cmd=.venv/bin/twine upload --repository testpypi dist/*;
}

workflow[name="version"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Version information...";
  step-2: run cmd=cat VERSION;
  step-3: run cmd=.venv/bin/python -c "from importlib.metadata import version; print(f'Installed version: {version(\"sumd\")}')";
}

deploy {
  target: docker;
}

environment[name="local"] {
  runtime: docker-compose;
  env_file: .env;
  python_version: >=3.10;
}
```

## Interfaces

### CLI Entry Points

- `intract`
- `intract-mcp`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m intract
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m intract --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m intract --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m intract --help" 10000
ASSERT_EXIT_CODE 0
```

## Workflows

## Quality Pipeline (`pyqual.yaml`)

```yaml markpact:pyqual path=pyqual.yaml
pipeline:
  name: intract-quality

  metrics:
    coverage_min: 50

  stages:
    - name: test
      run: python -m pytest -q --tb=short
      timeout: 600

    - name: intract_contracts
      run: |
        python -m intract validate examples/full-stack --manifest examples/full-stack/intract.yaml
        python -m intract check examples/full-stack --manifest examples/full-stack/intract.yaml
        python -m intract duplicates examples/full-stack --threshold 0.5
      timeout: 120

    - name: intract_artifacts
      run: |
        mkdir -p .pyqual
        python -m intract scan . --all-artifacts --json > .pyqual/artifacts.json
      timeout: 120

    - name: intract_web_app
      run: |
        python -m intract validate examples/web-app/iterations/v1-pass \
          --manifest examples/web-app/intract.yaml
        python -m intract scan examples/web-app/iterations/v1-pass --all-artifacts
        bash examples/web-app/run-demo.sh
      timeout: 120

    - name: intract_demo_ci
      run: bash scripts/ci-full-stack.sh
      env:
        SKIP_VALLM: "1"
        SKIP_REDUP: "1"
      timeout: 300
```

## Configuration

```yaml
project:
  name: intract
  version: 0.5.12
  env: local
```

## Dependencies

### Runtime

```text markpact:deps python
pyyaml>=6.0
typer>=0.12.0
rich>=13.0
```

### Development

```text markpact:deps python scope=dev
pytest>=7.0
ruff>=0.4
mypy>=1.8
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
```

## Deployment

```bash markpact:run
pip install intract

# development install
pip install -e .[dev]
```

### Docker

- **base image**: `python:3.12-slim`
- **entrypoint**: `["intract"]`

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | `*(not set)*` | Required: OpenRouter API key (https://openrouter.ai/keys) |
| `LLM_MODEL` | `openrouter/qwen/qwen3-coder-next` | Model (default: openrouter/qwen/qwen3-coder-next) |
| `PFIX_AUTO_APPLY` | `true` | true = apply fixes without asking |
| `PFIX_AUTO_INSTALL_DEPS` | `true` | true = auto pip/uv install |
| `PFIX_AUTO_RESTART` | `false` | true = os.execv restart after fix |
| `PFIX_MAX_RETRIES` | `3` |  |
| `PFIX_DRY_RUN` | `false` |  |
| `PFIX_ENABLED` | `true` |  |
| `PFIX_GIT_COMMIT` | `false` | true = auto-commit fixes |
| `PFIX_GIT_PREFIX` | `pfix:` | commit message prefix |
| `PFIX_CREATE_BACKUPS` | `false` | false = disable .pfix_backups/ directory |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`intract`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `venv/lib/python3.13/site-packages/cryptography/__init__.py:__version__`

## Makefile Targets

- `help` — Default target
- `install` — Installation
- `install-dev`
- `test` — Testing
- `test-cov`
- `lint` — Code quality
- `format`
- `clean` — Utilities
- `publish` — Release helpers
- `publish-confirm`
- `publish-test`
- `version`
- `install`
- `test`
- `lint`
- `format`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# intract | 150f 10505L | python:131,typescript:7,shell:6,javascript:2,go:2,less:1,rust:1 | 2026-06-04
# stats: 437 func | 77 cls | 150 mod | CC̄=3.9 | critical:20 | cycles:0
# alerts[5]: CC python_block_extent=14; CC validate_sources_for_hunks=14; CC check=13; CC contract_line_to_manifest_entry=13; CC parse_contract_line=13
# hotspots[5]: check fan=21; watch fan=16; validate_sources_for_hunks fan=14; engine_suggest fan=14; engine_drift fan=14
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[150]:
  app.doql.less,119
  examples/full-stack/src/analyzer.py,4
  examples/full-stack/src/parser_a.py,4
  examples/full-stack/src/parser_b.py,4
  examples/full-stack/src/scanner.py,5
  examples/integration_tests/01_python_pass/app.py,9
  examples/integration_tests/02_typescript_violation_planfile/permission.ts,7
  examples/integration_tests/03_watch_engine_drift/reporter.py,5
  examples/integration_tests/03_watch_engine_drift/scanner.py,9
  examples/integration_tests/run_examples.py,118
  examples/markdown-generator/demo.py,69
  examples/markdown-generator/pass/generator.py,83
  examples/markdown-generator/run-demo.sh,8
  examples/markdown-generator/violation/generator.py,77
  examples/python/parse_extensions.py,9
  examples/showcase/server.py,143
  examples/toon/src/auth.js,17
  examples/toon/src/calc.py,16
  examples/toon/validate.sh,24
  examples/typescript/permission.ts,6
  examples/web-app/iterations/v1-pass/backend/auth.py,6
  examples/web-app/iterations/v1-pass/backend/routes.py,5
  examples/web-app/iterations/v1-pass/frontend/dashboard.ts,9
  examples/web-app/iterations/v2-violation/backend/auth.py,7
  examples/web-app/iterations/v2-violation/backend/routes.py,5
  examples/web-app/iterations/v2-violation/frontend/dashboard.ts,11
  examples/web-app/run-demo.sh,21
  extensions/vscode-intract/extension.js,52
  project.sh,50
  scripts/ci-full-stack.sh,77
  scripts/generate_toon_from_map.py,476
  sdks/go/examples/main.go,23
  sdks/go/intractsdk/sdk.go,69
  sdks/python/src/intract_plugin_example/__init__.py,27
  sdks/rust/src/lib.rs,55
  sdks/typescript/examples/basic.ts,14
  sdks/typescript/intract.config.ts,9
  sdks/typescript/src/index.ts,43
  src/intract/__init__.py,60
  src/intract/__main__.py,5
  src/intract/analyzers/__init__.py,21
  src/intract/analyzers/blocks.py,47
  src/intract/analyzers/csharp.py,66
  src/intract/analyzers/go.py,14
  src/intract/analyzers/java.py,28
  src/intract/analyzers/python_ast.py,71
  src/intract/analyzers/rust.py,16
  src/intract/analyzers/treesitter.py,63
  src/intract/analyzers/typescript.py,67
  src/intract/artifacts.py,6
  src/intract/check.py,298
  src/intract/cli.py,684
  src/intract/config.py,65
  src/intract/core/__init__.py,36
  src/intract/core/artifact.py,133
  src/intract/core/cache.py,100
  src/intract/core/models.py,155
  src/intract/core/normalizer.py,70
  src/intract/core/registry.py,7
  src/intract/core/signatures.py,123
  src/intract/coverage.py,35
  src/intract/duplicates/__init__.py,16
  src/intract/duplicates/grouping.py,139
  src/intract/duplicates/matcher.py,56
  src/intract/duplicates/scoring.py,38
  src/intract/duplicates.py,6
  src/intract/effects.py,6
  src/intract/engine/__init__.py,22
  src/intract/engine/analyzer.py,86
  src/intract/engine/assigner.py,110
  src/intract/engine/context.py,37
  src/intract/engine/drift.py,114
  src/intract/engine/monitor.py,33
  src/intract/engine/scanner.py,54
  src/intract/git.py,54
  src/intract/graph.py,69
  src/intract/integrations/__init__.py,45
  src/intract/integrations/nexu.py,190
  src/intract/integrations/planfile.py,142
  src/intract/integrations/planfile_adapter.py,256
  src/intract/integrations/redup.py,288
  src/intract/integrations/vallm.py,117
  src/intract/manifest_ops.py,244
  src/intract/manifest_schema.py,117
  src/intract/mcp/__init__.py,22
  src/intract/mcp/handlers.py,125
  src/intract/mcp/schemas.py,92
  src/intract/mcp/server.py,119
  src/intract/mcp_server.py,7
  src/intract/models.py,4
  src/intract/normalizer.py,4
  src/intract/parser.py,4
  src/intract/parsers/__init__.py,14
  src/intract/parsers/inline.py,336
  src/intract/parsers/manifest.py,178
  src/intract/parsers/openapi.py,64
  src/intract/parsers/toon.py,170
  src/intract/plugins/__init__.py,25
  src/intract/plugins/base.py,110
  src/intract/plugins/builtins.py,112
  src/intract/plugins/manager.py,62
  src/intract/policy.py,107
  src/intract/project.py,168
  src/intract/proposals.py,101
  src/intract/propose_llm.py,167
  src/intract/reporters/__init__.py,1
  src/intract/reporters/sarif.py,63
  src/intract/scan_artifacts.py,71
  src/intract/sdk.py,48
  src/intract/signature.py,4
  src/intract/validate_snippet.py,29
  src/intract/validation.py,14
  src/intract/validators/__init__.py,22
  src/intract/validators/artifacts.py,182
  src/intract/validators/base.py,51
  src/intract/validators/effects.py,53
  src/intract/validators/engine.py,55
  src/intract/validators/input_output.py,75
  src/intract/validators/registry.py,86
  src/intract/validators/requirements.py,14
  src/intract/watch.py,161
  src/intract/yaml_manifest.py,4
  tests/test_cache.py,36
  tests/test_check_staged.py,35
  tests/test_full_stack.py,28
  tests/test_generate_toon_from_map.py,97
  tests/test_hunk_filter.py,89
  tests/test_integrations.py,61
  tests/test_language_analyzers.py,117
  tests/test_manifest.py,27
  tests/test_manifest_ops.py,107
  tests/test_markdown_generator_example.py,79
  tests/test_mcp.py,63
  tests/test_new_modules.py,49
  tests/test_next_stage.py,37
  tests/test_parser.py,77
  tests/test_planfile_adapter.py,98
  tests/test_policy.py,46
  tests/test_proposals.py,18
  tests/test_python_ast.py,38
  tests/test_redup_policy.py,41
  tests/test_rule_registry.py,53
  tests/test_scan_artifacts.py,20
  tests/test_staged_e2e.py,79
  tests/test_toon.py,61
  tests/test_validate_snippet.py,17
  tests/test_validation.py,40
  tests/test_vallm_integration.py,30
  tests/test_web_app.py,32
  tree.sh,2
D:
  examples/full-stack/src/analyzer.py:
    e: detect_duplicates
    detect_duplicates(blocks)
  examples/full-stack/src/parser_a.py:
    e: parse_extensions
    parse_extensions(raw)
  examples/full-stack/src/parser_b.py:
    e: load_extension_list
    load_extension_list(value)
  examples/full-stack/src/scanner.py:
    e: scan_project_files
    scan_project_files(config)
  examples/integration_tests/01_python_pass/app.py:
    e: parse_extensions
    parse_extensions(raw_extensions)
  examples/integration_tests/03_watch_engine_drift/reporter.py:
    e: render_summary
    render_summary(file_list)
  examples/integration_tests/03_watch_engine_drift/scanner.py:
    e: collect_project_files
    collect_project_files(source_tree)
  examples/integration_tests/run_examples.py:
    e: print_result,run_example_01,run_example_02,run_example_03,run_example_04,main
    print_result(name;payload)
    run_example_01(base)
    run_example_02(base)
    run_example_03(base)
    run_example_04(base)
    main()
  examples/markdown-generator/demo.py:
    e: _validate_project,_load_pass_generator,_violation_messages,main
    _validate_project(path;manifest_path)
    _load_pass_generator()
    _violation_messages(report)
    main()
  examples/markdown-generator/pass/generator.py:
    e: normalize_topic,build_markdown_outline,render_markdown_sections,guard_markdown_contract,generate_markdown_document
    normalize_topic(topic)
    build_markdown_outline(normalized_topic;required_sections)
    render_markdown_sections(markdown_outline;normalized_topic;audience)
    guard_markdown_contract(markdown_document;required_sections;normalized_topic)
    generate_markdown_document(topic;audience)
  examples/markdown-generator/violation/generator.py:
    e: normalize_topic,build_markdown_outline,render_markdown_sections,guard_markdown_contract,generate_markdown_document
    normalize_topic(topic)
    build_markdown_outline(normalized_topic;required_sections)
    render_markdown_sections(markdown_outline;normalized_topic;audience)
    guard_markdown_contract(markdown_document;required_sections;normalized_topic)
    generate_markdown_document(topic;audience)
  examples/python/parse_extensions.py:
    e: parse_extensions
    parse_extensions(raw_extensions)
  examples/showcase/server.py:
    e: load_env_file,resolve_runtime_config,main,ShowcaseHandler
    ShowcaseHandler: __init__(0),_write_json(2),do_GET(0),do_POST(0)
    load_env_file(path)
    resolve_runtime_config()
    main()
  examples/toon/src/calc.py:
    e: add,divide,write_to_log
    add(a;b)
    divide(a;b)
    write_to_log(msg)
  examples/web-app/iterations/v1-pass/backend/auth.py:
    e: check_permission
    check_permission(user;resource)
  examples/web-app/iterations/v1-pass/backend/routes.py:
    e: read_profile
    read_profile(user_id;users)
  examples/web-app/iterations/v2-violation/backend/auth.py:
    e: check_permission
    check_permission(user;resource)
  examples/web-app/iterations/v2-violation/backend/routes.py:
    e: read_profile
    read_profile(user_id;users)
  scripts/generate_toon_from_map.py:
    e: _slug,_parse_intent_from_name,_iter_section_lines,_parse_modules,_extract_symbol_names,_parse_functions,_contract_fragment,_toon_uri,_llm_contract_fragment,_resolve_output_profile,_effective_include,_default_function_fragment,_function_fragment,generate_toon_lines,_build_parser,_run_validate,_ensure_parent,main,FunctionTarget,OutputProfileConfig
    FunctionTarget:
    OutputProfileConfig:
    _slug(value)
    _parse_intent_from_name(name)
    _iter_section_lines(lines)
    _parse_modules(lines)
    _extract_symbol_names(line)
    _parse_functions(lines)
    _contract_fragment()
    _toon_uri(file_path)
    _llm_contract_fragment()
    _resolve_output_profile(profile)
    _effective_include()
    _default_function_fragment()
    _function_fragment()
    generate_toon_lines()
    _build_parser()
    _run_validate(root;manifest)
    _ensure_parent(path)
    main(argv)
  sdks/python/src/intract_plugin_example/__init__.py:
    e: ExampleParserPlugin,ExampleValidatorPlugin
    ExampleParserPlugin: supports(1),parse(1)
    ExampleValidatorPlugin: supports(1),validate(2)
  src/intract/__init__.py:
  src/intract/__main__.py:
  src/intract/analyzers/__init__.py:
  src/intract/analyzers/blocks.py:
    e: scan_braced_block,block_extent_from_patterns
    scan_braced_block(lines;start_line)
    block_extent_from_patterns(source;start_line;start_patterns)
  src/intract/analyzers/csharp.py:
    e: csharp_block_extent,_scan_braced_block,_treesitter_csharp_extent
    csharp_block_extent(source;start_line)
    _scan_braced_block(lines;start_line)
    _treesitter_csharp_extent(source;start_line)
  src/intract/analyzers/go.py:
    e: go_block_extent
    go_block_extent(source;start_line)
  src/intract/analyzers/java.py:
    e: java_block_extent
    java_block_extent(source;start_line)
  src/intract/analyzers/python_ast.py:
    e: _decorator_lines,python_function_extent,python_block_extent
    _decorator_lines(node)
    python_function_extent(source;start_line)
    python_block_extent(source;start_line)
  src/intract/analyzers/rust.py:
    e: rust_block_extent
    rust_block_extent(source;start_line)
  src/intract/analyzers/treesitter.py:
    e: _load_parser,_find_extent,typescript_function_extent,csharp_method_extent
    _load_parser(language)
    _find_extent(source;start_line;language;node_types)
    typescript_function_extent(source;start_line)
    csharp_method_extent(source;start_line)
  src/intract/analyzers/typescript.py:
    e: typescript_block_extent,_scan_braced_block,_treesitter_typescript_extent
    typescript_block_extent(source;start_line)
    _scan_braced_block(lines;start_line)
    _treesitter_typescript_extent(source;start_line)
  src/intract/artifacts.py:
  src/intract/check.py:
    e: parse_unified_diff_hunks,load_selected_sources,_manifest_changed,changed_lines_by_file,_language_block_extent,_is_python_declaration,_is_fallback_preamble,_fallback_block_extent,block_extent,signature_touched,validate_sources_for_hunks,validate_selected_paths,staged_check,changed_check,ChangedHunk
    ChangedHunk: to_dict(0)
    parse_unified_diff_hunks(diff_text)
    load_selected_sources(root;files)
    _manifest_changed(files)
    changed_lines_by_file(hunks)
    _language_block_extent(source;start_line;file_path)
    _is_python_declaration(stripped)
    _is_fallback_preamble(stripped)
    _fallback_block_extent(source;start_line)
    block_extent(source;start_line)
    signature_touched(signature;changed_lines;source)
    validate_sources_for_hunks(root;files;hunks)
    validate_selected_paths(root;files)
    staged_check(root)
    changed_check(root)
  src/intract/cli.py:
    e: main,init,_print_artifact_scan_report,_scan_artifacts,_is_scan_candidate,_scan_contract_file,_scan_inline_records,_scan_row,_print_scan_table,scan,validate,check,coverage,duplicates,graph,tickets,planfile_push,planfile_pull,planfile_sync,planfile_webhook_test,planfile_webhook_apply,watch,engine_suggest,engine_drift,engine_run,_export_tickets,_print_validation_report,_format_check_text,check_manifest,artifact_validate,propose_delta,propose_llm_cmd,manifest_apply_ledger
    main(version)
    init(path;force)
    _print_artifact_scan_report(artifact_report)
    _scan_artifacts(path)
    _is_scan_candidate(path)
    _scan_contract_file(path)
    _scan_inline_records(path)
    _scan_row(record)
    _print_scan_table(data)
    scan(path;json_output;all_artifacts)
    validate(path;manifest;json_output;planfile)
    check(path;staged;changed;base;hunks;manifest;fmt;output;planfile)
    coverage(path;json_output)
    duplicates(path;threshold;json_output)
    graph(path;manifest;fmt;output)
    tickets(path;manifest)
    planfile_push(path;manifest;api_url;token;project)
    planfile_pull(path;api_url;token;project;json_output)
    planfile_sync(path;manifest;api_url;token;project)
    planfile_webhook_test(webhook_url;secret)
    planfile_webhook_apply(path;event_file)
    watch(path;manifest;interval;planfile;once;json_output)
    engine_suggest(path;json_output)
    engine_drift(path;manifest;json_output)
    engine_run(path;manifest;planfile;json_output)
    _export_tickets(path;report)
    _print_validation_report(report)
    _format_check_text(report;decision;files)
    check_manifest(manifest;json_output)
    artifact_validate(path;json_output)
    propose_delta(keep;delete;stage;capsule;json_output)
    propose_llm_cmd(file;goal;model;json_output)
    manifest_apply_ledger(manifest;ledger;workspace;capsule;target;dry_run;json_output)
  src/intract/config.py:
    e: load_config,IntractConfig
    IntractConfig: from_mapping(2)
    load_config(root)
  src/intract/core/__init__.py:
  src/intract/core/artifact.py:
    e: infer_language,_kind_from_filename,_kind_from_structured_content,infer_artifact_kind,ArtifactKind,Artifact
    ArtifactKind:
    Artifact: from_path(2)
    infer_language(path)
    _kind_from_filename(path;name;suffix)
    _kind_from_structured_content(suffix;content)
    infer_artifact_kind(path;content)
  src/intract/core/cache.py:
    e: CacheEntry,IntractDecisionCache
    CacheEntry:
    IntractDecisionCache: __init__(1),_hash(1),_get_key(2),load(0),save(0),get_decision(2),set_decision(6)  # Git-friendly, text-based JSON ledger cache for Intract's dec
  src/intract/core/models.py:
    e: ValidationStatus,Contract,ContractRecord,ContractSignature,ValidationIssue,ValidationResult,ProjectReport
    ValidationStatus:
    Contract: key(0)
    ContractRecord:
    ContractSignature: key(0)
    ValidationIssue:
    ValidationResult: to_dict(0)
    ProjectReport: passed(0),partial(0),failed(0),violations(0),to_dict(0)
  src/intract/core/normalizer.py:
    e: normalize_label,normalize_action,normalize_many,normalize_requirement
    normalize_label(value)
    normalize_action(action)
    normalize_many(values)
    normalize_requirement(value)
  src/intract/core/registry.py:
  src/intract/core/signatures.py:
    e: make_block_id,_normalize_contract,_add_feature_values,_signature_features,_exact_hash,_block_id,build_signature,build_signatures,_NormalizedContract
    _NormalizedContract:
    make_block_id(file_path;start_line;end_line;scope)
    _normalize_contract(record)
    _add_feature_values(features;prefix;values)
    _signature_features(record;normalized)
    _exact_hash(features)
    _block_id(record)
    build_signature(record)
    build_signatures(records)
  src/intract/coverage.py:
    e: calculate_coverage,CoverageReport
    CoverageReport: to_dict(0)
    calculate_coverage(root)
  src/intract/duplicates/__init__.py:
  src/intract/duplicates/grouping.py:
    e: union_find_groups,pairs_to_duplicate_contracts,pairs_to_intent_groups,find_duplicate_contracts,DuplicateContract,IntentDuplicateGroup
    DuplicateContract: to_dict(0)
    IntentDuplicateGroup: to_dict(0)
    union_find_groups(pairs)
    pairs_to_duplicate_contracts(pairs;signatures_by_id)
    pairs_to_intent_groups(pairs;signatures_by_id)
    find_duplicate_contracts(root;threshold)
  src/intract/duplicates/matcher.py:
    e: bucket_signatures,find_intent_pairs,IntentPair
    IntentPair:
    bucket_signatures(signatures)
    find_intent_pairs(signatures;threshold)
  src/intract/duplicates/scoring.py:
    e: jaccard,object_similarity,score_similarity
    jaccard(a;b)
    object_similarity(left;right)
    score_similarity(left;right)
  src/intract/duplicates.py:
  src/intract/effects.py:
  src/intract/engine/__init__.py:
  src/intract/engine/analyzer.py:
    e: _line_number,_fragment_id,_slice_until_next_match,analyze_source_units
    _line_number(text;pos)
    _fragment_id(path;kind;name;start;end)
    _slice_until_next_match(text;start_pos;next_positions)
    analyze_source_units(units)
  src/intract/engine/assigner.py:
    e: _split_name,_infer_action,_infer_object,_infer_effects,suggest_contract_for_fragment,suggest_contracts_for_fragments
    _split_name(name)
    _infer_action(name;text)
    _infer_object(name;action)
    _infer_effects(text)
    suggest_contract_for_fragment(fragment)
    suggest_contracts_for_fragments(fragments)
  src/intract/engine/context.py:
    e: EngineConfig,LogicalFragment,ContractSuggestion
    EngineConfig:
    LogicalFragment:
    ContractSuggestion:
  src/intract/engine/drift.py:
    e: hash_text,state_from_fragments,save_state,load_state,detect_drift,FragmentState,DriftIssue
    FragmentState:
    DriftIssue:
    hash_text(text)
    state_from_fragments(fragments)
    save_state(path;fragments)
    load_state(path)
    detect_drift(previous;current_fragments)
  src/intract/engine/monitor.py:
    e: scan_suggest_and_validate
    scan_suggest_and_validate(config)
  src/intract/engine/scanner.py:
    e: collect_source_units,SourceUnit
    SourceUnit:
    collect_source_units(root)
  src/intract/git.py:
    e: _run_git,staged_files,changed_files,staged_hunks,paths_from_changes,GitChange
    GitChange:
    _run_git(args;root)
    staged_files(root)
    changed_files(root;base_ref)
    staged_hunks(root;path)
    paths_from_changes(changes)
  src/intract/graph.py:
    e: _safe,build_graph,ContractGraph
    ContractGraph: to_dict(0),to_mermaid(0)
    _safe(value)
    build_graph(root;manifest)
  src/intract/integrations/__init__.py:
  src/intract/integrations/nexu.py:
    e: format_intract_v1_line,parse_intract_line,scan_contracts_in_text,scan_contracts_in_file,_contract_items,_list_field,_base_intent_contract,read_manifest_contracts,_read_yaml_mapping,_toon_target,_target_line_value,_toon_intent_contract,read_toon_manifest_contracts,IntentContract
    IntentContract: key(0)
    format_intract_v1_line(contract)
    parse_intract_line(line)
    scan_contracts_in_text(text)
    scan_contracts_in_file(path;root)
    _contract_items(data)
    _list_field(item;key)
    _base_intent_contract(item;path)
    read_manifest_contracts(path)
    _read_yaml_mapping(path)
    _toon_target(item)
    _target_line_value(target)
    _toon_intent_contract(item;path)
    read_toon_manifest_contracts(path)
  src/intract/integrations/planfile.py:
    e: _severity_from_status,tickets_from_report,Ticket,PlanfileExporter
    Ticket:
    PlanfileExporter: __init__(1),export(1),_write_yaml(2),_write_json(2),_write_todo(2)
    _severity_from_status(status)
    tickets_from_report(report)
  src/intract/integrations/planfile_adapter.py:
    e: _ticket_from_dict,_default_created_at,PlanfileConfig,PlanfileSyncResult,PlanfileWebhookResult,PlanfileApiAdapter
    PlanfileConfig: from_env(1)
    PlanfileSyncResult:
    PlanfileWebhookResult:
    PlanfileApiAdapter: __init__(1),export_local(1),push(1),pull(0),sync_from_report(1),emit_webhook(2),apply_webhook_event(1),_webhook_label(1),_endpoint(1),_request(3)  # Sync Intract tickets with a planfile-compatible HTTP API or 
    _ticket_from_dict(data)
    _default_created_at()
  src/intract/integrations/redup.py:
    e: block_text,block_file_path,block_start_line,block_end_line,signatures_from_text,signatures_from_blocks,signatures_from_manifest,_with_block_lines,find_intent_duplicate_groups,parse_policy_tokens,_resolve_manifest_path,_graph_for_policy,_intent_duplicate_label,_duplicate_reasons,_apply_duplicate_policy,validate_for_redup,scan_blocks_for_intent_duplicates,CodeBlockLike,BlockAdapter,RedupScanResult,RedupPolicyResult
    CodeBlockLike:
    BlockAdapter:
    RedupScanResult: to_dict(0)
    RedupPolicyResult: to_dict(0)
    block_text(block)
    block_file_path(block)
    block_start_line(block)
    block_end_line(block)
    signatures_from_text(text)
    signatures_from_blocks(blocks)
    signatures_from_manifest(manifest_path)
    _with_block_lines(signature;block)
    find_intent_duplicate_groups(blocks)
    parse_policy_tokens(value)
    _resolve_manifest_path(project_root;manifest;config)
    _graph_for_policy(project_root;manifest_path;fail_on)
    _intent_duplicate_label(group)
    _duplicate_reasons(intent_groups)
    _apply_duplicate_policy(reasons;warnings)
    validate_for_redup(root)
    scan_blocks_for_intent_duplicates(blocks)
  src/intract/integrations/vallm.py:
    e: map_validation_result,map_project_report,validate_for_vallm,validate_proposal,MappedIssue,MappedValidationResult
    MappedIssue:
    MappedValidationResult: to_dict(0)
    map_validation_result(result)
    map_project_report(report)
    validate_for_vallm(root)
    validate_proposal(code)
  src/intract/manifest_ops.py:
    e: load_manifest_document,write_manifest_document,contract_line_to_manifest_entry,load_policy_ledger,resolve_manifest_paths,_existing_contract_ids,_should_apply_ledger_entry,_iter_ledger_proposals,_append_manifest_proposal,apply_ledger_to_manifest,apply_ledger_to_manifests,ManifestApplyResult,ManifestApplyBatchResult
    ManifestApplyResult: to_dict(0)
    ManifestApplyBatchResult: added_total(0),to_dict(0)
    load_manifest_document(path)
    write_manifest_document(path;data)
    contract_line_to_manifest_entry(line)
    load_policy_ledger(path)
    resolve_manifest_paths()
    _existing_contract_ids(manifest)
    _should_apply_ledger_entry(entry)
    _iter_ledger_proposals(ledger_path)
    _append_manifest_proposal(proposal;manifest;existing_ids;result)
    apply_ledger_to_manifest(manifest_path;ledger_path)
    apply_ledger_to_manifests()
  src/intract/manifest_schema.py:
    e: _load_schema,_manifest_report,_invalid_manifest_report,_load_manifest_data,_jsonschema_issues,_fallback_issues,validate_manifest,ManifestIssue,ManifestValidationReport
    ManifestIssue:
    ManifestValidationReport: to_dict(0)
    _load_schema()
    _manifest_report(path;issues)
    _invalid_manifest_report(path;message)
    _load_manifest_data(path)
    _jsonschema_issues(data)
    _fallback_issues(data)
    validate_manifest(path)
  src/intract/mcp/__init__.py:
  src/intract/mcp/handlers.py:
    e: _resolve_path,_resolve_manifest,handle_validate_project,handle_validate_staged,handle_validate_intent_snippet,handle_find_duplicates,handle_build_graph,handle_scan_artifacts,handle_project_info
    _resolve_path(params)
    _resolve_manifest(root;params)
    handle_validate_project(params)
    handle_validate_staged(params)
    handle_validate_intent_snippet(params)
    handle_find_duplicates(params)
    handle_build_graph(params)
    handle_scan_artifacts(params)
    handle_project_info(_)
  src/intract/mcp/schemas.py:
  src/intract/mcp/server.py:
    e: handle_initialize,handle_tools_list,handle_tools_call,handle_request,run_server
    handle_initialize(request_id)
    handle_tools_list(request_id)
    handle_tools_call(request_id;params)
    handle_request(request)
    run_server()
  src/intract/mcp_server.py:
  src/intract/models.py:
  src/intract/normalizer.py:
  src/intract/parser.py:
  src/intract/parsers/__init__.py:
  src/intract/parsers/inline.py:
    e: clean_comment_line,split_csv,parse_priority,parse_key_value,marker_payload,extract_intract_uri,_parse_uri_contract,_set_intent,_set_action,_set_object,_set_scope,_set_priority,_set_domain,_set_contract_id,_set_meaning,_extend_list,_add_relation,_add_unknown_tag,_parse_special_token,_apply_key_value_pair,_resolve_action_object,parse_contract_line,extract_contract_records_from_text,_ContractParserState
    _ContractParserState: __init__(1)
    clean_comment_line(line)
    split_csv(value)
    parse_priority(token)
    parse_key_value(token)
    marker_payload(line)
    extract_intract_uri(payload)
    _parse_uri_contract(payload;default_scope)
    _set_intent(_key;value;state)
    _set_action(_key;value;state)
    _set_object(_key;value;state)
    _set_scope(_key;value;state)
    _set_priority(_key;value;state)
    _set_domain(_key;value;state)
    _set_contract_id(_key;value;state)
    _set_meaning(_key;value;state)
    _extend_list(attribute)
    _add_relation(key;value;state)
    _add_unknown_tag(key;value;state)
    _parse_special_token(token;state)
    _apply_key_value_pair(key;value;state)
    _resolve_action_object(state)
    parse_contract_line(line)
    extract_contract_records_from_text(source)
  src/intract/parsers/manifest.py:
    e: _to_tuple,_parse_intent,contract_from_mapping,_target_mapping,_target_line,_target_tags,_with_target_tags,_top_level_contract_record,_top_level_contract_records,_file_contract_records,load_manifest_records,create_sample_manifest
    _to_tuple(value)
    _parse_intent(value)
    contract_from_mapping(data)
    _target_mapping(item)
    _target_line(target)
    _target_tags(target)
    _with_target_tags(contract;target)
    _top_level_contract_record(item;path;index)
    _top_level_contract_records(data;path)
    _file_contract_records(files)
    load_manifest_records(path)
    create_sample_manifest()
  src/intract/parsers/openapi.py:
    e: parse_openapi_contracts,parse_openapi_text
    parse_openapi_contracts(path)
    parse_openapi_text(content)
  src/intract/parsers/toon.py:
    e: _parse_action_object_from_intent,_extract_file_path,_get_first,_get_list,_get_first_alias,_get_list_alias,_build_tags,_start_line,_priority,_action_object,_contract_from_uri,parse_toon_uri_line,load_toon_records
    _parse_action_object_from_intent(intent;contract_id)
    _extract_file_path(parsed)
    _get_first(params;key;default)
    _get_list(params;key)
    _get_first_alias(params)
    _get_list_alias(params)
    _build_tags(func_val;xpath_val;fragment_params)
    _start_line(line_val)
    _priority(fragment_params)
    _action_object(fragment_params)
    _contract_from_uri(text;fragment_params)
    parse_toon_uri_line(line;line_num)
    load_toon_records(path)
  src/intract/plugins/__init__.py:
  src/intract/plugins/base.py:
    e: PluginResult,ParserPlugin,ValidatorPlugin,ReporterPlugin,IntegrationPlugin,PluginRegistry
    PluginResult:
    ParserPlugin: supports(1),parse(1)
    ValidatorPlugin: supports(1),validate(2)
    ReporterPlugin: render(1)
    IntegrationPlugin: install(1)
    PluginRegistry: add_parser(1),add_validator(1),add_reporter(1),add_integration(1),parse_artifact(1),validate_artifact(2)
  src/intract/plugins/builtins.py:
    e: InlineContractParserPlugin,OpenAPIParserPlugin,ManifestParserPlugin,BasicContractValidatorPlugin,ArtifactStructureValidatorPlugin,JsonReporterPlugin
    InlineContractParserPlugin: supports(1),parse(1)
    OpenAPIParserPlugin: supports(1),parse(1)
    ManifestParserPlugin: supports(1),parse(1)
    BasicContractValidatorPlugin: supports(1),validate(2)
    ArtifactStructureValidatorPlugin: supports(1),validate(2)
    JsonReporterPlugin: render(1)
  src/intract/plugins/manager.py:
    e: _register_unique,load_builtin_plugins,discover_plugins
    _register_unique(registry;kind;plugin)
    load_builtin_plugins()
    discover_plugins()
  src/intract/policy.py:
    e: _p1_missing_reasons,_result_status,_result_policy_line,_collect_result_policy,_invalid_manifest_reasons,_missing_required_p1_reasons,decide_policy,PolicyDecision
    PolicyDecision:
    _p1_missing_reasons(graph;manifest_path)
    _result_status(result)
    _result_policy_line(result;status)
    _collect_result_policy(report)
    _invalid_manifest_reasons(manifest_path)
    _missing_required_p1_reasons(graph;manifest_path)
    decide_policy(report)
  src/intract/project.py:
    e: load_project_sources,extract_signatures_from_sources,_validate_observed_signatures,_validate_manifest_signature,_validate_manifest_signatures,_project_status,validate_sources,validate_project
    load_project_sources(root)
    extract_signatures_from_sources(sources)
    _validate_observed_signatures(observed_signatures;sources)
    _validate_manifest_signature(required_signature;observed_signatures;sources)
    _validate_manifest_signatures(manifest_records;observed_signatures;sources)
    _project_status(results)
    validate_sources(sources)
    validate_project(root)
  src/intract/proposals.py:
    e: _ui_contract_line,propose_ui_delta_contracts,propose_ui_delta_contract_dicts,ProposedContract
    ProposedContract: to_dict(0)
    _ui_contract_line()
    propose_ui_delta_contracts()
    propose_ui_delta_contract_dicts()
  src/intract/propose_llm.py:
    e: _extract_intract_lines,_lines_to_proposals,_load_litellm_completion,_resolve_model,_resolve_api_key,_build_prompt,_message_content_to_text,_strip_markdown_fence,_json_line_strings,propose_contracts_llm
    _extract_intract_lines(text)
    _lines_to_proposals(lines)
    _load_litellm_completion()
    _resolve_model(model)
    _resolve_api_key(api_key)
    _build_prompt(source)
    _message_content_to_text(content)
    _strip_markdown_fence(raw)
    _json_line_strings(raw)
    propose_contracts_llm(source)
  src/intract/reporters/__init__.py:
  src/intract/reporters/sarif.py:
    e: report_to_sarif
    report_to_sarif(report)
  src/intract/scan_artifacts.py:
    e: discover_artifact_paths,scan_all_artifacts,ArtifactScanReport
    ArtifactScanReport: violations(0),to_dict(0)
    discover_artifact_paths(root)
    scan_all_artifacts(root)
  src/intract/sdk.py:
    e: contract,ContractBuilder
    ContractBuilder: to_inline(1)
    contract()
  src/intract/signature.py:
  src/intract/validate_snippet.py:
    e: validate_artifact_with_proposals
    validate_artifact_with_proposals(artifact;proposals)
  src/intract/validation.py:
  src/intract/validators/__init__.py:
  src/intract/validators/artifacts.py:
    e: validate_openapi,validate_dockerfile,validate_github_actions,validate_kubernetes,validate_artifact,ArtifactValidationReport
    ArtifactValidationReport: to_dict(0)
    validate_openapi(path)
    validate_dockerfile(path)
    validate_github_actions(path)
    validate_kubernetes(path)
    validate_artifact(path)
  src/intract/validators/base.py:
    e: merge_rule_results,RuleResult,ValidationContext,ValidationRule
    RuleResult:
    ValidationContext:
    ValidationRule: supports(1),validate(3)
    merge_rule_results(results)
  src/intract/validators/effects.py:
    e: detect_effects,NoForbiddenEffectRule
    NoForbiddenEffectRule: supports(1),validate(3)
    detect_effects(source)
  src/intract/validators/engine.py:
    e: validate_contract_against_source
    validate_contract_against_source(signature;source)
  src/intract/validators/input_output.py:
    e: contains_token_like,has_return_value,InputPresenceRule,OutputPresenceRule,ReturnValueRule
    InputPresenceRule: supports(1),validate(3)
    OutputPresenceRule: supports(1),validate(3)
    ReturnValueRule: supports(1),validate(3)
    contains_token_like(source;token)
    has_return_value(source)
  src/intract/validators/registry.py:
    e: _discover_entry_point_rules,get_rule_registry,RuleRegistry
    RuleRegistry: __init__(1),register(1),rules(0),run(4),rule_status(2),summarize(2)  # Registry of contract validation rules with optional plugin d
    _discover_entry_point_rules()
    get_rule_registry()
  src/intract/validators/requirements.py:
    e: validate_required_contracts
    validate_required_contracts(required_signature;observed_signatures)
  src/intract/watch.py:
    e: hash_file,should_scan,snapshot_tree,diff_snapshots,watch_tree,changes_to_paths,FileState,FileChange,WatchConfig
    FileState:
    FileChange:
    WatchConfig:
    hash_file(path)
    should_scan(path;root;config)
    snapshot_tree(root;config)
    diff_snapshots(old;new)
    watch_tree(root;callback)
    changes_to_paths(changes)
  src/intract/yaml_manifest.py:
  tests/test_cache.py:
    e: test_decision_cache_lifecycle
    test_decision_cache_lifecycle(tmp_path)
  tests/test_check_staged.py:
    e: test_manifest_changed_helper,test_validate_selected_paths_full_graph
    test_manifest_changed_helper()
    test_validate_selected_paths_full_graph(tmp_path)
  tests/test_full_stack.py:
    e: test_full_stack_validate_passes,test_full_stack_graph_covers_requires,test_full_stack_finds_intent_duplicates
    test_full_stack_validate_passes()
    test_full_stack_graph_covers_requires()
    test_full_stack_finds_intent_duplicates()
  tests/test_generate_toon_from_map.py:
    e: _sample_map_text,test_parse_modules_reads_m_section_entries,test_parse_functions_extracts_symbols_and_skips_private,test_generate_toon_lines_dev_profile_filters_project_and_shapes_functions,test_generate_toon_lines_ci_security_profile_includes_project_and_security_validate
    _sample_map_text()
    test_parse_modules_reads_m_section_entries()
    test_parse_functions_extracts_symbols_and_skips_private()
    test_generate_toon_lines_dev_profile_filters_project_and_shapes_functions(tmp_path)
    test_generate_toon_lines_ci_security_profile_includes_project_and_security_validate(tmp_path)
  tests/test_hunk_filter.py:
    e: test_changed_lines_by_file,test_block_extent_finds_function_body,test_signature_touched_by_body_change,test_validate_sources_for_hunks_only_touched_contract,test_validate_sources_for_hunks_catches_violation_in_touched_block
    test_changed_lines_by_file()
    test_block_extent_finds_function_body()
    test_signature_touched_by_body_change()
    test_validate_sources_for_hunks_only_touched_contract(tmp_path)
    test_validate_sources_for_hunks_catches_violation_in_touched_block(tmp_path)
  tests/test_integrations.py:
    e: test_redup_finds_intent_duplicate_groups,test_duplicate_contracts_cli_parity,test_find_intent_duplicate_groups_from_blocks
    test_redup_finds_intent_duplicate_groups()
    test_duplicate_contracts_cli_parity(tmp_path)
    test_find_intent_duplicate_groups_from_blocks()
  tests/test_language_analyzers.py:
    e: test_typescript_block_extent_finds_async_function,test_block_extent_uses_typescript_analyzer_for_ts_files,test_csharp_block_extent_finds_method,test_block_extent_uses_csharp_analyzer,test_java_block_extent,test_go_block_extent,test_rust_block_extent,test_rust_decorator_block_extent,test_block_extent_routes_java_go_rust
    test_typescript_block_extent_finds_async_function()
    test_block_extent_uses_typescript_analyzer_for_ts_files()
    test_csharp_block_extent_finds_method()
    test_block_extent_uses_csharp_analyzer()
    test_java_block_extent()
    test_go_block_extent()
    test_rust_block_extent()
    test_rust_decorator_block_extent()
    test_block_extent_routes_java_go_rust()
  tests/test_manifest.py:
    e: test_load_manifest_records
    test_load_manifest_records(tmp_path)
  tests/test_manifest_ops.py:
    e: test_contract_line_to_manifest_entry_parses_ui_line,test_apply_ledger_to_manifest_adds_only_evolved,test_apply_ledger_to_manifests_both_targets
    test_contract_line_to_manifest_entry_parses_ui_line()
    test_apply_ledger_to_manifest_adds_only_evolved(tmp_path)
    test_apply_ledger_to_manifests_both_targets(tmp_path)
  tests/test_markdown_generator_example.py:
    e: _load_pass_generator,test_markdown_generator_pass_validates_and_generates_required_format,test_markdown_generator_violation_flags_forbidden_effects,test_markdown_guard_rejects_topic_drift_and_html_format,test_markdown_generator_demo_script_runs
    _load_pass_generator()
    test_markdown_generator_pass_validates_and_generates_required_format()
    test_markdown_generator_violation_flags_forbidden_effects()
    test_markdown_guard_rejects_topic_drift_and_html_format()
    test_markdown_generator_demo_script_runs()
  tests/test_mcp.py:
    e: test_tool_schema_lists_core_tools,test_initialize_response,test_tools_list_response,test_validate_intent_snippet_handler,test_validate_project_on_full_stack,test_tools_call_routes_handler
    test_tool_schema_lists_core_tools()
    test_initialize_response()
    test_tools_list_response()
    test_validate_intent_snippet_handler()
    test_validate_project_on_full_stack()
    test_tools_call_routes_handler()
  tests/test_new_modules.py:
    e: test_coverage,test_duplicates,test_graph_missing_requirement
    test_coverage(tmp_path)
    test_duplicates(tmp_path)
    test_graph_missing_requirement(tmp_path)
  tests/test_next_stage.py:
    e: test_manifest_schema_valid,test_parse_hunks,test_dockerfile_artifact_violation
    test_manifest_schema_valid(tmp_path)
    test_parse_hunks()
    test_dockerfile_artifact_violation(tmp_path)
  tests/test_parser.py:
    e: test_parse_full_contract_line,test_parse_comment_prefix_ts,test_parse_malformed_quoted_contract_returns_none,test_parse_decorator_matches_comment_intent_form,test_parse_uri_decorator_matches_comment_form,test_parse_rust_attribute_wrapper
    test_parse_full_contract_line()
    test_parse_comment_prefix_ts()
    test_parse_malformed_quoted_contract_returns_none()
    test_parse_decorator_matches_comment_intent_form()
    test_parse_uri_decorator_matches_comment_form()
    test_parse_rust_attribute_wrapper()
  tests/test_planfile_adapter.py:
    e: test_planfile_push_local_only,test_planfile_pull_reads_local_export,test_planfile_webhook_apply_updates_local_status,test_planfile_webhook_emit_delivers
    test_planfile_push_local_only(tmp_path)
    test_planfile_pull_reads_local_export(tmp_path)
    test_planfile_webhook_apply_updates_local_status(tmp_path)
    test_planfile_webhook_emit_delivers()
  tests/test_policy.py:
    e: test_missing_required_p1_fails_policy,test_full_stack_passes_without_p1_gate
    test_missing_required_p1_fails_policy(tmp_path)
    test_full_stack_passes_without_p1_gate()
  tests/test_proposals.py:
    e: test_propose_ui_delta_delete_and_keep
    test_propose_ui_delta_delete_and_keep()
  tests/test_python_ast.py:
    e: test_python_function_extent_finds_async_def,test_python_block_extent_includes_decorators_and_imports,test_block_extent_uses_ast_for_python_files
    test_python_function_extent_finds_async_def()
    test_python_block_extent_includes_decorators_and_imports()
    test_block_extent_uses_ast_for_python_files()
  tests/test_redup_policy.py:
    e: test_validate_for_redup_passes_full_stack,test_validate_for_redup_fails_on_intent_duplicate,test_parse_policy_tokens_csv
    test_validate_for_redup_passes_full_stack()
    test_validate_for_redup_fails_on_intent_duplicate()
    test_parse_policy_tokens_csv()
  tests/test_rule_registry.py:
    e: test_rule_registry_lists_builtin_rules,test_rule_registry_reports_per_rule_status,test_rule_registry_discovers_entry_points,test_custom_rule_can_be_registered
    test_rule_registry_lists_builtin_rules()
    test_rule_registry_reports_per_rule_status()
    test_rule_registry_discovers_entry_points()
    test_custom_rule_can_be_registered()
  tests/test_scan_artifacts.py:
    e: test_discover_dockerfile,test_scan_all_artifacts_reports_violation
    test_discover_dockerfile(tmp_path)
    test_scan_all_artifacts_reports_violation(tmp_path)
  tests/test_staged_e2e.py:
    e: _subprocess_env,_git,test_staged_hunk_check_fails_on_network_violation,test_staged_hunk_check_passes_clean_contract
    _subprocess_env()
    _git(cwd)
    test_staged_hunk_check_fails_on_network_violation(tmp_path)
    test_staged_hunk_check_passes_clean_contract(tmp_path)
  tests/test_toon.py:
    e: test_parse_toon_uri_line,test_parse_toon_uri_line_without_scheme,test_parse_toon_uri_line_id_fallback_without_intent,test_load_toon_records
    test_parse_toon_uri_line()
    test_parse_toon_uri_line_without_scheme()
    test_parse_toon_uri_line_id_fallback_without_intent()
    test_load_toon_records(tmp_path)
  tests/test_validate_snippet.py:
    e: test_validate_artifact_with_proposals_passes_minimal_html
    test_validate_artifact_with_proposals_passes_minimal_html()
  tests/test_validation.py:
    e: test_python_contract_passes,test_typescript_contract_detects_network_violation
    test_python_contract_passes()
    test_typescript_contract_detects_network_violation()
  tests/test_vallm_integration.py:
    e: test_validate_for_vallm_web_app_v1_pass,test_validate_proposal_maps_violation
    test_validate_for_vallm_web_app_v1_pass()
    test_validate_proposal_maps_violation()
  tests/test_web_app.py:
    e: test_web_app_v1_overall_pass,test_web_app_v2_has_network_violations,test_web_app_graph_has_no_missing_requires
    test_web_app_v1_overall_pass()
    test_web_app_v2_has_network_violations()
    test_web_app_graph_has_no_missing_requires()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('intract', '0.5.12', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 119, 'less').
project_file('examples/full-stack/src/analyzer.py', 4, 'python').
project_file('examples/full-stack/src/parser_a.py', 4, 'python').
project_file('examples/full-stack/src/parser_b.py', 4, 'python').
project_file('examples/full-stack/src/scanner.py', 5, 'python').
project_file('examples/integration_tests/01_python_pass/app.py', 9, 'python').
project_file('examples/integration_tests/02_typescript_violation_planfile/permission.ts', 7, 'typescript').
project_file('examples/integration_tests/03_watch_engine_drift/reporter.py', 5, 'python').
project_file('examples/integration_tests/03_watch_engine_drift/scanner.py', 9, 'python').
project_file('examples/integration_tests/run_examples.py', 118, 'python').
project_file('examples/markdown-generator/demo.py', 69, 'python').
project_file('examples/markdown-generator/pass/generator.py', 83, 'python').
project_file('examples/markdown-generator/run-demo.sh', 8, 'shell').
project_file('examples/markdown-generator/violation/generator.py', 77, 'python').
project_file('examples/python/parse_extensions.py', 9, 'python').
project_file('examples/showcase/server.py', 143, 'python').
project_file('examples/toon/src/auth.js', 17, 'javascript').
project_file('examples/toon/src/calc.py', 16, 'python').
project_file('examples/toon/validate.sh', 24, 'shell').
project_file('examples/typescript/permission.ts', 6, 'typescript').
project_file('examples/web-app/iterations/v1-pass/backend/auth.py', 6, 'python').
project_file('examples/web-app/iterations/v1-pass/backend/routes.py', 5, 'python').
project_file('examples/web-app/iterations/v1-pass/frontend/dashboard.ts', 9, 'typescript').
project_file('examples/web-app/iterations/v2-violation/backend/auth.py', 7, 'python').
project_file('examples/web-app/iterations/v2-violation/backend/routes.py', 5, 'python').
project_file('examples/web-app/iterations/v2-violation/frontend/dashboard.ts', 11, 'typescript').
project_file('examples/web-app/run-demo.sh', 21, 'shell').
project_file('extensions/vscode-intract/extension.js', 52, 'javascript').
project_file('project.sh', 50, 'shell').
project_file('scripts/ci-full-stack.sh', 77, 'shell').
project_file('scripts/generate_toon_from_map.py', 476, 'python').
project_file('sdks/go/examples/main.go', 23, 'go').
project_file('sdks/go/intractsdk/sdk.go', 69, 'go').
project_file('sdks/python/src/intract_plugin_example/__init__.py', 27, 'python').
project_file('sdks/rust/src/lib.rs', 55, 'rust').
project_file('sdks/typescript/examples/basic.ts', 14, 'typescript').
project_file('sdks/typescript/intract.config.ts', 9, 'typescript').
project_file('sdks/typescript/src/index.ts', 43, 'typescript').
project_file('src/intract/__init__.py', 60, 'python').
project_file('src/intract/__main__.py', 5, 'python').
project_file('src/intract/analyzers/__init__.py', 21, 'python').
project_file('src/intract/analyzers/blocks.py', 47, 'python').
project_file('src/intract/analyzers/csharp.py', 66, 'python').
project_file('src/intract/analyzers/go.py', 14, 'python').
project_file('src/intract/analyzers/java.py', 28, 'python').
project_file('src/intract/analyzers/python_ast.py', 71, 'python').
project_file('src/intract/analyzers/rust.py', 16, 'python').
project_file('src/intract/analyzers/treesitter.py', 63, 'python').
project_file('src/intract/analyzers/typescript.py', 67, 'python').
project_file('src/intract/artifacts.py', 6, 'python').
project_file('src/intract/check.py', 298, 'python').
project_file('src/intract/cli.py', 684, 'python').
project_file('src/intract/config.py', 65, 'python').
project_file('src/intract/core/__init__.py', 36, 'python').
project_file('src/intract/core/artifact.py', 133, 'python').
project_file('src/intract/core/cache.py', 100, 'python').
project_file('src/intract/core/models.py', 155, 'python').
project_file('src/intract/core/normalizer.py', 70, 'python').
project_file('src/intract/core/registry.py', 7, 'python').
project_file('src/intract/core/signatures.py', 123, 'python').
project_file('src/intract/coverage.py', 35, 'python').
project_file('src/intract/duplicates/__init__.py', 16, 'python').
project_file('src/intract/duplicates/grouping.py', 139, 'python').
project_file('src/intract/duplicates/matcher.py', 56, 'python').
project_file('src/intract/duplicates/scoring.py', 38, 'python').
project_file('src/intract/duplicates.py', 6, 'python').
project_file('src/intract/effects.py', 6, 'python').
project_file('src/intract/engine/__init__.py', 22, 'python').
project_file('src/intract/engine/analyzer.py', 86, 'python').
project_file('src/intract/engine/assigner.py', 110, 'python').
project_file('src/intract/engine/context.py', 37, 'python').
project_file('src/intract/engine/drift.py', 114, 'python').
project_file('src/intract/engine/monitor.py', 33, 'python').
project_file('src/intract/engine/scanner.py', 54, 'python').
project_file('src/intract/git.py', 54, 'python').
project_file('src/intract/graph.py', 69, 'python').
project_file('src/intract/integrations/__init__.py', 45, 'python').
project_file('src/intract/integrations/nexu.py', 190, 'python').
project_file('src/intract/integrations/planfile.py', 142, 'python').
project_file('src/intract/integrations/planfile_adapter.py', 256, 'python').
project_file('src/intract/integrations/redup.py', 288, 'python').
project_file('src/intract/integrations/vallm.py', 117, 'python').
project_file('src/intract/manifest_ops.py', 244, 'python').
project_file('src/intract/manifest_schema.py', 117, 'python').
project_file('src/intract/mcp/__init__.py', 22, 'python').
project_file('src/intract/mcp/handlers.py', 125, 'python').
project_file('src/intract/mcp/schemas.py', 92, 'python').
project_file('src/intract/mcp/server.py', 119, 'python').
project_file('src/intract/mcp_server.py', 7, 'python').
project_file('src/intract/models.py', 4, 'python').
project_file('src/intract/normalizer.py', 4, 'python').
project_file('src/intract/parser.py', 4, 'python').
project_file('src/intract/parsers/__init__.py', 14, 'python').
project_file('src/intract/parsers/inline.py', 336, 'python').
project_file('src/intract/parsers/manifest.py', 178, 'python').
project_file('src/intract/parsers/openapi.py', 64, 'python').
project_file('src/intract/parsers/toon.py', 170, 'python').
project_file('src/intract/plugins/__init__.py', 25, 'python').
project_file('src/intract/plugins/base.py', 110, 'python').
project_file('src/intract/plugins/builtins.py', 112, 'python').
project_file('src/intract/plugins/manager.py', 62, 'python').
project_file('src/intract/policy.py', 107, 'python').
project_file('src/intract/project.py', 168, 'python').
project_file('src/intract/proposals.py', 101, 'python').
project_file('src/intract/propose_llm.py', 167, 'python').
project_file('src/intract/reporters/__init__.py', 1, 'python').
project_file('src/intract/reporters/sarif.py', 63, 'python').
project_file('src/intract/scan_artifacts.py', 71, 'python').
project_file('src/intract/sdk.py', 48, 'python').
project_file('src/intract/signature.py', 4, 'python').
project_file('src/intract/validate_snippet.py', 29, 'python').
project_file('src/intract/validation.py', 14, 'python').
project_file('src/intract/validators/__init__.py', 22, 'python').
project_file('src/intract/validators/artifacts.py', 182, 'python').
project_file('src/intract/validators/base.py', 51, 'python').
project_file('src/intract/validators/effects.py', 53, 'python').
project_file('src/intract/validators/engine.py', 55, 'python').
project_file('src/intract/validators/input_output.py', 75, 'python').
project_file('src/intract/validators/registry.py', 86, 'python').
project_file('src/intract/validators/requirements.py', 14, 'python').
project_file('src/intract/watch.py', 161, 'python').
project_file('src/intract/yaml_manifest.py', 4, 'python').
project_file('tests/test_cache.py', 36, 'python').
project_file('tests/test_check_staged.py', 35, 'python').
project_file('tests/test_full_stack.py', 28, 'python').
project_file('tests/test_generate_toon_from_map.py', 97, 'python').
project_file('tests/test_hunk_filter.py', 89, 'python').
project_file('tests/test_integrations.py', 61, 'python').
project_file('tests/test_language_analyzers.py', 117, 'python').
project_file('tests/test_manifest.py', 27, 'python').
project_file('tests/test_manifest_ops.py', 107, 'python').
project_file('tests/test_markdown_generator_example.py', 79, 'python').
project_file('tests/test_mcp.py', 63, 'python').
project_file('tests/test_new_modules.py', 49, 'python').
project_file('tests/test_next_stage.py', 37, 'python').
project_file('tests/test_parser.py', 77, 'python').
project_file('tests/test_planfile_adapter.py', 98, 'python').
project_file('tests/test_policy.py', 46, 'python').
project_file('tests/test_proposals.py', 18, 'python').
project_file('tests/test_python_ast.py', 38, 'python').
project_file('tests/test_redup_policy.py', 41, 'python').
project_file('tests/test_rule_registry.py', 53, 'python').
project_file('tests/test_scan_artifacts.py', 20, 'python').
project_file('tests/test_staged_e2e.py', 79, 'python').
project_file('tests/test_toon.py', 61, 'python').
project_file('tests/test_validate_snippet.py', 17, 'python').
project_file('tests/test_validation.py', 40, 'python').
project_file('tests/test_vallm_integration.py', 30, 'python').
project_file('tests/test_web_app.py', 32, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/full-stack/src/analyzer.py', 'detect_duplicates', 1, 1, 1).
python_function('examples/full-stack/src/parser_a.py', 'parse_extensions', 1, 3, 2).
python_function('examples/full-stack/src/parser_b.py', 'load_extension_list', 1, 1, 1).
python_function('examples/full-stack/src/scanner.py', 'scan_project_files', 1, 1, 1).
python_function('examples/integration_tests/01_python_pass/app.py', 'parse_extensions', 1, 3, 3).
python_function('examples/integration_tests/03_watch_engine_drift/reporter.py', 'render_summary', 1, 1, 1).
python_function('examples/integration_tests/03_watch_engine_drift/scanner.py', 'collect_project_files', 1, 3, 2).
python_function('examples/integration_tests/run_examples.py', 'print_result', 2, 1, 2).
python_function('examples/integration_tests/run_examples.py', 'run_example_01', 1, 1, 2).
python_function('examples/integration_tests/run_examples.py', 'run_example_02', 1, 2, 8).
python_function('examples/integration_tests/run_examples.py', 'run_example_03', 1, 2, 12).
python_function('examples/integration_tests/run_examples.py', 'run_example_04', 1, 1, 2).
python_function('examples/integration_tests/run_examples.py', 'main', 0, 10, 9).
python_function('examples/markdown-generator/demo.py', '_validate_project', 2, 2, 3).
python_function('examples/markdown-generator/demo.py', '_load_pass_generator', 0, 3, 4).
python_function('examples/markdown-generator/demo.py', '_violation_messages', 1, 4, 1).
python_function('examples/markdown-generator/demo.py', 'main', 0, 4, 6).
python_function('examples/markdown-generator/pass/generator.py', 'normalize_topic', 1, 2, 4).
python_function('examples/markdown-generator/pass/generator.py', 'build_markdown_outline', 2, 3, 1).
python_function('examples/markdown-generator/pass/generator.py', 'render_markdown_sections', 3, 2, 0).
python_function('examples/markdown-generator/pass/generator.py', 'guard_markdown_contract', 3, 4, 5).
python_function('examples/markdown-generator/pass/generator.py', 'generate_markdown_document', 2, 2, 5).
python_function('examples/markdown-generator/violation/generator.py', 'normalize_topic', 1, 2, 4).
python_function('examples/markdown-generator/violation/generator.py', 'build_markdown_outline', 2, 3, 4).
python_function('examples/markdown-generator/violation/generator.py', 'render_markdown_sections', 3, 2, 2).
python_function('examples/markdown-generator/violation/generator.py', 'guard_markdown_contract', 3, 3, 4).
python_function('examples/markdown-generator/violation/generator.py', 'generate_markdown_document', 2, 2, 5).
python_function('examples/python/parse_extensions.py', 'parse_extensions', 1, 3, 3).
python_function('examples/showcase/server.py', 'load_env_file', 1, 6, 6).
python_function('examples/showcase/server.py', 'resolve_runtime_config', 0, 4, 4).
python_function('examples/showcase/server.py', 'main', 0, 1, 6).
python_function('examples/toon/src/calc.py', 'add', 2, 1, 0).
python_function('examples/toon/src/calc.py', 'divide', 2, 2, 1).
python_function('examples/toon/src/calc.py', 'write_to_log', 1, 1, 2).
python_function('examples/web-app/iterations/v1-pass/backend/auth.py', 'check_permission', 2, 2, 1).
python_function('examples/web-app/iterations/v1-pass/backend/routes.py', 'read_profile', 2, 1, 1).
python_function('examples/web-app/iterations/v2-violation/backend/auth.py', 'check_permission', 2, 1, 1).
python_function('examples/web-app/iterations/v2-violation/backend/routes.py', 'read_profile', 2, 1, 1).
python_function('scripts/generate_toon_from_map.py', '_slug', 1, 2, 3).
python_function('scripts/generate_toon_from_map.py', '_parse_intent_from_name', 1, 5, 6).
python_function('scripts/generate_toon_from_map.py', '_iter_section_lines', 1, 6, 1).
python_function('scripts/generate_toon_from_map.py', '_parse_modules', 1, 4, 5).
python_function('scripts/generate_toon_from_map.py', '_extract_symbol_names', 1, 5, 4).
python_function('scripts/generate_toon_from_map.py', '_parse_functions', 1, 9, 11).
python_function('scripts/generate_toon_from_map.py', '_contract_fragment', 0, 5, 4).
python_function('scripts/generate_toon_from_map.py', '_toon_uri', 1, 2, 1).
python_function('scripts/generate_toon_from_map.py', '_llm_contract_fragment', 0, 8, 6).
python_function('scripts/generate_toon_from_map.py', '_resolve_output_profile', 1, 3, 1).
python_function('scripts/generate_toon_from_map.py', '_effective_include', 0, 2, 0).
python_function('scripts/generate_toon_from_map.py', '_default_function_fragment', 0, 2, 3).
python_function('scripts/generate_toon_from_map.py', '_function_fragment', 0, 3, 2).
python_function('scripts/generate_toon_from_map.py', 'generate_toon_lines', 0, 6, 13).
python_function('scripts/generate_toon_from_map.py', '_build_parser', 0, 1, 4).
python_function('scripts/generate_toon_from_map.py', '_run_validate', 2, 1, 3).
python_function('scripts/generate_toon_from_map.py', '_ensure_parent', 1, 3, 2).
python_function('scripts/generate_toon_from_map.py', 'main', 1, 5, 12).
python_function('src/intract/analyzers/blocks.py', 'scan_braced_block', 2, 8, 2).
python_function('src/intract/analyzers/blocks.py', 'block_extent_from_patterns', 3, 7, 6).
python_function('src/intract/analyzers/csharp.py', 'csharp_block_extent', 2, 8, 6).
python_function('src/intract/analyzers/csharp.py', '_scan_braced_block', 2, 8, 2).
python_function('src/intract/analyzers/csharp.py', '_treesitter_csharp_extent', 2, 2, 1).
python_function('src/intract/analyzers/go.py', 'go_block_extent', 2, 1, 1).
python_function('src/intract/analyzers/java.py', 'java_block_extent', 2, 4, 6).
python_function('src/intract/analyzers/python_ast.py', '_decorator_lines', 1, 3, 2).
python_function('src/intract/analyzers/python_ast.py', 'python_function_extent', 2, 8, 7).
python_function('src/intract/analyzers/python_ast.py', 'python_block_extent', 2, 14, 7).
python_function('src/intract/analyzers/rust.py', 'rust_block_extent', 2, 1, 1).
python_function('src/intract/analyzers/treesitter.py', '_load_parser', 1, 3, 4).
python_function('src/intract/analyzers/treesitter.py', '_find_extent', 4, 7, 8).
python_function('src/intract/analyzers/treesitter.py', 'typescript_function_extent', 2, 1, 1).
python_function('src/intract/analyzers/treesitter.py', 'csharp_method_extent', 2, 1, 1).
python_function('src/intract/analyzers/typescript.py', 'typescript_block_extent', 2, 7, 6).
python_function('src/intract/analyzers/typescript.py', '_scan_braced_block', 2, 11, 4).
python_function('src/intract/analyzers/typescript.py', '_treesitter_typescript_extent', 2, 2, 1).
python_function('src/intract/check.py', 'parse_unified_diff_hunks', 1, 6, 9).
python_function('src/intract/check.py', 'load_selected_sources', 2, 5, 4).
python_function('src/intract/check.py', '_manifest_changed', 1, 2, 2).
python_function('src/intract/check.py', 'changed_lines_by_file', 1, 4, 4).
python_function('src/intract/check.py', '_language_block_extent', 3, 3, 5).
python_function('src/intract/check.py', '_is_python_declaration', 1, 1, 1).
python_function('src/intract/check.py', '_is_fallback_preamble', 1, 3, 1).
python_function('src/intract/check.py', '_fallback_block_extent', 2, 11, 7).
python_function('src/intract/check.py', 'block_extent', 2, 2, 2).
python_function('src/intract/check.py', 'signature_touched', 3, 2, 4).
python_function('src/intract/check.py', 'validate_sources_for_hunks', 3, 14, 14).
python_function('src/intract/check.py', 'validate_selected_paths', 2, 8, 7).
python_function('src/intract/check.py', 'staged_check', 1, 4, 7).
python_function('src/intract/check.py', 'changed_check', 1, 1, 4).
python_function('src/intract/cli.py', 'main', 1, 2, 4).
python_function('src/intract/cli.py', 'init', 2, 3, 9).
python_function('src/intract/cli.py', '_print_artifact_scan_report', 1, 3, 2).
python_function('src/intract/cli.py', '_scan_artifacts', 1, 3, 6).
python_function('src/intract/cli.py', '_is_scan_candidate', 1, 2, 1).
python_function('src/intract/cli.py', '_scan_contract_file', 1, 2, 2).
python_function('src/intract/cli.py', '_scan_inline_records', 1, 5, 7).
python_function('src/intract/cli.py', '_scan_row', 1, 1, 0).
python_function('src/intract/cli.py', '_print_scan_table', 1, 2, 5).
python_function('src/intract/cli.py', 'scan', 3, 4, 10).
python_function('src/intract/cli.py', 'validate', 4, 3, 10).
python_function('src/intract/cli.py', 'check', 9, 13, 21).
python_function('src/intract/cli.py', 'coverage', 2, 2, 9).
python_function('src/intract/cli.py', 'duplicates', 3, 4, 13).
python_function('src/intract/cli.py', 'graph', 4, 5, 12).
python_function('src/intract/cli.py', 'tickets', 2, 1, 7).
python_function('src/intract/cli.py', 'planfile_push', 5, 1, 9).
python_function('src/intract/cli.py', 'planfile_pull', 5, 3, 11).
python_function('src/intract/cli.py', 'planfile_sync', 5, 1, 9).
python_function('src/intract/cli.py', 'planfile_webhook_test', 2, 1, 6).
python_function('src/intract/cli.py', 'planfile_webhook_apply', 2, 1, 9).
python_function('src/intract/cli.py', 'watch', 6, 3, 16).
python_function('src/intract/cli.py', 'engine_suggest', 2, 3, 14).
python_function('src/intract/cli.py', 'engine_drift', 3, 4, 14).
python_function('src/intract/cli.py', 'engine_run', 4, 4, 13).
python_function('src/intract/cli.py', '_export_tickets', 2, 1, 6).
python_function('src/intract/cli.py', '_print_validation_report', 1, 4, 7).
python_function('src/intract/cli.py', '_format_check_text', 3, 7, 4).
python_function('src/intract/cli.py', 'check_manifest', 2, 4, 10).
python_function('src/intract/cli.py', 'artifact_validate', 2, 4, 8).
python_function('src/intract/cli.py', 'propose_delta', 5, 4, 7).
python_function('src/intract/cli.py', 'propose_llm_cmd', 4, 6, 10).
python_function('src/intract/cli.py', 'manifest_apply_ledger', 7, 10, 13).
python_function('src/intract/config.py', 'load_config', 1, 11, 10).
python_function('src/intract/core/artifact.py', 'infer_language', 1, 1, 3).
python_function('src/intract/core/artifact.py', '_kind_from_filename', 3, 10, 2).
python_function('src/intract/core/artifact.py', '_kind_from_structured_content', 2, 7, 1).
python_function('src/intract/core/artifact.py', 'infer_artifact_kind', 2, 3, 4).
python_function('src/intract/core/normalizer.py', 'normalize_label', 1, 7, 10).
python_function('src/intract/core/normalizer.py', 'normalize_action', 1, 4, 2).
python_function('src/intract/core/normalizer.py', 'normalize_many', 1, 4, 3).
python_function('src/intract/core/normalizer.py', 'normalize_requirement', 1, 6, 8).
python_function('src/intract/core/signatures.py', 'make_block_id', 4, 1, 3).
python_function('src/intract/core/signatures.py', '_normalize_contract', 1, 2, 6).
python_function('src/intract/core/signatures.py', '_add_feature_values', 3, 2, 1).
python_function('src/intract/core/signatures.py', '_signature_features', 2, 2, 2).
python_function('src/intract/core/signatures.py', '_exact_hash', 1, 1, 5).
python_function('src/intract/core/signatures.py', '_block_id', 1, 2, 1).
python_function('src/intract/core/signatures.py', 'build_signature', 1, 3, 6).
python_function('src/intract/core/signatures.py', 'build_signatures', 1, 2, 1).
python_function('src/intract/coverage.py', 'calculate_coverage', 1, 3, 8).
python_function('src/intract/duplicates/grouping.py', 'union_find_groups', 1, 5, 7).
python_function('src/intract/duplicates/grouping.py', 'pairs_to_duplicate_contracts', 2, 3, 6).
python_function('src/intract/duplicates/grouping.py', 'pairs_to_intent_groups', 2, 6, 13).
python_function('src/intract/duplicates/grouping.py', 'find_duplicate_contracts', 2, 2, 5).
python_function('src/intract/duplicates/matcher.py', 'bucket_signatures', 1, 2, 2).
python_function('src/intract/duplicates/matcher.py', 'find_intent_pairs', 2, 6, 6).
python_function('src/intract/duplicates/scoring.py', 'jaccard', 2, 5, 1).
python_function('src/intract/duplicates/scoring.py', 'object_similarity', 2, 2, 3).
python_function('src/intract/duplicates/scoring.py', 'score_similarity', 2, 5, 4).
python_function('src/intract/engine/analyzer.py', '_line_number', 2, 1, 1).
python_function('src/intract/engine/analyzer.py', '_fragment_id', 5, 1, 3).
python_function('src/intract/engine/analyzer.py', '_slice_until_next_match', 3, 3, 2).
python_function('src/intract/engine/analyzer.py', 'analyze_source_units', 1, 12, 11).
python_function('src/intract/engine/assigner.py', '_split_name', 1, 3, 3).
python_function('src/intract/engine/assigner.py', '_infer_action', 2, 10, 5).
python_function('src/intract/engine/assigner.py', '_infer_object', 2, 4, 2).
python_function('src/intract/engine/assigner.py', '_infer_effects', 1, 8, 2).
python_function('src/intract/engine/assigner.py', 'suggest_contract_for_fragment', 1, 3, 5).
python_function('src/intract/engine/assigner.py', 'suggest_contracts_for_fragments', 1, 4, 1).
python_function('src/intract/engine/drift.py', 'hash_text', 1, 1, 3).
python_function('src/intract/engine/drift.py', 'state_from_fragments', 1, 2, 2).
python_function('src/intract/engine/drift.py', 'save_state', 2, 2, 7).
python_function('src/intract/engine/drift.py', 'load_state', 1, 3, 6).
python_function('src/intract/engine/drift.py', 'detect_drift', 2, 5, 5).
python_function('src/intract/engine/monitor.py', 'scan_suggest_and_validate', 1, 4, 9).
python_function('src/intract/engine/scanner.py', 'collect_source_units', 1, 9, 12).
python_function('src/intract/git.py', '_run_git', 2, 2, 2).
python_function('src/intract/git.py', 'staged_files', 1, 4, 7).
python_function('src/intract/git.py', 'changed_files', 2, 4, 7).
python_function('src/intract/git.py', 'staged_hunks', 2, 2, 2).
python_function('src/intract/git.py', 'paths_from_changes', 1, 2, 1).
python_function('src/intract/graph.py', '_safe', 1, 3, 2).
python_function('src/intract/graph.py', 'build_graph', 2, 9, 14).
python_function('src/intract/integrations/nexu.py', 'format_intract_v1_line', 1, 3, 1).
python_function('src/intract/integrations/nexu.py', 'parse_intract_line', 1, 9, 7).
python_function('src/intract/integrations/nexu.py', 'scan_contracts_in_text', 1, 3, 4).
python_function('src/intract/integrations/nexu.py', 'scan_contracts_in_file', 2, 3, 4).
python_function('src/intract/integrations/nexu.py', '_contract_items', 1, 4, 2).
python_function('src/intract/integrations/nexu.py', '_list_field', 2, 2, 2).
python_function('src/intract/integrations/nexu.py', '_base_intent_contract', 2, 2, 5).
python_function('src/intract/integrations/nexu.py', 'read_manifest_contracts', 1, 4, 5).
python_function('src/intract/integrations/nexu.py', '_read_yaml_mapping', 1, 4, 3).
python_function('src/intract/integrations/nexu.py', '_toon_target', 1, 3, 2).
python_function('src/intract/integrations/nexu.py', '_target_line_value', 1, 2, 2).
python_function('src/intract/integrations/nexu.py', '_toon_intent_contract', 2, 5, 5).
python_function('src/intract/integrations/nexu.py', 'read_toon_manifest_contracts', 1, 4, 4).
python_function('src/intract/integrations/planfile.py', '_severity_from_status', 1, 4, 0).
python_function('src/intract/integrations/planfile.py', 'tickets_from_report', 1, 11, 8).
python_function('src/intract/integrations/planfile_adapter.py', '_ticket_from_dict', 1, 2, 5).
python_function('src/intract/integrations/planfile_adapter.py', '_default_created_at', 0, 1, 2).
python_function('src/intract/integrations/redup.py', 'block_text', 1, 4, 1).
python_function('src/intract/integrations/redup.py', 'block_file_path', 1, 3, 2).
python_function('src/intract/integrations/redup.py', 'block_start_line', 1, 3, 2).
python_function('src/intract/integrations/redup.py', 'block_end_line', 1, 3, 3).
python_function('src/intract/integrations/redup.py', 'signatures_from_text', 1, 1, 2).
python_function('src/intract/integrations/redup.py', 'signatures_from_blocks', 1, 5, 6).
python_function('src/intract/integrations/redup.py', 'signatures_from_manifest', 1, 1, 3).
python_function('src/intract/integrations/redup.py', '_with_block_lines', 2, 1, 3).
python_function('src/intract/integrations/redup.py', 'find_intent_duplicate_groups', 1, 8, 8).
python_function('src/intract/integrations/redup.py', 'parse_policy_tokens', 1, 7, 4).
python_function('src/intract/integrations/redup.py', '_resolve_manifest_path', 3, 3, 2).
python_function('src/intract/integrations/redup.py', '_graph_for_policy', 3, 3, 1).
python_function('src/intract/integrations/redup.py', '_intent_duplicate_label', 1, 2, 2).
python_function('src/intract/integrations/redup.py', '_duplicate_reasons', 1, 2, 1).
python_function('src/intract/integrations/redup.py', '_apply_duplicate_policy', 2, 5, 4).
python_function('src/intract/integrations/redup.py', 'validate_for_redup', 1, 4, 12).
python_function('src/intract/integrations/redup.py', 'scan_blocks_for_intent_duplicates', 1, 2, 4).
python_function('src/intract/integrations/vallm.py', 'map_validation_result', 1, 6, 3).
python_function('src/intract/integrations/vallm.py', 'map_project_report', 1, 7, 3).
python_function('src/intract/integrations/vallm.py', 'validate_for_vallm', 1, 2, 3).
python_function('src/intract/integrations/vallm.py', 'validate_proposal', 1, 12, 8).
python_function('src/intract/manifest_ops.py', 'load_manifest_document', 1, 5, 6).
python_function('src/intract/manifest_ops.py', 'write_manifest_document', 2, 1, 3).
python_function('src/intract/manifest_ops.py', 'contract_line_to_manifest_entry', 1, 13, 5).
python_function('src/intract/manifest_ops.py', 'load_policy_ledger', 1, 6, 5).
python_function('src/intract/manifest_ops.py', 'resolve_manifest_paths', 0, 5, 1).
python_function('src/intract/manifest_ops.py', '_existing_contract_ids', 1, 4, 4).
python_function('src/intract/manifest_ops.py', '_should_apply_ledger_entry', 1, 2, 2).
python_function('src/intract/manifest_ops.py', '_iter_ledger_proposals', 1, 6, 4).
python_function('src/intract/manifest_ops.py', '_append_manifest_proposal', 4, 5, 6).
python_function('src/intract/manifest_ops.py', 'apply_ledger_to_manifest', 2, 4, 7).
python_function('src/intract/manifest_ops.py', 'apply_ledger_to_manifests', 0, 2, 4).
python_function('src/intract/manifest_schema.py', '_load_schema', 0, 2, 5).
python_function('src/intract/manifest_schema.py', '_manifest_report', 2, 1, 2).
python_function('src/intract/manifest_schema.py', '_invalid_manifest_report', 2, 1, 3).
python_function('src/intract/manifest_schema.py', '_load_manifest_data', 1, 3, 3).
python_function('src/intract/manifest_schema.py', '_jsonschema_issues', 1, 5, 8).
python_function('src/intract/manifest_schema.py', '_fallback_issues', 1, 9, 5).
python_function('src/intract/manifest_schema.py', 'validate_manifest', 1, 4, 7).
python_function('src/intract/mcp/handlers.py', '_resolve_path', 1, 1, 4).
python_function('src/intract/mcp/handlers.py', '_resolve_manifest', 2, 4, 6).
python_function('src/intract/mcp/handlers.py', 'handle_validate_project', 1, 1, 5).
python_function('src/intract/mcp/handlers.py', 'handle_validate_staged', 1, 4, 10).
python_function('src/intract/mcp/handlers.py', 'handle_validate_intent_snippet', 1, 1, 4).
python_function('src/intract/mcp/handlers.py', 'handle_find_duplicates', 1, 2, 7).
python_function('src/intract/mcp/handlers.py', 'handle_build_graph', 1, 1, 5).
python_function('src/intract/mcp/handlers.py', 'handle_scan_artifacts', 1, 1, 4).
python_function('src/intract/mcp/handlers.py', 'handle_project_info', 1, 1, 5).
python_function('src/intract/mcp/server.py', 'handle_initialize', 1, 1, 0).
python_function('src/intract/mcp/server.py', 'handle_tools_list', 1, 2, 1).
python_function('src/intract/mcp/server.py', 'handle_tools_call', 2, 4, 1).
python_function('src/intract/mcp/server.py', 'handle_request', 1, 5, 4).
python_function('src/intract/mcp/server.py', 'run_server', 0, 5, 8).
python_function('src/intract/parsers/inline.py', 'clean_comment_line', 1, 12, 4).
python_function('src/intract/parsers/inline.py', 'split_csv', 1, 6, 5).
python_function('src/intract/parsers/inline.py', 'parse_priority', 1, 5, 7).
python_function('src/intract/parsers/inline.py', 'parse_key_value', 1, 2, 4).
python_function('src/intract/parsers/inline.py', 'marker_payload', 1, 3, 3).
python_function('src/intract/parsers/inline.py', 'extract_intract_uri', 1, 9, 6).
python_function('src/intract/parsers/inline.py', '_parse_uri_contract', 2, 6, 2).
python_function('src/intract/parsers/inline.py', '_set_intent', 3, 2, 2).
python_function('src/intract/parsers/inline.py', '_set_action', 3, 1, 0).
python_function('src/intract/parsers/inline.py', '_set_object', 3, 1, 0).
python_function('src/intract/parsers/inline.py', '_set_scope', 3, 2, 0).
python_function('src/intract/parsers/inline.py', '_set_priority', 3, 2, 4).
python_function('src/intract/parsers/inline.py', '_set_domain', 3, 1, 0).
python_function('src/intract/parsers/inline.py', '_set_contract_id', 3, 1, 0).
python_function('src/intract/parsers/inline.py', '_set_meaning', 3, 1, 0).
python_function('src/intract/parsers/inline.py', '_extend_list', 1, 1, 3).
python_function('src/intract/parsers/inline.py', '_add_relation', 3, 2, 2).
python_function('src/intract/parsers/inline.py', '_add_unknown_tag', 3, 1, 1).
python_function('src/intract/parsers/inline.py', '_parse_special_token', 2, 8, 4).
python_function('src/intract/parsers/inline.py', '_apply_key_value_pair', 3, 1, 2).
python_function('src/intract/parsers/inline.py', '_resolve_action_object', 1, 5, 2).
python_function('src/intract/parsers/inline.py', 'parse_contract_line', 1, 13, 12).
python_function('src/intract/parsers/inline.py', 'extract_contract_records_from_text', 1, 3, 5).
python_function('src/intract/parsers/manifest.py', '_to_tuple', 1, 9, 6).
python_function('src/intract/parsers/manifest.py', '_parse_intent', 1, 3, 2).
python_function('src/intract/parsers/manifest.py', 'contract_from_mapping', 1, 3, 7).
python_function('src/intract/parsers/manifest.py', '_target_mapping', 1, 3, 2).
python_function('src/intract/parsers/manifest.py', '_target_line', 1, 3, 4).
python_function('src/intract/parsers/manifest.py', '_target_tags', 1, 3, 3).
python_function('src/intract/parsers/manifest.py', '_with_target_tags', 2, 2, 2).
python_function('src/intract/parsers/manifest.py', '_top_level_contract_record', 3, 3, 7).
python_function('src/intract/parsers/manifest.py', '_top_level_contract_records', 2, 4, 4).
python_function('src/intract/parsers/manifest.py', '_file_contract_records', 1, 6, 7).
python_function('src/intract/parsers/manifest.py', 'load_manifest_records', 1, 4, 7).
python_function('src/intract/parsers/manifest.py', 'create_sample_manifest', 0, 1, 0).
python_function('src/intract/parsers/openapi.py', 'parse_openapi_contracts', 1, 8, 10).
python_function('src/intract/parsers/openapi.py', 'parse_openapi_text', 1, 8, 9).
python_function('src/intract/parsers/toon.py', '_parse_action_object_from_intent', 2, 8, 1).
python_function('src/intract/parsers/toon.py', '_extract_file_path', 1, 2, 0).
python_function('src/intract/parsers/toon.py', '_get_first', 3, 1, 1).
python_function('src/intract/parsers/toon.py', '_get_list', 2, 4, 5).
python_function('src/intract/parsers/toon.py', '_get_first_alias', 1, 3, 1).
python_function('src/intract/parsers/toon.py', '_get_list_alias', 1, 3, 1).
python_function('src/intract/parsers/toon.py', '_build_tags', 3, 3, 3).
python_function('src/intract/parsers/toon.py', '_start_line', 1, 2, 2).
python_function('src/intract/parsers/toon.py', '_priority', 1, 2, 3).
python_function('src/intract/parsers/toon.py', '_action_object', 1, 3, 3).
python_function('src/intract/parsers/toon.py', '_contract_from_uri', 2, 1, 9).
python_function('src/intract/parsers/toon.py', 'parse_toon_uri_line', 2, 3, 10).
python_function('src/intract/parsers/toon.py', 'load_toon_records', 1, 5, 6).
python_function('src/intract/plugins/manager.py', '_register_unique', 3, 3, 2).
python_function('src/intract/plugins/manager.py', 'load_builtin_plugins', 0, 1, 8).
python_function('src/intract/plugins/manager.py', 'discover_plugins', 0, 6, 6).
python_function('src/intract/policy.py', '_p1_missing_reasons', 2, 7, 6).
python_function('src/intract/policy.py', '_result_status', 1, 1, 2).
python_function('src/intract/policy.py', '_result_policy_line', 2, 1, 2).
python_function('src/intract/policy.py', '_collect_result_policy', 1, 5, 4).
python_function('src/intract/policy.py', '_invalid_manifest_reasons', 1, 3, 1).
python_function('src/intract/policy.py', '_missing_required_p1_reasons', 2, 4, 3).
python_function('src/intract/policy.py', 'decide_policy', 1, 6, 6).
python_function('src/intract/project.py', 'load_project_sources', 1, 9, 7).
python_function('src/intract/project.py', 'extract_signatures_from_sources', 1, 2, 4).
python_function('src/intract/project.py', '_validate_observed_signatures', 2, 2, 2).
python_function('src/intract/project.py', '_validate_manifest_signature', 3, 4, 4).
python_function('src/intract/project.py', '_validate_manifest_signatures', 3, 2, 2).
python_function('src/intract/project.py', '_project_status', 1, 9, 2).
python_function('src/intract/project.py', 'validate_sources', 1, 2, 6).
python_function('src/intract/project.py', 'validate_project', 1, 6, 7).
python_function('src/intract/proposals.py', '_ui_contract_line', 0, 1, 0).
python_function('src/intract/proposals.py', 'propose_ui_delta_contracts', 0, 9, 5).
python_function('src/intract/proposals.py', 'propose_ui_delta_contract_dicts', 0, 2, 2).
python_function('src/intract/propose_llm.py', '_extract_intract_lines', 1, 4, 5).
python_function('src/intract/propose_llm.py', '_lines_to_proposals', 1, 7, 6).
python_function('src/intract/propose_llm.py', '_load_litellm_completion', 0, 2, 1).
python_function('src/intract/propose_llm.py', '_resolve_model', 1, 4, 1).
python_function('src/intract/propose_llm.py', '_resolve_api_key', 1, 4, 2).
python_function('src/intract/propose_llm.py', '_build_prompt', 1, 2, 0).
python_function('src/intract/propose_llm.py', '_message_content_to_text', 1, 5, 4).
python_function('src/intract/propose_llm.py', '_strip_markdown_fence', 1, 2, 3).
python_function('src/intract/propose_llm.py', '_json_line_strings', 1, 5, 4).
python_function('src/intract/propose_llm.py', 'propose_contracts_llm', 1, 3, 12).
python_function('src/intract/reporters/sarif.py', 'report_to_sarif', 1, 11, 7).
python_function('src/intract/scan_artifacts.py', 'discover_artifact_paths', 1, 7, 10).
python_function('src/intract/scan_artifacts.py', 'scan_all_artifacts', 1, 3, 6).
python_function('src/intract/sdk.py', 'contract', 0, 1, 1).
python_function('src/intract/validate_snippet.py', 'validate_artifact_with_proposals', 2, 3, 7).
python_function('src/intract/validators/artifacts.py', 'validate_openapi', 1, 9, 11).
python_function('src/intract/validators/artifacts.py', 'validate_dockerfile', 1, 6, 7).
python_function('src/intract/validators/artifacts.py', 'validate_github_actions', 1, 8, 8).
python_function('src/intract/validators/artifacts.py', 'validate_kubernetes', 1, 8, 8).
python_function('src/intract/validators/artifacts.py', 'validate_artifact', 1, 9, 11).
python_function('src/intract/validators/base.py', 'merge_rule_results', 1, 2, 3).
python_function('src/intract/validators/effects.py', 'detect_effects', 1, 9, 4).
python_function('src/intract/validators/engine.py', 'validate_contract_against_source', 2, 8, 13).
python_function('src/intract/validators/input_output.py', 'contains_token_like', 2, 7, 4).
python_function('src/intract/validators/input_output.py', 'has_return_value', 1, 3, 2).
python_function('src/intract/validators/registry.py', '_discover_entry_point_rules', 0, 5, 5).
python_function('src/intract/validators/registry.py', 'get_rule_registry', 0, 6, 6).
python_function('src/intract/validators/requirements.py', 'validate_required_contracts', 2, 6, 1).
python_function('src/intract/watch.py', 'hash_file', 1, 2, 6).
python_function('src/intract/watch.py', 'should_scan', 3, 10, 5).
python_function('src/intract/watch.py', 'snapshot_tree', 2, 4, 9).
python_function('src/intract/watch.py', 'diff_snapshots', 2, 5, 4).
python_function('src/intract/watch.py', 'watch_tree', 2, 7, 6).
python_function('src/intract/watch.py', 'changes_to_paths', 1, 3, 1).
python_function('tests/test_cache.py', 'test_decision_cache_lifecycle', 1, 7, 4).
python_function('tests/test_check_staged.py', 'test_manifest_changed_helper', 0, 3, 1).
python_function('tests/test_check_staged.py', 'test_validate_selected_paths_full_graph', 1, 3, 3).
python_function('tests/test_full_stack.py', 'test_full_stack_validate_passes', 0, 2, 1).
python_function('tests/test_full_stack.py', 'test_full_stack_graph_covers_requires', 0, 4, 1).
python_function('tests/test_full_stack.py', 'test_full_stack_finds_intent_duplicates', 0, 5, 2).
python_function('tests/test_generate_toon_from_map.py', '_sample_map_text', 0, 1, 0).
python_function('tests/test_generate_toon_from_map.py', 'test_parse_modules_reads_m_section_entries', 0, 2, 3).
python_function('tests/test_generate_toon_from_map.py', 'test_parse_functions_extracts_symbols_and_skips_private', 0, 8, 3).
python_function('tests/test_generate_toon_from_map.py', 'test_generate_toon_lines_dev_profile_filters_project_and_shapes_functions', 1, 7, 4).
python_function('tests/test_generate_toon_from_map.py', 'test_generate_toon_lines_ci_security_profile_includes_project_and_security_validate', 1, 4, 4).
python_function('tests/test_hunk_filter.py', 'test_changed_lines_by_file', 0, 2, 2).
python_function('tests/test_hunk_filter.py', 'test_block_extent_finds_function_body', 0, 3, 1).
python_function('tests/test_hunk_filter.py', 'test_signature_touched_by_body_change', 0, 3, 3).
python_function('tests/test_hunk_filter.py', 'test_validate_sources_for_hunks_only_touched_contract', 1, 4, 5).
python_function('tests/test_hunk_filter.py', 'test_validate_sources_for_hunks_catches_violation_in_touched_block', 1, 2, 3).
python_function('tests/test_integrations.py', 'test_redup_finds_intent_duplicate_groups', 0, 4, 2).
python_function('tests/test_integrations.py', 'test_duplicate_contracts_cli_parity', 1, 2, 2).
python_function('tests/test_integrations.py', 'test_find_intent_duplicate_groups_from_blocks', 0, 2, 2).
python_function('tests/test_language_analyzers.py', 'test_typescript_block_extent_finds_async_function', 0, 3, 2).
python_function('tests/test_language_analyzers.py', 'test_block_extent_uses_typescript_analyzer_for_ts_files', 0, 3, 2).
python_function('tests/test_language_analyzers.py', 'test_csharp_block_extent_finds_method', 0, 3, 1).
python_function('tests/test_language_analyzers.py', 'test_block_extent_uses_csharp_analyzer', 0, 2, 1).
python_function('tests/test_language_analyzers.py', 'test_java_block_extent', 0, 3, 1).
python_function('tests/test_language_analyzers.py', 'test_go_block_extent', 0, 2, 1).
python_function('tests/test_language_analyzers.py', 'test_rust_block_extent', 0, 3, 1).
python_function('tests/test_language_analyzers.py', 'test_rust_decorator_block_extent', 0, 3, 1).
python_function('tests/test_language_analyzers.py', 'test_block_extent_routes_java_go_rust', 0, 4, 1).
python_function('tests/test_manifest.py', 'test_load_manifest_records', 1, 4, 3).
python_function('tests/test_manifest_ops.py', 'test_contract_line_to_manifest_entry_parses_ui_line', 0, 5, 1).
python_function('tests/test_manifest_ops.py', 'test_apply_ledger_to_manifest_adds_only_evolved', 1, 4, 4).
python_function('tests/test_manifest_ops.py', 'test_apply_ledger_to_manifests_both_targets', 1, 4, 5).
python_function('tests/test_markdown_generator_example.py', '_load_pass_generator', 0, 3, 3).
python_function('tests/test_markdown_generator_example.py', 'test_markdown_generator_pass_validates_and_generates_required_format', 0, 7, 4).
python_function('tests/test_markdown_generator_example.py', 'test_markdown_generator_violation_flags_forbidden_effects', 0, 6, 2).
python_function('tests/test_markdown_generator_example.py', 'test_markdown_guard_rejects_topic_drift_and_html_format', 0, 6, 2).
python_function('tests/test_markdown_generator_example.py', 'test_markdown_generator_demo_script_runs', 0, 5, 2).
python_function('tests/test_mcp.py', 'test_tool_schema_lists_core_tools', 0, 4, 0).
python_function('tests/test_mcp.py', 'test_initialize_response', 0, 2, 1).
python_function('tests/test_mcp.py', 'test_tools_list_response', 0, 3, 1).
python_function('tests/test_mcp.py', 'test_validate_intent_snippet_handler', 0, 2, 1).
python_function('tests/test_mcp.py', 'test_validate_project_on_full_stack', 0, 3, 4).
python_function('tests/test_mcp.py', 'test_tools_call_routes_handler', 0, 2, 2).
python_function('tests/test_new_modules.py', 'test_coverage', 1, 3, 2).
python_function('tests/test_new_modules.py', 'test_duplicates', 1, 2, 2).
python_function('tests/test_new_modules.py', 'test_graph_missing_requirement', 1, 2, 2).
python_function('tests/test_next_stage.py', 'test_manifest_schema_valid', 1, 2, 2).
python_function('tests/test_next_stage.py', 'test_parse_hunks', 0, 3, 2).
python_function('tests/test_next_stage.py', 'test_dockerfile_artifact_violation', 1, 3, 2).
python_function('tests/test_parser.py', 'test_parse_full_contract_line', 0, 10, 1).
python_function('tests/test_parser.py', 'test_parse_comment_prefix_ts', 0, 4, 1).
python_function('tests/test_parser.py', 'test_parse_malformed_quoted_contract_returns_none', 0, 2, 1).
python_function('tests/test_parser.py', 'test_parse_decorator_matches_comment_intent_form', 0, 6, 1).
python_function('tests/test_parser.py', 'test_parse_uri_decorator_matches_comment_form', 0, 7, 1).
python_function('tests/test_parser.py', 'test_parse_rust_attribute_wrapper', 0, 4, 1).
python_function('tests/test_planfile_adapter.py', 'test_planfile_push_local_only', 1, 4, 7).
python_function('tests/test_planfile_adapter.py', 'test_planfile_pull_reads_local_export', 1, 3, 7).
python_function('tests/test_planfile_adapter.py', 'test_planfile_webhook_apply_updates_local_status', 1, 3, 8).
python_function('tests/test_planfile_adapter.py', 'test_planfile_webhook_emit_delivers', 0, 3, 12).
python_function('tests/test_policy.py', 'test_missing_required_p1_fails_policy', 1, 3, 5).
python_function('tests/test_policy.py', 'test_full_stack_passes_without_p1_gate', 0, 2, 5).
python_function('tests/test_proposals.py', 'test_propose_ui_delta_delete_and_keep', 0, 9, 3).
python_function('tests/test_python_ast.py', 'test_python_function_extent_finds_async_def', 0, 2, 1).
python_function('tests/test_python_ast.py', 'test_python_block_extent_includes_decorators_and_imports', 0, 3, 1).
python_function('tests/test_python_ast.py', 'test_block_extent_uses_ast_for_python_files', 0, 3, 1).
python_function('tests/test_redup_policy.py', 'test_validate_for_redup_passes_full_stack', 0, 3, 1).
python_function('tests/test_redup_policy.py', 'test_validate_for_redup_fails_on_intent_duplicate', 0, 3, 2).
python_function('tests/test_redup_policy.py', 'test_parse_policy_tokens_csv', 0, 2, 1).
python_function('tests/test_rule_registry.py', 'test_rule_registry_lists_builtin_rules', 0, 6, 2).
python_function('tests/test_rule_registry.py', 'test_rule_registry_reports_per_rule_status', 0, 3, 3).
python_function('tests/test_rule_registry.py', 'test_rule_registry_discovers_entry_points', 0, 3, 3).
python_function('tests/test_rule_registry.py', 'test_custom_rule_can_be_registered', 0, 2, 5).
python_function('tests/test_scan_artifacts.py', 'test_discover_dockerfile', 1, 2, 4).
python_function('tests/test_scan_artifacts.py', 'test_scan_all_artifacts_reports_violation', 1, 3, 2).
python_function('tests/test_staged_e2e.py', '_subprocess_env', 0, 2, 4).
python_function('tests/test_staged_e2e.py', '_git', 1, 1, 1).
python_function('tests/test_staged_e2e.py', 'test_staged_hunk_check_fails_on_network_violation', 1, 3, 6).
python_function('tests/test_staged_e2e.py', 'test_staged_hunk_check_passes_clean_contract', 1, 3, 6).
python_function('tests/test_toon.py', 'test_parse_toon_uri_line', 0, 11, 1).
python_function('tests/test_toon.py', 'test_parse_toon_uri_line_without_scheme', 0, 7, 1).
python_function('tests/test_toon.py', 'test_parse_toon_uri_line_id_fallback_without_intent', 0, 6, 1).
python_function('tests/test_toon.py', 'test_load_toon_records', 1, 4, 3).
python_function('tests/test_validate_snippet.py', 'test_validate_artifact_with_proposals_passes_minimal_html', 0, 3, 1).
python_function('tests/test_validation.py', 'test_python_contract_passes', 0, 2, 3).
python_function('tests/test_validation.py', 'test_typescript_contract_detects_network_violation', 0, 3, 3).
python_function('tests/test_vallm_integration.py', 'test_validate_for_vallm_web_app_v1_pass', 0, 3, 2).
python_function('tests/test_vallm_integration.py', 'test_validate_proposal_maps_violation', 0, 4, 2).
python_function('tests/test_web_app.py', 'test_web_app_v1_overall_pass', 0, 6, 2).
python_function('tests/test_web_app.py', 'test_web_app_v2_has_network_violations', 0, 4, 1).
python_function('tests/test_web_app.py', 'test_web_app_graph_has_no_missing_requires', 0, 4, 1).

% ── Python Classes ───────────────────────────────────────
python_class('examples/showcase/server.py', 'ShowcaseHandler').
python_method('ShowcaseHandler', '__init__', 0, 1, 3).
python_method('ShowcaseHandler', '_write_json', 2, 1, 8).
python_method('ShowcaseHandler', 'do_GET', 0, 2, 5).
python_method('ShowcaseHandler', 'do_POST', 0, 8, 18).
python_class('scripts/generate_toon_from_map.py', 'FunctionTarget').
python_class('scripts/generate_toon_from_map.py', 'OutputProfileConfig').
python_class('sdks/python/src/intract_plugin_example/__init__.py', 'ExampleParserPlugin').
python_method('ExampleParserPlugin', 'supports', 1, 1, 0).
python_method('ExampleParserPlugin', 'parse', 1, 1, 1).
python_class('sdks/python/src/intract_plugin_example/__init__.py', 'ExampleValidatorPlugin').
python_method('ExampleValidatorPlugin', 'supports', 1, 1, 0).
python_method('ExampleValidatorPlugin', 'validate', 2, 1, 2).
python_class('src/intract/check.py', 'ChangedHunk').
python_method('ChangedHunk', 'to_dict', 0, 1, 1).
python_class('src/intract/config.py', 'IntractConfig').
python_method('IntractConfig', 'from_mapping', 2, 2, 5).
python_class('src/intract/core/artifact.py', 'ArtifactKind').
python_class('src/intract/core/artifact.py', 'Artifact').
python_method('Artifact', 'from_path', 2, 2, 6).
python_class('src/intract/core/cache.py', 'CacheEntry').
python_class('src/intract/core/cache.py', 'IntractDecisionCache').
python_method('IntractDecisionCache', '__init__', 1, 1, 2).
python_method('IntractDecisionCache', '_hash', 1, 1, 3).
python_method('IntractDecisionCache', '_get_key', 2, 1, 4).
python_method('IntractDecisionCache', 'load', 0, 4, 6).
python_method('IntractDecisionCache', 'save', 0, 3, 5).
python_method('IntractDecisionCache', 'get_decision', 2, 1, 2).
python_method('IntractDecisionCache', 'set_decision', 6, 3, 6).
python_class('src/intract/core/models.py', 'ValidationStatus').
python_class('src/intract/core/models.py', 'Contract').
python_method('Contract', 'key', 0, 1, 0).
python_class('src/intract/core/models.py', 'ContractRecord').
python_class('src/intract/core/models.py', 'ContractSignature').
python_method('ContractSignature', 'key', 0, 1, 0).
python_class('src/intract/core/models.py', 'ValidationIssue').
python_class('src/intract/core/models.py', 'ValidationResult').
python_method('ValidationResult', 'to_dict', 0, 2, 1).
python_class('src/intract/core/models.py', 'ProjectReport').
python_method('ProjectReport', 'passed', 0, 3, 0).
python_method('ProjectReport', 'partial', 0, 3, 0).
python_method('ProjectReport', 'failed', 0, 3, 0).
python_method('ProjectReport', 'violations', 0, 3, 0).
python_method('ProjectReport', 'to_dict', 0, 2, 2).
python_class('src/intract/core/signatures.py', '_NormalizedContract').
python_class('src/intract/coverage.py', 'CoverageReport').
python_method('CoverageReport', 'to_dict', 0, 1, 1).
python_class('src/intract/duplicates/grouping.py', 'DuplicateContract').
python_method('DuplicateContract', 'to_dict', 0, 1, 1).
python_class('src/intract/duplicates/grouping.py', 'IntentDuplicateGroup').
python_method('IntentDuplicateGroup', 'to_dict', 0, 1, 1).
python_class('src/intract/duplicates/matcher.py', 'IntentPair').
python_class('src/intract/engine/context.py', 'EngineConfig').
python_class('src/intract/engine/context.py', 'LogicalFragment').
python_class('src/intract/engine/context.py', 'ContractSuggestion').
python_class('src/intract/engine/drift.py', 'FragmentState').
python_class('src/intract/engine/drift.py', 'DriftIssue').
python_class('src/intract/engine/scanner.py', 'SourceUnit').
python_class('src/intract/git.py', 'GitChange').
python_class('src/intract/graph.py', 'ContractGraph').
python_method('ContractGraph', 'to_dict', 0, 1, 1).
python_method('ContractGraph', 'to_mermaid', 0, 5, 3).
python_class('src/intract/integrations/nexu.py', 'IntentContract').
python_method('IntentContract', 'key', 0, 3, 0).
python_class('src/intract/integrations/planfile.py', 'Ticket').
python_class('src/intract/integrations/planfile.py', 'PlanfileExporter').
python_method('PlanfileExporter', '__init__', 1, 1, 1).
python_method('PlanfileExporter', 'export', 1, 1, 4).
python_method('PlanfileExporter', '_write_yaml', 2, 7, 5).
python_method('PlanfileExporter', '_write_json', 2, 2, 3).
python_method('PlanfileExporter', '_write_todo', 2, 8, 3).
python_class('src/intract/integrations/planfile_adapter.py', 'PlanfileConfig').
python_method('PlanfileConfig', 'from_env', 1, 6, 3).
python_class('src/intract/integrations/planfile_adapter.py', 'PlanfileSyncResult').
python_class('src/intract/integrations/planfile_adapter.py', 'PlanfileWebhookResult').
python_class('src/intract/integrations/planfile_adapter.py', 'PlanfileApiAdapter').
python_method('PlanfileApiAdapter', '__init__', 1, 2, 1).
python_method('PlanfileApiAdapter', 'export_local', 1, 1, 2).
python_method('PlanfileApiAdapter', 'push', 1, 6, 8).
python_method('PlanfileApiAdapter', 'pull', 0, 7, 8).
python_method('PlanfileApiAdapter', 'sync_from_report', 1, 3, 7).
python_method('PlanfileApiAdapter', 'emit_webhook', 2, 5, 8).
python_method('PlanfileApiAdapter', 'apply_webhook_event', 1, 13, 10).
python_method('PlanfileApiAdapter', '_webhook_label', 1, 3, 0).
python_method('PlanfileApiAdapter', '_endpoint', 1, 1, 1).
python_method('PlanfileApiAdapter', '_request', 3, 6, 8).
python_class('src/intract/integrations/redup.py', 'CodeBlockLike').
python_class('src/intract/integrations/redup.py', 'BlockAdapter').
python_class('src/intract/integrations/redup.py', 'RedupScanResult').
python_method('RedupScanResult', 'to_dict', 0, 1, 1).
python_class('src/intract/integrations/redup.py', 'RedupPolicyResult').
python_method('RedupPolicyResult', 'to_dict', 0, 1, 1).
python_class('src/intract/integrations/vallm.py', 'MappedIssue').
python_class('src/intract/integrations/vallm.py', 'MappedValidationResult').
python_method('MappedValidationResult', 'to_dict', 0, 2, 0).
python_class('src/intract/manifest_ops.py', 'ManifestApplyResult').
python_method('ManifestApplyResult', 'to_dict', 0, 2, 1).
python_class('src/intract/manifest_ops.py', 'ManifestApplyBatchResult').
python_method('ManifestApplyBatchResult', 'added_total', 0, 2, 2).
python_method('ManifestApplyBatchResult', 'to_dict', 0, 2, 1).
python_class('src/intract/manifest_schema.py', 'ManifestIssue').
python_class('src/intract/manifest_schema.py', 'ManifestValidationReport').
python_method('ManifestValidationReport', 'to_dict', 0, 2, 1).
python_class('src/intract/parsers/inline.py', '_ContractParserState').
python_method('_ContractParserState', '__init__', 1, 1, 0).
python_class('src/intract/plugins/base.py', 'PluginResult').
python_class('src/intract/plugins/base.py', 'ParserPlugin').
python_method('ParserPlugin', 'supports', 1, 1, 0).
python_method('ParserPlugin', 'parse', 1, 1, 0).
python_class('src/intract/plugins/base.py', 'ValidatorPlugin').
python_method('ValidatorPlugin', 'supports', 1, 1, 0).
python_method('ValidatorPlugin', 'validate', 2, 1, 0).
python_class('src/intract/plugins/base.py', 'ReporterPlugin').
python_method('ReporterPlugin', 'render', 1, 1, 0).
python_class('src/intract/plugins/base.py', 'IntegrationPlugin').
python_method('IntegrationPlugin', 'install', 1, 1, 0).
python_class('src/intract/plugins/base.py', 'PluginRegistry').
python_method('PluginRegistry', 'add_parser', 1, 1, 1).
python_method('PluginRegistry', 'add_validator', 1, 1, 1).
python_method('PluginRegistry', 'add_reporter', 1, 1, 1).
python_method('PluginRegistry', 'add_integration', 1, 1, 1).
python_method('PluginRegistry', 'parse_artifact', 1, 5, 3).
python_method('PluginRegistry', 'validate_artifact', 2, 3, 3).
python_class('src/intract/plugins/builtins.py', 'InlineContractParserPlugin').
python_method('InlineContractParserPlugin', 'supports', 1, 1, 0).
python_method('InlineContractParserPlugin', 'parse', 1, 1, 3).
python_class('src/intract/plugins/builtins.py', 'OpenAPIParserPlugin').
python_method('OpenAPIParserPlugin', 'supports', 1, 1, 0).
python_method('OpenAPIParserPlugin', 'parse', 1, 1, 3).
python_class('src/intract/plugins/builtins.py', 'ManifestParserPlugin').
python_method('ManifestParserPlugin', 'supports', 1, 1, 0).
python_method('ManifestParserPlugin', 'parse', 1, 1, 4).
python_class('src/intract/plugins/builtins.py', 'BasicContractValidatorPlugin').
python_method('BasicContractValidatorPlugin', 'supports', 1, 1, 0).
python_method('BasicContractValidatorPlugin', 'validate', 2, 3, 5).
python_class('src/intract/plugins/builtins.py', 'ArtifactStructureValidatorPlugin').
python_method('ArtifactStructureValidatorPlugin', 'supports', 1, 1, 0).
python_method('ArtifactStructureValidatorPlugin', 'validate', 2, 3, 4).
python_class('src/intract/plugins/builtins.py', 'JsonReporterPlugin').
python_method('JsonReporterPlugin', 'render', 1, 2, 3).
python_class('src/intract/policy.py', 'PolicyDecision').
python_class('src/intract/proposals.py', 'ProposedContract').
python_method('ProposedContract', 'to_dict', 0, 1, 0).
python_class('src/intract/scan_artifacts.py', 'ArtifactScanReport').
python_method('ArtifactScanReport', 'violations', 0, 4, 1).
python_method('ArtifactScanReport', 'to_dict', 0, 2, 2).
python_class('src/intract/sdk.py', 'ContractBuilder').
python_method('ContractBuilder', 'to_inline', 1, 9, 2).
python_class('src/intract/validators/artifacts.py', 'ArtifactValidationReport').
python_method('ArtifactValidationReport', 'to_dict', 0, 2, 1).
python_class('src/intract/validators/base.py', 'RuleResult').
python_class('src/intract/validators/base.py', 'ValidationContext').
python_class('src/intract/validators/base.py', 'ValidationRule').
python_method('ValidationRule', 'supports', 1, 1, 0).
python_method('ValidationRule', 'validate', 3, 1, 0).
python_class('src/intract/validators/effects.py', 'NoForbiddenEffectRule').
python_method('NoForbiddenEffectRule', 'supports', 1, 1, 0).
python_method('NoForbiddenEffectRule', 'validate', 3, 3, 4).
python_class('src/intract/validators/input_output.py', 'InputPresenceRule').
python_method('InputPresenceRule', 'supports', 1, 1, 0).
python_method('InputPresenceRule', 'validate', 3, 3, 6).
python_class('src/intract/validators/input_output.py', 'OutputPresenceRule').
python_method('OutputPresenceRule', 'supports', 1, 1, 0).
python_method('OutputPresenceRule', 'validate', 3, 3, 6).
python_class('src/intract/validators/input_output.py', 'ReturnValueRule').
python_method('ReturnValueRule', 'supports', 1, 1, 0).
python_method('ReturnValueRule', 'validate', 3, 3, 2).
python_class('src/intract/validators/registry.py', 'RuleRegistry').
python_method('RuleRegistry', '__init__', 1, 2, 1).
python_method('RuleRegistry', 'register', 1, 3, 1).
python_method('RuleRegistry', 'rules', 0, 1, 1).
python_method('RuleRegistry', 'run', 4, 5, 4).
python_method('RuleRegistry', 'rule_status', 2, 7, 0).
python_method('RuleRegistry', 'summarize', 2, 2, 1).
python_class('src/intract/watch.py', 'FileState').
python_class('src/intract/watch.py', 'FileChange').
python_class('src/intract/watch.py', 'WatchConfig').

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('help', 'Default target').
makefile_target('install', 'Installation').
makefile_target('install-dev', '').
makefile_target('test', 'Testing').
makefile_target('test-cov', '').
makefile_target('lint', 'Code quality').
makefile_target('format', '').
makefile_target('clean', 'Utilities').
makefile_target('publish', 'Release helpers').
makefile_target('publish-confirm', '').
makefile_target('publish-test', '').
makefile_target('version', '').
makefile_target('install', '').
makefile_target('test', '').
makefile_target('lint', '').
makefile_target('format', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', '*(not set)*', 'Required: OpenRouter API key (https://openrouter.ai/keys)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Model (default: openrouter/qwen/qwen3-coder-next)').
env_variable('PFIX_AUTO_APPLY', 'true', 'true = apply fixes without asking').
env_variable('PFIX_AUTO_INSTALL_DEPS', 'true', 'true = auto pip/uv install').
env_variable('PFIX_AUTO_RESTART', 'false', 'true = os.execv restart after fix').
env_variable('PFIX_MAX_RETRIES', '3', '').
env_variable('PFIX_DRY_RUN', 'false', '').
env_variable('PFIX_ENABLED', 'true', '').
env_variable('PFIX_GIT_COMMIT', 'false', 'true = auto-commit fixes').
env_variable('PFIX_GIT_PREFIX', 'pfix:', 'commit message prefix').
env_variable('PFIX_CREATE_BACKUPS', 'false', 'false = disable .pfix_backups/ directory').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('pyqual.yaml', 'pyqual').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('install', 'manual').
sumd_workflow_step('install', 1, 'echo "📦 Installing sumd..."').
sumd_workflow_step('install', 2, 'if command -v uv > /dev/null 2>&1').
sumd_workflow_step('install', 3, 'uv pip install -e .').
sumd_workflow_step('install', 4, 'else \').
sumd_workflow_step('install', 5, 'pip install -e .').
sumd_workflow_step('install', 6, 'fi').
sumd_workflow_step('install', 7, 'echo "✅ Installation completed!"').
sumd_workflow('install-dev', 'manual').
sumd_workflow_step('install-dev', 1, 'echo "📦 Installing sumd with dev dependencies..."').
sumd_workflow_step('install-dev', 2, 'if command -v uv > /dev/null 2>&1').
sumd_workflow_step('install-dev', 3, 'uv pip install -e ".[dev]"').
sumd_workflow_step('install-dev', 4, 'else \').
sumd_workflow_step('install-dev', 5, 'pip install -e ".[dev]"').
sumd_workflow_step('install-dev', 6, 'fi').
sumd_workflow_step('install-dev', 7, 'echo "✅ Dev installation completed!"').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'echo "🧪 Running tests..."').
sumd_workflow_step('test', 2, '.venv/bin/python -m pytest tests/ -v --tb=short').
sumd_workflow('test-cov', 'manual').
sumd_workflow_step('test-cov', 1, 'echo "🧪 Running tests with coverage..."').
sumd_workflow_step('test-cov', 2, '.venv/bin/python -m pytest tests/ -v --cov=sumd --cov-report=term-missing --cov-report=json').
sumd_workflow('lint', 'manual').
sumd_workflow_step('lint', 1, 'echo "🔍 Running linting with ruff..."').
sumd_workflow_step('lint', 2, '.venv/bin/python -m ruff check sumd/').
sumd_workflow_step('lint', 3, '.venv/bin/python -m ruff check tests/').
sumd_workflow('format', 'manual').
sumd_workflow_step('format', 1, 'echo "📝 Formatting code with ruff..."').
sumd_workflow_step('format', 2, '.venv/bin/python -m ruff format sumd/').
sumd_workflow_step('format', 3, '.venv/bin/python -m ruff format tests/').
sumd_workflow('clean', 'manual').
sumd_workflow_step('clean', 1, 'echo "🧹 Cleaning temporary files..."').
sumd_workflow_step('clean', 2, 'find . -type f -name "*.pyc" -delete').
sumd_workflow_step('clean', 3, 'find . -type d -name "__pycache__" -delete').
sumd_workflow('publish', 'manual').
sumd_workflow_step('publish', 1, 'echo "📦 Publishing to PyPI..."').
sumd_workflow_step('publish', 2, 'command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build)').
sumd_workflow_step('publish', 3, 'rm -rf dist/ build/ *.egg-info/').
sumd_workflow_step('publish', 4, '.venv/bin/python -m build').
sumd_workflow_step('publish', 5, '.venv/bin/twine check dist/*').
sumd_workflow_step('publish', 6, 'echo "⚡ Ready to upload. Run: make publish-confirm to upload to PyPI"').
sumd_workflow('publish-confirm', 'manual').
sumd_workflow_step('publish-confirm', 1, 'echo "🚀 Uploading to PyPI..."').
sumd_workflow_step('publish-confirm', 2, '.venv/bin/twine upload dist/*').
sumd_workflow('publish-test', 'manual').
sumd_workflow_step('publish-test', 1, 'echo "📦 Publishing to TestPyPI..."').
sumd_workflow_step('publish-test', 2, 'command -v .venv/bin/twine > /dev/null 2>&1 || (.venv/bin/pip install --upgrade twine build)').
sumd_workflow_step('publish-test', 3, 'rm -rf dist/ build/ *.egg-info/').
sumd_workflow_step('publish-test', 4, '.venv/bin/python -m build').
sumd_workflow_step('publish-test', 5, '.venv/bin/twine upload --repository testpypi dist/*').
sumd_workflow('version', 'manual').
sumd_workflow_step('version', 1, 'echo "📦 Version information..."').
sumd_workflow_step('version', 2, 'cat VERSION').
sumd_workflow_step('version', 3, '.venv/bin/python -c "from importlib.metadata import version').
```

## Call Graph

*329 nodes · 378 edges · 65 modules · CC̄=3.5*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `contract_from_mapping` *(in src.intract.parsers.manifest)* | 3 | 4 | 59 | **63** |
| `manifest_apply_ledger` *(in src.intract.cli)* | 10 ⚠ | 0 | 30 | **30** |
| `do_POST` *(in examples.showcase.server.ShowcaseHandler)* | 8 | 0 | 28 | **28** |
| `normalize_label` *(in src.intract.core.normalizer)* | 7 | 11 | 16 | **27** |
| `validate_project` *(in src.intract.project)* | 6 | 17 | 10 | **27** |
| `parse_contract_line` *(in src.intract.parsers.inline)* | 13 ⚠ | 4 | 21 | **25** |
| `tickets_from_report` *(in src.intract.integrations.planfile)* | 11 ⚠ | 3 | 21 | **24** |
| `generate_toon_lines` *(in scripts.generate_toon_from_map)* | 6 | 1 | 23 | **24** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/intract
# generated in 0.15s
# nodes: 329 | edges: 378 | modules: 65
# CC̄=3.5

HUBS[20]:
  src.intract.parsers.manifest.contract_from_mapping
    CC=3  in:4  out:59  total:63
  src.intract.cli.manifest_apply_ledger
    CC=10  in:0  out:30  total:30
  examples.showcase.server.ShowcaseHandler.do_POST
    CC=8  in:0  out:28  total:28
  src.intract.core.normalizer.normalize_label
    CC=7  in:11  out:16  total:27
  src.intract.project.validate_project
    CC=6  in:17  out:10  total:27
  src.intract.parsers.inline.parse_contract_line
    CC=13  in:4  out:21  total:25
  src.intract.integrations.planfile.tickets_from_report
    CC=11  in:3  out:21  total:24
  scripts.generate_toon_from_map.generate_toon_lines
    CC=6  in:1  out:23  total:24
  src.intract.core.signatures._normalize_contract
    CC=2  in:1  out:22  total:23
  src.intract.integrations.planfile_adapter._ticket_from_dict
    CC=2  in:2  out:21  total:23
  src.intract.graph.build_graph
    CC=9  in:5  out:18  total:23
  src.intract.integrations.nexu._base_intent_contract
    CC=2  in:2  out:21  total:23
  src.intract.parsers.inline.clean_comment_line
    CC=12  in:2  out:20  total:22
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:3  out:17  total:20
  src.intract.parsers.toon._contract_from_uri
    CC=1  in:1  out:19  total:20
  src.intract.validators.engine.validate_contract_against_source
    CC=8  in:5  out:14  total:19
  src.intract.cli.engine_suggest
    CC=3  in:0  out:18  total:18
  src.intract.config.load_config
    CC=11  in:4  out:14  total:18

MODULES:
  examples.integration_tests.run_examples  [6 funcs]
    main  CC=10  out:9
    print_result  CC=1  out:3
    run_example_01  CC=1  out:4
    run_example_02  CC=2  out:10
    run_example_03  CC=2  out:17
    run_example_04  CC=1  out:3
  examples.markdown-generator.demo  [3 funcs]
    _load_pass_generator  CC=3  out:4
    _validate_project  CC=2  out:4
    main  CC=4  out:14
  examples.markdown-generator.pass.generator  [5 funcs]
    build_markdown_outline  CC=3  out:1
    generate_markdown_document  CC=2  out:5
    guard_markdown_contract  CC=4  out:7
    normalize_topic  CC=2  out:4
    render_markdown_sections  CC=2  out:0
  examples.markdown-generator.violation.generator  [5 funcs]
    build_markdown_outline  CC=3  out:4
    generate_markdown_document  CC=2  out:5
    guard_markdown_contract  CC=3  out:6
    normalize_topic  CC=2  out:4
    render_markdown_sections  CC=2  out:2
  examples.showcase.server  [4 funcs]
    do_GET  CC=2  out:5
    do_POST  CC=8  out:28
    load_env_file  CC=6  out:10
    resolve_runtime_config  CC=4  out:8
  extensions.vscode-intract.extension  [6 funcs]
    activate  CC=2  out:11
    root  CC=1  out:1
    runIntract  CC=1  out:6
    runShell  CC=1  out:3
    uri  CC=1  out:1
    workspaceRoot  CC=4  out:0
  scripts.generate_toon_from_map  [17 funcs]
    _build_parser  CC=1  out:15
    _contract_fragment  CC=5  out:9
    _default_function_fragment  CC=2  out:4
    _effective_include  CC=2  out:0
    _ensure_parent  CC=3  out:2
    _extract_symbol_names  CC=5  out:8
    _function_fragment  CC=3  out:3
    _iter_section_lines  CC=6  out:2
    _llm_contract_fragment  CC=8  out:9
    _parse_functions  CC=9  out:11
  sdks.go.intractsdk.sdk  [2 funcs]
    Inline  CC=11  out:5
    csv  CC=1  out:1
  sdks.java.src.main.java.io.intract.sdk.IntractContract  [2 funcs]
    inline  CC=11  out:4
    join  CC=2  out:3
  sdks.rust.src  [2 funcs]
    csv  CC=1  out:1
    inline_contract  CC=10  out:6
  sdks.typescript.src  [2 funcs]
    csv  CC=4  out:1
    inlineContract  CC=10  out:3
  src.intract.analyzers.blocks  [2 funcs]
    block_extent_from_patterns  CC=7  out:7
    scan_braced_block  CC=8  out:2
  src.intract.analyzers.csharp  [3 funcs]
    _scan_braced_block  CC=8  out:2
    _treesitter_csharp_extent  CC=2  out:1
    csharp_block_extent  CC=8  out:8
  src.intract.analyzers.go  [1 funcs]
    go_block_extent  CC=1  out:1
  src.intract.analyzers.java  [1 funcs]
    java_block_extent  CC=4  out:7
  src.intract.analyzers.python_ast  [3 funcs]
    _decorator_lines  CC=3  out:2
    python_block_extent  CC=14  out:11
    python_function_extent  CC=8  out:8
  src.intract.analyzers.rust  [1 funcs]
    rust_block_extent  CC=1  out:1
  src.intract.analyzers.treesitter  [4 funcs]
    _find_extent  CC=7  out:8
    _load_parser  CC=3  out:4
    csharp_method_extent  CC=1  out:1
    typescript_function_extent  CC=1  out:1
  src.intract.analyzers.typescript  [3 funcs]
    _scan_braced_block  CC=11  out:5
    _treesitter_typescript_extent  CC=2  out:1
    typescript_block_extent  CC=7  out:7
  src.intract.check  [14 funcs]
    _fallback_block_extent  CC=11  out:9
    _is_fallback_preamble  CC=3  out:2
    _is_python_declaration  CC=1  out:1
    _language_block_extent  CC=3  out:5
    _manifest_changed  CC=2  out:2
    block_extent  CC=2  out:2
    changed_check  CC=1  out:4
    changed_lines_by_file  CC=4  out:4
    load_selected_sources  CC=5  out:4
    parse_unified_diff_hunks  CC=6  out:16
  src.intract.cli  [26 funcs]
    _export_tickets  CC=1  out:6
    _is_scan_candidate  CC=2  out:1
    _print_artifact_scan_report  CC=3  out:5
    _print_scan_table  CC=2  out:15
    _print_validation_report  CC=4  out:15
    _scan_artifacts  CC=3  out:6
    _scan_contract_file  CC=2  out:2
    _scan_inline_records  CC=5  out:10
    _scan_row  CC=1  out:0
    artifact_validate  CC=4  out:11
  src.intract.config  [1 funcs]
    load_config  CC=11  out:14
  src.intract.core.artifact  [5 funcs]
    from_path  CC=2  out:8
    _kind_from_filename  CC=10  out:2
    _kind_from_structured_content  CC=7  out:1
    infer_artifact_kind  CC=3  out:6
    infer_language  CC=1  out:3
  src.intract.core.normalizer  [4 funcs]
    normalize_action  CC=4  out:3
    normalize_label  CC=7  out:16
    normalize_many  CC=4  out:4
    normalize_requirement  CC=6  out:10
  src.intract.core.signatures  [8 funcs]
    _add_feature_values  CC=2  out:1
    _block_id  CC=2  out:1
    _exact_hash  CC=1  out:5
    _normalize_contract  CC=2  out:22
    _signature_features  CC=2  out:10
    build_signature  CC=3  out:7
    build_signatures  CC=2  out:1
    make_block_id  CC=1  out:3
  src.intract.coverage  [1 funcs]
    calculate_coverage  CC=3  out:14
  src.intract.duplicates.grouping  [4 funcs]
    find_duplicate_contracts  CC=2  out:5
    pairs_to_duplicate_contracts  CC=3  out:6
    pairs_to_intent_groups  CC=6  out:16
    union_find_groups  CC=5  out:10
  src.intract.duplicates.matcher  [2 funcs]
    bucket_signatures  CC=2  out:2
    find_intent_pairs  CC=6  out:8
  src.intract.duplicates.scoring  [3 funcs]
    jaccard  CC=5  out:2
    object_similarity  CC=2  out:5
    score_similarity  CC=5  out:14
  src.intract.engine.analyzer  [3 funcs]
    _line_number  CC=1  out:1
    _slice_until_next_match  CC=3  out:2
    analyze_source_units  CC=12  out:17
  src.intract.engine.assigner  [6 funcs]
    _infer_action  CC=10  out:5
    _infer_effects  CC=8  out:8
    _infer_object  CC=4  out:2
    _split_name  CC=3  out:3
    suggest_contract_for_fragment  CC=3  out:7
    suggest_contracts_for_fragments  CC=4  out:1
  src.intract.engine.drift  [5 funcs]
    detect_drift  CC=5  out:12
    hash_text  CC=1  out:3
    load_state  CC=3  out:6
    save_state  CC=2  out:7
    state_from_fragments  CC=2  out:2
  src.intract.engine.monitor  [1 funcs]
    scan_suggest_and_validate  CC=4  out:10
  src.intract.engine.scanner  [1 funcs]
    collect_source_units  CC=9  out:14
  src.intract.git  [5 funcs]
    _run_git  CC=2  out:2
    changed_files  CC=4  out:7
    paths_from_changes  CC=2  out:1
    staged_files  CC=4  out:7
    staged_hunks  CC=2  out:2
  src.intract.graph  [3 funcs]
    to_mermaid  CC=5  out:9
    _safe  CC=3  out:2
    build_graph  CC=9  out:18
  src.intract.integrations.nexu  [12 funcs]
    _base_intent_contract  CC=2  out:21
    _contract_items  CC=4  out:2
    _list_field  CC=2  out:2
    _read_yaml_mapping  CC=4  out:3
    _target_line_value  CC=2  out:2
    _toon_intent_contract  CC=5  out:10
    _toon_target  CC=3  out:2
    parse_intract_line  CC=9  out:14
    read_manifest_contracts  CC=4  out:5
    read_toon_manifest_contracts  CC=4  out:4
  src.intract.integrations.planfile  [1 funcs]
    tickets_from_report  CC=11  out:21
  src.intract.integrations.planfile_adapter  [3 funcs]
    pull  CC=7  out:10
    sync_from_report  CC=3  out:9
    _ticket_from_dict  CC=2  out:21
  src.intract.integrations.redup  [16 funcs]
    _apply_duplicate_policy  CC=5  out:4
    _duplicate_reasons  CC=2  out:1
    _graph_for_policy  CC=3  out:1
    _intent_duplicate_label  CC=2  out:4
    _resolve_manifest_path  CC=3  out:2
    _with_block_lines  CC=1  out:3
    block_end_line  CC=3  out:4
    block_file_path  CC=3  out:3
    block_start_line  CC=3  out:3
    block_text  CC=4  out:3
  src.intract.integrations.vallm  [4 funcs]
    map_project_report  CC=7  out:3
    map_validation_result  CC=6  out:4
    validate_for_vallm  CC=2  out:3
    validate_proposal  CC=12  out:9
  src.intract.manifest_ops  [11 funcs]
    _append_manifest_proposal  CC=5  out:15
    _existing_contract_ids  CC=4  out:6
    _iter_ledger_proposals  CC=6  out:4
    _should_apply_ledger_entry  CC=2  out:2
    apply_ledger_to_manifest  CC=4  out:7
    apply_ledger_to_manifests  CC=2  out:4
    contract_line_to_manifest_entry  CC=13  out:10
    load_manifest_document  CC=5  out:8
    load_policy_ledger  CC=6  out:6
    resolve_manifest_paths  CC=5  out:1
  src.intract.manifest_schema  [7 funcs]
    _fallback_issues  CC=9  out:14
    _invalid_manifest_report  CC=1  out:3
    _jsonschema_issues  CC=5  out:8
    _load_manifest_data  CC=3  out:3
    _load_schema  CC=2  out:5
    _manifest_report  CC=1  out:2
    validate_manifest  CC=4  out:7
  src.intract.mcp.handlers  [8 funcs]
    _resolve_manifest  CC=4  out:6
    _resolve_path  CC=1  out:4
    handle_build_graph  CC=1  out:5
    handle_find_duplicates  CC=2  out:7
    handle_scan_artifacts  CC=1  out:4
    handle_validate_intent_snippet  CC=1  out:5
    handle_validate_project  CC=1  out:5
    handle_validate_staged  CC=4  out:11
  src.intract.mcp.server  [5 funcs]
    handle_initialize  CC=1  out:0
    handle_request  CC=5  out:6
    handle_tools_call  CC=4  out:2
    handle_tools_list  CC=2  out:1
    run_server  CC=5  out:14
  src.intract.parsers.inline  [14 funcs]
    _add_relation  CC=2  out:2
    _apply_key_value_pair  CC=1  out:2
    _extend_list  CC=1  out:3
    _parse_special_token  CC=8  out:9
    _parse_uri_contract  CC=6  out:3
    _resolve_action_object  CC=5  out:2
    clean_comment_line  CC=12  out:20
    extract_contract_records_from_text  CC=3  out:5
    extract_intract_uri  CC=9  out:11
    marker_payload  CC=3  out:3
  src.intract.parsers.manifest  [11 funcs]
    _file_contract_records  CC=6  out:9
    _parse_intent  CC=3  out:7
    _target_line  CC=3  out:4
    _target_mapping  CC=3  out:2
    _target_tags  CC=3  out:7
    _top_level_contract_record  CC=3  out:8
    _top_level_contract_records  CC=4  out:4
    _with_target_tags  CC=2  out:2
    contract_from_mapping  CC=3  out:59
    create_sample_manifest  CC=1  out:0
  src.intract.parsers.openapi  [2 funcs]
    parse_openapi_contracts  CC=8  out:16
    parse_openapi_text  CC=8  out:14
  src.intract.parsers.toon  [13 funcs]
    _action_object  CC=3  out:5
    _build_tags  CC=3  out:4
    _contract_from_uri  CC=1  out:19
    _extract_file_path  CC=2  out:0
    _get_first  CC=1  out:1
    _get_first_alias  CC=3  out:1
    _get_list  CC=4  out:6
    _get_list_alias  CC=3  out:1
    _parse_action_object_from_intent  CC=8  out:5
    _priority  CC=2  out:3
  src.intract.plugins.builtins  [5 funcs]
    validate  CC=3  out:4
    validate  CC=3  out:5
    parse  CC=1  out:3
    parse  CC=1  out:4
    parse  CC=1  out:3
  src.intract.plugins.manager  [3 funcs]
    _register_unique  CC=3  out:2
    discover_plugins  CC=6  out:15
    load_builtin_plugins  CC=1  out:13
  src.intract.policy  [7 funcs]
    _collect_result_policy  CC=5  out:5
    _invalid_manifest_reasons  CC=3  out:1
    _missing_required_p1_reasons  CC=4  out:3
    _p1_missing_reasons  CC=7  out:6
    _result_policy_line  CC=1  out:3
    _result_status  CC=1  out:3
    decide_policy  CC=6  out:7
  src.intract.project  [8 funcs]
    _project_status  CC=9  out:3
    _validate_manifest_signature  CC=4  out:4
    _validate_manifest_signatures  CC=2  out:2
    _validate_observed_signatures  CC=2  out:2
    extract_signatures_from_sources  CC=2  out:4
    load_project_sources  CC=9  out:8
    validate_project  CC=6  out:10
    validate_sources  CC=2  out:6
  src.intract.proposals  [2 funcs]
    propose_ui_delta_contract_dicts  CC=2  out:2
    propose_ui_delta_contracts  CC=9  out:14
  src.intract.propose_llm  [8 funcs]
    _build_prompt  CC=2  out:0
    _json_line_strings  CC=5  out:6
    _lines_to_proposals  CC=7  out:6
    _load_litellm_completion  CC=2  out:1
    _resolve_api_key  CC=4  out:3
    _resolve_model  CC=4  out:2
    _strip_markdown_fence  CC=2  out:4
    propose_contracts_llm  CC=3  out:13
  src.intract.scan_artifacts  [2 funcs]
    discover_artifact_paths  CC=7  out:11
    scan_all_artifacts  CC=3  out:7
  src.intract.validate_snippet  [1 funcs]
    validate_artifact_with_proposals  CC=3  out:7
  src.intract.validators.artifacts  [5 funcs]
    validate_artifact  CC=9  out:17
    validate_dockerfile  CC=6  out:14
    validate_github_actions  CC=8  out:12
    validate_kubernetes  CC=8  out:13
    validate_openapi  CC=9  out:16
  src.intract.validators.base  [1 funcs]
    merge_rule_results  CC=2  out:4
  src.intract.validators.effects  [2 funcs]
    validate  CC=3  out:5
    detect_effects  CC=9  out:13
  src.intract.validators.engine  [1 funcs]
    validate_contract_against_source  CC=8  out:14
  src.intract.validators.input_output  [5 funcs]
    validate  CC=5  out:7
    validate  CC=5  out:7
    validate  CC=3  out:2
    contains_token_like  CC=7  out:5
    has_return_value  CC=3  out:4
  src.intract.validators.registry  [2 funcs]
    _discover_entry_point_rules  CC=5  out:7
    get_rule_registry  CC=6  out:6
  src.intract.validators.requirements  [1 funcs]
    validate_required_contracts  CC=6  out:2
  src.intract.watch  [5 funcs]
    diff_snapshots  CC=5  out:11
    hash_file  CC=2  out:6
    should_scan  CC=10  out:8
    snapshot_tree  CC=4  out:9
    watch_tree  CC=7  out:10

EDGES:
  examples.showcase.server.resolve_runtime_config → examples.showcase.server.load_env_file
  examples.showcase.server.ShowcaseHandler.do_GET → examples.showcase.server.resolve_runtime_config
  examples.showcase.server.ShowcaseHandler.do_POST → examples.showcase.server.resolve_runtime_config
  examples.integration_tests.run_examples.run_example_01 → src.intract.project.validate_project
  examples.integration_tests.run_examples.run_example_02 → src.intract.project.validate_project
  examples.integration_tests.run_examples.run_example_02 → src.intract.integrations.planfile.tickets_from_report
  examples.integration_tests.run_examples.run_example_03 → src.intract.watch.snapshot_tree
  examples.integration_tests.run_examples.run_example_03 → src.intract.watch.diff_snapshots
  examples.integration_tests.run_examples.run_example_03 → src.intract.engine.monitor.scan_suggest_and_validate
  examples.integration_tests.run_examples.run_example_04 → src.intract.project.validate_project
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_01
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_02
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_03
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_04
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.print_result
  src.intract.watch.snapshot_tree → src.intract.watch.should_scan
  src.intract.watch.snapshot_tree → src.intract.watch.hash_file
  src.intract.watch.watch_tree → src.intract.watch.snapshot_tree
  src.intract.watch.watch_tree → src.intract.watch.diff_snapshots
  src.intract.scan_artifacts.discover_artifact_paths → src.intract.core.artifact.infer_artifact_kind
  src.intract.scan_artifacts.scan_all_artifacts → src.intract.scan_artifacts.discover_artifact_paths
  src.intract.scan_artifacts.scan_all_artifacts → src.intract.validators.artifacts.validate_artifact
  src.intract.proposals.propose_ui_delta_contract_dicts → src.intract.proposals.propose_ui_delta_contracts
  src.intract.coverage.calculate_coverage → src.intract.project.load_project_sources
  src.intract.coverage.calculate_coverage → src.intract.project.extract_signatures_from_sources
  src.intract.graph.ContractGraph.to_mermaid → src.intract.graph._safe
  src.intract.graph.build_graph → src.intract.project.load_project_sources
  src.intract.graph.build_graph → src.intract.project.extract_signatures_from_sources
  src.intract.git.staged_files → src.intract.git._run_git
  src.intract.git.changed_files → src.intract.git._run_git
  src.intract.git.staged_hunks → src.intract.git._run_git
  src.intract.validate_snippet.validate_artifact_with_proposals → src.intract.integrations.vallm.validate_proposal
  src.intract.duplicates.scoring.object_similarity → src.intract.duplicates.scoring.jaccard
  src.intract.duplicates.scoring.score_similarity → src.intract.duplicates.scoring.object_similarity
  src.intract.duplicates.scoring.score_similarity → src.intract.duplicates.scoring.jaccard
  src.intract.duplicates.matcher.find_intent_pairs → src.intract.duplicates.matcher.bucket_signatures
  src.intract.duplicates.matcher.find_intent_pairs → src.intract.duplicates.scoring.score_similarity
  src.intract.duplicates.grouping.pairs_to_intent_groups → src.intract.duplicates.grouping.union_find_groups
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.project.load_project_sources
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.project.extract_signatures_from_sources
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.duplicates.matcher.find_intent_pairs
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.duplicates.grouping.pairs_to_duplicate_contracts
  src.intract.validators.artifacts.validate_openapi → src.intract.parsers.openapi.parse_openapi_contracts
  src.intract.validators.artifacts.validate_openapi → src.intract.core.signatures.build_signature
  src.intract.validators.artifacts.validate_artifact → src.intract.validators.artifacts.validate_dockerfile
  src.intract.validators.artifacts.validate_artifact → src.intract.validators.artifacts.validate_github_actions
  src.intract.validators.artifacts.validate_artifact → src.intract.validators.artifacts.validate_openapi
  src.intract.validators.artifacts.validate_artifact → src.intract.validators.artifacts.validate_kubernetes
  src.intract.validators.engine.validate_contract_against_source → src.intract.validators.base.merge_rule_results
  src.intract.validators.engine.validate_contract_against_source → src.intract.validators.registry.get_rule_registry
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Intent

Intent contract tagging, validation and semantic mapping for codebases.
