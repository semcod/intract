from __future__ import annotations

import re
import shlex
from collections.abc import Callable
from dataclasses import replace

from intract.core.models import VALID_SCOPES, Contract, ContractRecord

CONTRACT_MARKERS = ("@intract.v1", "@intract", "@ridl.v1")
_URI_VALUE_RE = re.compile(
    r"""uri\s*=\s*(?:"([^"]+)"|'([^']+)'|(intract://\S+|toon://\S+))""",
    re.IGNORECASE,
)


def clean_comment_line(line: str) -> str:
    text = line.strip()
    if text.startswith("<!--"):
        text = text[4:].strip()
    if text.endswith("-->"):
        text = text[:-3].strip()
    if text.startswith("/*"):
        text = text[2:].strip()
    if text.endswith("*/"):
        text = text[:-2].strip()
    while text.startswith("*"):
        text = text[1:].strip()
    # Rust-style attribute wrapper: #[intract.v1 ...] (before generic # comment strip)
    if text.startswith("#["):
        text = text[2:].strip()
        if text.endswith("]"):
            text = text[:-1].strip()
    else:
        for prefix in ("#", "//", "--", ";"):
            if text.startswith(prefix):
                return text[len(prefix):].strip()
    if text.startswith("intract") and not text.startswith("@intract"):
        text = "@" + text
    return text


def split_csv(value: str | None) -> tuple[str, ...]:
    if value is None:
        return ()
    text = str(value).strip()
    if not text or text.lower() in {"none", "null", "empty", "-"}:
        return ()
    return tuple(part.strip() for part in text.split(",") if part.strip())


def parse_priority(token: str) -> int | None:
    text = token.strip().lower()
    if text.startswith("!p") and text[2:].isdigit():
        raw = text[2:]
    elif text.startswith("p") and text[1:].isdigit():
        raw = text[1:]
    else:
        return None
    return max(1, min(5, int(raw)))


def parse_key_value(token: str) -> tuple[str, str] | None:
    match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)(:|=)(.+)$", token)
    if not match:
        return None
    return match.group(1).lower(), match.group(3).strip()


def marker_payload(line: str) -> str | None:
    cleaned = clean_comment_line(line)
    for marker in CONTRACT_MARKERS:
        if marker in cleaned:
            return cleaned.split(marker, 1)[1].strip()
    return None


def extract_intract_uri(payload: str) -> str | None:
    """Extract an intract:// URI from uri=... in an @intract.v1 payload."""
    text = payload.strip()
    match = _URI_VALUE_RE.search(text)
    if match:
        return (match.group(1) or match.group(2) or match.group(3)).strip()
    try:
        for token in shlex.split(text, comments=False, posix=True):
            kv = parse_key_value(token)
            if kv and kv[0] == "uri":
                value = kv[1].strip().strip("\"'")
                if value.startswith(("intract://", "toon://")):
                    return value
    except ValueError:
        pass
    return None


def _parse_uri_contract(payload: str, default_scope: str) -> Contract | None:
    from intract.parsers.toon import parse_toon_uri_line

    record = parse_toon_uri_line(payload)
    if record is None:
        return None
    contract = record.contract
    contract = replace(contract, raw=payload)
    if contract.scope == "block" and default_scope != "block":
        contract = replace(contract, scope=default_scope)
    if not contract.action or not contract.object:
        return None
    return contract


class _ContractParserState:
    def __init__(self, default_scope: str):
        self.action = ""
        self.object_name = ""
        self.priority = 3
        self.scope = default_scope
        self.default_scope = default_scope
        self.domain = ""
        self.inputs: list[str] = []
        self.outputs: list[str] = []
        self.effects: list[str] = []
        self.forbidden: list[str] = []
        self.required: list[str] = []
        self.validators: list[str] = []
        self.tags: list[str] = []
        self.algorithms: list[str] = []
        self.relations: list[str] = []
        self.contract_id = ""
        self.meaning = ""
        self.positional: list[str] = []


def _set_intent(_key: str, value: str, state: _ContractParserState) -> None:
    if ":" in value:
        state.action, state.object_name = value.split(":", 1)
    else:
        state.positional.append(value)


def _set_action(_key: str, value: str, state: _ContractParserState) -> None:
    state.action = value


def _set_object(_key: str, value: str, state: _ContractParserState) -> None:
    state.object_name = value


def _set_scope(_key: str, value: str, state: _ContractParserState) -> None:
    state.scope = value if value in VALID_SCOPES else state.default_scope


def _set_priority(_key: str, value: str, state: _ContractParserState) -> None:
    if value.isdigit():
        state.priority = max(1, min(5, int(value)))


def _set_domain(_key: str, value: str, state: _ContractParserState) -> None:
    state.domain = value


def _set_contract_id(_key: str, value: str, state: _ContractParserState) -> None:
    state.contract_id = value


def _set_meaning(_key: str, value: str, state: _ContractParserState) -> None:
    state.meaning = value


def _extend_list(attribute: str) -> Callable[[str, str, _ContractParserState], None]:
    def apply(_key: str, value: str, state: _ContractParserState) -> None:
        getattr(state, attribute).extend(split_csv(value))

    return apply


def _add_relation(key: str, value: str, state: _ContractParserState) -> None:
    state.relations.extend(f"{key}:{item}" for item in split_csv(value))


def _add_unknown_tag(key: str, value: str, state: _ContractParserState) -> None:
    state.tags.append(f"{key}:{value}")


_KEY_VALUE_HANDLERS: dict[str, Callable[[str, str, _ContractParserState], None]] = {
    "intent": _set_intent,
    "action": _set_action,
    "act": _set_action,
    "object": _set_object,
    "obj": _set_object,
    "target": _set_object,
    "scope": _set_scope,
    "priority": _set_priority,
    "domain": _set_domain,
    "input": _extend_list("inputs"),
    "inputs": _extend_list("inputs"),
    "in": _extend_list("inputs"),
    "output": _extend_list("outputs"),
    "outputs": _extend_list("outputs"),
    "out": _extend_list("outputs"),
    "effect": _extend_list("effects"),
    "effects": _extend_list("effects"),
    "fx": _extend_list("effects"),
    "forbid": _extend_list("forbidden"),
    "forbidden": _extend_list("forbidden"),
    "no": _extend_list("forbidden"),
    "require": _extend_list("required"),
    "requires": _extend_list("required"),
    "req": _extend_list("required"),
    "validate": _extend_list("validators"),
    "validators": _extend_list("validators"),
    "rules": _extend_list("validators"),
    "tag": _extend_list("tags"),
    "tags": _extend_list("tags"),
    "algorithm": _extend_list("algorithms"),
    "algorithms": _extend_list("algorithms"),
    "alg": _extend_list("algorithms"),
    "algo": _extend_list("algorithms"),
    "relation": _add_relation,
    "relations": _add_relation,
    "rel": _add_relation,
    "uses": _add_relation,
    "partof": _add_relation,
    "before": _add_relation,
    "after": _add_relation,
    "id": _set_contract_id,
    "contract_id": _set_contract_id,
    "meaning": _set_meaning,
}


def _parse_special_token(token: str, state: _ContractParserState) -> bool:
    priority_value = parse_priority(token)
    if priority_value is not None:
        state.priority = priority_value
        return True
    if token.startswith("@") and len(token) > 1:
        state.domain = token[1:]
        return True
    if token.startswith("#") and len(token) > 1:
        state.tags.append(token[1:])
        return True
    if token.startswith("~") and len(token) > 1:
        state.algorithms.append(token[1:])
        return True
    return False


def _apply_key_value_pair(key: str, value: str, state: _ContractParserState) -> None:
    handler = _KEY_VALUE_HANDLERS.get(key, _add_unknown_tag)
    handler(key, value, state)


def _resolve_action_object(state: _ContractParserState) -> None:
    if not state.action and state.positional:
        state.action = state.positional[0]
    if not state.object_name and len(state.positional) > 1:
        state.object_name = "_".join(state.positional[1:])


def parse_contract_line(line: str, *, default_scope: str = "block") -> Contract | None:
    payload = marker_payload(line)
    if payload is None or not payload:
        return None

    uri = extract_intract_uri(payload)
    if uri:
        return _parse_uri_contract(uri, default_scope)

    try:
        tokens = shlex.split(payload, comments=False, posix=True)
    except ValueError:
        return None

    state = _ContractParserState(default_scope)

    for token in tokens:
        if _parse_special_token(token, state):
            continue

        kv = parse_key_value(token)
        if kv is None:
            if ":" in token and not state.action and not state.object_name:
                state.action, state.object_name = token.split(":", 1)
            else:
                state.positional.append(token)
            continue

        key, value = kv
        _apply_key_value_pair(key, value, state)

    _resolve_action_object(state)
    if not state.action or not state.object_name:
        return None

    return Contract(
        action=state.action,
        object=state.object_name,
        scope=state.scope,
        priority=state.priority,
        domain=state.domain,
        inputs=tuple(state.inputs),
        outputs=tuple(state.outputs),
        effects=tuple(state.effects),
        forbidden=tuple(state.forbidden),
        required=tuple(state.required),
        validators=tuple(state.validators),
        tags=tuple(state.tags),
        algorithms=tuple(state.algorithms),
        relations=tuple(state.relations),
        contract_id=state.contract_id,
        meaning=state.meaning,
        raw=payload,
    )


def extract_contract_records_from_text(
    source: str,
    *,
    file_path: str,
    default_scope: str = "block",
) -> list[ContractRecord]:
    records: list[ContractRecord] = []
    for index, line in enumerate(source.splitlines(), start=1):
        contract = parse_contract_line(line, default_scope=default_scope)
        if contract is None:
            continue
        records.append(
            ContractRecord(
                contract=contract,
                file_path=file_path,
                start_line=index,
                end_line=index,
            )
        )
    return records
