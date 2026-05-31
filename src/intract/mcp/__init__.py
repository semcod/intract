"""MCP server package for Intract."""

from intract.mcp.handlers import TOOL_HANDLERS
from intract.mcp.schemas import TOOL_SCHEMA_INTRACT
from intract.mcp.server import (
    handle_initialize,
    handle_request,
    handle_tools_call,
    handle_tools_list,
    run_server,
)

__all__ = [
    "TOOL_SCHEMA_INTRACT",
    "TOOL_HANDLERS",
    "handle_initialize",
    "handle_tools_list",
    "handle_tools_call",
    "handle_request",
    "run_server",
]
