from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class IntractConfig:
    manifest: str = "intract.yaml"
    mode: str = "project"
    fail_on: list[str] = field(default_factory=lambda: ["violation", "invalid_manifest"])
    warn_on: list[str] = field(default_factory=lambda: ["partial", "unknown"])
    ignore: list[str] = field(default_factory=list)
    min_contract_coverage: float = 0.0
    min_changed_coverage: float = 0.0
    plugins: list[str] = field(default_factory=lambda: ["inline", "manifest", "basic"])

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "IntractConfig":
        tool = data.get("tool", {}).get("intract", data.get("intract", data))
        plugins = tool.get("plugins", {})
        enabled_plugins = plugins.get("enabled", tool.get("plugins", cls().plugins))
        return cls(
            manifest=str(tool.get("manifest", "intract.yaml")),
            mode=str(tool.get("mode", "project")),
            fail_on=list(tool.get("fail_on", ["violation", "invalid_manifest"])),
            warn_on=list(tool.get("warn_on", ["partial", "unknown"])),
            ignore=list(tool.get("ignore", [])),
            min_contract_coverage=float(tool.get("min_contract_coverage", 0.0)),
            min_changed_coverage=float(tool.get("min_changed_coverage", 0.0)),
            plugins=list(enabled_plugins or []),
        )


def load_config(root: str | Path = ".") -> IntractConfig:
    root = Path(root)
    for name in ("intract.config.yaml", ".intract.yaml", "intract.yaml"):
        path = root / name
        if path.exists():
            try:
                raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                if "contracts" in raw or "project" in raw:
                    # This is a manifest, not a tool config.
                    continue
                return IntractConfig.from_mapping(raw)
            except Exception:
                continue

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        try:
            if hasattr(__import__("tomllib"), "loads"):
                import tomllib
                raw = tomllib.loads(pyproject.read_text(encoding="utf-8"))
                tool_data = raw.get("tool", {}).get("intract")
                if tool_data:
                    return IntractConfig.from_mapping({"tool": {"intract": tool_data}})
        except Exception:
            pass

    return IntractConfig()
