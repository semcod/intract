from __future__ import annotations

import hashlib

from .models import ContractRecord, ContractSignature
from .normalizer import normalize_action, normalize_label, normalize_many, normalize_requirement


def make_block_id(file_path: str, start_line: int, end_line: int, scope: str) -> str:
    raw = f"{file_path}:{start_line}:{end_line}:{scope}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def build_signature(record: ContractRecord) -> ContractSignature:
    contract = record.contract
    action = normalize_action(contract.action)
    object_name = normalize_label(contract.object)
    domain = normalize_label(contract.domain)
    inputs = frozenset(normalize_many(contract.inputs))
    outputs = frozenset(normalize_many(contract.outputs))
    effects = frozenset(normalize_many(contract.effects))
    forbidden = frozenset(normalize_many(contract.forbidden))
    required = frozenset(normalize_requirement(item) for item in contract.required)
    validators = frozenset(normalize_many(contract.validators))
    tags = frozenset(normalize_many(contract.tags))
    algorithms = frozenset(normalize_many(contract.algorithms))
    relations = frozenset(normalize_many(contract.relations))

    features: set[str] = {
        f"action:{action}",
        f"object:{object_name}",
        f"priority:{contract.priority}",
        f"scope:{contract.scope}",
    }
    if domain:
        features.add(f"domain:{domain}")

    features.update(f"input:{item}" for item in inputs)
    features.update(f"output:{item}" for item in outputs)
    features.update(f"effect:{item}" for item in effects)
    features.update(f"forbid:{item}" for item in forbidden)
    features.update(f"require:{item}" for item in required)
    features.update(f"validate:{item}" for item in validators)
    features.update(f"tag:{item}" for item in tags)
    features.update(f"algorithm:{item}" for item in algorithms)
    features.update(f"relation:{item}" for item in relations)

    exact_hash = hashlib.sha256("\\n".join(sorted(features)).encode("utf-8")).hexdigest()
    block_id = contract.contract_id or make_block_id(record.file_path, record.start_line, record.end_line, contract.scope)

    return ContractSignature(
        block_id=block_id,
        file_path=record.file_path,
        start_line=record.start_line,
        end_line=record.end_line,
        scope=contract.scope,
        action=action,
        object=object_name,
        domain=domain,
        priority=contract.priority,
        inputs=inputs,
        outputs=outputs,
        effects=effects,
        forbidden=forbidden,
        required=frozenset(item for item in required if item),
        validators=validators,
        tags=tags,
        algorithms=algorithms,
        relations=relations,
        features=frozenset(features),
        exact_hash=exact_hash,
        raw=contract.raw,
        meaning=contract.meaning,
    )


def build_signatures(records: list[ContractRecord]) -> list[ContractSignature]:
    return [build_signature(record) for record in records]
