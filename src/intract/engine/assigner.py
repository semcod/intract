from __future__ import annotations

import re

from .context import ContractSuggestion, LogicalFragment


ACTION_HINTS = [
    ("validate", {"validate", "check", "verify", "ensure", "authorize", "guard", "can_", "is_", "has_"}),
    ("parse", {"parse", "read", "load", "extract"}),
    ("build", {"build", "create", "make", "generate", "construct"}),
    ("detect", {"detect", "find", "search", "match"}),
    ("render", {"render", "format", "write", "export", "serialize"}),
    ("scan", {"scan", "collect", "walk"}),
    ("transform", {"transform", "normalize", "convert", "map"}),
]


def _split_name(name: str) -> list[str]:
    name = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", name)
    return [p for p in re.split(r"[_\\W]+", name.lower()) if p]


def _infer_action(name: str, text: str) -> tuple[str, float]:
    lower = name.lower()
    words = set(_split_name(name))

    for action, hints in ACTION_HINTS:
        if action in words:
            return action, 0.85
        if any(lower.startswith(hint) for hint in hints):
            return action, 0.8
        if words & hints:
            return action, 0.75

    if "return" in text and ("==" in text or " is " in text or " in " in text):
        return "validate", 0.55
    return "implement", 0.45


def _infer_object(name: str, action: str) -> str:
    parts = _split_name(name)
    filtered = [p for p in parts if p not in {action, "get", "set", "run", "do", "handle"}]
    return "_".join(filtered) if filtered else "logic"


def _infer_effects(text: str) -> tuple[list[str], list[str]]:
    effects: list[str] = []
    forbid = ["secret_leak"]

    if any(x in text for x in ["requests.", "fetch(", "httpx.", "HttpClient"]):
        effects.append("network")
    else:
        forbid.append("network")

    if any(x in text for x in [".write(", "write_text(", "File.Write", "INSERT ", "UPDATE ", "DELETE "]):
        effects.append("write")

    if any(x in text for x in [".read(", "read_text(", "open(", "Directory.GetFiles", "SELECT "]):
        effects.append("read")

    if not effects:
        effects.append("none")

    return effects, forbid


def suggest_contract_for_fragment(fragment: LogicalFragment) -> ContractSuggestion:
    action, confidence = _infer_action(fragment.name, fragment.text)
    obj = _infer_object(fragment.name, action)
    effects, forbid = _infer_effects(fragment.text)

    validate = ["input_presence", "return_value", "no_forbidden_effect"]
    if action in {"render", "build", "parse", "detect", "scan"}:
        validate = ["return_value", "no_forbidden_effect"]

    contract = (
        f"# @intract.v1 scope:{fragment.kind} "
        f"intent:{action}:{obj} "
        f"priority:3 "
        f"domain:{fragment.language or 'code'} "
        f"effect:{','.join(effects)} "
        f"forbid:{','.join(forbid)} "
        f"validate:{','.join(validate)} "
        f'meaning:"auto-suggested contract for {fragment.kind} {fragment.name}"'
    )

    return ContractSuggestion(
        fragment_id=fragment.id,
        file_path=fragment.file_path,
        line=fragment.start_line,
        contract_line=contract,
        confidence=confidence,
        reason=f"Inferred from {fragment.kind} name '{fragment.name}' and lightweight source heuristics.",
        metadata={
            "kind": fragment.kind,
            "name": fragment.name,
            "language": fragment.language,
        },
    )


def suggest_contracts_for_fragments(
    fragments: list[LogicalFragment],
    *,
    min_confidence: float = 0.5,
) -> list[ContractSuggestion]:
    suggestions = [suggest_contract_for_fragment(fragment) for fragment in fragments]
    return [s for s in suggestions if s.confidence >= min_confidence]
