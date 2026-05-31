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
- **version**: `0.5.6`
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
  version: 0.5.6;
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
  step-1: run cmd=pip install -e .[dev];
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=pytest -q;
}

workflow[name="lint"] {
  trigger: manual;
  step-1: run cmd=ruff check .;
}

workflow[name="format"] {
  trigger: manual;
  step-1: run cmd=ruff format .;
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

*185 nodes · 223 edges · 54 modules · CC̄=4.1*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `contract_from_mapping` *(in src.intract.parsers.manifest)* | 3 | 4 | 59 | **63** |
| `parse_contract_line` *(in src.intract.parsers.inline)* | 42 ⚠ | 1 | 51 | **52** |
| `build_signature` *(in src.intract.core.signatures)* | 15 ⚠ | 3 | 40 | **43** |
| `validate_manifest` *(in src.intract.manifest_schema)* | 15 ⚠ | 2 | 35 | **37** |
| `normalize_label` *(in src.intract.core.normalizer)* | 7 | 11 | 16 | **27** |
| `load_manifest_records` *(in src.intract.parsers.manifest)* | 11 ⚠ | 7 | 19 | **26** |
| `tickets_from_report` *(in src.intract.integrations.planfile)* | 11 ⚠ | 3 | 21 | **24** |
| `_ticket_from_dict` *(in src.intract.integrations.planfile_adapter)* | 2 | 2 | 21 | **23** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/intract
# generated in 0.08s
# nodes: 185 | edges: 223 | modules: 54
# CC̄=4.1

HUBS[20]:
  src.intract.parsers.manifest.contract_from_mapping
    CC=3  in:4  out:59  total:63
  src.intract.parsers.inline.parse_contract_line
    CC=42  in:1  out:51  total:52
  src.intract.core.signatures.build_signature
    CC=15  in:3  out:40  total:43
  src.intract.manifest_schema.validate_manifest
    CC=15  in:2  out:35  total:37
  src.intract.core.normalizer.normalize_label
    CC=7  in:11  out:16  total:27
  src.intract.parsers.manifest.load_manifest_records
    CC=11  in:7  out:19  total:26
  src.intract.integrations.planfile.tickets_from_report
    CC=11  in:3  out:21  total:24
  src.intract.integrations.planfile_adapter._ticket_from_dict
    CC=2  in:2  out:21  total:23
  src.intract.graph.build_graph
    CC=9  in:4  out:18  total:22
  src.intract.project.validate_project
    CC=4  in:13  out:8  total:21
  src.intract.policy.decide_policy
    CC=15  in:2  out:19  total:21
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:3  out:17  total:20
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
  src.intract.validators.engine.validate_contract_against_source
    CC=8  in:5  out:14  total:19
  src.intract.check.block_extent
    CC=20  in:1  out:18  total:19
  src.intract.cli.engine_suggest
    CC=3  in:0  out:18  total:18
  examples.integration_tests.run_examples.run_example_03
    CC=2  in:1  out:17  total:18
  src.intract.engine.analyzer.analyze_source_units
    CC=12  in:1  out:17  total:18
  src.intract.parsers.openapi.parse_openapi_contracts
    CC=8  in:1  out:16  total:17

MODULES:
  examples.integration_tests.run_examples  [5 funcs]
    main  CC=7  out:8
    print_result  CC=1  out:3
    run_example_01  CC=1  out:4
    run_example_02  CC=2  out:10
    run_example_03  CC=2  out:17
  extensions.vscode-intract.extension  [2 funcs]
    activate  CC=7  out:5
    runIntract  CC=1  out:6
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
  src.intract.check  [10 funcs]
    _manifest_changed  CC=2  out:2
    block_extent  CC=20  out:18
    changed_check  CC=1  out:4
    changed_lines_by_file  CC=4  out:4
    load_selected_sources  CC=5  out:4
    parse_unified_diff_hunks  CC=6  out:16
    signature_touched  CC=2  out:4
    staged_check  CC=4  out:8
    validate_selected_paths  CC=8  out:10
    validate_sources_for_hunks  CC=14  out:15
  src.intract.cli  [15 funcs]
    _export_tickets  CC=1  out:6
    _print_validation_report  CC=4  out:15
    artifact_validate  CC=4  out:11
    check_manifest  CC=4  out:12
    coverage  CC=2  out:12
    duplicates  CC=4  out:17
    engine_drift  CC=4  out:21
    engine_run  CC=4  out:20
    engine_suggest  CC=3  out:18
    graph  CC=5  out:16
  src.intract.config  [1 funcs]
    load_config  CC=11  out:14
  src.intract.core.artifact  [3 funcs]
    from_path  CC=2  out:8
    infer_artifact_kind  CC=17  out:8
    infer_language  CC=1  out:3
  src.intract.core.normalizer  [4 funcs]
    normalize_action  CC=4  out:3
    normalize_label  CC=7  out:16
    normalize_many  CC=4  out:4
    normalize_requirement  CC=6  out:10
  src.intract.core.signatures  [2 funcs]
    build_signature  CC=15  out:40
    build_signatures  CC=2  out:1
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
  src.intract.integrations.planfile  [1 funcs]
    tickets_from_report  CC=11  out:21
  src.intract.integrations.planfile_adapter  [3 funcs]
    pull  CC=7  out:10
    sync_from_report  CC=3  out:9
    _ticket_from_dict  CC=2  out:21
  src.intract.integrations.redup  [10 funcs]
    _with_block_lines  CC=1  out:3
    block_end_line  CC=3  out:4
    block_file_path  CC=3  out:3
    block_start_line  CC=3  out:3
    block_text  CC=4  out:3
    find_intent_duplicate_groups  CC=8  out:10
    scan_blocks_for_intent_duplicates  CC=2  out:4
    signatures_from_blocks  CC=5  out:6
    signatures_from_manifest  CC=1  out:3
    signatures_from_text  CC=1  out:2
  src.intract.integrations.vallm  [4 funcs]
    map_project_report  CC=7  out:3
    map_validation_result  CC=6  out:4
    validate_for_vallm  CC=2  out:3
    validate_proposal  CC=12  out:9
  src.intract.manifest_schema  [2 funcs]
    _load_schema  CC=2  out:5
    validate_manifest  CC=15  out:35
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
  src.intract.parsers.inline  [6 funcs]
    clean_comment_line  CC=8  out:14
    extract_contract_records_from_text  CC=3  out:5
    marker_payload  CC=3  out:3
    parse_contract_line  CC=42  out:51
    parse_key_value  CC=2  out:5
    parse_priority  CC=5  out:9
  src.intract.parsers.manifest  [4 funcs]
    _parse_intent  CC=3  out:7
    contract_from_mapping  CC=3  out:59
    create_sample_manifest  CC=1  out:0
    load_manifest_records  CC=11  out:19
  src.intract.parsers.openapi  [2 funcs]
    parse_openapi_contracts  CC=8  out:16
    parse_openapi_text  CC=8  out:14
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
  src.intract.policy  [2 funcs]
    _p1_missing_reasons  CC=7  out:6
    decide_policy  CC=15  out:19
  src.intract.project  [4 funcs]
    extract_signatures_from_sources  CC=2  out:4
    load_project_sources  CC=9  out:8
    validate_project  CC=4  out:8
    validate_sources  CC=16  out:15
  src.intract.scan_artifacts  [2 funcs]
    discover_artifact_paths  CC=7  out:11
    scan_all_artifacts  CC=3  out:7
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
  examples.integration_tests.run_examples.run_example_01 → src.intract.project.validate_project
  examples.integration_tests.run_examples.run_example_02 → src.intract.project.validate_project
  examples.integration_tests.run_examples.run_example_02 → src.intract.integrations.planfile.tickets_from_report
  examples.integration_tests.run_examples.run_example_03 → src.intract.watch.snapshot_tree
  examples.integration_tests.run_examples.run_example_03 → src.intract.watch.diff_snapshots
  examples.integration_tests.run_examples.run_example_03 → src.intract.engine.monitor.scan_suggest_and_validate
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_01
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_02
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_03
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.print_result
  src.intract.watch.snapshot_tree → src.intract.watch.should_scan
  src.intract.watch.snapshot_tree → src.intract.watch.hash_file
  src.intract.watch.watch_tree → src.intract.watch.snapshot_tree
  src.intract.watch.watch_tree → src.intract.watch.diff_snapshots
  src.intract.cli.init → src.intract.parsers.manifest.create_sample_manifest
  src.intract.cli.validate → src.intract.project.validate_project
  src.intract.cli.validate → src.intract.cli._print_validation_report
  src.intract.cli.validate → src.intract.cli._export_tickets
  src.intract.cli.coverage → src.intract.coverage.calculate_coverage
  src.intract.cli.duplicates → src.intract.duplicates.grouping.find_duplicate_contracts
  src.intract.cli.graph → src.intract.graph.build_graph
  src.intract.cli.tickets → src.intract.project.validate_project
  src.intract.cli.tickets → src.intract.cli._export_tickets
  src.intract.cli.planfile_push → src.intract.project.validate_project
  src.intract.cli.planfile_sync → src.intract.project.validate_project
  src.intract.cli.engine_suggest → src.intract.engine.monitor.scan_suggest_and_validate
  src.intract.cli.engine_drift → src.intract.engine.monitor.scan_suggest_and_validate
  src.intract.cli.engine_run → src.intract.engine.monitor.scan_suggest_and_validate
  src.intract.cli._export_tickets → src.intract.integrations.planfile.tickets_from_report
  src.intract.cli.check_manifest → src.intract.manifest_schema.validate_manifest
  src.intract.cli.artifact_validate → src.intract.validators.artifacts.validate_artifact
  src.intract.scan_artifacts.discover_artifact_paths → src.intract.core.artifact.infer_artifact_kind
  src.intract.scan_artifacts.scan_all_artifacts → src.intract.scan_artifacts.discover_artifact_paths
  src.intract.scan_artifacts.scan_all_artifacts → src.intract.validators.artifacts.validate_artifact
  src.intract.check.block_extent → src.intract.analyzers.python_ast.python_block_extent
  src.intract.check.block_extent → src.intract.analyzers.typescript.typescript_block_extent
  src.intract.check.block_extent → src.intract.analyzers.csharp.csharp_block_extent
  src.intract.check.block_extent → src.intract.analyzers.java.java_block_extent
  src.intract.check.block_extent → src.intract.analyzers.go.go_block_extent
  src.intract.check.signature_touched → src.intract.check.block_extent
  src.intract.check.validate_sources_for_hunks → src.intract.check.load_selected_sources
  src.intract.check.validate_sources_for_hunks → src.intract.check.changed_lines_by_file
  src.intract.check.validate_sources_for_hunks → src.intract.parsers.inline.extract_contract_records_from_text
  src.intract.check.validate_sources_for_hunks → src.intract.validators.engine.validate_contract_against_source
  src.intract.check.validate_sources_for_hunks → src.intract.core.signatures.build_signatures
  src.intract.check.validate_selected_paths → src.intract.check.load_selected_sources
  src.intract.check.validate_selected_paths → src.intract.project.validate_sources
  src.intract.check.validate_selected_paths → src.intract.project.validate_project
  src.intract.check.validate_selected_paths → src.intract.parsers.manifest.load_manifest_records
  src.intract.check.staged_check → src.intract.git.staged_files
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
# generated in 0.08s
# nodes: 185 | edges: 223 | modules: 54
# CC̄=4.1

HUBS[20]:
  src.intract.parsers.manifest.contract_from_mapping
    CC=3  in:4  out:59  total:63
  src.intract.parsers.inline.parse_contract_line
    CC=42  in:1  out:51  total:52
  src.intract.core.signatures.build_signature
    CC=15  in:3  out:40  total:43
  src.intract.manifest_schema.validate_manifest
    CC=15  in:2  out:35  total:37
  src.intract.core.normalizer.normalize_label
    CC=7  in:11  out:16  total:27
  src.intract.parsers.manifest.load_manifest_records
    CC=11  in:7  out:19  total:26
  src.intract.integrations.planfile.tickets_from_report
    CC=11  in:3  out:21  total:24
  src.intract.integrations.planfile_adapter._ticket_from_dict
    CC=2  in:2  out:21  total:23
  src.intract.graph.build_graph
    CC=9  in:4  out:18  total:22
  src.intract.project.validate_project
    CC=4  in:13  out:8  total:21
  src.intract.policy.decide_policy
    CC=15  in:2  out:19  total:21
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:3  out:17  total:20
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
  src.intract.validators.engine.validate_contract_against_source
    CC=8  in:5  out:14  total:19
  src.intract.check.block_extent
    CC=20  in:1  out:18  total:19
  src.intract.cli.engine_suggest
    CC=3  in:0  out:18  total:18
  examples.integration_tests.run_examples.run_example_03
    CC=2  in:1  out:17  total:18
  src.intract.engine.analyzer.analyze_source_units
    CC=12  in:1  out:17  total:18
  src.intract.parsers.openapi.parse_openapi_contracts
    CC=8  in:1  out:16  total:17

MODULES:
  examples.integration_tests.run_examples  [5 funcs]
    main  CC=7  out:8
    print_result  CC=1  out:3
    run_example_01  CC=1  out:4
    run_example_02  CC=2  out:10
    run_example_03  CC=2  out:17
  extensions.vscode-intract.extension  [2 funcs]
    activate  CC=7  out:5
    runIntract  CC=1  out:6
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
  src.intract.check  [10 funcs]
    _manifest_changed  CC=2  out:2
    block_extent  CC=20  out:18
    changed_check  CC=1  out:4
    changed_lines_by_file  CC=4  out:4
    load_selected_sources  CC=5  out:4
    parse_unified_diff_hunks  CC=6  out:16
    signature_touched  CC=2  out:4
    staged_check  CC=4  out:8
    validate_selected_paths  CC=8  out:10
    validate_sources_for_hunks  CC=14  out:15
  src.intract.cli  [15 funcs]
    _export_tickets  CC=1  out:6
    _print_validation_report  CC=4  out:15
    artifact_validate  CC=4  out:11
    check_manifest  CC=4  out:12
    coverage  CC=2  out:12
    duplicates  CC=4  out:17
    engine_drift  CC=4  out:21
    engine_run  CC=4  out:20
    engine_suggest  CC=3  out:18
    graph  CC=5  out:16
  src.intract.config  [1 funcs]
    load_config  CC=11  out:14
  src.intract.core.artifact  [3 funcs]
    from_path  CC=2  out:8
    infer_artifact_kind  CC=17  out:8
    infer_language  CC=1  out:3
  src.intract.core.normalizer  [4 funcs]
    normalize_action  CC=4  out:3
    normalize_label  CC=7  out:16
    normalize_many  CC=4  out:4
    normalize_requirement  CC=6  out:10
  src.intract.core.signatures  [2 funcs]
    build_signature  CC=15  out:40
    build_signatures  CC=2  out:1
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
  src.intract.integrations.planfile  [1 funcs]
    tickets_from_report  CC=11  out:21
  src.intract.integrations.planfile_adapter  [3 funcs]
    pull  CC=7  out:10
    sync_from_report  CC=3  out:9
    _ticket_from_dict  CC=2  out:21
  src.intract.integrations.redup  [10 funcs]
    _with_block_lines  CC=1  out:3
    block_end_line  CC=3  out:4
    block_file_path  CC=3  out:3
    block_start_line  CC=3  out:3
    block_text  CC=4  out:3
    find_intent_duplicate_groups  CC=8  out:10
    scan_blocks_for_intent_duplicates  CC=2  out:4
    signatures_from_blocks  CC=5  out:6
    signatures_from_manifest  CC=1  out:3
    signatures_from_text  CC=1  out:2
  src.intract.integrations.vallm  [4 funcs]
    map_project_report  CC=7  out:3
    map_validation_result  CC=6  out:4
    validate_for_vallm  CC=2  out:3
    validate_proposal  CC=12  out:9
  src.intract.manifest_schema  [2 funcs]
    _load_schema  CC=2  out:5
    validate_manifest  CC=15  out:35
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
  src.intract.parsers.inline  [6 funcs]
    clean_comment_line  CC=8  out:14
    extract_contract_records_from_text  CC=3  out:5
    marker_payload  CC=3  out:3
    parse_contract_line  CC=42  out:51
    parse_key_value  CC=2  out:5
    parse_priority  CC=5  out:9
  src.intract.parsers.manifest  [4 funcs]
    _parse_intent  CC=3  out:7
    contract_from_mapping  CC=3  out:59
    create_sample_manifest  CC=1  out:0
    load_manifest_records  CC=11  out:19
  src.intract.parsers.openapi  [2 funcs]
    parse_openapi_contracts  CC=8  out:16
    parse_openapi_text  CC=8  out:14
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
  src.intract.policy  [2 funcs]
    _p1_missing_reasons  CC=7  out:6
    decide_policy  CC=15  out:19
  src.intract.project  [4 funcs]
    extract_signatures_from_sources  CC=2  out:4
    load_project_sources  CC=9  out:8
    validate_project  CC=4  out:8
    validate_sources  CC=16  out:15
  src.intract.scan_artifacts  [2 funcs]
    discover_artifact_paths  CC=7  out:11
    scan_all_artifacts  CC=3  out:7
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
  examples.integration_tests.run_examples.run_example_01 → src.intract.project.validate_project
  examples.integration_tests.run_examples.run_example_02 → src.intract.project.validate_project
  examples.integration_tests.run_examples.run_example_02 → src.intract.integrations.planfile.tickets_from_report
  examples.integration_tests.run_examples.run_example_03 → src.intract.watch.snapshot_tree
  examples.integration_tests.run_examples.run_example_03 → src.intract.watch.diff_snapshots
  examples.integration_tests.run_examples.run_example_03 → src.intract.engine.monitor.scan_suggest_and_validate
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_01
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_02
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.run_example_03
  examples.integration_tests.run_examples.main → examples.integration_tests.run_examples.print_result
  src.intract.watch.snapshot_tree → src.intract.watch.should_scan
  src.intract.watch.snapshot_tree → src.intract.watch.hash_file
  src.intract.watch.watch_tree → src.intract.watch.snapshot_tree
  src.intract.watch.watch_tree → src.intract.watch.diff_snapshots
  src.intract.cli.init → src.intract.parsers.manifest.create_sample_manifest
  src.intract.cli.validate → src.intract.project.validate_project
  src.intract.cli.validate → src.intract.cli._print_validation_report
  src.intract.cli.validate → src.intract.cli._export_tickets
  src.intract.cli.coverage → src.intract.coverage.calculate_coverage
  src.intract.cli.duplicates → src.intract.duplicates.grouping.find_duplicate_contracts
  src.intract.cli.graph → src.intract.graph.build_graph
  src.intract.cli.tickets → src.intract.project.validate_project
  src.intract.cli.tickets → src.intract.cli._export_tickets
  src.intract.cli.planfile_push → src.intract.project.validate_project
  src.intract.cli.planfile_sync → src.intract.project.validate_project
  src.intract.cli.engine_suggest → src.intract.engine.monitor.scan_suggest_and_validate
  src.intract.cli.engine_drift → src.intract.engine.monitor.scan_suggest_and_validate
  src.intract.cli.engine_run → src.intract.engine.monitor.scan_suggest_and_validate
  src.intract.cli._export_tickets → src.intract.integrations.planfile.tickets_from_report
  src.intract.cli.check_manifest → src.intract.manifest_schema.validate_manifest
  src.intract.cli.artifact_validate → src.intract.validators.artifacts.validate_artifact
  src.intract.scan_artifacts.discover_artifact_paths → src.intract.core.artifact.infer_artifact_kind
  src.intract.scan_artifacts.scan_all_artifacts → src.intract.scan_artifacts.discover_artifact_paths
  src.intract.scan_artifacts.scan_all_artifacts → src.intract.validators.artifacts.validate_artifact
  src.intract.check.block_extent → src.intract.analyzers.python_ast.python_block_extent
  src.intract.check.block_extent → src.intract.analyzers.typescript.typescript_block_extent
  src.intract.check.block_extent → src.intract.analyzers.csharp.csharp_block_extent
  src.intract.check.block_extent → src.intract.analyzers.java.java_block_extent
  src.intract.check.block_extent → src.intract.analyzers.go.go_block_extent
  src.intract.check.signature_touched → src.intract.check.block_extent
  src.intract.check.validate_sources_for_hunks → src.intract.check.load_selected_sources
  src.intract.check.validate_sources_for_hunks → src.intract.check.changed_lines_by_file
  src.intract.check.validate_sources_for_hunks → src.intract.parsers.inline.extract_contract_records_from_text
  src.intract.check.validate_sources_for_hunks → src.intract.validators.engine.validate_contract_against_source
  src.intract.check.validate_sources_for_hunks → src.intract.core.signatures.build_signatures
  src.intract.check.validate_selected_paths → src.intract.check.load_selected_sources
  src.intract.check.validate_selected_paths → src.intract.project.validate_sources
  src.intract.check.validate_selected_paths → src.intract.project.validate_project
  src.intract.check.validate_selected_paths → src.intract.parsers.manifest.load_manifest_records
  src.intract.check.staged_check → src.intract.git.staged_files
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 142f 8337L | python:89,yaml:14,json:11,typescript:7,toml:4,shell:3,csharp:2,go:2,txt:1,yml:1,intract:1,javascript:1,java:1,rust:1 | 2026-05-31
# generated in 0.02s
# CC̅=4.1 | critical:8/297 | dups:0 | cycles:0

HEALTH[8]:
  🟡 CC    scan CC=15 (limit:15)
  🟡 CC    block_extent CC=20 (limit:15)
  🟡 CC    decide_policy CC=15 (limit:15)
  🟡 CC    validate_manifest CC=15 (limit:15)
  🟡 CC    infer_artifact_kind CC=17 (limit:15)
  🟡 CC    build_signature CC=15 (limit:15)
  🟡 CC    parse_contract_line CC=42 (limit:15)
  🟡 CC    validate_sources CC=16 (limit:15)

REFACTOR[1]:
  1. split 8 high-CC methods  (CC>15)

PIPELINES[114]:
  [1] Src [detect_duplicates]: detect_duplicates
      PURITY: 100% pure
  [2] Src [load_extension_list]: load_extension_list
      PURITY: 100% pure
  [3] Src [scan_project_files]: scan_project_files
      PURITY: 100% pure
  [4] Src [parse_extensions]: parse_extensions
      PURITY: 100% pure
  [5] Src [main]: main → run_example_01 → validate_project → load_project_sources → ...(1 more)
      PURITY: 100% pure
  [6] Src [canUpdateResource]: canUpdateResource
      PURITY: 100% pure
  [7] Src [response]: response
      PURITY: 100% pure
  [8] Src [render_summary]: render_summary
      PURITY: 100% pure
  [9] Src [collect_project_files]: collect_project_files
      PURITY: 100% pure
  [10] Src [parse_extensions]: parse_extensions
      PURITY: 100% pure
  [11] Src [CollectFiles]: CollectFiles
      PURITY: 100% pure
  [12] Src [from_mapping]: from_mapping
      PURITY: 100% pure
  [13] Src [main]: main
      PURITY: 100% pure
  [14] Src [init]: init → create_sample_manifest
      PURITY: 100% pure
  [15] Src [scan]: scan → scan_all_artifacts → discover_artifact_paths → infer_artifact_kind
      PURITY: 100% pure
  [16] Src [validate]: validate → validate_project → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [17] Src [check]: check → load_config
      PURITY: 100% pure
  [18] Src [coverage]: coverage → calculate_coverage → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [19] Src [duplicates]: duplicates → find_duplicate_contracts → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [20] Src [graph]: graph → build_graph → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [21] Src [tickets]: tickets → validate_project → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [22] Src [planfile_push]: planfile_push → validate_project → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [23] Src [planfile_pull]: planfile_pull
      PURITY: 100% pure
  [24] Src [planfile_sync]: planfile_sync → validate_project → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [25] Src [planfile_webhook_test]: planfile_webhook_test
      PURITY: 100% pure
  [26] Src [planfile_webhook_apply]: planfile_webhook_apply
      PURITY: 100% pure
  [27] Src [watch]: watch → validate_project → load_project_sources → infer_artifact_kind
      PURITY: 100% pure
  [28] Src [engine_suggest]: engine_suggest → scan_suggest_and_validate → collect_source_units → infer_language
      PURITY: 100% pure
  [29] Src [engine_drift]: engine_drift → scan_suggest_and_validate → collect_source_units → infer_language
      PURITY: 100% pure
  [30] Src [engine_run]: engine_run → scan_suggest_and_validate → collect_source_units → infer_language
      PURITY: 100% pure
  [31] Src [check_manifest]: check_manifest → validate_manifest → _load_schema
      PURITY: 100% pure
  [32] Src [artifact_validate]: artifact_validate → validate_artifact → validate_dockerfile
      PURITY: 100% pure
  [33] Src [to_dict]: to_dict
      PURITY: 100% pure
  [34] Src [to_dict]: to_dict
      PURITY: 100% pure
  [35] Src [to_dict]: to_dict
      PURITY: 100% pure
  [36] Src [to_dict]: to_dict
      PURITY: 100% pure
  [37] Src [to_mermaid]: to_mermaid → _safe
      PURITY: 100% pure
  [38] Src [to_inline]: to_inline
      PURITY: 100% pure
  [39] Src [contract]: contract
      PURITY: 100% pure
  [40] Src [to_dict]: to_dict
      PURITY: 100% pure
  [41] Src [to_dict]: to_dict
      PURITY: 100% pure
  [42] Src [to_dict]: to_dict
      PURITY: 100% pure
  [43] Src [to_dict]: to_dict
      PURITY: 100% pure
  [44] Src [validate]: validate → contains_token_like → normalize_label
      PURITY: 100% pure
  [45] Src [validate]: validate → contains_token_like → normalize_label
      PURITY: 100% pure
  [46] Src [validate]: validate → has_return_value
      PURITY: 100% pure
  [47] Src [validate]: validate → detect_effects
      PURITY: 100% pure
  [48] Src [__init__]: __init__
      PURITY: 100% pure
  [49] Src [register]: register
      PURITY: 100% pure
  [50] Src [rules]: rules
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=4.4    ←in:0  →out:0
  │ !! cli                        509L  0C   23m  CC=15     ←0
  │ !! check                      273L  1C   11m  CC=20     ←2
  │ planfile_adapter           255L  4C   13m  CC=13     ←0
  │ !! inline                     193L  0C    7m  CC=42     ←6
  │ artifacts                  181L  1C    6m  CC=9      ←3
  │ redup                      169L  3C   11m  CC=8      ←0
  │ watch                      160L  3C    6m  CC=10     ←2
  │ models                     153L  7C    2m  CC=2      ←0
  │ planfile                   141L  2C    7m  CC=11     ←3
  │ grouping                   138L  2C    6m  CC=6      ←3
  │ handlers                   124L  0C    9m  CC=4      ←0
  │ server                     118L  0C    5m  CC=5      ←0
  │ vallm                      116L  2C    5m  CC=12     ←1
  │ drift                      113L  2C    5m  CC=5      ←1
  │ manifest                   113L  0C    5m  CC=11     ←8
  │ builtins                   111L  6C   11m  CC=3      ←0
  │ base                       109L  6C   12m  CC=5      ←0
  │ assigner                   109L  0C    6m  CC=10     ←1
  │ !! project                     96L  0C    4m  CC=16     ←9
  │ !! manifest_schema             94L  2C    3m  CC=15     ←2
  │ !! artifact                    93L  2C    3m  CC=17     ←3
  │ schemas                     91L  0C    0m  CC=0.0    ←0
  │ registry                    85L  1C    8m  CC=7      ←1
  │ analyzer                    85L  0C    4m  CC=12     ←1
  │ !! signatures                  78L  0C    3m  CC=15     ←8
  │ input_output                74L  3C    8m  CC=7      ←0
  │ !! policy                      72L  1C    2m  CC=15     ←2
  │ scan_artifacts              70L  1C    3m  CC=7      ←2
  │ python_ast                  70L  0C    3m  CC=14     ←1
  │ normalizer                  69L  0C    4m  CC=7      ←4
  │ graph                       68L  1C    4m  CC=9      ←2
  │ typescript                  66L  0C    3m  CC=11     ←1
  │ csharp                      65L  0C    3m  CC=8      ←1
  │ config                      64L  1C    2m  CC=11     ←2
  │ openapi                     63L  0C    2m  CC=8      ←2
  │ sarif                       62L  0C    1m  CC=11     ←1
  │ treesitter                  62L  0C    4m  CC=7      ←2
  │ manager                     61L  0C    3m  CC=6      ←0
  │ matcher                     55L  1C    2m  CC=6      ←2
  │ engine                      54L  0C    1m  CC=8      ←4
  │ git                         53L  1C    5m  CC=4      ←1
  │ scanner                     53L  1C    1m  CC=9      ←1
  │ effects                     52L  1C    3m  CC=9      ←0
  │ base                        50L  3C    3m  CC=2      ←1
  │ sdk                         47L  1C    2m  CC=9      ←0
  │ blocks                      46L  0C    2m  CC=8      ←3
  │ scoring                     37L  0C    3m  CC=5      ←1
  │ context                     36L  3C    0m  CC=0.0    ←0
  │ __init__                    35L  0C    0m  CC=0.0    ←0
  │ coverage                    34L  1C    2m  CC=3      ←1
  │ monitor                     32L  0C    1m  CC=4      ←2
  │ __init__                    31L  0C    0m  CC=0.0    ←0
  │ java                        27L  0C    1m  CC=4      ←1
  │ __init__                    24L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ rust                        15L  0C    1m  CC=1      ←1
  │ __init__                    15L  0C    0m  CC=0.0    ←0
  │ requirements                13L  0C    1m  CC=6      ←1
  │ go                          13L  0C    1m  CC=1      ←1
  │ validation                  13L  0C    0m  CC=0.0    ←0
  │ __init__                    10L  0C    0m  CC=0.0    ←0
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
  examples/                       CC̄=1.8    ←in:0  →out:0
  │ v2-violation.validate.json   245L  0C    0m  CC=0.0    ←0
  │ v1-pass.validate.json      229L  0C    0m  CC=0.0    ←0
  │ run_examples               101L  0C    5m  CC=7      ←0
  │ v2-violation.artifacts.json    66L  0C    0m  CC=0.0    ←0
  │ v1-pass.artifacts.json      55L  0C    0m  CC=0.0    ←0
  │ intract.yaml                35L  0C    0m  CC=0.0    ←0
  │ intract.yaml                27L  0C    0m  CC=0.0    ←0
  │ v2-violation.graph.json     25L  0C    0m  CC=0.0    ←0
  │ v1-pass.graph.json          25L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 22L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                21L  0C    0m  CC=0.0    ←0
  │ openapi.yaml                21L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 20L  0C    0m  CC=0.0    ←0
  │ run-demo.sh                 20L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 19L  0C    0m  CC=0.0    ←0
  │ dashboard.ts                10L  0C    3m  CC=3      ←0
  │ scanner                      8L  0C    1m  CC=3      ←0
  │ app                          8L  0C    1m  CC=3      ←0
  │ dashboard.ts                 8L  0C    1m  CC=2      ←0
  │ ScanPipeline.cs              7L  0C    1m  CC=1      ←0
  │ Dockerfile                   7L  0C    0m  CC=0.0    ←0
  │ permission.ts                6L  0C    3m  CC=1      ←0
  │ auth                         6L  0C    1m  CC=1      ←0
  │ permission.ts                5L  0C    2m  CC=2      ←0
  │ auth                         5L  0C    1m  CC=2      ←0
  │ Dockerfile                   5L  0C    0m  CC=0.0    ←0
  │ scanner                      4L  0C    1m  CC=1      ←0
  │ reporter                     4L  0C    1m  CC=1      ←0
  │ routes                       4L  0C    1m  CC=1      ←0
  │ routes                       4L  0C    1m  CC=1      ←0
  │ analyzer                     3L  0C    1m  CC=1      ←0
  │ parser_b                     3L  0C    1m  CC=1      ←0
  │ parser_a                     3L  0C    1m  CC=3      ←0
  │
  extensions/                     CC̄=1.7    ←in:0  →out:0
  │ package.json                85L  0C    0m  CC=0.0    ←0
  │ extension.js                27L  0C    9m  CC=7      ←0
  │ intract.tmLanguage.json     19L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ ci-full-stack.sh            58L  0C    1m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ tree.txt                   257L  0C    0m  CC=0.0    ←0
  │ pyproject.toml             100L  0C    0m  CC=0.0    ←0
  │ action.yml                  91L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ pyqual.yaml                 30L  0C    0m  CC=0.0    ←0
  │ Makefile                    13L  0C    0m  CC=0.0    ←0
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
                              examples.integration_tests                 src.intract
  examples.integration_tests                          ──                           7
                 src.intract                          ←7                          ──  hub
  CYCLES: none
  HUB: src.intract/ (fan-in=7)

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 4 groups | 84f 5429L | 2026-05-31

SUMMARY:
  files_scanned: 84
  total_lines:   5429
  dup_groups:    4
  dup_fragments: 8
  saved_lines:   33
  scan_ms:       2335

HOTSPOTS[6] (files with most duplication):
  src/intract/analyzers/csharp.py  dup=25L  groups=2  frags=2  (0.5%)
  src/intract/analyzers/blocks.py  dup=19L  groups=1  frags=1  (0.3%)
  src/intract/mcp/handlers.py  dup=10L  groups=1  frags=2  (0.2%)
  src/intract/analyzers/typescript.py  dup=6L  groups=1  frags=1  (0.1%)
  examples/web-app/iterations/v1-pass/backend/routes.py  dup=3L  groups=1  frags=1  (0.1%)
  examples/web-app/iterations/v2-violation/backend/routes.py  dup=3L  groups=1  frags=1  (0.1%)

DUPLICATES[4] (ranked by impact):
  [ef612f5468430a71]   STRU  scan_braced_block  L=19 N=2 saved=19 sim=1.00
      src/intract/analyzers/blocks.py:6-24  (scan_braced_block)
      src/intract/analyzers/csharp.py:39-57  (_scan_braced_block)
  [ac0065a129c81ecd]   STRU  _treesitter_csharp_extent  L=6 N=2 saved=6 sim=1.00
      src/intract/analyzers/csharp.py:60-65  (_treesitter_csharp_extent)
      src/intract/analyzers/typescript.py:61-66  (_treesitter_typescript_extent)
  [a1077c782ef473a0]   STRU  handle_validate_project  L=5 N=2 saved=5 sim=1.00
      src/intract/mcp/handlers.py:36-40  (handle_validate_project)
      src/intract/mcp/handlers.py:90-94  (handle_build_graph)
  [1c8e027e2ce0b262]   EXAC  read_profile  L=3 N=2 saved=3 sim=1.00
      examples/web-app/iterations/v1-pass/backend/routes.py:2-4  (read_profile)
      examples/web-app/iterations/v2-violation/backend/routes.py:2-4  (read_profile)

REFACTOR[4] (ranked by priority):
  [1] ○ extract_function   → src/intract/analyzers/utils/scan_braced_block.py
      WHY: 2 occurrences of 19-line block across 2 files — saves 19 lines
      FILES: src/intract/analyzers/blocks.py, src/intract/analyzers/csharp.py
  [2] ○ extract_function   → src/intract/analyzers/utils/_treesitter_csharp_extent.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: src/intract/analyzers/csharp.py, src/intract/analyzers/typescript.py
  [3] ○ extract_function   → src/intract/mcp/utils/handle_validate_project.py
      WHY: 2 occurrences of 5-line block across 1 files — saves 5 lines
      FILES: src/intract/mcp/handlers.py
  [4] ○ extract_function   → examples/web-app/iterations/utils/read_profile.py
      WHY: 2 occurrences of 3-line block across 2 files — saves 3 lines
      FILES: examples/web-app/iterations/v1-pass/backend/routes.py, examples/web-app/iterations/v2-violation/backend/routes.py

QUICK_WINS[2] (low risk, high savings — do first):
  [1] extract_function   saved=19L  → src/intract/analyzers/utils/scan_braced_block.py
      FILES: blocks.py, csharp.py
  [2] extract_function   saved=6L  → src/intract/analyzers/utils/_treesitter_csharp_extent.py
      FILES: csharp.py, typescript.py

EFFORT_ESTIMATE (total ≈ 1.1h):
  medium scan_braced_block                   saved=19L  ~38min
  easy   _treesitter_csharp_extent           saved=6L  ~12min
  easy   handle_validate_project             saved=5L  ~10min
  easy   read_profile                        saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  4 → 0
  saved_lines: 33 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 269 func | 59f | 2026-05-31
# generated in 0.00s

NEXT[10] (ranked by impact):
  [1] !! SPLIT           src/intract/cli.py
      WHY: 509L, 0 classes, max CC=15
      EFFORT: ~4h  IMPACT: 7635

  [2] !! SPLIT-FUNC      parse_contract_line  CC=42  fan=28
      WHY: CC=42 exceeds 15
      EFFORT: ~1h  IMPACT: 1176

  [3] !  SPLIT-FUNC      scan  CC=15  fan=24
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 360

  [4] !  SPLIT-FUNC      block_extent  CC=20  fan=14
      WHY: CC=20 exceeds 15
      EFFORT: ~1h  IMPACT: 280

  [5] !  SPLIT-FUNC      validate_manifest  CC=15  fan=17
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 255

  [6] !  SPLIT-FUNC      build_signature  CC=15  fan=14
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 210

  [7] !  SPLIT-FUNC      decide_policy  CC=15  fan=12
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 180

  [8] !  SPLIT-FUNC      validate_sources  CC=16  fan=11
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 176

  [9] !  SPLIT-FUNC      infer_artifact_kind  CC=17  fan=6
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 102

  [10] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting goal.yaml may break 0 import paths
  ⚠ Splitting src/intract/cli.py may break 23 import paths

METRICS-TARGET:
  CC̄:          4.3 → ≤3.0
  max-CC:      42 → ≤20
  god-modules: 2 → 0
  high-CC(≥15): 8 → ≤4
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
  prev CC̄=4.3 → now CC̄=4.3
```

## Intent

Intent contract tagging, validation and semantic mapping for codebases.
