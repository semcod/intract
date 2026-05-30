"""Backward-compatible re-exports. Prefer `intract.validators.artifacts`."""

from intract.validators.artifacts import ArtifactValidationReport, validate_artifact

__all__ = ["ArtifactValidationReport", "validate_artifact"]
