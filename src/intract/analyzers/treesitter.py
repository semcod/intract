"""Optional tree-sitter analyzers with graceful fallback when bindings are missing."""

from __future__ import annotations


def _load_parser(language: str):
    try:
        from tree_sitter import Language, Parser
        import tree_sitter_languages
    except ImportError:
        return None

    try:
        lang = Language(tree_sitter_languages.get_language(language))
    except Exception:
        return None

    parser = Parser()
    parser.set_language(lang)
    return parser


def _find_extent(source: str, start_line: int, language: str, node_types: set[str]) -> tuple[int, int] | None:
    parser = _load_parser(language)
    if parser is None:
        return None

    try:
        tree = parser.parse(source.encode("utf-8"))
    except Exception:
        return None

    candidates: list[tuple[int, int]] = []
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        if node.type in node_types and node.start_point[0] + 1 >= start_line:
            candidates.append((node.start_point[0] + 1, node.end_point[0] + 1))
        stack.extend(reversed(node.children))

    if not candidates:
        return None

    return min(candidates, key=lambda item: item[0])


def typescript_function_extent(source: str, start_line: int) -> tuple[int, int] | None:
    return _find_extent(
        source,
        start_line,
        "typescript",
        {"function_declaration", "method_definition", "class_declaration", "arrow_function"},
    )


def csharp_method_extent(source: str, start_line: int) -> tuple[int, int] | None:
    return _find_extent(
        source,
        start_line,
        "c_sharp",
        {"method_declaration", "constructor_declaration", "class_declaration"},
    )
