from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import Artifact, ArtifactKind, PluginResult
from intract.parser import extract_contract_records_from_text
from intract.signature import build_signatures
from intract.validation import validate_contract_against_source


class InlineContractParserPlugin:
    name = "inline"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return "@intract" in artifact.content or "@ridl" in artifact.content

    def parse(self, artifact: Artifact) -> PluginResult:
        records = extract_contract_records_from_text(
            artifact.content,
            file_path=artifact.path,
            default_scope="block",
        )
        return PluginResult(plugin=self.name, ok=True, data=build_signatures(records))


class ManifestParserPlugin:
    name = "manifest"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return artifact.kind == ArtifactKind.MANIFEST

    def parse(self, artifact: Artifact) -> PluginResult:
        from intract.yaml_manifest import load_manifest_records

        records = load_manifest_records(Path(artifact.path))
        return PluginResult(plugin=self.name, ok=True, data=build_signatures(records))


class BasicContractValidatorPlugin:
    name = "basic"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return artifact.kind in {
            ArtifactKind.SOURCE_CODE,
            ArtifactKind.DOCKERFILE,
            ArtifactKind.COMPOSE,
            ArtifactKind.KUBERNETES,
            ArtifactKind.GITHUB_ACTIONS,
            ArtifactKind.GITLAB_CI,
            ArtifactKind.MANIFEST,
            ArtifactKind.MARKDOWN,
            ArtifactKind.UNKNOWN,
        }

    def validate(self, artifact: Artifact, contracts: list[Any]) -> PluginResult:
        results = []
        for contract in contracts:
            results.append(validate_contract_against_source(contract, artifact.content).to_dict())

        ok = not any(item["status"] == "violation" for item in results)
        return PluginResult(plugin=self.name, ok=ok, data=results)


class JsonReporterPlugin:
    name = "json"
    version = "0.1.0"
    extension = "json"

    def render(self, report: Any) -> str:
        if hasattr(report, "to_dict"):
            report = report.to_dict()
        return json.dumps(report, indent=2, ensure_ascii=False)
