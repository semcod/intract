from __future__ import annotations

import ast
from typing import Iterable


def _decorator_lines(node: ast.AST) -> Iterable[int]:
    for decorator in getattr(node, "decorator_list", []):
        if hasattr(decorator, "lineno"):
            yield decorator.lineno


def python_function_extent(source: str, start_line: int) -> tuple[int, int] | None:
    """Return (start, end) line numbers for the Python def/class at or after start_line."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    candidates: list[tuple[int, int, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        node_start = min([node.lineno, *_decorator_lines(node)])
        if node_start >= start_line and hasattr(node, "end_lineno") and node.end_lineno:
            candidates.append((node_start, node.end_lineno, node.lineno))

    if not candidates:
        return None

    node_start, node_end, _ = min(candidates, key=lambda item: (item[0], item[2]))
    return node_start, node_end


def python_block_extent(source: str, start_line: int) -> tuple[int, int]:
    """Map an @intract comment line to the Python block it annotates."""
    lines = source.splitlines()
    if start_line < 1 or start_line > len(lines):
        return start_line, start_line

    extent = python_function_extent(source, start_line)
    if extent is not None:
        _, block_end = extent
        return start_line, block_end

    end = start_line
    in_block = False
    for index in range(start_line + 1, len(lines) + 1):
        line = lines[index - 1]
        stripped = line.strip()
        if not in_block:
            if stripped.startswith(("def ", "class ", "async def ")):
                in_block = True
                end = index
                continue
            if stripped.startswith("#") or not stripped or stripped.startswith(("import ", "from ")):
                end = index
                continue
            break
        if not stripped:
            end = index
            continue
        if line[0].isspace():
            end = index
            continue
        if stripped.startswith(("def ", "class ", "async def ")) or "@intract" in line:
            break
        break

    return start_line, end
