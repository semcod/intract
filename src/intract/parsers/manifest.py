from __future__ import annotations

from dataclasses import replace
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


def _target_mapping(item: dict[str, Any]) -> dict[str, Any]:
    target = item.get("target") or {}
    return target if isinstance(target, dict) else {}


def _target_line(target: dict[str, Any]) -> int | None:
    value = target.get("line")
    if value is not None and str(value).isdigit():
        return int(value)
    return None


def _target_tags(target: dict[str, Any]) -> tuple[str, ...]:
    tags = []
    target_func = target.get("func", target.get("function"))
    target_xpath = target.get("xpath", target.get("xpatch"))
    if target_func:
        tags.append(f"target_func:{target_func}")
    if target_xpath:
        tags.append(f"target_xpath:{target_xpath}")
    return tuple(tags)


def _with_target_tags(contract: Contract, target: dict[str, Any]) -> Contract:
    tags = _target_tags(target)
    if not tags:
        return contract
    return replace(contract, tags=contract.tags + tags)


def _top_level_contract_record(item: dict[str, Any], path: Path, index: int) -> ContractRecord:
    target = _target_mapping(item)
    target_line = _target_line(target)
    start_line = target_line if target_line is not None else index
    target_file = target.get("file")

    return ContractRecord(
        contract=_with_target_tags(contract_from_mapping(item), target),
        file_path=str(target_file) if target_file else str(path),
        start_line=start_line,
        end_line=start_line,
    )


def _top_level_contract_records(data: dict[str, Any], path: Path) -> list[ContractRecord]:
    return [
        _top_level_contract_record(item, path, index)
        for index, item in enumerate(data.get("contracts", []) or [], start=1)
        if isinstance(item, dict)
    ]


def _file_contract_records(files: Any) -> list[ContractRecord]:
    records: list[ContractRecord] = []
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


def load_manifest_records(path: Path) -> list[ContractRecord]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return []
    records = _top_level_contract_records(data, path)
    records.extend(_file_contract_records(data.get("files", {}) or {}))
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
