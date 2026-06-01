from __future__ import annotations

import argparse
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SHOWCASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SHOWCASE_DIR.parent.parent
ENV_PATH = REPO_ROOT / ".env"


def load_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def resolve_runtime_config() -> dict[str, str]:
    env_file = load_env_file(ENV_PATH)
    api_key = os.getenv("OPENROUTER_API_KEY") or env_file.get("OPENROUTER_API_KEY", "")
    model = os.getenv("LLM_MODEL") or env_file.get("LLM_MODEL", "openrouter/deepseek/deepseek-v4-pro")
    api_base = os.getenv("OPENROUTER_API_BASE") or env_file.get("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")
    return {"api_key": api_key, "model": model, "api_base": api_base.rstrip("/")}


class ShowcaseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SHOWCASE_DIR), **kwargs)

    def _write_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path == "/api/config":
            config = resolve_runtime_config()
            self._write_json(
                {
                    "provider": "workspace",
                    "model": config["model"],
                    "api_path": "/api/chat/completions",
                    "configured": bool(config["api_key"]),
                }
            )
            return
        return super().do_GET()

    def do_POST(self):  # noqa: N802
        if self.path != "/api/chat/completions":
            self._write_json({"error": "Unknown API endpoint"}, status=404)
            return

        config = resolve_runtime_config()
        if not config["api_key"]:
            self._write_json(
                {"error": "Missing OPENROUTER_API_KEY in environment or .env"},
                status=500,
            )
            return

        content_len = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_len) if content_len else b"{}"

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self._write_json({"error": "Invalid JSON payload"}, status=400)
            return

        if not payload.get("model"):
            payload["model"] = config["model"]

        upstream_url = f"{config['api_base']}/chat/completions"
        req = Request(
            upstream_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['api_key']}",
            },
            method="POST",
        )

        try:
            with urlopen(req, timeout=60) as resp:
                body = resp.read()
                status = resp.getcode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            self._write_json(
                {
                    "error": "Upstream HTTP error",
                    "status": exc.code,
                    "details": details,
                },
                status=502,
            )
        except URLError as exc:
            self._write_json(
                {
                    "error": "Cannot reach upstream LLM API",
                    "details": str(exc.reason),
                },
                status=502,
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Intract showcase server with local LLM proxy")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8086)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), ShowcaseHandler)
    print(f"Serving showcase on http://{args.host}:{args.port}")
    print("API config endpoint: /api/config")
    print("API proxy endpoint:  /api/chat/completions")
    server.serve_forever()


if __name__ == "__main__":
    main()
