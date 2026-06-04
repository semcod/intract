from __future__ import annotations

import urllib.parse
from pathlib import Path

from intract.core.models import Contract, ContractRecord


def _parse_action_object_from_intent(intent: str, contract_id: str) -> tuple[str, str]:
    if ":" in intent:
        return intent.split(":", 1)
    elif "." in intent:
        return intent.split(".", 1)
    elif "-" in intent:
        return intent.split("-", 1)
    elif intent:
        return intent, "unknown"
    elif contract_id:
        if "-" in contract_id:
            return contract_id.split("-", 1)
        elif "_" in contract_id:
            return contract_id.split("_", 1)
        else:
            return "contract", contract_id
    return "", "unknown"


def _extract_file_path(parsed: urllib.parse.ParseResult) -> str:
    if parsed.scheme in {"intract", "toon"}:
        return parsed.netloc + parsed.path
    return parsed.path


def _get_first(params: dict[str, list[str]], key: str, default: str = "") -> str:
    return params.get(key, [default])[0]


def _get_list(params: dict[str, list[str]], key: str) -> tuple[str, ...]:
    vals = params.get(key, [])
    out = []
    for value in vals:
        out.extend(part.strip() for part in value.split(",") if part.strip())
    return tuple(out)


def _get_first_alias(params: dict[str, list[str]], *keys: str) -> str:
    for key in keys:
        value = _get_first(params, key)
        if value:
            return value
    return ""


def _get_list_alias(params: dict[str, list[str]], *keys: str) -> tuple[str, ...]:
    for key in keys:
        values = _get_list(params, key)
        if values:
            return values
    return ()


def _build_tags(func_val: str, xpath_val: str, fragment_params: dict[str, list[str]]) -> list[str]:
    tags = list(_get_list_alias(fragment_params, "tag", "tags"))
    if func_val:
        tags.append(f"target_func:{func_val}")
    if xpath_val:
        tags.append(f"target_xpath:{xpath_val}")
    return tags


def _start_line(line_val: str) -> int:
    return int(line_val) if line_val.isdigit() else 1


def _priority(fragment_params: dict[str, list[str]]) -> int:
    raw = _get_first(fragment_params, "priority", "3")
    return int(raw) if raw.isdigit() else 3


def _action_object(fragment_params: dict[str, list[str]]) -> tuple[str, str]:
    contract_id = _get_first_alias(fragment_params, "id", "contract_id")
    intent = _get_first(fragment_params, "intent")
    action = _get_first(fragment_params, "action")
    object_name = _get_first_alias(fragment_params, "object", "obj")
    if action and object_name:
        return action, object_name
    return _parse_action_object_from_intent(intent, contract_id)


def _contract_from_uri(
    text: str,
    fragment_params: dict[str, list[str]],
    *,
    func_val: str,
    xpath_val: str,
) -> Contract:
    action, object_name = _action_object(fragment_params)
    return Contract(
        action=action.strip(),
        object=object_name.strip(),
        scope=_get_first(fragment_params, "scope", "block"),
        priority=_priority(fragment_params),
        domain=_get_first(fragment_params, "domain"),
        inputs=_get_list_alias(fragment_params, "input", "inputs", "in"),
        outputs=_get_list_alias(fragment_params, "output", "outputs", "out"),
        effects=_get_list_alias(fragment_params, "effect", "effects", "fx"),
        forbidden=_get_list_alias(fragment_params, "forbid", "forbidden", "no"),
        required=_get_list_alias(fragment_params, "require", "requires", "req"),
        validators=_get_list_alias(fragment_params, "validate", "validators", "rules"),
        tags=tuple(_build_tags(func_val, xpath_val, fragment_params)),
        algorithms=_get_list_alias(fragment_params, "algorithm", "algorithms", "alg"),
        relations=_get_list_alias(fragment_params, "relation", "relations", "rel"),
        contract_id=_get_first_alias(fragment_params, "id", "contract_id"),
        meaning=_get_first(fragment_params, "meaning"),
        raw=text,
    )


def parse_toon_uri_line(line: str, line_num: int = 1) -> ContractRecord | None:
    """Parse a single flat Toon URI line into a ContractRecord.
    
    Format:
      intract://<file_path>?func=<func>&line=<line>&xpath=<xpath>#id=<id>&intent=<intent>&forbid=<forbid>
    """
    text = line.strip()
    if not text or text.startswith("#"):
        return None
        
    parsed = urllib.parse.urlparse(text)
    file_path = _extract_file_path(parsed)
        
    query = urllib.parse.parse_qs(parsed.query)
    func_val = _get_first_alias(query, "func", "function")
    line_val = _get_first(query, "line")
    xpath_val = _get_first_alias(query, "xpath", "xpatch")

    start_line = _start_line(line_val)
    end_line = start_line
    fragment_params = urllib.parse.parse_qs(parsed.fragment)
    contract = _contract_from_uri(
        text,
        fragment_params,
        func_val=func_val,
        xpath_val=xpath_val,
    )

    return ContractRecord(
        contract=contract,
        file_path=file_path.strip(),
        start_line=start_line,
        end_line=end_line,
        owner="toon_uri",
    )


def load_toon_records(path: Path) -> list[ContractRecord]:
    """Load flat line-by-line URI contracts from a Toon file."""
    if not path.exists():
        return []
    records = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []
    for idx, line in enumerate(lines, start=1):
        record = parse_toon_uri_line(line, line_num=idx)
        if record is not None:
            records.append(record)
    return records
