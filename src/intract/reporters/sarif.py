from __future__ import annotations

from typing import Any


def report_to_sarif(report: Any) -> dict:
    results = []
    rules = {}

    for item in getattr(report, "results", []) or []:
        status = getattr(getattr(item, "status", ""), "value", str(getattr(item, "status", "")))
        if status == "pass":
            continue

        rule_id = f"intract.{status}"
        rules[rule_id] = {
            "id": rule_id,
            "name": rule_id,
            "shortDescription": {"text": f"Intract {status} contract"},
        }

        file_path = getattr(item, "file_path", None) or "unknown"
        lines = getattr(item, "lines", None)
        start_line = lines[0] if lines else 1
        contract = getattr(item, "contract", "unknown.contract")
        missing = getattr(item, "missing", []) or []
        violations = getattr(item, "violations", []) or []
        messages = [getattr(v, "message", str(v)) for v in violations]
        if missing:
            messages.append("Missing: " + ", ".join(missing))

        results.append(
            {
                "ruleId": rule_id,
                "level": "error" if status in {"violation", "fail"} else "warning",
                "message": {"text": f"{contract}: {status}. " + " ".join(messages)},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": file_path},
                            "region": {"startLine": int(start_line)},
                        }
                    }
                ],
            }
        )

    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Intract",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }
