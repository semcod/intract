from pathlib import Path

from intract.parsers.toon import load_toon_records, parse_toon_uri_line


def test_parse_toon_uri_line():
    line = "intract://src/calculator.py?func=add_numbers&line=45#id=math-check&intent=pure-math&forbid=write,print"
    record = parse_toon_uri_line(line)
    
    assert record is not None
    assert record.file_path == "src/calculator.py"
    assert record.start_line == 45
    assert record.end_line == 45
    
    contract = record.contract
    assert contract.contract_id == "math-check"
    assert contract.action == "pure"
    assert contract.object == "math"
    assert "write" in contract.forbidden
    assert "print" in contract.forbidden
    assert "target_func:add_numbers" in contract.tags


def test_parse_toon_uri_line_without_scheme():
    line = "src/calculator.py?xpatch=//button#intent=click-btn&req=auth"
    record = parse_toon_uri_line(line)
    
    assert record is not None
    assert record.file_path == "src/calculator.py"
    assert record.contract.action == "click"
    assert record.contract.object == "btn"
    assert "auth" in record.contract.required
    assert "target_xpath://button" in record.contract.tags


def test_load_toon_records(tmp_path: Path):
    toon_file = tmp_path / "intract.toon"
    toon_file.write_text(
        "# This is a comment\n"
        "intract://src/calc.py?func=add#intent=math-add&forbid=print\n"
        "\n"
        "intract://src/ui.html?xpath=//div#intent=render-ui&req=css\n",
        encoding="utf-8"
    )
    
    records = load_toon_records(toon_file)
    assert len(records) == 2
    assert records[0].file_path == "src/calc.py"
    assert records[1].file_path == "src/ui.html"
