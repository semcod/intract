"""Read/write intract.yaml and merge cinema policy ledger entries."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml

from intract.parsers.inline import parse_contract_line

ManifestTarget = Literal["project", "capsule", "both"]


@dataclass
class ManifestApplyResult:
    manifest_path: str
    target: str = "project"
    added: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    dry_run: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "manifest_path": self.manifest_path,
            "target": self.target,
            "added": list(self.added),
            "skipped": list(self.skipped),
            "dry_run": self.dry_run,
        }


@dataclass
class ManifestApplyBatchResult:
    results: list[ManifestApplyResult] = field(default_factory=list)
    dry_run: bool = False

    @property
    def added_total(self) -> int:
        return sum(len(item.added) for item in self.results)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dry_run": self.dry_run,
            "added_total": self.added_total,
            "results": [item.to_dict() for item in self.results],
        }


def load_manifest_document(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": "intract.v1", "contracts": []}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid manifest document: {path}")
    data.setdefault("version", "intract.v1")
    data.setdefault("contracts", [])
    if not isinstance(data["contracts"], list):
        data["contracts"] = []
    return data


def write_manifest_document(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def contract_line_to_manifest_entry(line: str) -> dict[str, Any] | None:
    """Parse a single @intract.v1 line into an intract.yaml contract mapping."""
    normalized = line.strip()
    if not normalized.startswith("@intract"):
        normalized = f"@intract.v1 {normalized}"

    contract = parse_contract_line(normalized, default_scope="ui")
    if contract is None:
        return None

    intent = f"{contract.action}:{contract.object}" if contract.object else contract.action
    entry: dict[str, Any] = {
        "id": contract.contract_id or intent.replace(":", "."),
        "scope": contract.scope,
        "intent": intent,
        "priority": contract.priority,
        "domain": contract.domain or "general",
    }
    if contract.inputs:
        entry["input"] = list(contract.inputs)
    if contract.outputs:
        entry["output"] = list(contract.outputs)
    if contract.effects:
        entry["effect"] = list(contract.effects)
    if contract.forbidden:
        entry["forbid"] = list(contract.forbidden)
    if contract.required:
        entry["require"] = list(contract.required)
    if contract.validators:
        entry["validate"] = list(contract.validators)
    if contract.meaning:
        entry["meaning"] = contract.meaning
    return entry


def load_policy_ledger(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    data = json.loads(text)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def resolve_manifest_paths(
    *,
    workspace_root: Path,
    capsule_name: str,
    target: ManifestTarget = "project",
    project_manifest: Path | None = None,
    capsule_manifest: Path | None = None,
) -> list[tuple[str, Path]]:
    """Return (target_label, manifest_path) pairs for project/capsule/both."""
    root = workspace_root.resolve()
    project_path = project_manifest or (root / "intract.yaml")
    capsule_path = capsule_manifest or (root / ".nexu" / "capsules" / capsule_name / "intract.yaml")

    if target == "project":
        return [("project", project_path)]
    if target == "capsule":
        return [("capsule", capsule_path)]
    return [("project", project_path), ("capsule", capsule_path)]


def apply_ledger_to_manifest(
    manifest_path: Path,
    ledger_path: Path,
    *,
    dry_run: bool = False,
    only_evolved: bool = True,
    target: str = "project",
) -> ManifestApplyResult:
    """Append proposed contracts from cinema ledger into intract.yaml (by id, no duplicates)."""
    manifest = load_manifest_document(manifest_path)
    existing_ids = {
        str(item.get("id", "")).strip()
        for item in manifest.get("contracts", [])
        if isinstance(item, dict) and item.get("id")
    }

    result = ManifestApplyResult(
        manifest_path=str(manifest_path),
        dry_run=dry_run,
        target=target,
    )

    for entry in load_policy_ledger(ledger_path):
        if only_evolved and "evolved_by_llm" not in str(entry.get("status", "")):
            continue
        for proposal in entry.get("proposed_contracts", []) or []:
            if not isinstance(proposal, dict):
                continue
            line = str(proposal.get("line", "")).strip()
            manifest_entry = contract_line_to_manifest_entry(line)
            if manifest_entry is None:
                result.skipped.append(line or str(proposal.get("id", "")))
                continue
            contract_id = str(manifest_entry.get("id", "")).strip()
            if not contract_id:
                result.skipped.append(line)
                continue
            if contract_id in existing_ids:
                result.skipped.append(contract_id)
                continue
            manifest["contracts"].append(manifest_entry)
            existing_ids.add(contract_id)
            result.added.append(contract_id)

    if result.added and not dry_run:
        write_manifest_document(manifest_path, manifest)

    return result


def apply_ledger_to_manifests(
    *,
    workspace_root: Path,
    capsule_name: str,
    ledger_path: Path,
    target: ManifestTarget = "both",
    dry_run: bool = False,
    only_evolved: bool = True,
    project_manifest: Path | None = None,
    capsule_manifest: Path | None = None,
) -> ManifestApplyBatchResult:
    """Apply ledger entries to one or more manifest files (shared id dedupe per file)."""
    batch = ManifestApplyBatchResult(dry_run=dry_run)
    for label, manifest_path in resolve_manifest_paths(
        workspace_root=workspace_root,
        capsule_name=capsule_name,
        target=target,
        project_manifest=project_manifest,
        capsule_manifest=capsule_manifest,
    ):
        batch.results.append(
            apply_ledger_to_manifest(
                manifest_path,
                ledger_path,
                dry_run=dry_run,
                only_evolved=only_evolved,
                target=label,
            )
        )
    return batch
