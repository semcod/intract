from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from intract.integrations.planfile import PlanfileExporter, Ticket, tickets_from_report


@dataclass(frozen=True)
class PlanfileConfig:
    url: str | None = None
    token: str | None = None
    project: str | None = None
    output_dir: Path = Path(".intract")

    @classmethod
    def from_env(cls) -> PlanfileConfig:
        return cls(
            url=os.environ.get("PLANFILE_URL") or os.environ.get("INTRACT_PLANFILE_URL"),
            token=os.environ.get("PLANFILE_TOKEN") or os.environ.get("INTRACT_PLANFILE_TOKEN"),
            project=os.environ.get("PLANFILE_PROJECT") or os.environ.get("INTRACT_PLANFILE_PROJECT"),
            output_dir=Path(os.environ.get("INTRACT_PLANFILE_DIR", ".intract")),
        )


@dataclass(frozen=True)
class PlanfileSyncResult:
    pushed: int
    pulled: int
    local_files: dict[str, Path]
    remote_status: str


class PlanfileApiAdapter:
    """Sync Intract tickets with a planfile-compatible HTTP API or local export."""

    def __init__(self, config: PlanfileConfig | None = None) -> None:
        self.config = config or PlanfileConfig.from_env()

    def export_local(self, tickets: list[Ticket]) -> dict[str, Path]:
        exporter = PlanfileExporter(self.config.output_dir)
        return exporter.export(tickets)

    def push(self, tickets: list[Ticket]) -> PlanfileSyncResult:
        local_files = self.export_local(tickets)
        if not self.config.url:
            return PlanfileSyncResult(
                pushed=len(tickets),
                pulled=0,
                local_files=local_files,
                remote_status="local-only",
            )

        payload = {
            "project": self.config.project,
            "source": "intract",
            "tickets": [asdict(ticket) for ticket in tickets],
        }
        self._request("POST", self._endpoint("/tickets/bulk"), payload)
        return PlanfileSyncResult(
            pushed=len(tickets),
            pulled=0,
            local_files=local_files,
            remote_status="pushed",
        )

    def pull(self) -> list[Ticket]:
        if not self.config.url:
            json_path = self.config.output_dir / "planfile-tickets.json"
            if not json_path.exists():
                return []
            data = json.loads(json_path.read_text(encoding="utf-8"))
            return [_ticket_from_dict(item) for item in data.get("tickets", [])]

        query = f"?source=intract"
        if self.config.project:
            query += f"&project={self.config.project}"
        data = self._request("GET", self._endpoint(f"/tickets{query}"))
        items = data.get("tickets", data if isinstance(data, list) else [])
        return [_ticket_from_dict(item) for item in items]

    def sync_from_report(self, report: Any) -> PlanfileSyncResult:
        tickets = tickets_from_report(report)
        result = self.push(tickets)
        return PlanfileSyncResult(
            pushed=result.pushed,
            pulled=len(self.pull()),
            local_files=result.local_files,
            remote_status=result.remote_status,
        )

    def _endpoint(self, path: str) -> str:
        base = self.config.url.rstrip("/")
        return f"{base}{path}"

    def _request(self, method: str, url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.config.token:
            headers["Authorization"] = f"Bearer {self.config.token}"

        body = None
        if payload is not None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        request = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Planfile API {method} {url} failed: {exc.code} {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Planfile API {method} {url} failed: {exc.reason}") from exc


def _ticket_from_dict(data: dict[str, Any]) -> Ticket:
    return Ticket(
        id=str(data.get("id", "INTRACT-0000")),
        title=str(data.get("title", "Untitled")),
        severity=str(data.get("severity", "info")),
        status=str(data.get("status", "open")),
        source=str(data.get("source", "intract")),
        file_path=data.get("file_path"),
        line=data.get("line"),
        contract=data.get("contract"),
        details=str(data.get("details", "")),
        labels=list(data.get("labels", [])),
        created_at=str(data.get("created_at", "")) or _default_created_at(),
    )


def _default_created_at() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()
