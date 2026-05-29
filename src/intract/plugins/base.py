from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol, runtime_checkable


class ArtifactKind(str, Enum):
    SOURCE_CODE = "source_code"
    OPENAPI = "openapi"
    ASYNCAPI = "asyncapi"
    DOCKERFILE = "dockerfile"
    COMPOSE = "compose"
    KUBERNETES = "kubernetes"
    TERRAFORM = "terraform"
    GITHUB_ACTIONS = "github_actions"
    GITLAB_CI = "gitlab_ci"
    MARKDOWN = "markdown"
    MANIFEST = "manifest"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Artifact:
    path: str
    kind: ArtifactKind
    content: str
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_path(cls, path: str | Path, *, kind: ArtifactKind | None = None) -> "Artifact":
        p = Path(path)
        content = p.read_text(encoding="utf-8")
        return cls(
            path=str(p),
            kind=kind or infer_artifact_kind(str(p), content),
            content=content,
            language=infer_language(str(p)),
        )


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


def infer_language(path: str) -> str | None:
    suffix = Path(path).suffix.lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".jsx": "javascript",
        ".cs": "csharp",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
        ".php": "php",
        ".rb": "ruby",
        ".sh": "shell",
        ".sql": "sql",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
        ".md": "markdown",
    }.get(suffix)


def infer_artifact_kind(path: str, content: str = "") -> ArtifactKind:
    name = Path(path).name.lower()
    suffix = Path(path).suffix.lower()

    if name == "dockerfile" or name.startswith("dockerfile."):
        return ArtifactKind.DOCKERFILE
    if name in {"docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"}:
        return ArtifactKind.COMPOSE
    if name in {"intent.yaml", "intract.yaml", ".intract.yaml"}:
        return ArtifactKind.MANIFEST
    if ".github/workflows" in path.replace("\\", "/"):
        return ArtifactKind.GITHUB_ACTIONS
    if name == ".gitlab-ci.yml":
        return ArtifactKind.GITLAB_CI
    if suffix in {".tf", ".tfvars"}:
        return ArtifactKind.TERRAFORM
    if suffix in {".yaml", ".yml"} and "apiVersion:" in content and "kind:" in content:
        return ArtifactKind.KUBERNETES
    if suffix in {".yaml", ".yml", ".json"} and "openapi" in content[:500].lower():
        return ArtifactKind.OPENAPI
    if suffix in {".yaml", ".yml", ".json"} and "asyncapi" in content[:500].lower():
        return ArtifactKind.ASYNCAPI
    if suffix == ".md":
        return ArtifactKind.MARKDOWN
    if suffix in {".py", ".js", ".ts", ".tsx", ".jsx", ".cs", ".java", ".go", ".rs", ".php", ".rb", ".sh", ".sql"}:
        return ArtifactKind.SOURCE_CODE
    return ArtifactKind.UNKNOWN
