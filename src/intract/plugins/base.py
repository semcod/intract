from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from intract.core.artifact import Artifact, ArtifactKind, infer_artifact_kind, infer_language


@dataclass
class PluginResult:
    plugin: str
    ok: bool
    data: Any = None
    issues: list[dict[str, Any]] = field(default_factory=list)


@runtime_checkable
class ParserPlugin(Protocol):
    name: str
    version: str

    def supports(self, artifact: Artifact) -> bool:
        ...

    def parse(self, artifact: Artifact) -> PluginResult:
        ...


@runtime_checkable
class ValidatorPlugin(Protocol):
    name: str
    version: str

    def supports(self, artifact: Artifact) -> bool:
        ...

    def validate(self, artifact: Artifact, contracts: list[Any]) -> PluginResult:
        ...


@runtime_checkable
class ReporterPlugin(Protocol):
    name: str
    version: str
    extension: str

    def render(self, report: Any) -> str:
        ...


@runtime_checkable
class IntegrationPlugin(Protocol):
    name: str
    version: str

    def install(self, project_root: str | Path) -> PluginResult:
        ...


@dataclass
class PluginRegistry:
    parsers: list[ParserPlugin] = field(default_factory=list)
    validators: list[ValidatorPlugin] = field(default_factory=list)
    reporters: list[ReporterPlugin] = field(default_factory=list)
    integrations: list[IntegrationPlugin] = field(default_factory=list)

    def add_parser(self, plugin: ParserPlugin) -> None:
        self.parsers.append(plugin)

    def add_validator(self, plugin: ValidatorPlugin) -> None:
        self.validators.append(plugin)

    def add_reporter(self, plugin: ReporterPlugin) -> None:
        self.reporters.append(plugin)

    def add_integration(self, plugin: IntegrationPlugin) -> None:
        self.integrations.append(plugin)

    def parse_artifact(self, artifact: Artifact) -> list[Any]:
        contracts: list[Any] = []
        for parser in self.parsers:
            if parser.supports(artifact):
                result = parser.parse(artifact)
                if result.ok and result.data:
                    contracts.extend(result.data)
        return contracts

    def validate_artifact(self, artifact: Artifact, contracts: list[Any]) -> list[PluginResult]:
        results: list[PluginResult] = []
        for validator in self.validators:
            if validator.supports(artifact):
                results.append(validator.validate(artifact, contracts))
        return results


from pathlib import Path  # noqa: E402

__all__ = [
    "Artifact",
    "ArtifactKind",
    "ParserPlugin",
    "ValidatorPlugin",
    "ReporterPlugin",
    "IntegrationPlugin",
    "PluginRegistry",
    "PluginResult",
    "infer_artifact_kind",
    "infer_language",
]
