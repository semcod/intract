from __future__ import annotations

from importlib.metadata import entry_points

from .base import PluginRegistry


ENTRYPOINT_GROUPS = {
    "parsers": "intract.parsers",
    "validators": "intract.validators",
    "reporters": "intract.reporters",
    "integrations": "intract.integrations",
}


def _register_unique(registry: PluginRegistry, kind: str, plugin) -> None:
    collection = getattr(registry, kind)
    names = {item.name for item in collection}
    if plugin.name in names:
        return
    collection.append(plugin)


def load_builtin_plugins() -> PluginRegistry:
    from .builtins import (
        ArtifactStructureValidatorPlugin,
        BasicContractValidatorPlugin,
        InlineContractParserPlugin,
        JsonReporterPlugin,
        ManifestParserPlugin,
        OpenAPIParserPlugin,
    )

    registry = PluginRegistry()
    _register_unique(registry, "parsers", InlineContractParserPlugin())
    _register_unique(registry, "parsers", ManifestParserPlugin())
    _register_unique(registry, "parsers", OpenAPIParserPlugin())
    _register_unique(registry, "validators", BasicContractValidatorPlugin())
    _register_unique(registry, "validators", ArtifactStructureValidatorPlugin())
    _register_unique(registry, "reporters", JsonReporterPlugin())
    return registry


def discover_plugins(*, include_builtins: bool = True) -> PluginRegistry:
    registry = load_builtin_plugins() if include_builtins else PluginRegistry()

    eps = entry_points()

    for ep in eps.select(group=ENTRYPOINT_GROUPS["parsers"]):
        _register_unique(registry, "parsers", ep.load()())

    for ep in eps.select(group=ENTRYPOINT_GROUPS["validators"]):
        _register_unique(registry, "validators", ep.load()())

    for ep in eps.select(group=ENTRYPOINT_GROUPS["reporters"]):
        _register_unique(registry, "reporters", ep.load()())

    for ep in eps.select(group=ENTRYPOINT_GROUPS["integrations"]):
        _register_unique(registry, "integrations", ep.load()())

    return registry
