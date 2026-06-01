from __future__ import annotations

import urllib.parse
from pathlib import Path

from intract.core.models import Contract, ContractRecord


def parse_toon_uri_line(line: str, line_num: int = 1) -> ContractRecord | None:
    """Parse a single flat Toon URI line into a ContractRecord.
    
    Format:
      intract://<file_path>?func=<func>&line=<line>&xpath=<xpath>#id=<id>&intent=<intent>&forbid=<forbid>
    """
    text = line.strip()
    if not text or text.startswith("#"):
        return None
        
    parsed = urllib.parse.urlparse(text)
    # Extract file target path
    if parsed.scheme in {"intract", "toon"}:
        file_path = parsed.netloc + parsed.path
    else:
        file_path = parsed.path
        
    query = urllib.parse.parse_qs(parsed.query)
    func_val = query.get("func", query.get("function", [""]))[0]
    line_val = query.get("line", [""])[0]
    xpath_val = query.get("xpath", query.get("xpatch", [""]))[0]
    
    start_line = int(line_val) if line_val.isdigit() else 1
    end_line = start_line
    
    # Parse fragment for rules/parameters
    fragment_params = urllib.parse.parse_qs(parsed.fragment)
    
    def get_first(key: str, default: str = "") -> str:
        return fragment_params.get(key, [default])[0]
        
    def get_list(key: str) -> tuple[str, ...]:
        vals = fragment_params.get(key, [])
        out = []
        for v in vals:
            out.extend(x.strip() for x in v.split(",") if x.strip())
        return tuple(out)

    contract_id = get_first("id", get_first("contract_id"))
    intent = get_first("intent")
    action = get_first("action")
    object_name = get_first("object", get_first("obj"))
    if not action or not object_name:
        if ":" in intent:
            action, object_name = intent.split(":", 1)
        elif "." in intent:
            action, object_name = intent.split(".", 1)
        elif "-" in intent:
            action, object_name = intent.split("-", 1)
        elif intent:
            action, object_name = intent, "unknown"
        elif contract_id:
            if "-" in contract_id:
                action, object_name = contract_id.split("-", 1)
            elif "_" in contract_id:
                action, object_name = contract_id.split("_", 1)
            else:
                action, object_name = "contract", contract_id
        else:
            action, object_name = "", "unknown"
            
    tags = list(get_list("tag") or get_list("tags"))
    if func_val:
        tags.append(f"target_func:{func_val}")
    if xpath_val:
        tags.append(f"target_xpath:{xpath_val}")
        
    contract = Contract(
        action=action.strip(),
        object=object_name.strip(),
        scope=get_first("scope", "block"),
        priority=int(get_first("priority", "3") if get_first("priority", "3").isdigit() else "3"),
        domain=get_first("domain"),
        inputs=get_list("input") or get_list("inputs") or get_list("in"),
        outputs=get_list("output") or get_list("outputs") or get_list("out"),
        effects=get_list("effect") or get_list("effects") or get_list("fx"),
        forbidden=get_list("forbid") or get_list("forbidden") or get_list("no"),
        required=get_list("require") or get_list("requires") or get_list("req"),
        validators=get_list("validate") or get_list("validators") or get_list("rules"),
        tags=tuple(tags),
        algorithms=get_list("algorithm") or get_list("algorithms") or get_list("alg"),
        relations=get_list("relation") or get_list("relations") or get_list("rel"),
        contract_id=contract_id,
        meaning=get_first("meaning"),
        raw=text,
    )
    
    return ContractRecord(
        contract=contract,
        file_path=file_path.strip(),
        start_line=start_line,
        end_line=end_line,
        owner="toon_uri",
    )


def load_toon_records(path: Path) -> list[ContractRecord]:
    """Load flat line-by-line URI contracts from a Toon file."""
    if not path.exists():
        return []
    records = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []
    for idx, line in enumerate(lines, start=1):
        record = parse_toon_uri_line(line, line_num=idx)
        if record is not None:
            records.append(record)
    return records
