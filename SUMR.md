# Intract

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `intract`
- **version**: `0.5.1`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, Dockerfile, project/(5 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: intract;
  version: 0.5.1;
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

*136 nodes · 153 edges · 39 modules · CC̄=4.1*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `contract_from_mapping` *(in src.intract.parsers.manifest)* | 3 | 4 | 59 | **63** |
| `parse_contract_line` *(in src.intract.parsers.inline)* | 42 ⚠ | 1 | 51 | **52** |
| `build_signature` *(in src.intract.core.signatures)* | 15 ⚠ | 3 | 40 | **43** |
| `validate_manifest` *(in src.intract.manifest_schema)* | 15 ⚠ | 1 | 35 | **36** |
| `check` *(in src.intract.cli)* | 10 ⚠ | 0 | 29 | **29** |
| `normalize_label` *(in src.intract.core.normalizer)* | 7 | 11 | 16 | **27** |
| `load_manifest_records` *(in src.intract.parsers.manifest)* | 11 ⚠ | 6 | 19 | **25** |
| `tickets_from_report` *(in src.intract.integrations.planfile)* | 11 ⚠ | 2 | 21 | **23** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/intract
# generated in 0.13s
# nodes: 136 | edges: 153 | modules: 39
# CC̄=4.1

HUBS[20]:
  src.intract.parsers.manifest.contract_from_mapping
    CC=3  in:4  out:59  total:63
  src.intract.parsers.inline.parse_contract_line
    CC=42  in:1  out:51  total:52
  src.intract.core.signatures.build_signature
    CC=15  in:3  out:40  total:43
  src.intract.manifest_schema.validate_manifest
    CC=15  in:1  out:35  total:36
  src.intract.cli.check
    CC=10  in:0  out:29  total:29
  src.intract.core.normalizer.normalize_label
    CC=7  in:11  out:16  total:27
  src.intract.parsers.manifest.load_manifest_records
    CC=11  in:6  out:19  total:25
  src.intract.integrations.planfile.tickets_from_report
    CC=11  in:2  out:21  total:23
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
  src.intract.graph.build_graph
    CC=9  in:1  out:18  total:19
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:2  out:17  total:19
  examples.integration_tests.run_examples.run_example_03
    CC=2  in:1  out:17  total:18
  src.intract.engine.analyzer.analyze_source_units
    CC=12  in:1  out:17  total:18
  src.intract.cli.engine_suggest
    CC=3  in:0  out:18  total:18
  src.intract.parsers.openapi.parse_openapi_contracts
    CC=8  in:1  out:16  total:17
  src.intract.project.validate_sources
    CC=16  in:2  out:15  total:17
  src.intract.project.validate_project
    CC=4  in:9  out:8  total:17
  src.intract.duplicates.grouping.pairs_to_intent_groups
    CC=6  in:1  out:16  total:17
  src.intract.validators.artifacts.validate_openapi
    CC=9  in:1  out:16  total:17

MODULES:
  examples.integration_tests.run_examples  [5 funcs]
    main  CC=7  out:8
    print_result  CC=1  out:3
    run_example_01  CC=1  out:4
    run_example_02  CC=2  out:10
    run_example_03  CC=2  out:17
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
  src.intract.check  [5 funcs]
    changed_check  CC=1  out:3
    load_selected_sources  CC=5  out:4
    parse_unified_diff_hunks  CC=6  out:16
    staged_check  CC=1  out:5
    validate_selected_paths  CC=4  out:7
  src.intract.cli  [14 funcs]
    _export_tickets  CC=1  out:6
    _print_validation_report  CC=4  out:15
    artifact_validate  CC=4  out:11
    check  CC=10  out:29
    check_manifest  CC=4  out:12
    coverage  CC=2  out:12
    duplicates  CC=4  out:17
    engine_drift  CC=4  out:21
    engine_run  CC=4  out:20
    engine_suggest  CC=3  out:18
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
  src.intract.integrations.vallm  [3 funcs]
    map_project_report  CC=7  out:3
    map_validation_result  CC=6  out:4
    validate_for_vallm  CC=2  out:3
  src.intract.manifest_schema  [2 funcs]
    _load_schema  CC=2  out:5
    validate_manifest  CC=15  out:35
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
  src.intract.project  [4 funcs]
    extract_signatures_from_sources  CC=2  out:4
    load_project_sources  CC=7  out:6
    validate_project  CC=4  out:8
    validate_sources  CC=16  out:15
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
    validate_contract_against_source  CC=9  out:13
  src.intract.validators.input_output  [5 funcs]
    validate  CC=5  out:7
    validate  CC=5  out:7
    validate  CC=3  out:2
    contains_token_like  CC=7  out:5
    has_return_value  CC=3  out:4
  src.intract.validators.requirements  [1 funcs]
    validate_required_contracts  CC=6  out:2
  src.intract.watch  [5 funcs]
    diff_snapshots  CC=5  out:11
    hash_file  CC=2  out:6
    should_scan  CC=10  out:8
    snapshot_tree  CC=4  out:9
    watch_tree  CC=7  out:10

EDGES:
  src.intract.watch.snapshot_tree → src.intract.watch.should_scan
  src.intract.watch.snapshot_tree → src.intract.watch.hash_file
  src.intract.watch.watch_tree → src.intract.watch.snapshot_tree
  src.intract.watch.watch_tree → src.intract.watch.diff_snapshots
  src.intract.graph.ContractGraph.to_mermaid → src.intract.graph._safe
  src.intract.graph.build_graph → src.intract.project.load_project_sources
  src.intract.graph.build_graph → src.intract.project.extract_signatures_from_sources
  src.intract.git.staged_files → src.intract.git._run_git
  src.intract.git.changed_files → src.intract.git._run_git
  src.intract.git.staged_hunks → src.intract.git._run_git
  src.intract.coverage.calculate_coverage → src.intract.project.load_project_sources
  src.intract.coverage.calculate_coverage → src.intract.project.extract_signatures_from_sources
  src.intract.duplicates.scoring.object_similarity → src.intract.duplicates.scoring.jaccard
  src.intract.duplicates.scoring.score_similarity → src.intract.duplicates.scoring.object_similarity
  src.intract.duplicates.scoring.score_similarity → src.intract.duplicates.scoring.jaccard
  src.intract.validators.engine.validate_contract_against_source → src.intract.validators.base.merge_rule_results
  src.intract.validators.input_output.contains_token_like → src.intract.core.normalizer.normalize_label
  src.intract.validators.input_output.InputPresenceRule.validate → src.intract.validators.input_output.contains_token_like
  src.intract.validators.input_output.OutputPresenceRule.validate → src.intract.validators.input_output.contains_token_like
  src.intract.validators.input_output.ReturnValueRule.validate → src.intract.validators.input_output.has_return_value
  src.intract.duplicates.grouping.pairs_to_intent_groups → src.intract.duplicates.grouping.union_find_groups
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.project.load_project_sources
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.project.extract_signatures_from_sources
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.duplicates.matcher.find_intent_pairs
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.duplicates.grouping.pairs_to_duplicate_contracts
  src.intract.validators.effects.NoForbiddenEffectRule.validate → src.intract.validators.effects.detect_effects
  src.intract.core.normalizer.normalize_action → src.intract.core.normalizer.normalize_label
  src.intract.core.normalizer.normalize_many → src.intract.core.normalizer.normalize_label
  src.intract.core.normalizer.normalize_requirement → src.intract.core.normalizer.normalize_action
  src.intract.core.normalizer.normalize_requirement → src.intract.core.normalizer.normalize_label
  src.intract.duplicates.matcher.find_intent_pairs → src.intract.duplicates.matcher.bucket_signatures
  src.intract.duplicates.matcher.find_intent_pairs → src.intract.duplicates.scoring.score_similarity
  src.intract.core.signatures.build_signature → src.intract.core.normalizer.normalize_action
  src.intract.core.signatures.build_signature → src.intract.core.normalizer.normalize_label
  src.intract.core.signatures.build_signatures → src.intract.core.signatures.build_signature
  src.intract.plugins.builtins.InlineContractParserPlugin.parse → src.intract.parsers.inline.extract_contract_records_from_text
  src.intract.plugins.builtins.InlineContractParserPlugin.parse → src.intract.core.signatures.build_signatures
  src.intract.plugins.builtins.OpenAPIParserPlugin.parse → src.intract.parsers.openapi.parse_openapi_text
  src.intract.plugins.builtins.OpenAPIParserPlugin.parse → src.intract.core.signatures.build_signatures
  src.intract.plugins.builtins.ManifestParserPlugin.parse → src.intract.parsers.manifest.load_manifest_records
  src.intract.plugins.builtins.ManifestParserPlugin.parse → src.intract.core.signatures.build_signatures
  src.intract.plugins.builtins.BasicContractValidatorPlugin.validate → src.intract.validators.engine.validate_contract_against_source
  src.intract.plugins.builtins.ArtifactStructureValidatorPlugin.validate → src.intract.validators.artifacts.validate_artifact
  src.intract.plugins.manager.load_builtin_plugins → src.intract.plugins.manager._register_unique
  src.intract.plugins.manager.discover_plugins → src.intract.plugins.manager.load_builtin_plugins
  src.intract.plugins.manager.discover_plugins → src.intract.plugins.manager._register_unique
  src.intract.engine.analyzer.analyze_source_units → src.intract.engine.analyzer._slice_until_next_match
  src.intract.engine.analyzer.analyze_source_units → src.intract.engine.analyzer._line_number
  src.intract.check.validate_selected_paths → src.intract.check.load_selected_sources
  src.intract.check.validate_selected_paths → src.intract.project.validate_sources
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
# generated in 0.13s
# nodes: 136 | edges: 153 | modules: 39
# CC̄=4.1

HUBS[20]:
  src.intract.parsers.manifest.contract_from_mapping
    CC=3  in:4  out:59  total:63
  src.intract.parsers.inline.parse_contract_line
    CC=42  in:1  out:51  total:52
  src.intract.core.signatures.build_signature
    CC=15  in:3  out:40  total:43
  src.intract.manifest_schema.validate_manifest
    CC=15  in:1  out:35  total:36
  src.intract.cli.check
    CC=10  in:0  out:29  total:29
  src.intract.core.normalizer.normalize_label
    CC=7  in:11  out:16  total:27
  src.intract.parsers.manifest.load_manifest_records
    CC=11  in:6  out:19  total:25
  src.intract.integrations.planfile.tickets_from_report
    CC=11  in:2  out:21  total:23
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
  src.intract.graph.build_graph
    CC=9  in:1  out:18  total:19
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:2  out:17  total:19
  examples.integration_tests.run_examples.run_example_03
    CC=2  in:1  out:17  total:18
  src.intract.engine.analyzer.analyze_source_units
    CC=12  in:1  out:17  total:18
  src.intract.cli.engine_suggest
    CC=3  in:0  out:18  total:18
  src.intract.parsers.openapi.parse_openapi_contracts
    CC=8  in:1  out:16  total:17
  src.intract.project.validate_sources
    CC=16  in:2  out:15  total:17
  src.intract.project.validate_project
    CC=4  in:9  out:8  total:17
  src.intract.duplicates.grouping.pairs_to_intent_groups
    CC=6  in:1  out:16  total:17
  src.intract.validators.artifacts.validate_openapi
    CC=9  in:1  out:16  total:17

MODULES:
  examples.integration_tests.run_examples  [5 funcs]
    main  CC=7  out:8
    print_result  CC=1  out:3
    run_example_01  CC=1  out:4
    run_example_02  CC=2  out:10
    run_example_03  CC=2  out:17
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
  src.intract.check  [5 funcs]
    changed_check  CC=1  out:3
    load_selected_sources  CC=5  out:4
    parse_unified_diff_hunks  CC=6  out:16
    staged_check  CC=1  out:5
    validate_selected_paths  CC=4  out:7
  src.intract.cli  [14 funcs]
    _export_tickets  CC=1  out:6
    _print_validation_report  CC=4  out:15
    artifact_validate  CC=4  out:11
    check  CC=10  out:29
    check_manifest  CC=4  out:12
    coverage  CC=2  out:12
    duplicates  CC=4  out:17
    engine_drift  CC=4  out:21
    engine_run  CC=4  out:20
    engine_suggest  CC=3  out:18
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
  src.intract.integrations.vallm  [3 funcs]
    map_project_report  CC=7  out:3
    map_validation_result  CC=6  out:4
    validate_for_vallm  CC=2  out:3
  src.intract.manifest_schema  [2 funcs]
    _load_schema  CC=2  out:5
    validate_manifest  CC=15  out:35
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
  src.intract.project  [4 funcs]
    extract_signatures_from_sources  CC=2  out:4
    load_project_sources  CC=7  out:6
    validate_project  CC=4  out:8
    validate_sources  CC=16  out:15
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
    validate_contract_against_source  CC=9  out:13
  src.intract.validators.input_output  [5 funcs]
    validate  CC=5  out:7
    validate  CC=5  out:7
    validate  CC=3  out:2
    contains_token_like  CC=7  out:5
    has_return_value  CC=3  out:4
  src.intract.validators.requirements  [1 funcs]
    validate_required_contracts  CC=6  out:2
  src.intract.watch  [5 funcs]
    diff_snapshots  CC=5  out:11
    hash_file  CC=2  out:6
    should_scan  CC=10  out:8
    snapshot_tree  CC=4  out:9
    watch_tree  CC=7  out:10

EDGES:
  src.intract.watch.snapshot_tree → src.intract.watch.should_scan
  src.intract.watch.snapshot_tree → src.intract.watch.hash_file
  src.intract.watch.watch_tree → src.intract.watch.snapshot_tree
  src.intract.watch.watch_tree → src.intract.watch.diff_snapshots
  src.intract.graph.ContractGraph.to_mermaid → src.intract.graph._safe
  src.intract.graph.build_graph → src.intract.project.load_project_sources
  src.intract.graph.build_graph → src.intract.project.extract_signatures_from_sources
  src.intract.git.staged_files → src.intract.git._run_git
  src.intract.git.changed_files → src.intract.git._run_git
  src.intract.git.staged_hunks → src.intract.git._run_git
  src.intract.coverage.calculate_coverage → src.intract.project.load_project_sources
  src.intract.coverage.calculate_coverage → src.intract.project.extract_signatures_from_sources
  src.intract.duplicates.scoring.object_similarity → src.intract.duplicates.scoring.jaccard
  src.intract.duplicates.scoring.score_similarity → src.intract.duplicates.scoring.object_similarity
  src.intract.duplicates.scoring.score_similarity → src.intract.duplicates.scoring.jaccard
  src.intract.validators.engine.validate_contract_against_source → src.intract.validators.base.merge_rule_results
  src.intract.validators.input_output.contains_token_like → src.intract.core.normalizer.normalize_label
  src.intract.validators.input_output.InputPresenceRule.validate → src.intract.validators.input_output.contains_token_like
  src.intract.validators.input_output.OutputPresenceRule.validate → src.intract.validators.input_output.contains_token_like
  src.intract.validators.input_output.ReturnValueRule.validate → src.intract.validators.input_output.has_return_value
  src.intract.duplicates.grouping.pairs_to_intent_groups → src.intract.duplicates.grouping.union_find_groups
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.project.load_project_sources
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.project.extract_signatures_from_sources
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.duplicates.matcher.find_intent_pairs
  src.intract.duplicates.grouping.find_duplicate_contracts → src.intract.duplicates.grouping.pairs_to_duplicate_contracts
  src.intract.validators.effects.NoForbiddenEffectRule.validate → src.intract.validators.effects.detect_effects
  src.intract.core.normalizer.normalize_action → src.intract.core.normalizer.normalize_label
  src.intract.core.normalizer.normalize_many → src.intract.core.normalizer.normalize_label
  src.intract.core.normalizer.normalize_requirement → src.intract.core.normalizer.normalize_action
  src.intract.core.normalizer.normalize_requirement → src.intract.core.normalizer.normalize_label
  src.intract.duplicates.matcher.find_intent_pairs → src.intract.duplicates.matcher.bucket_signatures
  src.intract.duplicates.matcher.find_intent_pairs → src.intract.duplicates.scoring.score_similarity
  src.intract.core.signatures.build_signature → src.intract.core.normalizer.normalize_action
  src.intract.core.signatures.build_signature → src.intract.core.normalizer.normalize_label
  src.intract.core.signatures.build_signatures → src.intract.core.signatures.build_signature
  src.intract.plugins.builtins.InlineContractParserPlugin.parse → src.intract.parsers.inline.extract_contract_records_from_text
  src.intract.plugins.builtins.InlineContractParserPlugin.parse → src.intract.core.signatures.build_signatures
  src.intract.plugins.builtins.OpenAPIParserPlugin.parse → src.intract.parsers.openapi.parse_openapi_text
  src.intract.plugins.builtins.OpenAPIParserPlugin.parse → src.intract.core.signatures.build_signatures
  src.intract.plugins.builtins.ManifestParserPlugin.parse → src.intract.parsers.manifest.load_manifest_records
  src.intract.plugins.builtins.ManifestParserPlugin.parse → src.intract.core.signatures.build_signatures
  src.intract.plugins.builtins.BasicContractValidatorPlugin.validate → src.intract.validators.engine.validate_contract_against_source
  src.intract.plugins.builtins.ArtifactStructureValidatorPlugin.validate → src.intract.validators.artifacts.validate_artifact
  src.intract.plugins.manager.load_builtin_plugins → src.intract.plugins.manager._register_unique
  src.intract.plugins.manager.discover_plugins → src.intract.plugins.manager.load_builtin_plugins
  src.intract.plugins.manager.discover_plugins → src.intract.plugins.manager._register_unique
  src.intract.engine.analyzer.analyze_source_units → src.intract.engine.analyzer._slice_until_next_match
  src.intract.engine.analyzer.analyze_source_units → src.intract.engine.analyzer._line_number
  src.intract.check.validate_selected_paths → src.intract.check.load_selected_sources
  src.intract.check.validate_selected_paths → src.intract.project.validate_sources
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 96f 5520L | python:65,yaml:8,typescript:5,toml:4,json:3,csharp:2,go:2,shell:1,txt:1,intract:1,java:1,rust:1 | 2026-05-30
# generated in 0.06s
# CC̅=4.1 | critical:5/208 | dups:0 | cycles:0

HEALTH[5]:
  🟡 CC    build_signature CC=15 (limit:15)
  🟡 CC    parse_contract_line CC=42 (limit:15)
  🟡 CC    infer_artifact_kind CC=17 (limit:15)
  🟡 CC    validate_manifest CC=15 (limit:15)
  🟡 CC    validate_sources CC=16 (limit:15)

REFACTOR[1]:
  1. split 5 high-CC methods  (CC>15)

PIPELINES[71]:
  [1] Src [CollectFiles]: CollectFiles
      PURITY: 100% pure
  [2] Src [canUpdateResource]: canUpdateResource
      PURITY: 100% pure
  [3] Src [response]: response
      PURITY: 100% pure
  [4] Src [to_dict]: to_dict
      PURITY: 100% pure
  [5] Src [to_mermaid]: to_mermaid → _safe
      PURITY: 100% pure
  [6] Src [collect_project_files]: collect_project_files
      PURITY: 100% pure
  [7] Src [to_dict]: to_dict
      PURITY: 100% pure
  [8] Src [to_inline]: to_inline
      PURITY: 100% pure
  [9] Src [contract]: contract
      PURITY: 100% pure
  [10] Src [parse_extensions]: parse_extensions
      PURITY: 100% pure
  [11] Src [validate]: validate → contains_token_like → normalize_label
      PURITY: 100% pure
  [12] Src [validate]: validate → contains_token_like → normalize_label
      PURITY: 100% pure
  [13] Src [validate]: validate → has_return_value
      PURITY: 100% pure
  [14] Src [to_dict]: to_dict
      PURITY: 100% pure
  [15] Src [to_dict]: to_dict
      PURITY: 100% pure
  [16] Src [validate]: validate → detect_effects
      PURITY: 100% pure
  [17] Src [parse]: parse → extract_contract_records_from_text → parse_contract_line → marker_payload → ...(1 more)
      PURITY: 100% pure
  [18] Src [parse]: parse → parse_openapi_text → contract_from_mapping → _parse_intent
      PURITY: 100% pure
  [19] Src [parse]: parse → load_manifest_records → contract_from_mapping → _parse_intent
      PURITY: 100% pure
  [20] Src [validate]: validate → validate_contract_against_source → merge_rule_results
      PURITY: 100% pure
  [21] Src [validate]: validate → validate_artifact → validate_dockerfile
      PURITY: 100% pure
  [22] Src [render]: render
      PURITY: 100% pure
  [23] Src [discover_plugins]: discover_plugins → load_builtin_plugins → _register_unique
      PURITY: 100% pure
  [24] Src [parse_extensions]: parse_extensions
      PURITY: 100% pure
  [25] Src [to_dict]: to_dict
      PURITY: 100% pure
  [26] Src [render_summary]: render_summary
      PURITY: 100% pure
  [27] Src [validate_for_vallm]: validate_for_vallm → validate_project → load_project_sources
      PURITY: 100% pure
  [28] Src [inline]: inline → join
      PURITY: 100% pure
  [29] Src [Inline]: Inline → csv
      PURITY: 100% pure
  [30] Src [main]: main
      PURITY: 100% pure
  [31] Src [inlineContract]: inlineContract → csv
      PURITY: 100% pure
  [32] Src [inline_contract]: inline_contract → csv
      PURITY: 100% pure
  [33] Src [parse]: parse
      PURITY: 100% pure
  [34] Src [validate]: validate
      PURITY: 100% pure
  [35] Src [Inline]: Inline
      PURITY: 100% pure
  [36] Src [to_dict]: to_dict
      PURITY: 100% pure
  [37] Src [to_dict]: to_dict
      PURITY: 100% pure
  [38] Src [from_path]: from_path → infer_language
      PURITY: 100% pure
  [39] Src [to_dict]: to_dict
      PURITY: 100% pure
  [40] Src [__init__]: __init__
      PURITY: 100% pure
  [41] Src [export]: export
      PURITY: 100% pure
  [42] Src [_write_yaml]: _write_yaml
      PURITY: 100% pure
  [43] Src [_write_json]: _write_json
      PURITY: 100% pure
  [44] Src [_write_todo]: _write_todo
      PURITY: 100% pure
  [45] Src [main]: main
      PURITY: 100% pure
  [46] Src [init]: init → create_sample_manifest
      PURITY: 100% pure
  [47] Src [scan]: scan → extract_contract_records_from_text → parse_contract_line → marker_payload → ...(1 more)
      PURITY: 100% pure
  [48] Src [validate]: validate → validate_project → load_project_sources
      PURITY: 100% pure
  [49] Src [check]: check → load_config
      PURITY: 100% pure
  [50] Src [coverage]: coverage → calculate_coverage → load_project_sources
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
  src/                            CC̄=4.3    ←in:0  →out:0
  │ cli                        385L  0C   18m  CC=10     ←0
  │ !! inline                     193L  0C    7m  CC=42     ←4
  │ artifacts                  181L  1C    6m  CC=9      ←2
  │ redup                      169L  3C   11m  CC=8      ←0
  │ watch                      160L  3C    6m  CC=10     ←2
  │ models                     153L  7C    2m  CC=2      ←0
  │ planfile                   141L  2C    7m  CC=11     ←2
  │ grouping                   138L  2C    6m  CC=6      ←2
  │ drift                      113L  2C    5m  CC=5      ←1
  │ manifest                   113L  0C    5m  CC=11     ←7
  │ builtins                   111L  6C   11m  CC=3      ←0
  │ assigner                   109L  0C    6m  CC=10     ←1
  │ base                       109L  6C   12m  CC=5      ←0
  │ check                      105L  1C    6m  CC=6      ←1
  │ !! manifest_schema             94L  2C    3m  CC=15     ←1
  │ !! artifact                    93L  2C    3m  CC=17     ←1
  │ !! project                     88L  0C    4m  CC=16     ←8
  │ analyzer                    85L  0C    4m  CC=12     ←1
  │ vallm                       84L  2C    4m  CC=7      ←0
  │ !! signatures                  78L  0C    3m  CC=15     ←5
  │ input_output                74L  3C    8m  CC=7      ←0
  │ normalizer                  69L  0C    4m  CC=7      ←3
  │ graph                       68L  1C    4m  CC=9      ←1
  │ config                      64L  1C    2m  CC=11     ←1
  │ openapi                     63L  0C    2m  CC=8      ←2
  │ sarif                       62L  0C    1m  CC=11     ←1
  │ manager                     61L  0C    3m  CC=6      ←0
  │ matcher                     55L  1C    2m  CC=6      ←2
  │ git                         53L  1C    5m  CC=4      ←1
  │ scanner                     53L  1C    1m  CC=9      ←1
  │ effects                     52L  1C    3m  CC=9      ←0
  │ engine                      51L  0C    1m  CC=9      ←2
  │ base                        50L  3C    3m  CC=2      ←1
  │ sdk                         47L  1C    2m  CC=9      ←0
  │ scoring                     37L  0C    3m  CC=5      ←1
  │ policy                      36L  1C    1m  CC=7      ←1
  │ context                     36L  3C    0m  CC=0.0    ←0
  │ __init__                    35L  0C    0m  CC=0.0    ←0
  │ coverage                    34L  1C    2m  CC=3      ←1
  │ monitor                     32L  0C    1m  CC=4      ←2
  │ __init__                    31L  0C    0m  CC=0.0    ←0
  │ __init__                    24L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    21L  0C    0m  CC=0.0    ←0
  │ __init__                    15L  0C    0m  CC=0.0    ←0
  │ __init__                    14L  0C    0m  CC=0.0    ←0
  │ requirements                13L  0C    1m  CC=6      ←1
  │ validation                  13L  0C    0m  CC=0.0    ←0
  │ __init__                    10L  0C    0m  CC=0.0    ←0
  │ registry                     6L  0C    0m  CC=0.0    ←0
  │ effects                      5L  0C    0m  CC=0.0    ←0
  │ artifacts                    5L  0C    0m  CC=0.0    ←0
  │ __main__                     4L  0C    0m  CC=0.0    ←0
  │ signature                    3L  0C    0m  CC=0.0    ←0
  │ parser                       3L  0C    0m  CC=0.0    ←0
  │ yaml_manifest                3L  0C    0m  CC=0.0    ←0
  │ models                       3L  0C    0m  CC=0.0    ←0
  │ normalizer                   3L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  examples/                       CC̄=2.0    ←in:0  →out:0
  │ run_examples               101L  0C    5m  CC=7      ←0
  │ intent.yaml                 22L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 20L  0C    0m  CC=0.0    ←0
  │ intent.yaml                 19L  0C    0m  CC=0.0    ←0
  │ scanner                      8L  0C    1m  CC=3      ←0
  │ parse_extensions             8L  0C    1m  CC=3      ←0
  │ app                          8L  0C    1m  CC=3      ←0
  │ ScanPipeline.cs              7L  0C    1m  CC=1      ←0
  │ permission.ts                6L  0C    3m  CC=1      ←0
  │ permission.ts                5L  0C    2m  CC=2      ←0
  │ reporter                     4L  0C    1m  CC=1      ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  511L  0C    0m  CC=0.0    ←0
  │ tree.txt                   133L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              92L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ Makefile                    13L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   9L  0C    0m  CC=0.0    ←0
  │ .pre-commit-hooks.yaml       6L  0C    0m  CC=0.0    ←0
  │
  templates/                      CC̄=0.0    ←in:0  →out:0
  │ intract.yaml                36L  0C    0m  CC=0.0    ←0
  │ openapi.intract.yaml        21L  0C    0m  CC=0.0    ←0
  │ pyproject-intract.toml      16L  0C    0m  CC=0.0    ←0
  │ Dockerfile.intract          12L  0C    0m  CC=0.0    ←0
  │ .pre-commit-config.yaml      8L  0C    0m  CC=0.0    ←0
  │
  schemas/                        CC̄=0.0    ←in:0  →out:0
  │ intract.schema.json         99L  0C    0m  CC=0.0    ←0
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
# redup/duplication | 0 groups | 60f 3936L | 2026-05-30

SUMMARY:
  files_scanned: 60
  total_lines:   3936
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       2353
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 192 func | 45f | 2026-05-30
# generated in 0.00s

NEXT[6] (ranked by impact):
  [1] !! SPLIT-FUNC      parse_contract_line  CC=42  fan=28
      WHY: CC=42 exceeds 15
      EFFORT: ~1h  IMPACT: 1176

  [2] !  SPLIT-FUNC      validate_manifest  CC=15  fan=17
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 255

  [3] !  SPLIT-FUNC      build_signature  CC=15  fan=14
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 210

  [4] !  SPLIT-FUNC      validate_sources  CC=16  fan=11
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 176

  [5] !  SPLIT-FUNC      infer_artifact_kind  CC=17  fan=6
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 102

  [6] !! SPLIT           goal.yaml
      WHY: 511L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[1]:
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          4.3 → ≤3.0
  max-CC:      42 → ≤20
  god-modules: 1 → 0
  high-CC(≥15): 5 → ≤2
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
  (first run — no previous data)
```

## Intent

Intent contract tagging, validation and semantic mapping for codebases.
