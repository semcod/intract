"""MCP tool schemas for Intract."""

from __future__ import annotations

from typing import Any

PROJECT_PROPERTIES: dict[str, Any] = {
    "path": {"type": "string", "description": "Project root directory", "default": "."},
    "manifest": {"type": "string", "description": "Path to intract.yaml / intent.yaml"},
}

SNIPPET_PROPERTIES: dict[str, Any] = {
    "code": {"type": "string", "description": "Source code containing @intract contracts"},
    "filename": {"type": "string", "description": "Optional filename for contract context"},
}

TOOL_SCHEMA_INTRACT = {
    "validate_project": {
        "name": "validate_project",
        "description": "Validate Intract intent contracts for a project directory",
        "inputSchema": {
            "type": "object",
            "properties": PROJECT_PROPERTIES,
            "required": ["path"],
        },
    },
    "validate_staged": {
        "name": "validate_staged",
        "description": "Validate staged Intract contracts (hunk-level when possible)",
        "inputSchema": {
            "type": "object",
            "properties": {
                **PROJECT_PROPERTIES,
                "hunks": {
                    "type": "boolean",
                    "default": True,
                    "description": "Validate only contracts touched by staged hunks",
                },
            },
            "required": ["path"],
        },
    },
    "validate_intent_snippet": {
        "name": "validate_intent_snippet",
        "description": "Validate inline @intract contracts in a code snippet",
        "inputSchema": {
            "type": "object",
            "properties": SNIPPET_PROPERTIES,
            "required": ["code"],
        },
    },
    "find_duplicates": {
        "name": "find_duplicates",
        "description": "Find duplicate or similar intent contracts",
        "inputSchema": {
            "type": "object",
            "properties": {
                **PROJECT_PROPERTIES,
                "threshold": {
                    "type": "number",
                    "default": 0.84,
                    "description": "Minimum similarity score",
                },
            },
            "required": ["path"],
        },
    },
    "build_graph": {
        "name": "build_graph",
        "description": "Build require/provide graph from contracts and manifest",
        "inputSchema": {
            "type": "object",
            "properties": PROJECT_PROPERTIES,
            "required": ["path"],
        },
    },
    "scan_artifacts": {
        "name": "scan_artifacts",
        "description": "Discover and validate OpenAPI, Dockerfile, GitHub Actions and Kubernetes artifacts",
        "inputSchema": {
            "type": "object",
            "properties": PROJECT_PROPERTIES,
            "required": ["path"],
        },
    },
    "project_info": {
        "name": "project_info",
        "description": "Show Intract version and available MCP tools",
        "inputSchema": {"type": "object", "properties": {}},
    },
}
