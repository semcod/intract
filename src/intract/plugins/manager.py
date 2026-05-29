from __future__ import annotations

from importlib.metadata import entry_points

from .base import PluginRegistry


ENTRYPOINT_GROUPS = {
    "parsers": "intract.parsers",
    "validators": "intract.validators",
    "reporters": "intract.reporters",
    "integrations": "intract.integrations",
}


def load_builtin_plugins() -> PluginRegistry:
    from .builtins import (
        BasicContractValidatorPlugin,
        InlineContractParserPlugin,
        JsonReporterPlugin,
        ManifestParserPlugin,
    )

    registry = PluginRegistry()
    registry.add_parser(InlineContractParserPlugin())
    registry.add_parser(ManifestParserPlugin())
    registry.add_validator(BasicContractValidatorPlugin())
    registry.add_reporter(JsonReporterPlugin())
    return registry


def discover_plugins(*, include_builtins: bool = True) -> PluginRegistry:
    registry = load_builtin_plugins() if include_builtins else PluginRegistry()

    eps = entry_points()

    for ep in eps.select(group=ENTRYPOINT_GROUPS["parsers"]):
        registry.add_parser(ep.load()())

    for ep in eps.select(group=ENTRYPOINT_GROUPS["validators"]):
        registry.add_validator(ep.load()())

    for ep in eps.select(group=ENTRYPOINT_GROUPS["reporters"]):
        registry.add_reporter(ep.load()())

    for ep in eps.select(group=ENTRYPOINT_GROUPS["integrations"]):
        registry.add_integration(ep.load()())

    return registry
