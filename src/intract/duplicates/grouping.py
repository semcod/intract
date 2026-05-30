from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

from .matcher import IntentPair, find_intent_pairs


@dataclass(frozen=True)
class DuplicateContract:
    left_file: str
    right_file: str
    left_contract: str
    right_contract: str
    score: float
    reason: dict[str, float | str | bool]

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class IntentDuplicateGroup:
    group_id: str
    contract_ids: tuple[str, ...]
    fragments: tuple[dict[str, object], ...]
    similarity: float
    metadata: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "group_id": self.group_id,
            "contract_ids": list(self.contract_ids),
            "fragments": list(self.fragments),
            "similarity": self.similarity,
            "metadata": self.metadata,
        }


def union_find_groups(pairs: list[IntentPair]) -> list[set[str]]:
    parent: dict[str, str] = {}

    def find(node: str) -> str:
        parent.setdefault(node, node)
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(left: str, right: str) -> None:
        root_left = find(left)
        root_right = find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    for pair in pairs:
        union(pair.left_id, pair.right_id)

    groups: dict[str, set[str]] = defaultdict(set)
    for node in parent:
        groups[find(node)].add(node)

    return [group for group in groups.values() if len(group) > 1]


def pairs_to_duplicate_contracts(pairs: list[IntentPair], signatures_by_id: dict) -> list[DuplicateContract]:
    duplicates: list[DuplicateContract] = []
    seen: set[tuple[str, str]] = set()

    for pair in pairs:
        left = signatures_by_id[pair.left_id]
        right = signatures_by_id[pair.right_id]
        key = tuple(sorted([pair.left_id, pair.right_id]))
        if key in seen:
            continue
        seen.add(key)
        duplicates.append(
            DuplicateContract(
                left_file=left.file_path,
                right_file=right.file_path,
                left_contract=left.key,
                right_contract=right.key,
                score=pair.score,
                reason=pair.reason,
            )
        )
    return duplicates


def pairs_to_intent_groups(
    pairs: list[IntentPair],
    signatures_by_id: dict,
) -> list[IntentDuplicateGroup]:
    pair_scores = {frozenset([pair.left_id, pair.right_id]): pair for pair in pairs}
    groups: list[IntentDuplicateGroup] = []

    for index, ids in enumerate(union_find_groups(pairs), start=1):
        fragments = []
        for signature_id in sorted(ids):
            signature = signatures_by_id[signature_id]
            fragments.append(
                {
                    "file_path": signature.file_path,
                    "start_line": signature.start_line,
                    "end_line": signature.end_line,
                    "contract": signature.key,
                    "block_id": signature.block_id,
                }
            )

        scores = [pair.score for key, pair in pair_scores.items() if key.issubset(ids)]
        avg_score = sum(scores) / max(1, len(scores))

        groups.append(
            IntentDuplicateGroup(
                group_id=f"intent_{index:04d}",
                contract_ids=tuple(sorted(ids)),
                fragments=tuple(fragments),
                similarity=round(avg_score, 4),
                metadata={
                    "engine": "intract",
                    "scores": scores,
                    "duplicate_type": "intent",
                },
            )
        )

    return groups


def find_duplicate_contracts(root: str | Path = ".", threshold: float = 0.84) -> list[DuplicateContract]:
    from intract.project import extract_signatures_from_sources, load_project_sources

    sources = load_project_sources(Path(root))
    signatures = extract_signatures_from_sources(sources)
    signatures_by_id = {signature.block_id: signature for signature in signatures}
    pairs = find_intent_pairs(signatures, threshold=threshold)
    return pairs_to_duplicate_contracts(pairs, signatures_by_id)
