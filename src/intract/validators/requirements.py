from __future__ import annotations

from intract.core.models import ContractSignature


def validate_required_contracts(
    required_signature: ContractSignature,
    observed_signatures: list[ContractSignature],
) -> tuple[list[str], list[str]]:
    observed_keys = {item.key for item in observed_signatures}
    satisfied = sorted(item for item in required_signature.required if item in observed_keys)
    missing = sorted(item for item in required_signature.required if item not in observed_keys)
    return satisfied, missing
