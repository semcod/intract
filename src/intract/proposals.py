"""Propose @intract.v1 contract lines from structured change feedback (UI/cinema deltas)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProposedContract:
    id: str
    kind: str
    element: str
    line: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "element": self.element,
            "line": self.line,
        }


def _ui_contract_line(
    *,
    contract_id: str,
    intent: str,
    domain: str,
    meaning: str,
    effect: str = "ui_change",
) -> str:
    return (
        f"@intract.v1 id:{contract_id} scope:ui intent:{intent} priority:3 "
        f"domain:{domain} effect:{effect} forbid:destructive_write,secret_leak "
        f"require:human_review validate:no_forbidden_effect "
        f'meaning:"{meaning}"'
    )


def propose_ui_delta_contracts(
    *,
    stage: int,
    keep: list[str] | None = None,
    delete: list[str] | None = None,
    capsule: str = "capsule",
    domain: str = "ui",
) -> list[ProposedContract]:
    """Build canonical @intract.v1 lines for spatial KEEP/DELETE feedback."""
    keep = [str(item).strip() for item in (keep or []) if str(item).strip()]
    delete = [str(item).strip() for item in (delete or []) if str(item).strip()]
    proposals: list[ProposedContract] = []

    for element_id in delete:
        contract_id = f"cinema.{capsule}.S{stage}.ui.remove.{element_id}"
        proposals.append(
            ProposedContract(
                id=contract_id,
                kind="delete",
                element=element_id,
                line=_ui_contract_line(
                    contract_id=contract_id,
                    intent=f"ui:remove:{element_id}",
                    domain=domain,
                    meaning=f"Cinema S{stage} removed #{element_id}",
                ),
            )
        )

    for element_id in keep:
        contract_id = f"cinema.{capsule}.S{stage}.ui.keep.{element_id}"
        proposals.append(
            ProposedContract(
                id=contract_id,
                kind="keep",
                element=element_id,
                line=_ui_contract_line(
                    contract_id=contract_id,
                    intent=f"ui:keep:{element_id}",
                    domain=domain,
                    effect="read",
                    meaning=f"Cinema S{stage} preserved #{element_id}",
                ),
            )
        )

    return proposals


def propose_ui_delta_contract_dicts(
    *,
    stage: int,
    keep: list[str] | None = None,
    delete: list[str] | None = None,
    capsule: str = "capsule",
    domain: str = "ui",
) -> list[dict[str, Any]]:
    return [item.to_dict() for item in propose_ui_delta_contracts(
        stage=stage, keep=keep, delete=delete, capsule=capsule, domain=domain
    )]
