from __future__ import annotations

from pathlib import Path
from typing import Any

from intract.project import validate_project

from .analyzer import analyze_source_units
from .assigner import suggest_contracts_for_fragments
from .context import EngineConfig
from .drift import detect_drift, load_state, save_state
from .scanner import collect_source_units


def scan_suggest_and_validate(config: EngineConfig) -> dict[str, Any]:
    units = collect_source_units(config.root, max_file_size=config.max_file_size)
    fragments = analyze_source_units(units)
    suggestions = suggest_contracts_for_fragments(fragments)

    previous = load_state(config.state_path)
    drift = detect_drift(previous, fragments)
    save_state(config.state_path, fragments)

    report = validate_project(config.root, manifest_path=config.manifest if config.manifest else None)

    return {
        "files": len(units),
        "fragments": len(fragments),
        "suggestions": [s.__dict__ for s in suggestions],
        "drift": [d.__dict__ for d in drift],
        "validation": report.to_dict(),
    }
