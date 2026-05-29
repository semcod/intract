from __future__ import annotations

from intract.plugins import Artifact, ArtifactKind, PluginResult


class ExampleParserPlugin:
    name = "example_parser"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return artifact.kind == ArtifactKind.SOURCE_CODE and "@example.intent" in artifact.content

    def parse(self, artifact: Artifact) -> PluginResult:
        # Return Intract ContractSignature objects in a real plugin.
        return PluginResult(plugin=self.name, ok=True, data=[])


class ExampleValidatorPlugin:
    name = "example_validator"
    version = "0.1.0"

    def supports(self, artifact: Artifact) -> bool:
        return artifact.kind == ArtifactKind.SOURCE_CODE

    def validate(self, artifact: Artifact, contracts: list[object]) -> PluginResult:
        return PluginResult(plugin=self.name, ok=True, data={"checked": len(contracts)})
