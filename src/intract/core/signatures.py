from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .models import ContractRecord, ContractSignature
from .normalizer import normalize_action, normalize_label, normalize_many, normalize_requirement


@dataclass(frozen=True)
class _NormalizedContract:
    action: str
    object_name: str
    domain: str
    inputs: frozenset[str]
    outputs: frozenset[str]
    effects: frozenset[str]
    forbidden: frozenset[str]
    required: frozenset[str]
    validators: frozenset[str]
    tags: frozenset[str]
    algorithms: frozenset[str]
    relations: frozenset[str]


def make_block_id(file_path: str, start_line: int, end_line: int, scope: str) -> str:
    raw = f"{file_path}:{start_line}:{end_line}:{scope}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _normalize_contract(record: ContractRecord) -> _NormalizedContract:
    contract = record.contract
    return _NormalizedContract(
        action=normalize_action(contract.action),
        object_name=normalize_label(contract.object),
        domain=normalize_label(contract.domain),
        inputs=frozenset(normalize_many(contract.inputs)),
        outputs=frozenset(normalize_many(contract.outputs)),
        effects=frozenset(normalize_many(contract.effects)),
        forbidden=frozenset(normalize_many(contract.forbidden)),
        required=frozenset(normalize_requirement(item) for item in contract.required),
        validators=frozenset(normalize_many(contract.validators)),
        tags=frozenset(normalize_many(contract.tags)),
        algorithms=frozenset(normalize_many(contract.algorithms)),
        relations=frozenset(normalize_many(contract.relations)),
    )


def _add_feature_values(features: set[str], prefix: str, values: frozenset[str]) -> None:
    features.update(f"{prefix}:{item}" for item in values)


def _signature_features(record: ContractRecord, normalized: _NormalizedContract) -> set[str]:
    contract = record.contract
    features: set[str] = {
        f"action:{normalized.action}",
        f"object:{normalized.object_name}",
        f"priority:{contract.priority}",
        f"scope:{contract.scope}",
    }
    if normalized.domain:
        features.add(f"domain:{normalized.domain}")

    _add_feature_values(features, "input", normalized.inputs)
    _add_feature_values(features, "output", normalized.outputs)
    _add_feature_values(features, "effect", normalized.effects)
    _add_feature_values(features, "forbid", normalized.forbidden)
    _add_feature_values(features, "require", normalized.required)
    _add_feature_values(features, "validate", normalized.validators)
    _add_feature_values(features, "tag", normalized.tags)
    _add_feature_values(features, "algorithm", normalized.algorithms)
    _add_feature_values(features, "relation", normalized.relations)
    return features


def _exact_hash(features: set[str]) -> str:
    return hashlib.sha256("\\n".join(sorted(features)).encode("utf-8")).hexdigest()


def _block_id(record: ContractRecord) -> str:
    contract = record.contract
    return contract.contract_id or make_block_id(
        record.file_path,
        record.start_line,
        record.end_line,
        contract.scope,
    )


def build_signature(record: ContractRecord) -> ContractSignature:
    contract = record.contract
    normalized = _normalize_contract(record)
    features = _signature_features(record, normalized)

    return ContractSignature(
        block_id=_block_id(record),
        file_path=record.file_path,
        start_line=record.start_line,
        end_line=record.end_line,
        scope=contract.scope,
        action=normalized.action,
        object=normalized.object_name,
        domain=normalized.domain,
        priority=contract.priority,
        inputs=normalized.inputs,
        outputs=normalized.outputs,
        effects=normalized.effects,
        forbidden=normalized.forbidden,
        required=frozenset(item for item in normalized.required if item),
        validators=normalized.validators,
        tags=normalized.tags,
        algorithms=normalized.algorithms,
        relations=normalized.relations,
        features=frozenset(features),
        exact_hash=_exact_hash(features),
        raw=contract.raw,
        meaning=contract.meaning,
    )


def build_signatures(records: list[ContractRecord]) -> list[ContractSignature]:
    return [build_signature(record) for record in records]
