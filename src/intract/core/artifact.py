from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


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


DOCKERFILE_NAMES = {"dockerfile"}
COMPOSE_NAMES = {"docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"}
MANIFEST_NAMES = {"intent.yaml", "intract.yaml", ".intract.yaml"}
STRUCTURED_SPEC_SUFFIXES = {".yaml", ".yml", ".json"}
TERRAFORM_SUFFIXES = {".tf", ".tfvars"}
SOURCE_CODE_SUFFIXES = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".cs",
    ".java",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".sh",
    ".sql",
}


@dataclass(frozen=True)
class Artifact:
    path: str
    kind: ArtifactKind
    content: str
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_path(cls, path: str | Path, *, kind: ArtifactKind | None = None) -> Artifact:
        p = Path(path)
        content = p.read_text(encoding="utf-8")
        return cls(
            path=str(p),
            kind=kind or infer_artifact_kind(str(p), content),
            content=content,
            language=infer_language(str(p)),
        )


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


def _kind_from_filename(path: str, name: str, suffix: str) -> ArtifactKind | None:
    normalized_path = path.replace("\\", "/")
    if name in DOCKERFILE_NAMES or name.startswith("dockerfile."):
        return ArtifactKind.DOCKERFILE
    if name in COMPOSE_NAMES:
        return ArtifactKind.COMPOSE
    if name in MANIFEST_NAMES:
        return ArtifactKind.MANIFEST
    if ".github/workflows" in normalized_path:
        return ArtifactKind.GITHUB_ACTIONS
    if name == ".gitlab-ci.yml":
        return ArtifactKind.GITLAB_CI
    if suffix in TERRAFORM_SUFFIXES:
        return ArtifactKind.TERRAFORM
    if suffix == ".md":
        return ArtifactKind.MARKDOWN
    if suffix in SOURCE_CODE_SUFFIXES:
        return ArtifactKind.SOURCE_CODE
    return None


def _kind_from_structured_content(suffix: str, content: str) -> ArtifactKind | None:
    if suffix not in STRUCTURED_SPEC_SUFFIXES:
        return None
    preview = content[:500].lower()
    if suffix in {".yaml", ".yml"} and "apiVersion:" in content and "kind:" in content:
        return ArtifactKind.KUBERNETES
    if "openapi" in preview:
        return ArtifactKind.OPENAPI
    if "asyncapi" in preview:
        return ArtifactKind.ASYNCAPI
    return None


def infer_artifact_kind(path: str, content: str = "") -> ArtifactKind:
    name = Path(path).name.lower()
    suffix = Path(path).suffix.lower()

    filename_kind = _kind_from_filename(path, name, suffix)
    if filename_kind is not None:
        return filename_kind

    content_kind = _kind_from_structured_content(suffix, content)
    return content_kind or ArtifactKind.UNKNOWN
