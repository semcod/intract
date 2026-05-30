from __future__ import annotations

import re
from collections.abc import Iterable


ACTION_SYNONYMS = {
    "validate": {"validate", "check", "verify", "ensure", "authorize", "guard"},
    "build": {"build", "create", "make", "construct", "generate", "assemble"},
    "parse": {"parse", "read", "load", "deserialize", "extract"},
    "compare": {"compare", "diff", "match"},
    "scan": {"scan", "collect", "discover", "find"},
    "render": {"render", "format", "serialize", "export"},
    "persist": {"persist", "save", "write", "store"},
    "transform": {"transform", "normalize", "convert", "map"},
    "detect": {"detect", "identify", "recognize", "classify"},
    "calculate": {"calculate", "compute", "count", "measure", "estimate"},
    "implement": {"implement", "provide", "expose"},
    "analyze": {"analyze", "inspect", "evaluate"},
    "group": {"group", "cluster", "merge"},
    "plan": {"plan", "suggest", "recommend"},
}

STOP_WORDS = {"a", "an", "the", "to", "from", "of", "for", "before", "after", "with", "without", "and", "or", "by"}


def normalize_label(value: str | None) -> str:
    if not value:
        return ""
    text = str(value).strip()
    text = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", text)
    text = text.replace("-", "_").replace("/", "_").replace(".", "_").replace(":", "_")
    text = re.sub(r"[^A-Za-z0-9_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_").lower()
    parts = []
    for part in text.split("_"):
        if not part or part in STOP_WORDS:
            continue
        if len(part) > 4 and part.endswith("s"):
            part = part[:-1]
        parts.append(part)
    return "_".join(parts)


def normalize_action(action: str | None) -> str:
    normalized = normalize_label(action)
    for canonical, variants in ACTION_SYNONYMS.items():
        if normalized in {normalize_label(item) for item in variants}:
            return canonical
    return normalized


def normalize_many(values: Iterable[str] | None) -> tuple[str, ...]:
    if not values:
        return ()
    normalized = {normalize_label(value) for value in values if normalize_label(value)}
    return tuple(sorted(normalized))


def normalize_requirement(value: str) -> str:
    value = str(value).strip().replace(":", ".")
    parts = [part for part in value.split(".") if part]
    if len(parts) == 1:
        return normalize_label(parts[0])
    action = normalize_action(parts[0])
    obj = normalize_label("_".join(parts[1:]))
    if not action or not obj:
        return normalize_label(value)
    return f"{action}.{obj}"
