from __future__ import annotations

import hashlib
import hmac
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
    webhook_url: str | None = None
    webhook_secret: str | None = None
    output_dir: Path = Path(".intract")

    @classmethod
    def from_env(cls) -> PlanfileConfig:
        return cls(
            url=os.environ.get("PLANFILE_URL") or os.environ.get("INTRACT_PLANFILE_URL"),
            token=os.environ.get("PLANFILE_TOKEN") or os.environ.get("INTRACT_PLANFILE_TOKEN"),
            project=os.environ.get("PLANFILE_PROJECT") or os.environ.get("INTRACT_PLANFILE_PROJECT"),
            webhook_url=os.environ.get("PLANFILE_WEBHOOK_URL") or os.environ.get("INTRACT_PLANFILE_WEBHOOK_URL"),
            webhook_secret=os.environ.get("PLANFILE_WEBHOOK_SECRET") or os.environ.get("INTRACT_PLANFILE_WEBHOOK_SECRET"),
            output_dir=Path(os.environ.get("INTRACT_PLANFILE_DIR", ".intract")),
        )


@dataclass(frozen=True)
class PlanfileSyncResult:
    pushed: int
    pulled: int
    local_files: dict[str, Path]
    remote_status: str
    webhook_status: str = "skipped"


@dataclass(frozen=True)
class PlanfileWebhookResult:
    delivered: bool
    status_code: int | None
    event: str


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
            webhook_status = "skipped"
            if self.config.webhook_url:
                webhook_status = self._webhook_label(
                    self.emit_webhook(
                        "tickets.exported",
                        {"project": self.config.project, "count": len(tickets)},
                    )
                )
            return PlanfileSyncResult(
                pushed=len(tickets),
                pulled=0,
                local_files=local_files,
                remote_status="local-only",
                webhook_status=webhook_status,
            )

        payload = {
            "project": self.config.project,
            "source": "intract",
            "tickets": [asdict(ticket) for ticket in tickets],
        }
        self._request("POST", self._endpoint("/tickets/bulk"), payload)
        webhook_status = "skipped"
        if self.config.webhook_url:
            webhook_status = self._webhook_label(
                self.emit_webhook(
                    "tickets.pushed",
                    {
                        "project": self.config.project,
                        "count": len(tickets),
                        "tickets": [asdict(t) for t in tickets],
                    },
                )
            )
        return PlanfileSyncResult(
            pushed=len(tickets),
            pulled=0,
            local_files=local_files,
            remote_status="pushed",
            webhook_status=webhook_status,
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
        webhook = None
        if self.config.webhook_url:
            webhook = self.emit_webhook(
                "tickets.synced",
                {"project": self.config.project, "pushed": result.pushed, "pulled": len(self.pull())},
            )
        return PlanfileSyncResult(
            pushed=result.pushed,
            pulled=len(self.pull()),
            local_files=result.local_files,
            remote_status=result.remote_status,
            webhook_status=self._webhook_label(webhook) if webhook else result.webhook_status,
        )

    def emit_webhook(self, event: str, payload: dict[str, Any]) -> PlanfileWebhookResult:
        if not self.config.webhook_url:
            return PlanfileWebhookResult(delivered=False, status_code=None, event=event)

        body = {
            "event": event,
            "source": "intract",
            "project": self.config.project,
            "payload": payload,
        }
        raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json", "User-Agent": "intract/planfile-webhook"}
        if self.config.webhook_secret:
            signature = hmac.new(
                self.config.webhook_secret.encode("utf-8"),
                raw,
                hashlib.sha256,
            ).hexdigest()
            headers["X-Intract-Signature"] = f"sha256={signature}"

        request = urllib.request.Request(self.config.webhook_url, data=raw, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return PlanfileWebhookResult(
                    delivered=True,
                    status_code=response.status,
                    event=event,
                )
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"Planfile webhook failed: {exc.code}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Planfile webhook failed: {exc.reason}") from exc

    def apply_webhook_event(self, payload: dict[str, Any]) -> int:
        """Apply inbound planfile ticket status updates to the local JSON export."""
        event = str(payload.get("event", ""))
        if event not in {"ticket.updated", "tickets.updated", "ticket.closed"}:
            return 0

        json_path = self.config.output_dir / "planfile-tickets.json"
        if not json_path.exists():
            return 0

        data = json.loads(json_path.read_text(encoding="utf-8"))
        tickets = data.get("tickets", [])
        updates = payload.get("tickets") or payload.get("payload", {}).get("tickets") or []
        if isinstance(updates, dict):
            updates = [updates]

        by_id = {str(item.get("id")): item for item in tickets if item.get("id")}
        changed = 0
        for update in updates:
            ticket_id = str(update.get("id", ""))
            if ticket_id not in by_id:
                continue
            new_status = update.get("status")
            if new_status and by_id[ticket_id].get("status") != new_status:
                by_id[ticket_id]["status"] = new_status
                changed += 1

        if changed:
            data["tickets"] = list(by_id.values())
            json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return changed

    @staticmethod
    def _webhook_label(result: PlanfileWebhookResult | None) -> str:
        if result is None:
            return "skipped"
        return "delivered" if result.delivered else "failed"

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
