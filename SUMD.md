# Intract

Intent contract tagging, validation and semantic mapping for codebases.

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
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
- **version**: `0.5.3`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, Dockerfile, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: intract;
  version: 0.5.3;
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

## Interfaces

### CLI Entry Points

- `intract`

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

## Configuration

```yaml
project:
  name: intract
  version: 0.5.3
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

- `install`
- `test`
- `lint`
- `format`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# intract | 95f 5431L | python:83,typescript:5,shell:3,go:2,less:1,rust:1 | 2026-05-30
# stats: 180 func | 60 cls | 95 mod | CC̄=4.8 | critical:19 | cycles:0
# alerts[5]: CC parse_contract_line=42; CC infer_artifact_kind=17; CC validate_sources=16; CC build_signature=15; CC validate_manifest=15
# hotspots[5]: check fan=21; scan fan=18; validate_manifest fan=17; watch fan=16; parse_contract_line fan=16
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[95]:
  app.doql.less,49
  examples/full-stack/src/analyzer.py,4
  examples/full-stack/src/parser_a.py,4
  examples/full-stack/src/parser_b.py,4
  examples/full-stack/src/scanner.py,5
  examples/integration_tests/01_python_pass/app.py,9
  examples/integration_tests/02_typescript_violation_planfile/permission.ts,7
  examples/integration_tests/03_watch_engine_drift/reporter.py,5
  examples/integration_tests/03_watch_engine_drift/scanner.py,9
  examples/integration_tests/run_examples.py,102
  examples/python/parse_extensions.py,9
  examples/typescript/permission.ts,6
  project.sh,50
  scripts/ci-full-stack.sh,59
  sdks/go/examples/main.go,23
  sdks/go/intractsdk/sdk.go,69
  sdks/python/src/intract_plugin_example/__init__.py,27
  sdks/rust/src/lib.rs,55
  sdks/typescript/examples/basic.ts,14
  sdks/typescript/intract.config.ts,9
  sdks/typescript/src/index.ts,43
  src/intract/__init__.py,32
  src/intract/__main__.py,5
  src/intract/artifacts.py,6
  src/intract/check.py,247
  src/intract/cli.py,398
  src/intract/config.py,65
  src/intract/core/__init__.py,36
  src/intract/core/artifact.py,94
  src/intract/core/models.py,154
  src/intract/core/normalizer.py,70
  src/intract/core/registry.py,7
  src/intract/core/signatures.py,79
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
  src/intract/integrations/__init__.py,16
  src/intract/integrations/planfile.py,142
  src/intract/integrations/redup.py,170
  src/intract/integrations/vallm.py,117
  src/intract/manifest_schema.py,95
  src/intract/models.py,4
  src/intract/normalizer.py,4
  src/intract/parser.py,4
  src/intract/parsers/__init__.py,11
  src/intract/parsers/inline.py,194
  src/intract/parsers/manifest.py,114
  src/intract/parsers/openapi.py,64
  src/intract/plugins/__init__.py,25
  src/intract/plugins/base.py,110
  src/intract/plugins/builtins.py,112
  src/intract/plugins/manager.py,62
  src/intract/policy.py,73
  src/intract/project.py,89
  src/intract/reporters/__init__.py,1
  src/intract/reporters/sarif.py,63
  src/intract/sdk.py,48
  src/intract/signature.py,4
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
  tests/test_check_staged.py,35
  tests/test_full_stack.py,28
  tests/test_hunk_filter.py,89
  tests/test_integrations.py,61
  tests/test_manifest.py,27
  tests/test_new_modules.py,49
  tests/test_next_stage.py,37
  tests/test_parser.py,30
  tests/test_policy.py,46
  tests/test_rule_registry.py,53
  tests/test_staged_e2e.py,65
  tests/test_validation.py,40
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
    e: print_result,run_example_01,run_example_02,run_example_03,main
    print_result(name;payload)
    run_example_01(base)
    run_example_02(base)
    run_example_03(base)
    main()
  examples/python/parse_extensions.py:
    e: parse_extensions
    parse_extensions(raw_extensions)
  sdks/python/src/intract_plugin_example/__init__.py:
    e: ExampleParserPlugin,ExampleValidatorPlugin
    ExampleParserPlugin: supports(1),parse(1)
    ExampleValidatorPlugin: supports(1),validate(2)
  src/intract/__init__.py:
  src/intract/__main__.py:
  src/intract/artifacts.py:
  src/intract/check.py:
    e: parse_unified_diff_hunks,load_selected_sources,_manifest_changed,changed_lines_by_file,block_extent,signature_touched,validate_sources_for_hunks,validate_selected_paths,staged_check,changed_check,ChangedHunk
    ChangedHunk: to_dict(0)
    parse_unified_diff_hunks(diff_text)
    load_selected_sources(root;files)
    _manifest_changed(files)
    changed_lines_by_file(hunks)
    block_extent(source;start_line)
    signature_touched(signature;changed_lines;source)
    validate_sources_for_hunks(root;files;hunks)
    validate_selected_paths(root;files)
    staged_check(root)
    changed_check(root)
  src/intract/cli.py:
    e: main,init,scan,validate,check,coverage,duplicates,graph,tickets,watch,engine_suggest,engine_drift,engine_run,_export_tickets,_print_validation_report,_format_check_text,check_manifest,artifact_validate
    main(version)
    init(path;force)
    scan(path;json_output)
    validate(path;manifest;json_output;planfile)
    check(path;staged;changed;base;hunks;manifest;fmt;output;planfile)
    coverage(path;json_output)
    duplicates(path;threshold;json_output)
    graph(path;manifest;fmt;output)
    tickets(path;manifest)
    watch(path;manifest;interval;planfile;once;json_output)
    engine_suggest(path;json_output)
    engine_drift(path;manifest;json_output)
    engine_run(path;manifest;planfile;json_output)
    _export_tickets(path;report)
    _print_validation_report(report)
    _format_check_text(report;decision;files)
    check_manifest(manifest;json_output)
    artifact_validate(path;json_output)
  src/intract/config.py:
    e: load_config,IntractConfig
    IntractConfig: from_mapping(2)
    load_config(root)
  src/intract/core/__init__.py:
  src/intract/core/artifact.py:
    e: infer_language,infer_artifact_kind,ArtifactKind,Artifact
    ArtifactKind:
    Artifact: from_path(2)
    infer_language(path)
    infer_artifact_kind(path;content)
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
    e: make_block_id,build_signature,build_signatures
    make_block_id(file_path;start_line;end_line;scope)
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
  src/intract/integrations/planfile.py:
    e: _severity_from_status,tickets_from_report,Ticket,PlanfileExporter
    Ticket:
    PlanfileExporter: __init__(1),export(1),_write_yaml(2),_write_json(2),_write_todo(2)
    _severity_from_status(status)
    tickets_from_report(report)
  src/intract/integrations/redup.py:
    e: block_text,block_file_path,block_start_line,block_end_line,signatures_from_text,signatures_from_blocks,signatures_from_manifest,_with_block_lines,find_intent_duplicate_groups,scan_blocks_for_intent_duplicates,CodeBlockLike,BlockAdapter,RedupScanResult
    CodeBlockLike:
    BlockAdapter:
    RedupScanResult: to_dict(0)
    block_text(block)
    block_file_path(block)
    block_start_line(block)
    block_end_line(block)
    signatures_from_text(text)
    signatures_from_blocks(blocks)
    signatures_from_manifest(manifest_path)
    _with_block_lines(signature;block)
    find_intent_duplicate_groups(blocks)
    scan_blocks_for_intent_duplicates(blocks)
  src/intract/integrations/vallm.py:
    e: map_validation_result,map_project_report,validate_for_vallm,validate_proposal,MappedIssue,MappedValidationResult
    MappedIssue:
    MappedValidationResult: to_dict(0)
    map_validation_result(result)
    map_project_report(report)
    validate_for_vallm(root)
    validate_proposal(code)
  src/intract/manifest_schema.py:
    e: _load_schema,validate_manifest,ManifestIssue,ManifestValidationReport
    ManifestIssue:
    ManifestValidationReport: to_dict(0)
    _load_schema()
    validate_manifest(path)
  src/intract/models.py:
  src/intract/normalizer.py:
  src/intract/parser.py:
  src/intract/parsers/__init__.py:
  src/intract/parsers/inline.py:
    e: clean_comment_line,split_csv,parse_priority,parse_key_value,marker_payload,parse_contract_line,extract_contract_records_from_text
    clean_comment_line(line)
    split_csv(value)
    parse_priority(token)
    parse_key_value(token)
    marker_payload(line)
    parse_contract_line(line)
    extract_contract_records_from_text(source)
  src/intract/parsers/manifest.py:
    e: _to_tuple,_parse_intent,contract_from_mapping,load_manifest_records,create_sample_manifest
    _to_tuple(value)
    _parse_intent(value)
    contract_from_mapping(data)
    load_manifest_records(path)
    create_sample_manifest()
  src/intract/parsers/openapi.py:
    e: parse_openapi_contracts,parse_openapi_text
    parse_openapi_contracts(path)
    parse_openapi_text(content)
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
    e: _p1_missing_reasons,decide_policy,PolicyDecision
    PolicyDecision:
    _p1_missing_reasons(graph;manifest_path)
    decide_policy(report)
  src/intract/project.py:
    e: load_project_sources,extract_signatures_from_sources,validate_sources,validate_project
    load_project_sources(root)
    extract_signatures_from_sources(sources)
    validate_sources(sources)
    validate_project(root)
  src/intract/reporters/__init__.py:
  src/intract/reporters/sarif.py:
    e: report_to_sarif
    report_to_sarif(report)
  src/intract/sdk.py:
    e: contract,ContractBuilder
    ContractBuilder: to_inline(1)
    contract()
  src/intract/signature.py:
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
  tests/test_check_staged.py:
    e: test_manifest_changed_helper,test_validate_selected_paths_full_graph
    test_manifest_changed_helper()
    test_validate_selected_paths_full_graph(tmp_path)
  tests/test_full_stack.py:
    e: test_full_stack_validate_passes,test_full_stack_graph_covers_requires,test_full_stack_finds_intent_duplicates
    test_full_stack_validate_passes()
    test_full_stack_graph_covers_requires()
    test_full_stack_finds_intent_duplicates()
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
  tests/test_manifest.py:
    e: test_load_manifest_records
    test_load_manifest_records(tmp_path)
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
    e: test_parse_full_contract_line,test_parse_comment_prefix_ts
    test_parse_full_contract_line()
    test_parse_comment_prefix_ts()
  tests/test_policy.py:
    e: test_missing_required_p1_fails_policy,test_full_stack_passes_without_p1_gate
    test_missing_required_p1_fails_policy(tmp_path)
    test_full_stack_passes_without_p1_gate()
  tests/test_rule_registry.py:
    e: test_rule_registry_lists_builtin_rules,test_rule_registry_reports_per_rule_status,test_rule_registry_discovers_entry_points,test_custom_rule_can_be_registered
    test_rule_registry_lists_builtin_rules()
    test_rule_registry_reports_per_rule_status()
    test_rule_registry_discovers_entry_points()
    test_custom_rule_can_be_registered()
  tests/test_staged_e2e.py:
    e: _git,test_staged_hunk_check_fails_on_network_violation,test_staged_hunk_check_passes_clean_contract
    _git(cwd)
    test_staged_hunk_check_fails_on_network_violation(tmp_path)
    test_staged_hunk_check_passes_clean_contract(tmp_path)
  tests/test_validation.py:
    e: test_python_contract_passes,test_typescript_contract_detects_network_violation
    test_python_contract_passes()
    test_typescript_contract_detects_network_violation()
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('intract', '0.5.3', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 49, 'less').
project_file('examples/full-stack/src/analyzer.py', 4, 'python').
project_file('examples/full-stack/src/parser_a.py', 4, 'python').
project_file('examples/full-stack/src/parser_b.py', 4, 'python').
project_file('examples/full-stack/src/scanner.py', 5, 'python').
project_file('examples/integration_tests/01_python_pass/app.py', 9, 'python').
project_file('examples/integration_tests/02_typescript_violation_planfile/permission.ts', 7, 'typescript').
project_file('examples/integration_tests/03_watch_engine_drift/reporter.py', 5, 'python').
project_file('examples/integration_tests/03_watch_engine_drift/scanner.py', 9, 'python').
project_file('examples/integration_tests/run_examples.py', 102, 'python').
project_file('examples/python/parse_extensions.py', 9, 'python').
project_file('examples/typescript/permission.ts', 6, 'typescript').
project_file('project.sh', 50, 'shell').
project_file('scripts/ci-full-stack.sh', 59, 'shell').
project_file('sdks/go/examples/main.go', 23, 'go').
project_file('sdks/go/intractsdk/sdk.go', 69, 'go').
project_file('sdks/python/src/intract_plugin_example/__init__.py', 27, 'python').
project_file('sdks/rust/src/lib.rs', 55, 'rust').
project_file('sdks/typescript/examples/basic.ts', 14, 'typescript').
project_file('sdks/typescript/intract.config.ts', 9, 'typescript').
project_file('sdks/typescript/src/index.ts', 43, 'typescript').
project_file('src/intract/__init__.py', 32, 'python').
project_file('src/intract/__main__.py', 5, 'python').
project_file('src/intract/artifacts.py', 6, 'python').
project_file('src/intract/check.py', 247, 'python').
project_file('src/intract/cli.py', 398, 'python').
project_file('src/intract/config.py', 65, 'python').
project_file('src/intract/core/__init__.py', 36, 'python').
project_file('src/intract/core/artifact.py', 94, 'python').
project_file('src/intract/core/models.py', 154, 'python').
project_file('src/intract/core/normalizer.py', 70, 'python').
project_file('src/intract/core/registry.py', 7, 'python').
project_file('src/intract/core/signatures.py', 79, 'python').
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
project_file('src/intract/integrations/__init__.py', 16, 'python').
project_file('src/intract/integrations/planfile.py', 142, 'python').
project_file('src/intract/integrations/redup.py', 170, 'python').
project_file('src/intract/integrations/vallm.py', 117, 'python').
project_file('src/intract/manifest_schema.py', 95, 'python').
project_file('src/intract/models.py', 4, 'python').
project_file('src/intract/normalizer.py', 4, 'python').
project_file('src/intract/parser.py', 4, 'python').
project_file('src/intract/parsers/__init__.py', 11, 'python').
project_file('src/intract/parsers/inline.py', 194, 'python').
project_file('src/intract/parsers/manifest.py', 114, 'python').
project_file('src/intract/parsers/openapi.py', 64, 'python').
project_file('src/intract/plugins/__init__.py', 25, 'python').
project_file('src/intract/plugins/base.py', 110, 'python').
project_file('src/intract/plugins/builtins.py', 112, 'python').
project_file('src/intract/plugins/manager.py', 62, 'python').
project_file('src/intract/policy.py', 73, 'python').
project_file('src/intract/project.py', 89, 'python').
project_file('src/intract/reporters/__init__.py', 1, 'python').
project_file('src/intract/reporters/sarif.py', 63, 'python').
project_file('src/intract/sdk.py', 48, 'python').
project_file('src/intract/signature.py', 4, 'python').
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
project_file('tests/test_check_staged.py', 35, 'python').
project_file('tests/test_full_stack.py', 28, 'python').
project_file('tests/test_hunk_filter.py', 89, 'python').
project_file('tests/test_integrations.py', 61, 'python').
project_file('tests/test_manifest.py', 27, 'python').
project_file('tests/test_new_modules.py', 49, 'python').
project_file('tests/test_next_stage.py', 37, 'python').
project_file('tests/test_parser.py', 30, 'python').
project_file('tests/test_policy.py', 46, 'python').
project_file('tests/test_rule_registry.py', 53, 'python').
project_file('tests/test_staged_e2e.py', 65, 'python').
project_file('tests/test_validation.py', 40, 'python').
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
python_function('examples/integration_tests/run_examples.py', 'main', 0, 7, 8).
python_function('examples/python/parse_extensions.py', 'parse_extensions', 1, 3, 3).
python_function('src/intract/check.py', 'parse_unified_diff_hunks', 1, 6, 9).
python_function('src/intract/check.py', 'load_selected_sources', 2, 5, 4).
python_function('src/intract/check.py', '_manifest_changed', 1, 2, 2).
python_function('src/intract/check.py', 'changed_lines_by_file', 1, 4, 4).
python_function('src/intract/check.py', 'block_extent', 2, 13, 6).
python_function('src/intract/check.py', 'signature_touched', 3, 2, 4).
python_function('src/intract/check.py', 'validate_sources_for_hunks', 3, 14, 14).
python_function('src/intract/check.py', 'validate_selected_paths', 2, 8, 7).
python_function('src/intract/check.py', 'staged_check', 1, 4, 7).
python_function('src/intract/check.py', 'changed_check', 1, 1, 4).
python_function('src/intract/cli.py', 'main', 1, 2, 4).
python_function('src/intract/cli.py', 'init', 2, 3, 9).
python_function('src/intract/cli.py', 'scan', 2, 10, 18).
python_function('src/intract/cli.py', 'validate', 4, 3, 10).
python_function('src/intract/cli.py', 'check', 9, 13, 21).
python_function('src/intract/cli.py', 'coverage', 2, 2, 9).
python_function('src/intract/cli.py', 'duplicates', 3, 4, 13).
python_function('src/intract/cli.py', 'graph', 4, 5, 12).
python_function('src/intract/cli.py', 'tickets', 2, 1, 7).
python_function('src/intract/cli.py', 'watch', 6, 3, 16).
python_function('src/intract/cli.py', 'engine_suggest', 2, 3, 14).
python_function('src/intract/cli.py', 'engine_drift', 3, 4, 14).
python_function('src/intract/cli.py', 'engine_run', 4, 4, 13).
python_function('src/intract/cli.py', '_export_tickets', 2, 1, 6).
python_function('src/intract/cli.py', '_print_validation_report', 1, 4, 7).
python_function('src/intract/cli.py', '_format_check_text', 3, 7, 4).
python_function('src/intract/cli.py', 'check_manifest', 2, 4, 10).
python_function('src/intract/cli.py', 'artifact_validate', 2, 4, 8).
python_function('src/intract/config.py', 'load_config', 1, 11, 10).
python_function('src/intract/core/artifact.py', 'infer_language', 1, 1, 3).
python_function('src/intract/core/artifact.py', 'infer_artifact_kind', 2, 17, 4).
python_function('src/intract/core/normalizer.py', 'normalize_label', 1, 7, 10).
python_function('src/intract/core/normalizer.py', 'normalize_action', 1, 4, 2).
python_function('src/intract/core/normalizer.py', 'normalize_many', 1, 4, 3).
python_function('src/intract/core/normalizer.py', 'normalize_requirement', 1, 6, 8).
python_function('src/intract/core/signatures.py', 'make_block_id', 4, 1, 3).
python_function('src/intract/core/signatures.py', 'build_signature', 1, 15, 14).
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
python_function('src/intract/integrations/planfile.py', '_severity_from_status', 1, 4, 0).
python_function('src/intract/integrations/planfile.py', 'tickets_from_report', 1, 11, 8).
python_function('src/intract/integrations/redup.py', 'block_text', 1, 4, 1).
python_function('src/intract/integrations/redup.py', 'block_file_path', 1, 3, 2).
python_function('src/intract/integrations/redup.py', 'block_start_line', 1, 3, 2).
python_function('src/intract/integrations/redup.py', 'block_end_line', 1, 3, 3).
python_function('src/intract/integrations/redup.py', 'signatures_from_text', 1, 1, 2).
python_function('src/intract/integrations/redup.py', 'signatures_from_blocks', 1, 5, 6).
python_function('src/intract/integrations/redup.py', 'signatures_from_manifest', 1, 1, 3).
python_function('src/intract/integrations/redup.py', '_with_block_lines', 2, 1, 3).
python_function('src/intract/integrations/redup.py', 'find_intent_duplicate_groups', 1, 8, 8).
python_function('src/intract/integrations/redup.py', 'scan_blocks_for_intent_duplicates', 1, 2, 4).
python_function('src/intract/integrations/vallm.py', 'map_validation_result', 1, 6, 3).
python_function('src/intract/integrations/vallm.py', 'map_project_report', 1, 7, 3).
python_function('src/intract/integrations/vallm.py', 'validate_for_vallm', 1, 2, 3).
python_function('src/intract/integrations/vallm.py', 'validate_proposal', 1, 12, 8).
python_function('src/intract/manifest_schema.py', '_load_schema', 0, 2, 5).
python_function('src/intract/manifest_schema.py', 'validate_manifest', 1, 15, 17).
python_function('src/intract/parsers/inline.py', 'clean_comment_line', 1, 8, 4).
python_function('src/intract/parsers/inline.py', 'split_csv', 1, 6, 5).
python_function('src/intract/parsers/inline.py', 'parse_priority', 1, 5, 7).
python_function('src/intract/parsers/inline.py', 'parse_key_value', 1, 2, 4).
python_function('src/intract/parsers/inline.py', 'marker_payload', 1, 3, 3).
python_function('src/intract/parsers/inline.py', 'parse_contract_line', 1, 42, 16).
python_function('src/intract/parsers/inline.py', 'extract_contract_records_from_text', 1, 3, 5).
python_function('src/intract/parsers/manifest.py', '_to_tuple', 1, 9, 6).
python_function('src/intract/parsers/manifest.py', '_parse_intent', 1, 3, 2).
python_function('src/intract/parsers/manifest.py', 'contract_from_mapping', 1, 3, 7).
python_function('src/intract/parsers/manifest.py', 'load_manifest_records', 1, 11, 10).
python_function('src/intract/parsers/manifest.py', 'create_sample_manifest', 0, 1, 0).
python_function('src/intract/parsers/openapi.py', 'parse_openapi_contracts', 1, 8, 10).
python_function('src/intract/parsers/openapi.py', 'parse_openapi_text', 1, 8, 9).
python_function('src/intract/plugins/manager.py', '_register_unique', 3, 3, 2).
python_function('src/intract/plugins/manager.py', 'load_builtin_plugins', 0, 1, 8).
python_function('src/intract/plugins/manager.py', 'discover_plugins', 0, 6, 6).
python_function('src/intract/policy.py', '_p1_missing_reasons', 2, 7, 6).
python_function('src/intract/policy.py', 'decide_policy', 1, 15, 11).
python_function('src/intract/project.py', 'load_project_sources', 1, 7, 6).
python_function('src/intract/project.py', 'extract_signatures_from_sources', 1, 2, 4).
python_function('src/intract/project.py', 'validate_sources', 1, 16, 11).
python_function('src/intract/project.py', 'validate_project', 1, 4, 6).
python_function('src/intract/reporters/sarif.py', 'report_to_sarif', 1, 11, 7).
python_function('src/intract/sdk.py', 'contract', 0, 1, 1).
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
python_function('tests/test_check_staged.py', 'test_manifest_changed_helper', 0, 3, 1).
python_function('tests/test_check_staged.py', 'test_validate_selected_paths_full_graph', 1, 3, 3).
python_function('tests/test_full_stack.py', 'test_full_stack_validate_passes', 0, 2, 1).
python_function('tests/test_full_stack.py', 'test_full_stack_graph_covers_requires', 0, 4, 1).
python_function('tests/test_full_stack.py', 'test_full_stack_finds_intent_duplicates', 0, 5, 2).
python_function('tests/test_hunk_filter.py', 'test_changed_lines_by_file', 0, 2, 2).
python_function('tests/test_hunk_filter.py', 'test_block_extent_finds_function_body', 0, 3, 1).
python_function('tests/test_hunk_filter.py', 'test_signature_touched_by_body_change', 0, 3, 3).
python_function('tests/test_hunk_filter.py', 'test_validate_sources_for_hunks_only_touched_contract', 1, 4, 5).
python_function('tests/test_hunk_filter.py', 'test_validate_sources_for_hunks_catches_violation_in_touched_block', 1, 2, 3).
python_function('tests/test_integrations.py', 'test_redup_finds_intent_duplicate_groups', 0, 4, 2).
python_function('tests/test_integrations.py', 'test_duplicate_contracts_cli_parity', 1, 2, 2).
python_function('tests/test_integrations.py', 'test_find_intent_duplicate_groups_from_blocks', 0, 2, 2).
python_function('tests/test_manifest.py', 'test_load_manifest_records', 1, 4, 3).
python_function('tests/test_new_modules.py', 'test_coverage', 1, 3, 2).
python_function('tests/test_new_modules.py', 'test_duplicates', 1, 2, 2).
python_function('tests/test_new_modules.py', 'test_graph_missing_requirement', 1, 2, 2).
python_function('tests/test_next_stage.py', 'test_manifest_schema_valid', 1, 2, 2).
python_function('tests/test_next_stage.py', 'test_parse_hunks', 0, 3, 2).
python_function('tests/test_next_stage.py', 'test_dockerfile_artifact_violation', 1, 3, 2).
python_function('tests/test_parser.py', 'test_parse_full_contract_line', 0, 10, 1).
python_function('tests/test_parser.py', 'test_parse_comment_prefix_ts', 0, 4, 1).
python_function('tests/test_policy.py', 'test_missing_required_p1_fails_policy', 1, 3, 5).
python_function('tests/test_policy.py', 'test_full_stack_passes_without_p1_gate', 0, 2, 5).
python_function('tests/test_rule_registry.py', 'test_rule_registry_lists_builtin_rules', 0, 6, 2).
python_function('tests/test_rule_registry.py', 'test_rule_registry_reports_per_rule_status', 0, 3, 3).
python_function('tests/test_rule_registry.py', 'test_rule_registry_discovers_entry_points', 0, 3, 3).
python_function('tests/test_rule_registry.py', 'test_custom_rule_can_be_registered', 0, 2, 5).
python_function('tests/test_staged_e2e.py', '_git', 1, 1, 1).
python_function('tests/test_staged_e2e.py', 'test_staged_hunk_check_fails_on_network_violation', 1, 3, 5).
python_function('tests/test_staged_e2e.py', 'test_staged_hunk_check_passes_clean_contract', 1, 3, 5).
python_function('tests/test_validation.py', 'test_python_contract_passes', 0, 2, 3).
python_function('tests/test_validation.py', 'test_typescript_contract_detects_network_violation', 0, 3, 3).

% ── Python Classes ───────────────────────────────────────
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
python_class('src/intract/integrations/planfile.py', 'Ticket').
python_class('src/intract/integrations/planfile.py', 'PlanfileExporter').
python_method('PlanfileExporter', '__init__', 1, 1, 1).
python_method('PlanfileExporter', 'export', 1, 1, 4).
python_method('PlanfileExporter', '_write_yaml', 2, 7, 5).
python_method('PlanfileExporter', '_write_json', 2, 2, 3).
python_method('PlanfileExporter', '_write_todo', 2, 8, 3).
python_class('src/intract/integrations/redup.py', 'CodeBlockLike').
python_class('src/intract/integrations/redup.py', 'BlockAdapter').
python_class('src/intract/integrations/redup.py', 'RedupScanResult').
python_method('RedupScanResult', 'to_dict', 0, 1, 1).
python_class('src/intract/integrations/vallm.py', 'MappedIssue').
python_class('src/intract/integrations/vallm.py', 'MappedValidationResult').
python_method('MappedValidationResult', 'to_dict', 0, 2, 0).
python_class('src/intract/manifest_schema.py', 'ManifestIssue').
python_class('src/intract/manifest_schema.py', 'ManifestValidationReport').
python_method('ManifestValidationReport', 'to_dict', 0, 2, 1).
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
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('install', 'manual').
sumd_workflow_step('install', 1, 'pip install -e .[dev]').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'pytest -q').
sumd_workflow('lint', 'manual').
sumd_workflow_step('lint', 1, 'ruff check .').
sumd_workflow('format', 'manual').
sumd_workflow_step('format', 1, 'ruff format .').
```

## Call Graph

*144 nodes · 172 edges · 40 modules · CC̄=4.2*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `contract_from_mapping` *(in src.intract.parsers.manifest)* | 3 | 4 | 59 | **63** |
| `parse_contract_line` *(in src.intract.parsers.inline)* | 42 ⚠ | 1 | 51 | **52** |
| `build_signature` *(in src.intract.core.signatures)* | 15 ⚠ | 3 | 40 | **43** |
| `validate_manifest` *(in src.intract.manifest_schema)* | 15 ⚠ | 2 | 35 | **37** |
| `normalize_label` *(in src.intract.core.normalizer)* | 7 | 11 | 16 | **27** |
| `load_manifest_records` *(in src.intract.parsers.manifest)* | 11 ⚠ | 7 | 19 | **26** |
| `tickets_from_report` *(in src.intract.integrations.planfile)* | 11 ⚠ | 2 | 21 | **23** |
| `engine_drift` *(in src.intract.cli)* | 4 | 0 | 21 | **21** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/semcod/intract
# generated in 0.06s
# nodes: 144 | edges: 172 | modules: 40
# CC̄=4.2

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
    CC=11  in:2  out:21  total:23
  src.intract.cli.engine_drift
    CC=4  in:0  out:21  total:21
  src.intract.policy.decide_policy
    CC=15  in:1  out:19  total:20
  src.intract.graph.build_graph
    CC=9  in:2  out:18  total:20
  src.intract.cli.engine_run
    CC=4  in:0  out:20  total:20
  src.intract.validators.artifacts.validate_artifact
    CC=9  in:2  out:17  total:19
  src.intract.validators.engine.validate_contract_against_source
    CC=8  in:5  out:14  total:19
  src.intract.engine.analyzer.analyze_source_units
    CC=12  in:1  out:17  total:18
  examples.integration_tests.run_examples.run_example_03
    CC=2  in:1  out:17  total:18
  src.intract.project.validate_project
    CC=4  in:10  out:8  total:18
  src.intract.cli.engine_suggest
    CC=3  in:0  out:18  total:18
  src.intract.duplicates.grouping.pairs_to_intent_groups
    CC=6  in:1  out:16  total:17
  src.intract.cli.duplicates
    CC=4  in:0  out:17  total:17
  src.intract.parsers.openapi.parse_openapi_contracts
    CC=8  in:1  out:16  total:17

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
  src.intract.check  [10 funcs]
    _manifest_changed  CC=2  out:2
    block_extent  CC=13  out:10
    changed_check  CC=1  out:4
    changed_lines_by_file  CC=4  out:4
    load_selected_sources  CC=5  out:4
    parse_unified_diff_hunks  CC=6  out:16
    signature_touched  CC=2  out:4
    staged_check  CC=4  out:8
    validate_selected_paths  CC=8  out:10
    validate_sources_for_hunks  CC=14  out:15
  src.intract.cli  [13 funcs]
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
  src.intract.integrations.vallm  [4 funcs]
    map_project_report  CC=7  out:3
    map_validation_result  CC=6  out:4
    validate_for_vallm  CC=2  out:3
    validate_proposal  CC=12  out:9
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
  src.intract.policy  [2 funcs]
    _p1_missing_reasons  CC=7  out:6
    decide_policy  CC=15  out:19
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
  src.intract.project.extract_signatures_from_sources → src.intract.core.signatures.build_signatures
  src.intract.project.extract_signatures_from_sources → src.intract.parsers.inline.extract_contract_records_from_text
  src.intract.project.validate_sources → src.intract.project.extract_signatures_from_sources
  src.intract.project.validate_sources → src.intract.core.signatures.build_signatures
  src.intract.project.validate_sources → src.intract.validators.engine.validate_contract_against_source
  src.intract.project.validate_sources → src.intract.validators.requirements.validate_required_contracts
  src.intract.project.validate_project → src.intract.project.load_project_sources
  src.intract.project.validate_project → src.intract.project.validate_sources
  src.intract.project.validate_project → src.intract.parsers.manifest.load_manifest_records
  src.intract.coverage.calculate_coverage → src.intract.project.load_project_sources
  src.intract.coverage.calculate_coverage → src.intract.project.extract_signatures_from_sources
  src.intract.graph.ContractGraph.to_mermaid → src.intract.graph._safe
  src.intract.graph.build_graph → src.intract.project.load_project_sources
  src.intract.graph.build_graph → src.intract.project.extract_signatures_from_sources
  src.intract.git.staged_files → src.intract.git._run_git
  src.intract.git.changed_files → src.intract.git._run_git
  src.intract.git.staged_hunks → src.intract.git._run_git
  src.intract.manifest_schema.validate_manifest → src.intract.manifest_schema._load_schema
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
  src.intract.validators.input_output.contains_token_like → src.intract.core.normalizer.normalize_label
  src.intract.validators.input_output.InputPresenceRule.validate → src.intract.validators.input_output.contains_token_like
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Intent

Intent contract tagging, validation and semantic mapping for codebases.
