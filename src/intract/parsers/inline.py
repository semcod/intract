from __future__ import annotations

import re
import shlex

from intract.core.models import VALID_SCOPES, Contract, ContractRecord

CONTRACT_MARKERS = ("@intract.v1", "@intract", "@ridl.v1")


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
    for prefix in ("#", "//", "--", ";"):
        if text.startswith(prefix):
            return text[len(prefix):].strip()
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


def parse_contract_line(line: str, *, default_scope: str = "block") -> Contract | None:
    payload = marker_payload(line)
    if payload is None or not payload:
        return None

    try:
        tokens = shlex.split(payload, comments=False, posix=True)
    except ValueError:
        return None
    action = ""
    object_name = ""
    priority = 3
    scope = default_scope
    domain = ""
    inputs: list[str] = []
    outputs: list[str] = []
    effects: list[str] = []
    forbidden: list[str] = []
    required: list[str] = []
    validators: list[str] = []
    tags: list[str] = []
    algorithms: list[str] = []
    relations: list[str] = []
    contract_id = ""
    meaning = ""
    positional: list[str] = []

    for token in tokens:
        priority_value = parse_priority(token)
        if priority_value is not None:
            priority = priority_value
            continue
        if token.startswith("@") and len(token) > 1:
            domain = token[1:]
            continue
        if token.startswith("#") and len(token) > 1:
            tags.append(token[1:])
            continue
        if token.startswith("~") and len(token) > 1:
            algorithms.append(token[1:])
            continue

        kv = parse_key_value(token)
        if kv is None:
            if ":" in token and not action and not object_name:
                action, object_name = token.split(":", 1)
            else:
                positional.append(token)
            continue

        key, value = kv
        if key == "intent":
            if ":" in value:
                action, object_name = value.split(":", 1)
            else:
                positional.append(value)
        elif key in {"action", "act"}:
            action = value
        elif key in {"object", "obj", "target"}:
            object_name = value
        elif key == "scope":
            scope = value if value in VALID_SCOPES else default_scope
        elif key == "priority":
            if value.isdigit():
                priority = max(1, min(5, int(value)))
        elif key == "domain":
            domain = value
        elif key in {"input", "inputs", "in"}:
            inputs.extend(split_csv(value))
        elif key in {"output", "outputs", "out"}:
            outputs.extend(split_csv(value))
        elif key in {"effect", "effects", "fx"}:
            effects.extend(split_csv(value))
        elif key in {"forbid", "forbidden", "no"}:
            forbidden.extend(split_csv(value))
        elif key in {"require", "requires", "req"}:
            required.extend(split_csv(value))
        elif key in {"validate", "validators", "rules"}:
            validators.extend(split_csv(value))
        elif key in {"tag", "tags"}:
            tags.extend(split_csv(value))
        elif key in {"algorithm", "algorithms", "alg", "algo"}:
            algorithms.extend(split_csv(value))
        elif key in {"relation", "relations", "rel", "uses", "partof", "before", "after"}:
            relations.extend(f"{key}:{item}" for item in split_csv(value))
        elif key in {"id", "contract_id"}:
            contract_id = value
        elif key == "meaning":
            meaning = value
        else:
            tags.append(f"{key}:{value}")

    if not action and positional:
        action = positional[0]
    if not object_name and len(positional) > 1:
        object_name = "_".join(positional[1:])
    if not action or not object_name:
        return None

    return Contract(
        action=action,
        object=object_name,
        scope=scope,
        priority=priority,
        domain=domain,
        inputs=tuple(inputs),
        outputs=tuple(outputs),
        effects=tuple(effects),
        forbidden=tuple(forbidden),
        required=tuple(required),
        validators=tuple(validators),
        tags=tuple(tags),
        algorithms=tuple(algorithms),
        relations=tuple(relations),
        contract_id=contract_id,
        meaning=meaning,
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
