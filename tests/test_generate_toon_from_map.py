from pathlib import Path
import importlib.util
import sys


_SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "generate_toon_from_map.py"
_SPEC = importlib.util.spec_from_file_location("generate_toon_from_map", _SCRIPT_PATH)
assert _SPEC is not None and _SPEC.loader is not None
gen = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = gen
_SPEC.loader.exec_module(gen)


def _sample_map_text() -> str:
    return """M[
  src/mod_a.py, module
  src/mod_b.py
D:
  src/mod_a.py:
    parse_data(x)
    Service: run(), _internal(), for(item)
  src/mod_b.py:
    _private()
    save_item(payload)
"""


def test_parse_modules_reads_m_section_entries() -> None:
    lines = _sample_map_text().splitlines()

    modules = gen._parse_modules(lines)

    assert modules == ["src/mod_a.py", "src/mod_b.py"]


def test_parse_functions_extracts_symbols_and_skips_private() -> None:
    lines = _sample_map_text().splitlines()

    targets = gen._parse_functions(lines)
    as_pairs = {(item.file_path, item.function_name) for item in targets}

    assert ("src/mod_a.py", "parse_data") in as_pairs
    assert ("src/mod_a.py", "run") in as_pairs
    assert ("src/mod_b.py", "save_item") in as_pairs
    assert ("src/mod_a.py", "_internal") not in as_pairs
    assert ("src/mod_a.py", "for") not in as_pairs
    assert ("src/mod_b.py", "_private") not in as_pairs


def test_generate_toon_lines_dev_profile_filters_project_and_shapes_functions(tmp_path: Path) -> None:
    map_file = tmp_path / "map.toon.yaml"
    map_file.write_text(_sample_map_text(), encoding="utf-8")

    lines = gen.generate_toon_lines(
        map_file=map_file,
        include_project=True,
        include_files=True,
        include_functions=True,
        llm=False,
        llm_goal="",
        llm_model=None,
        output_profile="dev",
    )

    body = "\n".join(lines)
    function_lines = [line for line in lines if "?func=" in line]
    function_body = "\n".join(function_lines)

    assert "intract://.#id=project.auto.overview" not in body
    assert "domain=development" in function_body
    assert "validate=return_value" in function_body
    assert "no_forbidden_effect" not in function_body


def test_generate_toon_lines_ci_security_profile_includes_project_and_security_validate(
    tmp_path: Path,
) -> None:
    map_file = tmp_path / "map.toon.yaml"
    map_file.write_text(_sample_map_text(), encoding="utf-8")

    lines = gen.generate_toon_lines(
        map_file=map_file,
        include_project=True,
        include_files=True,
        include_functions=True,
        llm=False,
        llm_goal="",
        llm_model=None,
        output_profile="ci-security",
    )

    body = "\n".join(lines)

    assert "intract://.#id=project.auto.overview" in body
    assert "domain=security" in body
    assert "validate=no_forbidden_effect" in body
