# System Architecture Analysis
<!-- generated in 0.00s -->

## Overview

- **Project**: /home/tom/github/semcod/intract
- **Primary Language**: python
- **Languages**: python: 69, yaml: 10, typescript: 5, toml: 4, json: 3
- **Analysis Mode**: static
- **Total Functions**: 227
- **Total Classes**: 64
- **Modules**: 103
- **Entry Points**: 106

## Architecture by Module

### src.intract.cli
- **Functions**: 18
- **File**: `cli.py`

### src.intract.plugins.base
- **Functions**: 12
- **Classes**: 6
- **File**: `base.py`

### src.intract.plugins.builtins
- **Functions**: 11
- **Classes**: 6
- **File**: `builtins.py`

### src.intract.integrations.redup
- **Functions**: 11
- **Classes**: 3
- **File**: `redup.py`

### src.intract.check
- **Functions**: 11
- **Classes**: 1
- **File**: `check.py`

### src.intract.validators.input_output
- **Functions**: 8
- **Classes**: 3
- **File**: `input_output.py`

### src.intract.validators.registry
- **Functions**: 8
- **Classes**: 1
- **File**: `registry.py`

### src.intract.parsers.inline
- **Functions**: 7
- **File**: `inline.py`

### src.intract.integrations.planfile
- **Functions**: 7
- **Classes**: 2
- **File**: `planfile.py`

### src.intract.watch
- **Functions**: 6
- **Classes**: 3
- **File**: `watch.py`

### src.intract.duplicates.grouping
- **Functions**: 6
- **Classes**: 2
- **File**: `grouping.py`

### src.intract.validators.artifacts
- **Functions**: 6
- **Classes**: 1
- **File**: `artifacts.py`

### src.intract.engine.assigner
- **Functions**: 6
- **File**: `assigner.py`

### examples.integration_tests.run_examples
- **Functions**: 5
- **File**: `run_examples.py`

### src.intract.git
- **Functions**: 5
- **Classes**: 1
- **File**: `git.py`

### src.intract.engine.drift
- **Functions**: 5
- **Classes**: 2
- **File**: `drift.py`

### src.intract.parsers.manifest
- **Functions**: 5
- **File**: `manifest.py`

### src.intract.integrations.vallm
- **Functions**: 5
- **Classes**: 2
- **File**: `vallm.py`

### src.intract.project
- **Functions**: 4
- **File**: `project.py`

### src.intract.graph
- **Functions**: 4
- **Classes**: 1
- **File**: `graph.py`

## Key Entry Points

Main execution flows into the system:

### src.intract.cli.check
> Policy-aware validation for pre-commit/CI.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option

### src.intract.cli.scan
> Scan files for inline @intract contracts.
- **Calls**: app.command, typer.Argument, typer.Option, path.is_file, Table, table.add_column, table.add_column, table.add_column

### src.intract.cli.watch
> Watch folder and re-validate Intract contracts when logical files change.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, typer.Option, typer.Option, console.print

### src.intract.config.IntractConfig.from_mapping
- **Calls**: None.get, tool.get, plugins.get, cls, data.get, tool.get, data.get, str

### src.intract.cli.engine_drift
- **Calls**: engine_app.command, typer.Argument, typer.Option, typer.Option, src.intract.engine.monitor.scan_suggest_and_validate, console.print, console.print, console.print

### src.intract.cli.engine_run
- **Calls**: engine_app.command, typer.Argument, typer.Option, typer.Option, typer.Option, src.intract.engine.monitor.scan_suggest_and_validate, console.print, console.print

### src.intract.cli.engine_suggest
- **Calls**: engine_app.command, typer.Argument, typer.Option, src.intract.engine.monitor.scan_suggest_and_validate, Table, table.add_column, table.add_column, table.add_column

### src.intract.cli.duplicates
> Find duplicate/similar intent contracts.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, src.intract.duplicates.grouping.find_duplicate_contracts, Table, table.add_column, table.add_column

### src.intract.cli.graph
> Build require/provide graph from contracts.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, src.intract.graph.build_graph, Path, json.dumps

### src.intract.sdk.ContractBuilder.to_inline
- **Calls**: parts.append, parts.append, parts.append, parts.append, parts.append, parts.append, parts.append, parts.append

### src.intract.plugins.manager.discover_plugins
- **Calls**: entry_points, eps.select, eps.select, eps.select, eps.select, src.intract.plugins.manager.load_builtin_plugins, PluginRegistry, src.intract.plugins.manager._register_unique

### src.intract.integrations.planfile.PlanfileExporter._write_yaml
- **Calls**: path.write_text, asdict, yaml.safe_dump, path.write_text, lines.append, lines.append, lines.append, lines.append

### src.intract.cli.validate
> Validate project contracts.
- **Calls**: app.command, typer.Argument, typer.Option, typer.Option, typer.Option, src.intract.project.validate_project, src.intract.cli._print_validation_report, Path

### src.intract.cli.coverage
> Show contract coverage for project files.
- **Calls**: app.command, typer.Argument, typer.Option, src.intract.coverage.calculate_coverage, console.print, console.print, console.print, console.print

### src.intract.cli.check_manifest
> Validate intract.yaml against the Intract schema.
- **Calls**: app.command, typer.Argument, typer.Option, src.intract.manifest_schema.validate_manifest, Path, console.print_json, console.print, console.print

### src.intract.cli.artifact_validate
> Validate a non-code artifact: OpenAPI, Dockerfile, GitHub Actions or Kubernetes.
- **Calls**: app.command, typer.Argument, typer.Option, src.intract.validators.artifacts.validate_artifact, console.print, console.print, console.print_json, console.print

### src.intract.cli.init
> Create a sample intract.yaml manifest.
- **Calls**: app.command, typer.Argument, typer.Option, target.write_text, console.print, Path, target.exists, console.print

### src.intract.graph.ContractGraph.to_mermaid
- **Calls**: None.join, src.intract.graph._safe, lines.append, lines.append, lines.append, lines.append, src.intract.graph._safe, src.intract.graph._safe

### src.intract.integrations.vallm.validate_proposal
> Validate inline @intract contracts in a single code snippet or file body.
- **Calls**: src.intract.parsers.inline.extract_contract_records_from_text, any, ProjectReport, src.intract.integrations.vallm.map_project_report, MappedValidationResult, src.intract.validators.engine.validate_contract_against_source, src.intract.core.signatures.build_signatures, all

### examples.integration_tests.run_examples.main
- **Calls**: results.items, print, None.resolve, examples.integration_tests.run_examples.run_example_01, examples.integration_tests.run_examples.run_example_02, examples.integration_tests.run_examples.run_example_03, examples.integration_tests.run_examples.print_result, Path

### src.intract.core.artifact.Artifact.from_path
- **Calls**: Path, p.read_text, cls, str, src.intract.core.artifact.infer_language, src.intract.core.artifact.infer_artifact_kind, str, str

### src.intract.validators.input_output.InputPresenceRule.validate
- **Calls**: sorted, RuleResult, src.intract.validators.input_output.contains_token_like, set, len, max, len

### src.intract.validators.input_output.OutputPresenceRule.validate
- **Calls**: sorted, RuleResult, src.intract.validators.input_output.contains_token_like, set, len, max, len

### src.intract.integrations.planfile.PlanfileExporter._write_todo
- **Calls**: path.write_text, lines.append, lines.append, lines.append, None.join, lines.append, lines.append

### src.intract.cli.tickets
> Validate and export failed/partial/violating results as planfile-style tickets.
- **Calls**: app.command, typer.Argument, typer.Option, src.intract.project.validate_project, src.intract.cli._export_tickets, console.print, Path

### src.intract.core.models.ProjectReport.to_dict
- **Calls**: len, len, len, len, len, item.to_dict

### sdks.rust.src.inline_contract
- **Calls**: sdks.rust.src.to_string, sdks.rust.src.Some, sdks.rust.src.push, sdks.rust.src.is_empty, sdks.rust.src.csv, sdks.rust.src.join

### src.intract.validators.effects.NoForbiddenEffectRule.validate
- **Calls**: src.intract.validators.effects.detect_effects, sorted, RuleResult, ValidationIssue, sorted

### src.intract.plugins.builtins.BasicContractValidatorPlugin.validate
- **Calls**: PluginResult, results.append, any, None.to_dict, src.intract.validators.engine.validate_contract_against_source

### sdks.go.intractsdk.sdk.Inline
- **Calls**: sdks.go.intractsdk.sdk.Sprintf, sdks.go.intractsdk.sdk.append, sdks.go.intractsdk.sdk.len, sdks.go.intractsdk.sdk.csv, sdks.go.intractsdk.sdk.Join

## Process Flows

Key execution flows identified:

### Flow 1: check
```
check [src.intract.cli]
```

### Flow 2: scan
```
scan [src.intract.cli]
```

### Flow 3: watch
```
watch [src.intract.cli]
```

### Flow 4: from_mapping
```
from_mapping [src.intract.config.IntractConfig]
```

### Flow 5: engine_drift
```
engine_drift [src.intract.cli]
  └─ →> scan_suggest_and_validate
      └─ →> collect_source_units
      └─ →> analyze_source_units
          └─> _slice_until_next_match
```

### Flow 6: engine_run
```
engine_run [src.intract.cli]
```

### Flow 7: engine_suggest
```
engine_suggest [src.intract.cli]
  └─ →> scan_suggest_and_validate
      └─ →> collect_source_units
      └─ →> analyze_source_units
          └─> _slice_until_next_match
```

### Flow 8: duplicates
```
duplicates [src.intract.cli]
  └─ →> find_duplicate_contracts
      └─> pairs_to_duplicate_contracts
      └─ →> load_project_sources
      └─ →> extract_signatures_from_sources
```

### Flow 9: graph
```
graph [src.intract.cli]
```

### Flow 10: to_inline
```
to_inline [src.intract.sdk.ContractBuilder]
```

## Key Classes

### src.intract.plugins.base.PluginRegistry
- **Methods**: 6
- **Key Methods**: src.intract.plugins.base.PluginRegistry.add_parser, src.intract.plugins.base.PluginRegistry.add_validator, src.intract.plugins.base.PluginRegistry.add_reporter, src.intract.plugins.base.PluginRegistry.add_integration, src.intract.plugins.base.PluginRegistry.parse_artifact, src.intract.plugins.base.PluginRegistry.validate_artifact

### src.intract.validators.registry.RuleRegistry
> Registry of contract validation rules with optional plugin discovery.
- **Methods**: 6
- **Key Methods**: src.intract.validators.registry.RuleRegistry.__init__, src.intract.validators.registry.RuleRegistry.register, src.intract.validators.registry.RuleRegistry.rules, src.intract.validators.registry.RuleRegistry.run, src.intract.validators.registry.RuleRegistry.rule_status, src.intract.validators.registry.RuleRegistry.summarize

### src.intract.core.models.ProjectReport
- **Methods**: 5
- **Key Methods**: src.intract.core.models.ProjectReport.passed, src.intract.core.models.ProjectReport.partial, src.intract.core.models.ProjectReport.failed, src.intract.core.models.ProjectReport.violations, src.intract.core.models.ProjectReport.to_dict

### src.intract.integrations.planfile.PlanfileExporter
- **Methods**: 5
- **Key Methods**: src.intract.integrations.planfile.PlanfileExporter.__init__, src.intract.integrations.planfile.PlanfileExporter.export, src.intract.integrations.planfile.PlanfileExporter._write_yaml, src.intract.integrations.planfile.PlanfileExporter._write_json, src.intract.integrations.planfile.PlanfileExporter._write_todo

### src.intract.graph.ContractGraph
- **Methods**: 2
- **Key Methods**: src.intract.graph.ContractGraph.to_dict, src.intract.graph.ContractGraph.to_mermaid

### src.intract.validators.input_output.InputPresenceRule
- **Methods**: 2
- **Key Methods**: src.intract.validators.input_output.InputPresenceRule.supports, src.intract.validators.input_output.InputPresenceRule.validate

### src.intract.validators.input_output.OutputPresenceRule
- **Methods**: 2
- **Key Methods**: src.intract.validators.input_output.OutputPresenceRule.supports, src.intract.validators.input_output.OutputPresenceRule.validate

### src.intract.validators.input_output.ReturnValueRule
- **Methods**: 2
- **Key Methods**: src.intract.validators.input_output.ReturnValueRule.supports, src.intract.validators.input_output.ReturnValueRule.validate

### src.intract.validators.base.ValidationRule
- **Methods**: 2
- **Key Methods**: src.intract.validators.base.ValidationRule.supports, src.intract.validators.base.ValidationRule.validate
- **Inherits**: Protocol

### src.intract.validators.effects.NoForbiddenEffectRule
- **Methods**: 2
- **Key Methods**: src.intract.validators.effects.NoForbiddenEffectRule.supports, src.intract.validators.effects.NoForbiddenEffectRule.validate

### src.intract.plugins.base.ParserPlugin
- **Methods**: 2
- **Key Methods**: src.intract.plugins.base.ParserPlugin.supports, src.intract.plugins.base.ParserPlugin.parse
- **Inherits**: Protocol

### src.intract.plugins.base.ValidatorPlugin
- **Methods**: 2
- **Key Methods**: src.intract.plugins.base.ValidatorPlugin.supports, src.intract.plugins.base.ValidatorPlugin.validate
- **Inherits**: Protocol

### src.intract.plugins.builtins.InlineContractParserPlugin
- **Methods**: 2
- **Key Methods**: src.intract.plugins.builtins.InlineContractParserPlugin.supports, src.intract.plugins.builtins.InlineContractParserPlugin.parse

### src.intract.plugins.builtins.OpenAPIParserPlugin
- **Methods**: 2
- **Key Methods**: src.intract.plugins.builtins.OpenAPIParserPlugin.supports, src.intract.plugins.builtins.OpenAPIParserPlugin.parse

### src.intract.plugins.builtins.ManifestParserPlugin
- **Methods**: 2
- **Key Methods**: src.intract.plugins.builtins.ManifestParserPlugin.supports, src.intract.plugins.builtins.ManifestParserPlugin.parse

### src.intract.plugins.builtins.BasicContractValidatorPlugin
- **Methods**: 2
- **Key Methods**: src.intract.plugins.builtins.BasicContractValidatorPlugin.supports, src.intract.plugins.builtins.BasicContractValidatorPlugin.validate

### src.intract.plugins.builtins.ArtifactStructureValidatorPlugin
- **Methods**: 2
- **Key Methods**: src.intract.plugins.builtins.ArtifactStructureValidatorPlugin.supports, src.intract.plugins.builtins.ArtifactStructureValidatorPlugin.validate

### sdks.java.src.main.java.io.intract.sdk.IntractContract.IntractContract
- **Methods**: 2
- **Key Methods**: sdks.java.src.main.java.io.intract.sdk.IntractContract.IntractContract.inline, sdks.java.src.main.java.io.intract.sdk.IntractContract.IntractContract.join

### sdks.python.src.intract_plugin_example.ExampleParserPlugin
- **Methods**: 2
- **Key Methods**: sdks.python.src.intract_plugin_example.ExampleParserPlugin.supports, sdks.python.src.intract_plugin_example.ExampleParserPlugin.parse

### sdks.python.src.intract_plugin_example.ExampleValidatorPlugin
- **Methods**: 2
- **Key Methods**: sdks.python.src.intract_plugin_example.ExampleValidatorPlugin.supports, sdks.python.src.intract_plugin_example.ExampleValidatorPlugin.validate

## Data Transformation Functions

Key functions that process and transform data:

### examples.integration_tests.01_python_pass.app.parse_extensions
- **Output to**: None.lower, raw_extensions.split, item.strip, item.strip

### src.intract.project.validate_sources
- **Output to**: src.intract.project.extract_signatures_from_sources, any, ProjectReport, observed_by_file.get, results.append

### src.intract.project.validate_project
- **Output to**: Path, src.intract.project.load_project_sources, src.intract.project.validate_sources, str, src.intract.parsers.manifest.load_manifest_records

### src.intract.manifest_schema.validate_manifest
- **Output to**: Path, ManifestValidationReport, manifest_path.exists, ManifestValidationReport, Draft202012Validator

### src.intract.validators.artifacts.validate_openapi
- **Output to**: src.intract.parsers.openapi.parse_openapi_contracts, None.lower, ArtifactValidationReport, src.intract.core.signatures.build_signature, record.owner.lower

### src.intract.validators.artifacts.validate_dockerfile
- **Output to**: path.read_text, re.search, re.search, ArtifactValidationReport, issues.append

### src.intract.validators.artifacts.validate_github_actions
- **Output to**: path.read_text, text.lower, any, ArtifactValidationReport, any

### src.intract.validators.artifacts.validate_kubernetes
- **Output to**: path.read_text, text.lower, any, ArtifactValidationReport, issues.append

### src.intract.validators.artifacts.validate_artifact
- **Output to**: Path, p.name.lower, p.read_text, ArtifactValidationReport, name.startswith

### src.intract.validators.input_output.InputPresenceRule.validate
- **Output to**: sorted, RuleResult, src.intract.validators.input_output.contains_token_like, set, len

### src.intract.validators.input_output.OutputPresenceRule.validate
- **Output to**: sorted, RuleResult, src.intract.validators.input_output.contains_token_like, set, len

### src.intract.validators.input_output.ReturnValueRule.validate
- **Output to**: src.intract.validators.input_output.has_return_value, RuleResult

### src.intract.validators.base.ValidationRule.validate

### src.intract.validators.requirements.validate_required_contracts
- **Output to**: sorted, sorted

### src.intract.validators.effects.NoForbiddenEffectRule.validate
- **Output to**: src.intract.validators.effects.detect_effects, sorted, RuleResult, ValidationIssue, sorted

### src.intract.plugins.base.ParserPlugin.parse

### src.intract.plugins.base.ValidatorPlugin.validate

### src.intract.plugins.base.PluginRegistry.add_parser
- **Output to**: self.parsers.append

### src.intract.plugins.base.PluginRegistry.parse_artifact
- **Output to**: parser.supports, parser.parse, contracts.extend

### src.intract.plugins.base.PluginRegistry.validate_artifact
- **Output to**: validator.supports, results.append, validator.validate

### src.intract.plugins.builtins.InlineContractParserPlugin.parse
- **Output to**: src.intract.parsers.inline.extract_contract_records_from_text, PluginResult, src.intract.core.signatures.build_signatures

### src.intract.plugins.builtins.OpenAPIParserPlugin.parse
- **Output to**: src.intract.parsers.openapi.parse_openapi_text, PluginResult, src.intract.core.signatures.build_signatures

### src.intract.plugins.builtins.ManifestParserPlugin.parse
- **Output to**: src.intract.parsers.manifest.load_manifest_records, PluginResult, Path, src.intract.core.signatures.build_signatures

### src.intract.plugins.builtins.BasicContractValidatorPlugin.validate
- **Output to**: PluginResult, results.append, any, None.to_dict, src.intract.validators.engine.validate_contract_against_source

### src.intract.plugins.builtins.ArtifactStructureValidatorPlugin.validate
- **Output to**: src.intract.validators.artifacts.validate_artifact, PluginResult, item.to_dict, any

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `src.intract.parsers.manifest.contract_from_mapping` - 59 calls
- `src.intract.parsers.inline.parse_contract_line` - 51 calls
- `src.intract.core.signatures.build_signature` - 40 calls
- `src.intract.manifest_schema.validate_manifest` - 35 calls
- `src.intract.cli.check` - 32 calls
- `src.intract.cli.scan` - 30 calls
- `src.intract.cli.watch` - 28 calls
- `src.intract.config.IntractConfig.from_mapping` - 23 calls
- `src.intract.integrations.planfile.tickets_from_report` - 21 calls
- `src.intract.cli.engine_drift` - 21 calls
- `src.intract.cli.engine_run` - 20 calls
- `src.intract.reporters.sarif.report_to_sarif` - 19 calls
- `src.intract.parsers.manifest.load_manifest_records` - 19 calls
- `src.intract.policy.decide_policy` - 19 calls
- `src.intract.graph.build_graph` - 18 calls
- `src.intract.cli.engine_suggest` - 18 calls
- `examples.integration_tests.run_examples.run_example_03` - 17 calls
- `src.intract.validators.artifacts.validate_artifact` - 17 calls
- `src.intract.engine.analyzer.analyze_source_units` - 17 calls
- `src.intract.cli.duplicates` - 17 calls
- `src.intract.duplicates.grouping.pairs_to_intent_groups` - 16 calls
- `src.intract.validators.artifacts.validate_openapi` - 16 calls
- `src.intract.core.normalizer.normalize_label` - 16 calls
- `src.intract.parsers.openapi.parse_openapi_contracts` - 16 calls
- `src.intract.cli.graph` - 16 calls
- `src.intract.check.parse_unified_diff_hunks` - 16 calls
- `src.intract.project.validate_sources` - 15 calls
- `src.intract.sdk.ContractBuilder.to_inline` - 15 calls
- `src.intract.plugins.manager.discover_plugins` - 15 calls
- `src.intract.check.validate_sources_for_hunks` - 15 calls
- `src.intract.config.load_config` - 14 calls
- `src.intract.coverage.calculate_coverage` - 14 calls
- `src.intract.duplicates.scoring.score_similarity` - 14 calls
- `src.intract.validators.artifacts.validate_dockerfile` - 14 calls
- `src.intract.engine.scanner.collect_source_units` - 14 calls
- `src.intract.parsers.inline.clean_comment_line` - 14 calls
- `src.intract.parsers.openapi.parse_openapi_text` - 14 calls
- `src.intract.validators.engine.validate_contract_against_source` - 14 calls
- `src.intract.validators.artifacts.validate_kubernetes` - 13 calls
- `src.intract.validators.effects.detect_effects` - 13 calls

## System Interactions

How components interact:

```mermaid
graph TD
    check --> command
    check --> Argument
    check --> Option
    scan --> command
    scan --> Argument
    scan --> Option
    scan --> is_file
    scan --> Table
    watch --> command
    watch --> Argument
    watch --> Option
    from_mapping --> get
    from_mapping --> cls
    engine_drift --> command
    engine_drift --> Argument
    engine_drift --> Option
    engine_drift --> scan_suggest_and_val
    engine_run --> command
    engine_run --> Argument
    engine_run --> Option
    engine_suggest --> command
    engine_suggest --> Argument
    engine_suggest --> Option
    engine_suggest --> scan_suggest_and_val
    engine_suggest --> Table
    duplicates --> command
    duplicates --> Argument
    duplicates --> Option
    duplicates --> find_duplicate_contr
    graph --> command
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.