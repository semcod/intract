from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class IntentPair:
    left_id: str
    right_id: str
    score: float
    reason: dict[str, object]


def bucket_signatures(signatures):
    buckets: dict[str, list] = defaultdict(list)
    for signature in signatures:
        buckets[signature.action].append(signature)
    return buckets


def find_intent_pairs(signatures, threshold: float = 0.84) -> list[IntentPair]:
    from .scoring import score_similarity

    pairs: list[IntentPair] = []

    for bucket in bucket_signatures(signatures).values():
        for left, right in combinations(bucket, 2):
            if left.block_id == right.block_id:
                continue

            if left.exact_hash == right.exact_hash:
                pairs.append(
                    IntentPair(
                        left_id=left.block_id,
                        right_id=right.block_id,
                        score=1.0,
                        reason={"exact_contract_hash": True},
                    )
                )
                continue

            score, reason = score_similarity(left, right)
            if score >= threshold:
                pairs.append(
                    IntentPair(
                        left_id=left.block_id,
                        right_id=right.block_id,
                        score=score,
                        reason=reason,
                    )
                )

    return pairs
