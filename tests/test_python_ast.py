from intract.analyzers.python_ast import python_block_extent, python_function_extent
from intract.check import block_extent


def test_python_function_extent_finds_async_def():
    source = (
        "async def load():\n"
        "    return 1\n"
    )
    assert python_function_extent(source, 1) == (1, 2)


def test_python_block_extent_includes_decorators_and_imports():
    source = (
        "# @intract.v1 scope:function intent:parse:extensions\n"
        "from pathlib import Path\n"
        "@staticmethod\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n"
    )
    start, end = python_block_extent(source, 1)
    assert start == 1
    assert end >= 5


def test_block_extent_uses_ast_for_python_files():
    source = (
        "# @intract.v1 scope:function intent:parse:extensions\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n"
        "\n"
        "def other():\n"
        "    pass\n"
    )
    start, end = block_extent(source, 1, file_path="parser.py")
    assert start == 1
    assert end == 3
