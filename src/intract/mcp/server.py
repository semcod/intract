"""MCP JSON-RPC server for Intract."""

from __future__ import annotations

import json
import sys
from typing import Any

from intract import __version__
from intract.mcp.handlers import TOOL_HANDLERS
from intract.mcp.schemas import TOOL_SCHEMA_INTRACT

_PROTOCOL_VERSION = "2024-11-05"
_NOTIFICATIONS = frozenset({"notifications/initialized", "notifications/cancelled"})


def handle_initialize(request_id: Any, params: dict[str, Any] | None = None) -> dict[str, Any]:
    client_version = (params or {}).get("protocolVersion", _PROTOCOL_VERSION)
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": client_version,
            "serverInfo": {"name": "intract", "version": __version__},
            "capabilities": {"tools": {}},
        },
    }


def handle_tools_list(request_id: Any) -> dict[str, Any]:
    tools = [
        {
            "name": schema["name"],
            "description": schema["description"],
            "inputSchema": schema["inputSchema"],
        }
        for schema in TOOL_SCHEMA_INTRACT.values()
    ]
    return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools}}


def handle_tools_call(request_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    tool_name = params.get("name")
    arguments = params.get("arguments", {}) or {}

    if tool_name not in TOOL_HANDLERS:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"},
        }

    try:
        result = TOOL_HANDLERS[tool_name](arguments)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": result}]},
        }
    except Exception as exc:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32603, "message": f"Tool execution failed: {exc}"},
        }


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    method = request.get("method", "")
    params = request.get("params", {}) or {}
    request_id = request.get("id")

    if method in _NOTIFICATIONS:
        return {}
    if method == "initialize":
        return handle_initialize(request_id, params)
    if method == "tools/list":
        return handle_tools_list(request_id)
    if method == "tools/call":
        return handle_tools_call(request_id, params)

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Method '{method}' not found"},
    }


def run_server() -> None:
    print("Intract MCP Server started", file=sys.stderr)
    print(f"Available tools: {', '.join(sorted(TOOL_SCHEMA_INTRACT.keys()))}", file=sys.stderr)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response:
                print(json.dumps(response), flush=True)
        except json.JSONDecodeError as exc:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "error": {"code": -32700, "message": f"Parse error: {exc}"},
                    }
                ),
                flush=True,
            )
        except Exception as exc:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "error": {"code": -32603, "message": f"Internal error: {exc}"},
                    }
                ),
                flush=True,
            )


if __name__ == "__main__":
    run_server()
