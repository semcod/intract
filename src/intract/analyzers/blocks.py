from __future__ import annotations

import re


def scan_braced_block(lines: list[str], start_line: int) -> int:
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
        if started:
            end = index

    return end


def block_extent_from_patterns(
    source: str,
    start_line: int,
    start_patterns: list[re.Pattern[str]],
) -> tuple[int, int]:
    lines = source.splitlines()
    if start_line < 1 or start_line > len(lines):
        return start_line, start_line

    block_start = None
    for index in range(start_line, len(lines) + 1):
        line = lines[index - 1]
        if any(pattern.match(line) for pattern in start_patterns):
            block_start = index
            break

    if block_start is None:
        return start_line, start_line

    return start_line, scan_braced_block(lines, block_start)
