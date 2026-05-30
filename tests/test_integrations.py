from intract.duplicates import find_duplicate_contracts
from intract.integrations.redup import BlockAdapter, find_intent_duplicate_groups, scan_blocks_for_intent_duplicates


def test_redup_finds_intent_duplicate_groups():
    blocks = [
        BlockAdapter(
            file_path="a.py",
            content=(
                "# @intract.v1 scope:function intent:parse:extensions priority:2 domain:cli\n"
                "def parse_extensions(raw):\n"
                "    return raw.split(',')\n"
            ),
        ),
        BlockAdapter(
            file_path="b.py",
            content=(
                "# @intract.v1 scope:function intent:read:extension_list priority:2 domain:cli\n"
                "def load_exts(value):\n"
                "    return value.split(',')\n"
            ),
        ),
    ]

    result = scan_blocks_for_intent_duplicates(blocks, threshold=0.5)
    assert result.signatures
    assert result.groups
    assert result.groups[0]["metadata"]["duplicate_type"] == "intent"


def test_duplicate_contracts_cli_parity(tmp_path):
    (tmp_path / "a.py").write_text(
        "# @intract.v1 scope:function intent:parse:extensions priority:2 domain:cli\n"
        "def parse_extensions(raw):\n"
        "    return raw.split(',')\n",
        encoding="utf-8",
    )
    (tmp_path / "b.py").write_text(
        "# @intract.v1 scope:function intent:parse:extension_list priority:2 domain:cli\n"
        "def load_extensions(raw):\n"
        "    return raw.split(',')\n",
        encoding="utf-8",
    )
    matches = find_duplicate_contracts(tmp_path, threshold=0.5)
    assert matches


def test_find_intent_duplicate_groups_from_blocks():
    blocks = [
        BlockAdapter(
            file_path="cli/options.py",
            content="# @intract.v1 scope:function intent:parse:extensions domain:cli\npass",
        ),
        BlockAdapter(
            file_path="utils/extensions.py",
            content="# @intract.v1 scope:function intent:read:extension_list domain:cli\npass",
        ),
    ]
    groups = find_intent_duplicate_groups(blocks=blocks, threshold=0.5)
    assert groups
