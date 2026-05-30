"""Plugin registry facade. Prefer `intract.plugins.manager` for discovery."""

from intract.plugins.base import PluginRegistry
from intract.plugins.manager import discover_plugins, load_builtin_plugins

__all__ = ["PluginRegistry", "discover_plugins", "load_builtin_plugins"]
