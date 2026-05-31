from pathlib import Path
import json

from intract.integrations.planfile import tickets_from_report
from intract.integrations.planfile_adapter import PlanfileApiAdapter, PlanfileConfig
from intract.project import validate_project


def test_planfile_push_local_only(tmp_path: Path):
    (tmp_path / "bad.py").write_text(
        "# @intract.v1 scope:function intent:validate:user forbid:network\n"
        "import requests\n"
        "def validate_user():\n"
        "    return requests.get('https://example.com')\n",
        encoding="utf-8",
    )
    report = validate_project(tmp_path)
    adapter = PlanfileApiAdapter(PlanfileConfig(output_dir=tmp_path / ".intract"))
    result = adapter.push(tickets_from_report(report))

    assert result.pushed >= 1
    assert result.remote_status == "local-only"
    assert (tmp_path / ".intract" / "planfile-tickets.json").exists()


def test_planfile_pull_reads_local_export(tmp_path: Path):
    (tmp_path / "bad.py").write_text(
        "# @intract.v1 scope:function intent:validate:user forbid:network\n"
        "import requests\n"
        "def validate_user():\n"
        "    return requests.get('https://example.com')\n",
        encoding="utf-8",
    )
    report = validate_project(tmp_path)
    adapter = PlanfileApiAdapter(PlanfileConfig(output_dir=tmp_path / ".intract"))
    adapter.push(tickets_from_report(report))
    pulled = adapter.pull()

    assert pulled
    assert pulled[0].source == "intract"


def test_planfile_webhook_apply_updates_local_status(tmp_path: Path):
    export_dir = tmp_path / ".intract"
    export_dir.mkdir()
    (export_dir / "planfile-tickets.json").write_text(
        json.dumps(
            {
                "tickets": [
                    {
                        "id": "INTRACT-0001",
                        "title": "VIOLATION: validate.user",
                        "severity": "high",
                        "status": "open",
                        "source": "intract",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    adapter = PlanfileApiAdapter(PlanfileConfig(output_dir=export_dir))
    changed = adapter.apply_webhook_event(
        {"event": "ticket.updated", "tickets": [{"id": "INTRACT-0001", "status": "closed"}]}
    )
    assert changed == 1
    data = json.loads((export_dir / "planfile-tickets.json").read_text(encoding="utf-8"))
    assert data["tickets"][0]["status"] == "closed"


def test_planfile_webhook_emit_delivers():
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

    received = {}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.get("Content-Length", "0"))
            received["body"] = self.rfile.read(length)
            self.send_response(204)
            self.end_headers()

        def log_message(self, format, *args):
            return

    server = HTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_address[1]}/hook"

    adapter = PlanfileApiAdapter(PlanfileConfig(webhook_url=url, webhook_secret="secret"))
    result = adapter.emit_webhook("ping", {"ok": True})
    server.shutdown()

    assert result.delivered is True
    assert received["body"]
