from __future__ import annotations

import re


TS_BLOCK_START = re.compile(
    r"^\s*(?:export\s+)?(?:async\s+)?function\s+\w+|"
    r"^\s*(?:export\s+)?class\s+\w+|"
    r"^\s*(?:public|private|protected)\s+\w+|"
    r"^\s*(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?(?:\([^)]*\)|[\w$]+)\s*=>",
    re.MULTILINE,
)


def typescript_block_extent(source: str, start_line: int) -> tuple[int, int]:
    lines = source.splitlines()
    if start_line < 1 or start_line > len(lines):
        return start_line, start_line

    treesitter_extent = _treesitter_typescript_extent(source, start_line)
    if treesitter_extent is not None:
        return start_line, treesitter_extent[1]

    block_start = None
    for index in range(start_line, len(lines) + 1):
        line = lines[index - 1]
        if TS_BLOCK_START.match(line):
            block_start = index
            break

    if block_start is None:
        return start_line, start_line

    end = _scan_braced_block(lines, block_start)
    return start_line, end


def _scan_braced_block(lines: list[str], start_line: int) -> int:
    depth = 0
    started = False
    end = start_line

    for index in range(start_line, len(lines) + 1):
        line = lines[index - 1]
        for char in line:
            if char == "{":
                depth += 1
                started = True
            elif char == "}":
                depth -= 1
                if started and depth == 0:
                    return index
        if not started and line.strip() and not line.strip().startswith("//"):
            end = index
        elif started:
            end = index

    return end


def _treesitter_typescript_extent(source: str, start_line: int) -> tuple[int, int] | None:
    try:
        from intract.analyzers.treesitter import typescript_function_extent
    except ImportError:
        return None
    return typescript_function_extent(source, start_line)
