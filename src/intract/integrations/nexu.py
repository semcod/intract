from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from intract.parsers.inline import clean_comment_line, parse_contract_line


@dataclass
class IntentContract:
    raw: str
    contract_id: str = ""
    scope: str = "block"
    intent: str = ""
    priority: int = 3
    domain: str = "general"
    input: list[str] = field(default_factory=list)
    output: list[str] = field(default_factory=list)
    effect: list[str] = field(default_factory=list)
    forbid: list[str] = field(default_factory=list)
    require: list[str] = field(default_factory=list)
    validate: list[str] = field(default_factory=list)
    meaning: str = ""
    source: str = ""
    line: int = 0
    target_file: str = ""
    target_function: str = ""
    target_line: int | None = None
    target_xpath: str = ""

    @property
    def key(self) -> str:
        return self.contract_id or self.intent or self.raw


def format_intract_v1_line(contract: IntentContract) -> str:
    meaning = contract.meaning.replace('"', "'") if contract.meaning else ""
    meaning_part = f' meaning:"{meaning}"' if meaning else ""
    return (
        f"@intract.v1 id:{contract.contract_id} scope:{contract.scope} "
        f"intent:{contract.intent} priority:{contract.priority} domain:{contract.domain}"
        f"{meaning_part}"
    )


def parse_intract_line(
    line: str,
    *,
    source: str = "",
    line_number: int = 0,
) -> IntentContract | None:
    cleaned = clean_comment_line(line)
    if "@intract.v1" not in cleaned and "@intract" not in cleaned:
        return None

    contract = parse_contract_line(line)
    if contract is None:
        return None

    intent = f"{contract.action}:{contract.object}" if contract.object else contract.action
    target_function = ""
    target_xpath = ""
    for tag in contract.tags:
        if tag.startswith("target_func:"):
            target_function = tag.split(":", 1)[1]
        elif tag.startswith("target_xpath:"):
            target_xpath = tag.split(":", 1)[1]

    return IntentContract(
        raw=line.strip(),
        contract_id=contract.contract_id,
        scope=contract.scope,
        intent=intent,
        priority=contract.priority,
        domain=contract.domain or "general",
        input=list(contract.inputs),
        output=list(contract.outputs),
        effect=list(contract.effects),
        forbid=list(contract.forbidden),
        require=list(contract.required),
        validate=list(contract.validators),
        meaning=contract.meaning,
        source=source,
        line=line_number,
        target_function=target_function,
        target_xpath=target_xpath,
    )


def scan_contracts_in_text(text: str, *, source: str = "") -> list[IntentContract]:
    contracts = []
    for index, line in enumerate(text.splitlines(), start=1):
        contract = parse_intract_line(line, source=source, line_number=index)
        if contract is not None:
            contracts.append(contract)
    return contracts


def scan_contracts_in_file(path: Path, root: Path | None = None) -> list[IntentContract]:
    source = path.relative_to(root).as_posix() if root else path.as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    return scan_contracts_in_text(text, source=source)


def _contract_items(data) -> list[dict]:
    return [item for item in data.get("contracts", []) or [] if isinstance(item, dict)]


def _list_field(item: dict, key: str) -> list[str]:
    return list(item.get(key, []) or [])


def _base_intent_contract(
    item: dict,
    path: Path,
    *,
    raw_prefix: str,
    default_scope: str,
) -> IntentContract:
    intent = str(item.get("intent", ""))
    return IntentContract(
        raw=f"{raw_prefix}:{item.get('id', intent)}",
        contract_id=str(item.get("id", "")),
        scope=str(item.get("scope", default_scope)),
        intent=intent,
        priority=int(item.get("priority", 3) or 3),
        domain=str(item.get("domain", "general")),
        input=_list_field(item, "input"),
        output=_list_field(item, "output"),
        effect=_list_field(item, "effect"),
        forbid=_list_field(item, "forbid"),
        require=_list_field(item, "require"),
        validate=_list_field(item, "validate"),
        meaning=str(item.get("meaning", "")),
        source=str(path),
        line=0,
    )


def read_manifest_contracts(path: Path) -> list[IntentContract]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [
        _base_intent_contract(item, path, raw_prefix="manifest", default_scope="project")
        for item in _contract_items(data)
    ]


def _read_yaml_mapping(path: Path) -> dict | None:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _toon_target(item: dict) -> dict:
    target = item.get("target") or {}
    return target if isinstance(target, dict) else {}


def _target_line_value(target: dict) -> int | None:
    value = target.get("line")
    return int(value) if value is not None else None


def _toon_intent_contract(item: dict, path: Path) -> IntentContract:
    target = _toon_target(item)
    contract = _base_intent_contract(item, path, raw_prefix="toon", default_scope="toon")
    contract.target_file = str(target.get("file") or "")
    contract.target_function = str(target.get("function") or "")
    contract.target_line = _target_line_value(target)
    contract.target_xpath = str(target.get("xpath") or target.get("xpatch") or "")
    return contract


def read_toon_manifest_contracts(path: Path) -> list[IntentContract]:
    if not path.exists():
        return []
    data = _read_yaml_mapping(path)
    if data is None:
        return []
    return [_toon_intent_contract(item, path) for item in _contract_items(data)]
