from pathlib import Path

from intract.core.signatures import build_signatures
from intract.parsers.inline import extract_contract_records_from_text
from intract.parsers.openapi import parse_openapi_text
from intract.validators.artifacts import validate_artifact
from intract.validators.engine import validate_contract_against_source

from .base import Artifact, ArtifactKind, PluginResult


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


class OpenAPIParserPlugin:
    name = "openapi"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return artifact.kind == ArtifactKind.OPENAPI

    def parse(self, artifact: Artifact) -> PluginResult:
        records = parse_openapi_text(artifact.content, file_path=artifact.path)
        return PluginResult(plugin=self.name, ok=True, data=build_signatures(records))


class ManifestParserPlugin:
    name = "manifest"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return artifact.kind == ArtifactKind.MANIFEST

    def parse(self, artifact: Artifact) -> PluginResult:
        from pathlib import Path

        from intract.parsers.manifest import load_manifest_records

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

    def validate(self, artifact: Artifact, contracts: list) -> PluginResult:
        results = []
        for contract in contracts:
            results.append(validate_contract_against_source(contract, artifact.content).to_dict())

        ok = not any(item["status"] == "violation" for item in results)
        return PluginResult(plugin=self.name, ok=ok, data=results)


class ArtifactStructureValidatorPlugin:
    name = "artifact"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return artifact.kind in {
            ArtifactKind.DOCKERFILE,
            ArtifactKind.GITHUB_ACTIONS,
            ArtifactKind.KUBERNETES,
            ArtifactKind.OPENAPI,
        }

    def validate(self, artifact: Artifact, contracts: list) -> PluginResult:
        report = validate_artifact(artifact.path)
        results = [item.to_dict() for item in report.results]
        ok = not any(item["status"] == "violation" for item in results)
        return PluginResult(plugin=self.name, ok=ok, data=results)


class JsonReporterPlugin:
    name = "json"
    version = "0.1.0"
    extension = "json"

    def render(self, report) -> str:
        import json

        if hasattr(report, "to_dict"):
            report = report.to_dict()
        return json.dumps(report, indent=2, ensure_ascii=False)
