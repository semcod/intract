from pathlib import Path

from intract.analyzers.csharp import csharp_block_extent
from intract.analyzers.typescript import typescript_block_extent
from intract.check import block_extent


PERMISSION_TS = Path(__file__).resolve().parents[1] / "examples" / "integration_tests" / "02_typescript_violation_planfile" / "permission.ts"


def test_typescript_block_extent_finds_async_function():
    source = PERMISSION_TS.read_text(encoding="utf-8")
    start, end = typescript_block_extent(source, 1)
    assert start == 1
    assert end >= 6


def test_block_extent_uses_typescript_analyzer_for_ts_files():
    source = PERMISSION_TS.read_text(encoding="utf-8")
    start, end = block_extent(source, 1, file_path="permission.ts")
    assert start == 1
    assert end >= 6


def test_csharp_block_extent_finds_method():
    source = (
        "// @intract.v1 scope:method intent:validate:user forbid:network\n"
        "public async Task<bool> ValidateUserAsync()\n"
        "{\n"
        "    return true;\n"
        "}\n"
    )
    start, end = csharp_block_extent(source, 1)
    assert start == 1
    assert end == 5


def test_block_extent_uses_csharp_analyzer():
    source = (
        "// @intract.v1 scope:method intent:validate:user\n"
        "public bool ValidateUser()\n"
        "{\n"
        "    return true;\n"
        "}\n"
    )
    start, end = block_extent(source, 1, file_path="AuthService.cs")
    assert end == 5


def test_java_block_extent():
    from intract.analyzers.java import java_block_extent

    source = (
        "// @intract.v1 scope:method intent:validate:user forbid:network\n"
        "public boolean validateUser() {\n"
        "    return true;\n"
        "}\n"
    )
    start, end = java_block_extent(source, 1)
    assert start == 1
    assert end == 4


def test_go_block_extent():
    from intract.analyzers.go import go_block_extent

    source = (
        "// @intract.v1 scope:function intent:validate:user\n"
        "func validateUser() {\n"
        "    return true\n"
        "}\n"
    )
    start, end = go_block_extent(source, 1)
    assert end == 4


def test_rust_block_extent():
    from intract.analyzers.rust import rust_block_extent

    source = (
        "/// @intract.v1 scope:function intent:validate:user\n"
        "pub fn validate_user() -> bool {\n"
        "    true\n"
        "}\n"
    )
    start, end = rust_block_extent(source, 2)
    assert start == 2
    assert end == 4


def test_rust_decorator_block_extent():
    from intract.analyzers.rust import rust_block_extent

    source = (
        '@intract.v1 uri="intract://src/decoder.rs?func=decode_header#id=safe-decoder&forbid=unsafe"\n'
        "pub fn decode_header(raw_data: &[u8]) -> Header {\n"
        "    true\n"
        "}\n"
    )
    start, end = rust_block_extent(source, 1)
    assert start == 1
    assert end == 4


def test_block_extent_routes_java_go_rust():
    java = "// @intract.v1 scope:method intent:x\npublic void run() {\n    return;\n}\n"
    go = "// @intract.v1 scope:function intent:x\nfunc run() {\n    return\n}\n"
    rust = "// @intract.v1 scope:function intent:x\nfn run() {\n    true\n}\n"
    for source, name in (
        (java, "App.java"),
        (go, "main.go"),
        (rust, "lib.rs"),
    ):
        start, end = block_extent(source, 1, file_path=name)
        assert start == 1
        assert end >= 3
