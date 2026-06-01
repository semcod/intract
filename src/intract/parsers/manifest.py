from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from intract.core.models import Contract, ContractRecord


def _to_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        if value.lower() in {"none", "null", "-"}:
            return ()
        return tuple(part.strip() for part in value.split(",") if part.strip())
    if isinstance(value, (list, tuple, set)):
        return tuple(str(item) for item in value if str(item).strip())
    return (str(value),)


def _parse_intent(value: str) -> tuple[str, str]:
    if ":" in value:
        left, right = value.split(":", 1)
        return left.strip(), right.strip()
    if "." in value:
        left, right = value.split(".", 1)
        return left.strip(), right.strip()
    return value.strip(), "unknown"


def contract_from_mapping(data: dict[str, Any]) -> Contract:
    action = str(data.get("action", "")).strip()
    object_name = str(data.get("object", data.get("obj", ""))).strip()
    if not action or not object_name:
        intent = str(data.get("intent", "")).strip()
        action, object_name = _parse_intent(intent)
    return Contract(
        action=action,
        object=object_name,
        scope=str(data.get("scope", "block")),
        priority=int(data.get("priority", 3)),
        domain=str(data.get("domain", "")),
        inputs=_to_tuple(data.get("input", data.get("inputs", data.get("in")))),
        outputs=_to_tuple(data.get("output", data.get("outputs", data.get("out")))),
        effects=_to_tuple(data.get("effect", data.get("effects", data.get("fx")))),
        forbidden=_to_tuple(data.get("forbid", data.get("forbidden", data.get("no")))),
        required=_to_tuple(data.get("require", data.get("requires", data.get("req")))),
        validators=_to_tuple(data.get("validate", data.get("validators", data.get("rules")))),
        tags=_to_tuple(data.get("tags", data.get("tag"))),
        algorithms=_to_tuple(data.get("algorithms", data.get("algorithm", data.get("alg")))),
        relations=_to_tuple(data.get("relations", data.get("relation", data.get("rel")))),
        contract_id=str(data.get("id", data.get("contract_id", ""))),
        meaning=str(data.get("meaning", "")),
        raw=str(data),
    )


def load_manifest_records(path: Path) -> list[ContractRecord]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    records: list[ContractRecord] = []
    for index, item in enumerate(data.get("contracts", []) or [], start=1):
        if isinstance(item, dict):
            target = item.get("target") or {}
            target_file = target.get("file")
            target_line_val = target.get("line")
            target_line = None
            if target_line_val is not None and str(target_line_val).isdigit():
                target_line = int(target_line_val)
            
            contract = contract_from_mapping(item)
            target_func = target.get("func", target.get("function"))
            target_xpath = target.get("xpath", target.get("xpatch"))
            if target_func or target_xpath:
                new_tags = list(contract.tags)
                if target_func:
                    new_tags.append(f"target_func:{target_func}")
                if target_xpath:
                    new_tags.append(f"target_xpath:{target_xpath}")
                # Reconstruct contract with updated tags
                contract = Contract(
                    action=contract.action,
                    object=contract.object,
                    scope=contract.scope,
                    priority=contract.priority,
                    domain=contract.domain,
                    inputs=contract.inputs,
                    outputs=contract.outputs,
                    effects=contract.effects,
                    forbidden=contract.forbidden,
                    required=contract.required,
                    validators=contract.validators,
                    tags=tuple(new_tags),
                    algorithms=contract.algorithms,
                    relations=contract.relations,
                    contract_id=contract.contract_id,
                    meaning=contract.meaning,
                    raw=contract.raw,
                )
                
            file_path = str(target_file) if target_file else str(path)
            start_line = target_line if target_line is not None else index
            end_line = start_line
            records.append(
                ContractRecord(
                    contract=contract,
                    file_path=file_path,
                    start_line=start_line,
                    end_line=end_line,
                )
            )
    files = data.get("files", {}) or {}
    if isinstance(files, dict):
        for file_path, file_contracts in files.items():
            if not isinstance(file_contracts, list):
                continue
            for index, item in enumerate(file_contracts, start=1):
                if isinstance(item, dict):
                    records.append(
                        ContractRecord(
                            contract=contract_from_mapping(item),
                            file_path=str(file_path),
                            start_line=index,
                            end_line=index,
                        )
                    )
    return records


def create_sample_manifest() -> str:
    return """project:
  name: intract-sample

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
      - render.report
    validate:
      - required_intents
      - no_forbidden_effect
    meaning: "Project should analyze source code duplication and produce refactoring guidance."

files:
  src/scanner.py:
    - scope: file
      intent: scan:project_files
      priority: 1
      domain: scanner
      input: [ScanConfig]
      output: [file_list]
      effect: [read]
      forbid: [network]
      validate: [no_forbidden_effect]
      meaning: "Scanner should collect project files."
"""
