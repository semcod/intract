# Intract

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Quality Pipeline (`pyqual.yaml`)](#quality-pipeline-pyqualyaml)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `intract`
- **version**: `0.5.13`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, pyqual.yaml, goal.yaml, .env.example, Dockerfile, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: intract;
  version: 0.5.13;
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
  src.intract.graph.build_graph
    CC=9  in:5  out:18  total:23
  src.intract.integrations.planfile_adapter._ticket_from_dict
    CC=2  in:2  out:21  total:23
  src.intract.integrations.nexu._base_intent_contract
    CC=2  in:2  out:21  total:23
  src.intract.parsers.inline.clean_comment_line
    CC=12  in:2  out:20  total:22
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:3  out:17  total:20
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
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
  examples.markdown-generator.demo._validate_project → src.intract.project.validate_project
  examples.markdown-generator.demo.main → examples.markdown-generator.demo._load_pass_generator
  examples.markdown-generator.demo.main → examples.markdown-generator.demo._validate_project
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.normalize_topic
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.build_markdown_outline
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.render_markdown_sections
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.guard_markdown_contract
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.normalize_topic
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.build_markdown_outline
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.render_markdown_sections
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.guard_markdown_contract
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
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._load_litellm_completion
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._resolve_model
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._resolve_api_key
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._build_prompt
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._strip_markdown_fence
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._json_line_strings
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._lines_to_proposals
  src.intract.watch.snapshot_tree → src.intract.watch.should_scan
  src.intract.watch.snapshot_tree → src.intract.watch.hash_file
  src.intract.watch.watch_tree → src.intract.watch.snapshot_tree
  src.intract.watch.watch_tree → src.intract.watch.diff_snapshots
  src.intract.cli.init → src.intract.parsers.manifest.create_sample_manifest
  src.intract.cli._scan_artifacts → src.intract.scan_artifacts.scan_all_artifacts
  src.intract.cli._scan_artifacts → src.intract.cli._print_artifact_scan_report
  src.intract.cli._scan_contract_file → src.intract.parsers.inline.extract_contract_records_from_text
  src.intract.cli._scan_inline_records → src.intract.cli._scan_contract_file
  src.intract.cli._scan_inline_records → src.intract.cli._is_scan_candidate
  src.intract.cli.scan → src.intract.cli._print_scan_table
  src.intract.cli.scan → src.intract.cli._scan_artifacts
  src.intract.cli.scan → src.intract.cli._scan_row
  src.intract.cli.scan → src.intract.cli._scan_inline_records
  src.intract.cli.validate → src.intract.project.validate_project
  src.intract.cli.validate → src.intract.cli._print_validation_report
  src.intract.cli.validate → src.intract.cli._export_tickets
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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
  src.intract.graph.build_graph
    CC=9  in:5  out:18  total:23
  src.intract.integrations.planfile_adapter._ticket_from_dict
    CC=2  in:2  out:21  total:23
  src.intract.integrations.nexu._base_intent_contract
    CC=2  in:2  out:21  total:23
  src.intract.parsers.inline.clean_comment_line
    CC=12  in:2  out:20  total:22
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:3  out:17  total:20
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
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
  examples.markdown-generator.demo._validate_project → src.intract.project.validate_project
  examples.markdown-generator.demo.main → examples.markdown-generator.demo._load_pass_generator
  examples.markdown-generator.demo.main → examples.markdown-generator.demo._validate_project
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.normalize_topic
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.build_markdown_outline
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.render_markdown_sections
  examples.markdown-generator.pass.generator.generate_markdown_document → examples.markdown-generator.pass.generator.guard_markdown_contract
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.normalize_topic
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.build_markdown_outline
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.render_markdown_sections
  examples.markdown-generator.violation.generator.generate_markdown_document → examples.markdown-generator.violation.generator.guard_markdown_contract
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
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._load_litellm_completion
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._resolve_model
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._resolve_api_key
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._build_prompt
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._strip_markdown_fence
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._json_line_strings
  src.intract.propose_llm.propose_contracts_llm → src.intract.propose_llm._lines_to_proposals
  src.intract.watch.snapshot_tree → src.intract.watch.should_scan
  src.intract.watch.snapshot_tree → src.intract.watch.hash_file
  src.intract.watch.watch_tree → src.intract.watch.snapshot_tree
  src.intract.watch.watch_tree → src.intract.watch.diff_snapshots
  src.intract.cli.init → src.intract.parsers.manifest.create_sample_manifest
  src.intract.cli._scan_artifacts → src.intract.scan_artifacts.scan_all_artifacts
  src.intract.cli._scan_artifacts → src.intract.cli._print_artifact_scan_report
  src.intract.cli._scan_contract_file → src.intract.parsers.inline.extract_contract_records_from_text
  src.intract.cli._scan_inline_records → src.intract.cli._scan_contract_file
  src.intract.cli._scan_inline_records → src.intract.cli._is_scan_candidate
  src.intract.cli.scan → src.intract.cli._print_scan_table
  src.intract.cli.scan → src.intract.cli._scan_artifacts
  src.intract.cli.scan → src.intract.cli._scan_row
  src.intract.cli.scan → src.intract.cli._scan_inline_records
  src.intract.cli.validate → src.intract.project.validate_project
  src.intract.cli.validate → src.intract.cli._print_validation_report
  src.intract.cli.validate → src.intract.cli._export_tickets
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 160f 11397L | python:101,yaml:16,json:11,typescript:7,shell:5,toml:4,javascript:2,csharp:2,go:2,txt:1,yml:1,intract:1,java:1,rust:1 | 2026-06-05
# generated in 0.03s
# CC̅=3.5 | critical:0/474 | dups:0 | cycles:0

HEALTH[0]: ok

REFACTOR[0]: none needed

PIPELINES[160]:
  [1] Src [read_profile]: read_profile
      PURITY: 100% pure
  [2] Src [check_permission]: check_permission
      PURITY: 100% pure
  [3] Src [check_permission]: check_permission
      PURITY: 100% pure
  [4] Src [renderDashboard]: renderDashboard
      PURITY: 100% pure
  [5] Src [detect_duplicates]: detect_duplicates
      PURITY: 100% pure
  [6] Src [load_extension_list]: load_extension_list
      PURITY: 100% pure
  [7] Src [scan_project_files]: scan_project_files
      PURITY: 100% pure
  [8] Src [parse_extensions]: parse_extensions
      PURITY: 100% pure
  [9] Src [main]: main → _load_pass_generator
      PURITY: 100% pure
  [10] Src [generate_markdown_document]: generate_markdown_document → normalize_topic
      PURITY: 100% pure
  [11] Src [generate_markdown_document]: generate_markdown_document → normalize_topic
      PURITY: 100% pure
  [12] Src [__init__]: __init__
      PURITY: 100% pure
  [13] Src [_write_json]: _write_json
      PURITY: 100% pure
  [14] Src [do_GET]: do_GET → resolve_runtime_config → load_env_file
      PURITY: 100% pure
  [15] Src [do_POST]: do_POST → resolve_runtime_config → load_env_file
      PURITY: 100% pure
  [16] Src [main]: main
      PURITY: 100% pure
  [17] Src [fetchUserProfile]: fetchUserProfile
      PURITY: 100% pure
  [18] Src [divide]: divide
      PURITY: 100% pure
  [19] Src [write_to_log]: write_to_log
      PURITY: 100% pure
  [20] Src [main]: main → run_example_01 → validate_project → load_project_sources → ...(2 more)
      PURITY: 100% pure
  [21] Src [canUpdateResource]: canUpdateResource
      PURITY: 100% pure
  [22] Src [response]: response
      PURITY: 100% pure
  [23] Src [render_summary]: render_summary
      PURITY: 100% pure
  [24] Src [collect_project_files]: collect_project_files
      PURITY: 100% pure
  [25] Src [parse_extensions]: parse_extensions
      PURITY: 100% pure
  [26] Src [CollectFiles]: CollectFiles
      PURITY: 100% pure
  [27] Src [from_mapping]: from_mapping
      PURITY: 100% pure
  [28] Src [main]: main
      PURITY: 100% pure
  [29] Src [init]: init → create_sample_manifest
      PURITY: 100% pure
  [30] Src [scan]: scan → _print_scan_table
      PURITY: 100% pure
  [31] Src [validate]: validate → validate_project → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [32] Src [check]: check → load_config
      PURITY: 100% pure
  [33] Src [coverage]: coverage → calculate_coverage → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [34] Src [duplicates]: duplicates → find_duplicate_contracts → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [35] Src [graph]: graph → build_graph → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [36] Src [tickets]: tickets → validate_project → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [37] Src [planfile_push]: planfile_push → validate_project → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [38] Src [planfile_pull]: planfile_pull
      PURITY: 100% pure
  [39] Src [planfile_sync]: planfile_sync → validate_project → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [40] Src [planfile_webhook_test]: planfile_webhook_test
      PURITY: 100% pure
  [41] Src [planfile_webhook_apply]: planfile_webhook_apply
      PURITY: 100% pure
  [42] Src [watch]: watch → validate_project → load_project_sources → infer_artifact_kind → ...(1 more)
      PURITY: 100% pure
  [43] Src [engine_suggest]: engine_suggest → scan_suggest_and_validate → collect_source_units → infer_language
      PURITY: 100% pure
  [44] Src [engine_drift]: engine_drift → scan_suggest_and_validate → collect_source_units → infer_language
      PURITY: 100% pure
  [45] Src [engine_run]: engine_run → scan_suggest_and_validate → collect_source_units → infer_language
      PURITY: 100% pure
  [46] Src [check_manifest]: check_manifest → validate_manifest → _load_manifest_data → _invalid_manifest_report → ...(1 more)
      PURITY: 100% pure
  [47] Src [artifact_validate]: artifact_validate → validate_artifact → validate_dockerfile
      PURITY: 100% pure
  [48] Src [propose_delta]: propose_delta → propose_ui_delta_contracts → _ui_contract_line
      PURITY: 100% pure
  [49] Src [propose_llm_cmd]: propose_llm_cmd → propose_contracts_llm → _load_litellm_completion
      PURITY: 100% pure
  [50] Src [manifest_apply_ledger]: manifest_apply_ledger → apply_ledger_to_manifest → load_manifest_document
      PURITY: 100% pure

LAYERS:
  sdks/                           CC̄=4.4    ←in:0  →out:0
  │ sdk.go                      68L  1C    2m  CC=11     ←0
  │ lib.rs                      54L  1C    2m  CC=10     ←0
  │ IntractContract.java        50L  1C    2m  CC=11     ←0
  │ index.ts                    42L  0C    3m  CC=10     ←0
  │ IntractContract.cs          38L  1C    1m  CC=9      ←0
  │ __init__                    26L  2C    4m  CC=2      ←0
  │ main.go                     22L  0C    1m  CC=1      ←0
  │ pyproject.toml              19L  0C    0m  CC=0.0    ←0
  │ package.json                16L  0C    0m  CC=0.0    ←0
  │ basic.ts                    13L  0C    0m  CC=0.0    ←0
  │ tsconfig.json               10L  0C    0m  CC=0.0    ←0
  │ Cargo.toml                   9L  0C    0m  CC=0.0    ←0
  │ intract.config.ts            8L  0C    0m  CC=0.0    ←0
  │
  src/                            CC̄=3.8    ←in:0  →out:0
  │ !! cli                        683L  0C   33m  CC=13     ←0
  │ inline                     335L  1C   24m  CC=13     ←9
  │ check                      297L  1C   15m  CC=14     ←2
  │ redup                      287L  4C   19m  CC=8      ←0
  │ planfile_adapter           255L  4C   13m  CC=13     ←0
  │ manifest_ops               243L  2C   13m  CC=13     ←1
  │ nexu                       189L  1C   13m  CC=9      ←0
  │ artifacts                  181L  1C    6m  CC=9      ←3
  │ manifest                   177L  0C   12m  CC=9      ←8
  │ toon                       169L  0C   13m  CC=8      ←2
  │ project                    167L  0C    8m  CC=9      ←11
  │ propose_llm                166L  0C   10m  CC=7      ←2
  │ watch                      160L  3C    6m  CC=10     ←2
  │ models                     154L  7C    2m  CC=2      ←0
  │ planfile                   141L  2C    7m  CC=11     ←3
  │ grouping                   138L  2C    6m  CC=6      ←3
  │ artifact                   132L  2C    5m  CC=10     ←3
  │ handlers                   124L  0C    9m  CC=4      ←0
  │ signatures                 122L  1C    8m  CC=3      ←8
  │ server                     118L  0C    5m  CC=5      ←0
  │ manifest_schema            116L  2C    8m  CC=9      ←2
  │ vallm                      116L  2C    5m  CC=12     ←2
  │ drift                      113L  2C    5m  CC=5      ←1
  │ builtins                   111L  6C   11m  CC=3      ←0
  │ base                       109L  6C   12m  CC=5      ←0
  │ assigner                   109L  0C    6m  CC=10     ←1
  │ policy                     106L  1C    7m  CC=7      ←3
  │ proposals                  100L  1C    4m  CC=9      ←1
  │ cache                       99L  2C    7m  CC=4      ←0
  │ schemas                     91L  0C    0m  CC=0.0    ←0
  │ registry                    85L  1C    8m  CC=7      ←1
  │ analyzer                    85L  0C    4m  CC=12     ←1
  │ input_output                74L  3C    8m  CC=7      ←0
  │ scan_artifacts              70L  1C    3m  CC=7      ←2
  │ python_ast                  70L  0C    3m  CC=14     ←0
  │ normalizer                  69L  0C    4m  CC=7      ←4
  │ graph                       68L  1C    4m  CC=9      ←3
  │ typescript                  66L  0C    3m  CC=11     ←0
  │ csharp                      65L  0C    3m  CC=8      ←0
  │ config                      64L  1C    2m  CC=11     ←3
  │ openapi                     63L  0C    2m  CC=8      ←2
  │ sarif                       62L  0C    1m  CC=11     ←1
  │ treesitter                  62L  0C    4m  CC=7      ←2
  │ manager                     61L  0C    3m  CC=6      ←0
  │ __init__                    59L  0C    0m  CC=0.0    ←0
  │ matcher                     55L  1C    2m  CC=6      ←2
  │ engine                      54L  0C    1m  CC=8      ←4
  │ git                         53L  1C    5m  CC=4      ←1
  │ scanner                     53L  1C    1m  CC=9      ←1
  │ effects                     52L  1C    3m  CC=9      ←0
  │ base                        50L  3C    3m  CC=2      ←1
  │ sdk                         47L  1C    2m  CC=9      ←0
  │ blocks                      46L  0C    2m  CC=8      ←3
  │ __init__                    44L  0C    0m  CC=0.0    ←0
  │ scoring                     37L  0C    3m  CC=5      ←1
  │ context                     36L  3C    0m  CC=0.0    ←0
  │ __init__                    35L  0C    0m  CC=0.0    ←0
  │ coverage                    34L  1C    2m  CC=3      ←1
  │ monitor                     32L  0C    1m  CC=4      ←2
  │ validate_snippet            28L  0C    1m  CC=3      ←0
  │ java                        27L  0C    1m  CC=4      ←0
  │ __init__                    24L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ rust                        15L  0C    1m  CC=1      ←0
  │ __init__                    15L  0C    0m  CC=0.0    ←0
  │ requirements                13L  0C    1m  CC=6      ←1
  │ go                          13L  0C    1m  CC=1      ←0
  │ validation                  13L  0C    0m  CC=0.0    ←0
  │ __init__                    13L  0C    0m  CC=0.0    ←0
  │ mcp_server                   6L  0C    0m  CC=0.0    ←0
  │ registry                     6L  0C    0m  CC=0.0    ←0
  │ artifacts                    5L  0C    0m  CC=0.0    ←0
  │ effects                      5L  0C    0m  CC=0.0    ←0
  │ __main__                     4L  0C    0m  CC=0.0    ←0
  │ normalizer                   3L  0C    0m  CC=0.0    ←0
  │ signature                    3L  0C    0m  CC=0.0    ←0
  │ parser                       3L  0C    0m  CC=0.0    ←0
  │ models                       3L  0C    0m  CC=0.0    ←0
  │ yaml_manifest                3L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=3.8    ←in:0  →out:2
  │ generate_toon_from_map     475L  2C   18m  CC=9      ←0
  │ ci-full-stack.sh            76L  0C    1m  CC=0.0    ←0
  │
  examples/                       CC̄=2.3    ←in:0  →out:0
  │ v2-violation.validate.json   245L  0C    0m  CC=0.0    ←0
  │ v1-pass.validate.json      229L  0C    0m  CC=0.0    ←0
  │ server                     142L  1C    7m  CC=8      ←0
  │ run_examples               117L  0C    6m  CC=10     ←0
  │ generator                   82L  0C    5m  CC=4      ←0
  │ intract.yaml                82L  0C    0m  CC=0.0    ←0
  │ generator                   76L  0C    5m  CC=3      ←0
  │ demo                        68L  0C    4m  CC=4      ←0
  │ v2-violation.artifacts.json    66L  0C    0m  CC=0.0    ←0
  │ v1-pass.artifacts.json      55L  0C    0m  CC=0.0    ←0
  │ intract.yaml                35L  0C    0m  CC=0.0    ←0
  │ intract.toon.yaml           34L  0C    0m  CC=0.0    ←0
  │ intract.yaml                27L  0C    0m  CC=0.0    ←0
  │ v2-violation.graph.json     25L  0C    0m  CC=0.0    ←0
  │ v1-pass.graph.json          25L  0C    0m  CC=0.0    ←0
  │ validate.sh                 23L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 22L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                21L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                21L  0C    0m  CC=0.0    ←0
  │ run-demo.sh                 20L  0C    0m  CC=0.0    ←0
  │ Makefile                    20L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 20L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 19L  0C    0m  CC=0.0    ←0
  │ auth.js                     16L  0C    3m  CC=3      ←0
  │ calc                        15L  0C    3m  CC=2      ←0
  │ dashboard.ts                10L  0C    3m  CC=3      ←0
  │ dashboard.ts                 8L  0C    1m  CC=2      ←0
  │ scanner                      8L  0C    1m  CC=3      ←0
  │ app                          8L  0C    1m  CC=3      ←0
  │ ScanPipeline.cs              7L  0C    1m  CC=1      ←0
  │ Dockerfile                   7L  0C    0m  CC=0.0    ←0
  │ run-demo.sh                  7L  0C    0m  CC=0.0    ←0
  │ auth                         6L  0C    1m  CC=1      ←0
  │ permission.ts                6L  0C    3m  CC=1      ←0
  │ auth                         5L  0C    1m  CC=2      ←0
  │ permission.ts                5L  0C    2m  CC=2      ←0
  │ Dockerfile                   5L  0C    0m  CC=0.0    ←0
  │ routes                       4L  0C    1m  CC=1      ←0
  │ scanner                      4L  0C    1m  CC=1      ←0
  │ reporter                     4L  0C    1m  CC=1      ←0
  │ analyzer                     3L  0C    1m  CC=1      ←0
  │ parser_b                     3L  0C    1m  CC=1      ←0
  │ parser_a                     3L  0C    1m  CC=3      ←0
  │
  extensions/                     CC̄=1.3    ←in:0  →out:0
  │ package.json               105L  0C    0m  CC=0.0    ←0
  │ extension.js                51L  0C   13m  CC=4      ←0
  │ intract.tmLanguage.json     19L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ tree.txt                   314L  0C    0m  CC=0.0    ←0
  │ Makefile                   111L  0C    0m  CC=0.0    ←0
  │ pyproject.toml             101L  0C    0m  CC=0.0    ←0
  │ action.yml                  91L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ pyqual.yaml                 38L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   9L  0C    0m  CC=0.0    ←0
  │ .pre-commit-hooks.yaml       6L  0C    0m  CC=0.0    ←0
  │
  schemas/                        CC̄=0.0    ←in:0  →out:0
  │ intract.schema.json         99L  0C    0m  CC=0.0    ←0
  │
  templates/                      CC̄=0.0    ←in:0  →out:0
  │ intract.yaml                36L  0C    0m  CC=0.0    ←0
  │ openapi.intract.yaml        21L  0C    0m  CC=0.0    ←0
  │ pyproject-intract.toml      16L  0C    0m  CC=0.0    ←0
  │ Dockerfile.intract          12L  0C    0m  CC=0.0    ←0
  │ .pre-commit-config.yaml      9L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │
  ── zero ──
     src/intract/reporters/__init__.py         0L

COUPLING:
                                               src.intract   examples.integration_tests                      scripts  examples.markdown-generator
                  src.intract                           ──                           ←9                           ←2                           ←1  hub
   examples.integration_tests                            9                           ──                                                            !! fan-out
                      scripts                            2                                                        ──                             
  examples.markdown-generator                            1                                                                                     ──
  CYCLES: none
  HUB: src.intract/ (fan-in=12)
  SMELL: examples.integration_tests/ fan-out=9 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 6 groups | 97f 8069L | 2026-06-05

SUMMARY:
  files_scanned: 97
  total_lines:   8069
  dup_groups:    6
  dup_fragments: 12
  saved_lines:   51
  scan_ms:       2418

HOTSPOTS[7] (files with most duplication):
  src/intract/analyzers/csharp.py  dup=25L  groups=2  frags=2  (0.3%)
  src/intract/analyzers/blocks.py  dup=19L  groups=1  frags=1  (0.2%)
  examples/markdown-generator/pass/generator.py  dup=18L  groups=2  frags=2  (0.2%)
  examples/markdown-generator/violation/generator.py  dup=18L  groups=2  frags=2  (0.2%)
  src/intract/mcp/handlers.py  dup=10L  groups=1  frags=2  (0.1%)
  src/intract/analyzers/typescript.py  dup=6L  groups=1  frags=1  (0.1%)
  examples/web-app/iterations/v1-pass/backend/routes.py  dup=3L  groups=1  frags=1  (0.0%)

DUPLICATES[6] (ranked by impact):
  [ef612f5468430a71]   STRU  scan_braced_block  L=19 N=2 saved=19 sim=1.00
      src/intract/analyzers/blocks.py:6-24  (scan_braced_block)
      src/intract/analyzers/csharp.py:39-57  (_scan_braced_block)
  [ff5c895aacf2a3d8]   EXAC  generate_markdown_document  L=13 N=2 saved=13 sim=1.00
      examples/markdown-generator/pass/generator.py:66-78  (generate_markdown_document)
      examples/markdown-generator/violation/generator.py:64-76  (generate_markdown_document)
  [ac0065a129c81ecd]   STRU  _treesitter_csharp_extent  L=6 N=2 saved=6 sim=1.00
      src/intract/analyzers/csharp.py:60-65  (_treesitter_csharp_extent)
      src/intract/analyzers/typescript.py:61-66  (_treesitter_typescript_extent)
  [16a76191517e9cbf]   EXAC  normalize_topic  L=5 N=2 saved=5 sim=1.00
      examples/markdown-generator/pass/generator.py:9-13  (normalize_topic)
      examples/markdown-generator/violation/generator.py:11-15  (normalize_topic)
  [a1077c782ef473a0]   STRU  handle_validate_project  L=5 N=2 saved=5 sim=1.00
      src/intract/mcp/handlers.py:36-40  (handle_validate_project)
      src/intract/mcp/handlers.py:90-94  (handle_build_graph)
  [1c8e027e2ce0b262]   EXAC  read_profile  L=3 N=2 saved=3 sim=1.00
      examples/web-app/iterations/v1-pass/backend/routes.py:2-4  (read_profile)
      examples/web-app/iterations/v2-violation/backend/routes.py:2-4  (read_profile)

REFACTOR[6] (ranked by priority):
  [1] ○ extract_function   → src/intract/analyzers/utils/scan_braced_block.py
      WHY: 2 occurrences of 19-line block across 2 files — saves 19 lines
      FILES: src/intract/analyzers/blocks.py, src/intract/analyzers/csharp.py
  [2] ○ extract_function   → examples/markdown-generator/utils/generate_markdown_document.py
      WHY: 2 occurrences of 13-line block across 2 files — saves 13 lines
      FILES: examples/markdown-generator/pass/generator.py, examples/markdown-generator/violation/generator.py
  [3] ○ extract_function   → src/intract/analyzers/utils/_treesitter_csharp_extent.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: src/intract/analyzers/csharp.py, src/intract/analyzers/typescript.py
  [4] ○ extract_function   → examples/markdown-generator/utils/normalize_topic.py
      WHY: 2 occurrences of 5-line block across 2 files — saves 5 lines
      FILES: examples/markdown-generator/pass/generator.py, examples/markdown-generator/violation/generator.py
  [5] ○ extract_function   → src/intract/mcp/utils/handle_validate_project.py
      WHY: 2 occurrences of 5-line block across 1 files — saves 5 lines
      FILES: src/intract/mcp/handlers.py
  [6] ○ extract_function   → examples/web-app/iterations/utils/read_profile.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: examples/web-app/iterations/v1-pass/backend/routes.py, examples/web-app/iterations/v2-violation/backend/routes.py

QUICK_WINS[3] (low risk, high savings — do first):
  [1] extract_function   saved=19L  → src/intract/analyzers/utils/scan_braced_block.py
      FILES: blocks.py, csharp.py
  [2] extract_function   saved=13L  → examples/markdown-generator/utils/generate_markdown_document.py
      FILES: generator.py, generator.py
  [3] extract_function   saved=6L  → src/intract/analyzers/utils/_treesitter_csharp_extent.py
      FILES: csharp.py, typescript.py

EFFORT_ESTIMATE (total ≈ 1.7h):
  medium scan_braced_block                   saved=19L  ~38min
  easy   generate_markdown_document          saved=13L  ~26min
  easy   _treesitter_csharp_extent           saved=6L  ~12min
  easy   normalize_topic                     saved=5L  ~10min
  easy   handle_validate_project             saved=5L  ~10min
  easy   read_profile                        saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  6 → 0
  saved_lines: 51 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 401 func | 66f | 2026-06-05
# generated in 0.00s

NEXT[2] (ranked by impact):
  [1] !! SPLIT           src/intract/cli.py
      WHY: 683L, 0 classes, max CC=13
      EFFORT: ~4h  IMPACT: 8879

  [2] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting src/intract/cli.py may break 33 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.7 → ≤2.6
  max-CC:      14 → ≤7
  god-modules: 2 → 0
  high-CC(≥15): 0 → ≤0
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=3.7 → now CC̄=3.7
```

## Intent

Intent contract tagging, validation and semantic mapping for codebases.
