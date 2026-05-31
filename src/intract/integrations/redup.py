from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Protocol, runtime_checkable

from intract.core.signatures import build_signature, build_signatures
from intract.duplicates import find_intent_pairs, pairs_to_intent_groups
from intract.parsers.inline import extract_contract_records_from_text
from intract.parsers.manifest import load_manifest_records


@runtime_checkable
class CodeBlockLike(Protocol):
    content: str
    file_path: str
    start_line: int
    end_line: int


@dataclass
class BlockAdapter:
    content: str
    file_path: str
    start_line: int = 1
    end_line: int = 1


def block_text(block: Any) -> str:
    return (
        getattr(block, "content", "")
        or getattr(block, "text", "")
        or getattr(block, "source", "")
        or ""
    )


def block_file_path(block: Any) -> str:
    return str(getattr(block, "file_path", "") or getattr(block, "path", "") or "")


def block_start_line(block: Any) -> int:
    return int(getattr(block, "start_line", None) or getattr(block, "start", 1) or 1)


def block_end_line(block: Any) -> int:
    start = block_start_line(block)
    return int(getattr(block, "end_line", None) or getattr(block, "end", start) or start)


def signatures_from_text(
    text: str,
    *,
    file_path: str,
    default_scope: str = "function",
):
    records = extract_contract_records_from_text(text, file_path=file_path, default_scope=default_scope)
    return build_signatures(records)


def signatures_from_blocks(
    blocks: Iterable[Any],
    *,
    default_scope: str = "function",
):
    signatures = []
    blocks_by_signature_id: dict[str, Any] = {}

    for block in blocks:
        text = block_text(block)
        file_path = block_file_path(block)
        if "@intract" not in text and "@ridl" not in text:
            continue

        records = extract_contract_records_from_text(
            text,
            file_path=file_path,
            default_scope=default_scope,
        )
        for record in records:
            signature = build_signature(record)
            signature = _with_block_lines(signature, block)
            signatures.append(signature)
            blocks_by_signature_id[signature.block_id] = block

    return signatures, blocks_by_signature_id


def signatures_from_manifest(manifest_path: str | Path):
    records = load_manifest_records(Path(manifest_path))
    return build_signatures(records)


def _with_block_lines(signature, block: Any):
    from dataclasses import replace

    return replace(
        signature,
        start_line=block_start_line(block),
        end_line=block_end_line(block),
    )


def find_intent_duplicate_groups(
    blocks: Iterable[Any] | None = None,
    *,
    signatures: list | None = None,
    manifest_path: str | Path | None = None,
    threshold: float = 0.84,
) -> list[dict[str, Any]]:
    """Return intent duplicate groups for reDUP or other consumers."""
    all_signatures: list = []
    blocks_by_signature_id: dict[str, Any] = {}

    if blocks is not None:
        block_sigs, block_map = signatures_from_blocks(blocks)
        all_signatures.extend(block_sigs)
        blocks_by_signature_id.update(block_map)

    if signatures:
        all_signatures.extend(signatures)

    if manifest_path:
        all_signatures.extend(signatures_from_manifest(manifest_path))

    if not all_signatures:
        return []

    signatures_by_id = {signature.block_id: signature for signature in all_signatures}
    pairs = find_intent_pairs(all_signatures, threshold=threshold)
    groups = pairs_to_intent_groups(pairs, signatures_by_id)

    payload = []
    for group in groups:
        item = group.to_dict()
        item["evidence"] = {
            "engine": "intract",
            "duplicate_type": "intent",
            "contracts": [signatures_by_id[cid].key for cid in group.contract_ids],
        }
        payload.append(item)
    return payload


@dataclass
class RedupScanResult:
    signatures: list = field(default_factory=list)
    groups: list[dict[str, Any]] = field(default_factory=list)
    threshold: float = 0.84

    def to_dict(self) -> dict[str, Any]:
        return {
            "threshold": self.threshold,
            "signatures": len(self.signatures),
            "groups": self.groups,
        }


@dataclass(frozen=True)
class RedupPolicyResult:
    should_fail: bool
    reasons: tuple[str, ...]
    warnings: tuple[str, ...]
    validation_status: str
    intent_duplicate_groups: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "should_fail": self.should_fail,
            "reasons": list(self.reasons),
            "warnings": list(self.warnings),
            "validation_status": self.validation_status,
            "intent_duplicate_groups": self.intent_duplicate_groups,
        }


def parse_policy_tokens(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [part.strip() for part in str(value).split(",") if part.strip()]


def validate_for_redup(
    root: str | Path,
    *,
    manifest: str | Path | None = None,
    intent_groups: list[dict[str, Any]] | None = None,
    fail_on: list[str] | None = None,
    warn_on: list[str] | None = None,
) -> RedupPolicyResult:
    """Apply Intract project policy for reDUP consumers (scan gates / CLI)."""
    from intract.config import load_config
    from intract.graph import build_graph
    from intract.policy import decide_policy
    from intract.project import validate_project

    project_root = Path(root)
    config = load_config(project_root)
    manifest_path = Path(manifest) if manifest else None
    if manifest_path is None and (project_root / config.manifest).exists():
        manifest_path = project_root / config.manifest

    report = validate_project(project_root, manifest_path=manifest_path)
    resolved_fail_on = fail_on or list(config.fail_on)
    resolved_warn_on = warn_on or list(config.warn_on)

    graph = None
    if manifest_path and "missing_required_p1" in resolved_fail_on:
        graph = build_graph(project_root, manifest=manifest_path)

    decision = decide_policy(
        report,
        fail_on=resolved_fail_on,
        warn_on=resolved_warn_on,
        graph=graph,
        manifest_path=manifest_path,
    )

    reasons = list(decision.reasons)
    warnings = list(decision.warnings)
    duplicate_groups = intent_groups or []

    if "intent_duplicate" in resolved_fail_on and duplicate_groups:
        for group in duplicate_groups:
            group_id = group.get("group_id", "unknown")
            contracts = group.get("evidence", {}).get("contracts", [])
            label = ",".join(contracts) if contracts else group_id
            reasons.append(f"intent_duplicate: {label}")

    if "intent_duplicate" in resolved_warn_on and duplicate_groups:
        warnings.append(f"intent_duplicate: {len(duplicate_groups)} group(s)")

    return RedupPolicyResult(
        should_fail=bool(reasons),
        reasons=tuple(reasons),
        warnings=tuple(warnings),
        validation_status=report.status.value,
        intent_duplicate_groups=len(duplicate_groups),
    )


def scan_blocks_for_intent_duplicates(
    blocks: Iterable[Any],
    *,
    manifest_path: str | Path | None = None,
    threshold: float = 0.84,
) -> RedupScanResult:
    signatures, _ = signatures_from_blocks(blocks)
    if manifest_path:
        signatures = signatures + signatures_from_manifest(manifest_path)
    groups = find_intent_duplicate_groups(signatures=signatures, threshold=threshold)
    return RedupScanResult(signatures=signatures, groups=groups, threshold=threshold)
