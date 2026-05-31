"""Validate artifacts with proposed @intract.v1 lines (cinema / LLM flows)."""

from __future__ import annotations

from typing import Any

from intract.integrations.vallm import validate_proposal


def validate_artifact_with_proposals(
    artifact: str,
    proposals: list[dict[str, Any]],
    *,
    filename: str = "artifact.html",
) -> dict[str, Any]:
    """
    Validate an HTML/code artifact together with proposed contract lines.

    Proposed lines are injected as HTML comments so inline parsers can see them.
    """
    header_lines = []
    for proposal in proposals:
        line = str(proposal.get("line", "")).strip()
        if line:
            header_lines.append(f"<!-- {line} -->")
    bundle = "\n".join(header_lines) + "\n" + artifact
    mapped = validate_proposal(bundle, filename=filename)
    return mapped.to_dict()
