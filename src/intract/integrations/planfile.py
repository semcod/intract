from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Ticket:
    id: str
    title: str
    severity: str
    status: str = "open"
    source: str = "intract"
    file_path: str | None = None
    line: int | None = None
    contract: str | None = None
    details: str = ""
    labels: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def _severity_from_status(status: str) -> str:
    if status == "violation":
        return "high"
    if status == "fail":
        return "medium"
    if status == "partial":
        return "low"
    return "info"


def tickets_from_report(report: Any) -> list[Ticket]:
    tickets: list[Ticket] = []

    results = getattr(report, "results", []) or []
    for index, result in enumerate(results, start=1):
        status = getattr(result, "status", "unknown")
        status_value = getattr(status, "value", str(status))

        if status_value in {"pass", "unknown"}:
            continue

        contract = getattr(result, "contract", "unknown.contract")
        file_path = getattr(result, "file_path", None)
        lines = getattr(result, "lines", None)
        line = lines[0] if lines else None

        missing = getattr(result, "missing", []) or []
        violations = getattr(result, "violations", []) or []
        violation_text = [getattr(v, "message", str(v)) for v in violations]

        details_parts = []
        if missing:
            details_parts.append("Missing: " + ", ".join(missing))
        if violation_text:
            details_parts.append("Violations: " + "; ".join(violation_text))

        tickets.append(
            Ticket(
                id=f"INTRACT-{index:04d}",
                title=f"{status_value.upper()}: {contract}",
                severity=_severity_from_status(status_value),
                file_path=file_path,
                line=line,
                contract=contract,
                details="\\n".join(details_parts) or f"Intract result: {status_value}",
                labels=["intract", "intent-contract", status_value],
            )
        )

    return tickets


class PlanfileExporter:
    def __init__(self, output_dir: str | Path = ".intract") -> None:
        self.output_dir = Path(output_dir)

    def export(self, tickets: list[Ticket]) -> dict[str, Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        yaml_path = self.output_dir / "planfile-tickets.yaml"
        todo_path = self.output_dir / "TODO.intract.md"
        json_path = self.output_dir / "planfile-tickets.json"

        self._write_yaml(yaml_path, tickets)
        self._write_todo(todo_path, tickets)
        self._write_json(json_path, tickets)

        return {
            "yaml": yaml_path,
            "todo": todo_path,
            "json": json_path,
        }

    def _write_yaml(self, path: Path, tickets: list[Ticket]) -> None:
        data = {"tickets": [asdict(ticket) for ticket in tickets]}
        try:
            import yaml

            path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        except Exception:
            # Minimal YAML fallback.
            lines = ["tickets:"]
            for ticket in tickets:
                lines.append(f"  - id: {ticket.id}")
                lines.append(f"    title: {ticket.title!r}")
                lines.append(f"    severity: {ticket.severity}")
                lines.append(f"    status: {ticket.status}")
                if ticket.file_path:
                    lines.append(f"    file_path: {ticket.file_path!r}")
                if ticket.line:
                    lines.append(f"    line: {ticket.line}")
                if ticket.contract:
                    lines.append(f"    contract: {ticket.contract!r}")
                lines.append(f"    details: {ticket.details!r}")
                lines.append("    labels: [" + ", ".join(ticket.labels) + "]")
            path.write_text("\\n".join(lines) + "\\n", encoding="utf-8")

    def _write_json(self, path: Path, tickets: list[Ticket]) -> None:
        import json

        path.write_text(
            json.dumps({"tickets": [asdict(ticket) for ticket in tickets]}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _write_todo(self, path: Path, tickets: list[Ticket]) -> None:
        lines = ["# Intract Tickets", ""]
        if not tickets:
            lines.append("No open Intract tickets.")
        for ticket in tickets:
            loc = f"{ticket.file_path}:{ticket.line}" if ticket.file_path and ticket.line else ticket.file_path or ""
            lines.append(f"- [ ] **{ticket.id}** `{ticket.severity}` {ticket.title}")
            if loc:
                lines.append(f"  - Location: `{loc}`")
            if ticket.details:
                lines.append(f"  - Details: {ticket.details}")
            lines.append("")
        path.write_text("\\n".join(lines), encoding="utf-8")
