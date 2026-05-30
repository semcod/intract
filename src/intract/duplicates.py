from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
from pathlib import Path

from .project import load_project_sources, extract_signatures_from_sources


@dataclass(frozen=True)
class DuplicateContract:
    left_file: str
    right_file: str
    left_contract: str
    right_contract: str
    score: float
    reason: dict[str, float | str]

    def to_dict(self):
        return asdict(self)


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def object_similarity(left: str, right: str) -> float:
    if left == right:
        return 1.0
    return jaccard(set(left.split("_")), set(right.split("_")))


def score_similarity(left, right) -> tuple[float, dict[str, float | str]]:
    action = 1.0 if left.action == right.action else 0.0
    obj = object_similarity(left.object, right.object)
    domain = 1.0 if (not left.domain and not right.domain) or left.domain == right.domain else 0.0
    inputs = jaccard(set(left.inputs), set(right.inputs))
    outputs = jaccard(set(left.outputs), set(right.outputs))
    effects = jaccard(set(left.effects), set(right.effects))
    tags = jaccard(set(left.tags), set(right.tags))
    score = 0.28 * action + 0.26 * obj + 0.14 * domain + 0.10 * inputs + 0.10 * outputs + 0.06 * effects + 0.06 * tags
    return round(score, 4), {
        "action": action,
        "object": obj,
        "domain": domain,
        "inputs": inputs,
        "outputs": outputs,
        "effects": effects,
        "tags": tags,
    }


def find_duplicate_contracts(root: str | Path = ".", threshold: float = 0.84) -> list[DuplicateContract]:
    sources = load_project_sources(Path(root))
    signatures = extract_signatures_from_sources(sources)
    duplicates: list[DuplicateContract] = []

    for left, right in combinations(signatures, 2):
        if left.block_id == right.block_id:
            continue
        if left.file_path == right.file_path and left.start_line == right.start_line:
            continue
        score, reason = score_similarity(left, right)
        if score >= threshold:
            duplicates.append(
                DuplicateContract(
                    left_file=left.file_path,
                    right_file=right.file_path,
                    left_contract=left.key,
                    right_contract=right.key,
                    score=score,
                    reason=reason,
                )
            )
    return duplicates
