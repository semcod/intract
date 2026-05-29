from __future__ import annotations

import json
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .engine import EngineConfig, scan_suggest_and_validate
from .integrations.planfile import PlanfileExporter, tickets_from_report
from .parser import extract_contract_records_from_text
from .project import validate_project
from .watch import WatchConfig, changes_to_paths, watch_tree
from .yaml_manifest import create_sample_manifest

app = typer.Typer(help="Intract — intent contracts for codebases.")
engine_app = typer.Typer(help="Intract engine: scan, suggest contracts and detect logic drift.")
app.add_typer(engine_app, name="engine")

console = Console()


@app.callback(invoke_without_command=True)
def main(version: bool = typer.Option(False, "--version", help="Show version.")):
    if version:
        console.print(f"intract {__version__}")
        raise typer.Exit()


@app.command()
def init(
    path: Path = typer.Argument(Path("."), help="Project path."),
    force: bool = typer.Option(False, "--force", help="Overwrite existing intent.yaml."),
):
    """Create a sample intent.yaml manifest."""
    target = path / "intent.yaml"
    if target.exists() and not force:
        console.print(f"[red]File already exists:[/] {target}")
        raise typer.Exit(1)
    target.write_text(create_sample_manifest(), encoding="utf-8")
    console.print(f"[green]Created[/] {target}")


@app.command()
def scan(
    path: Path = typer.Argument(Path("."), help="File or directory."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON."),
):
    """Scan files for inline @intract contracts."""
    records = []
    if path.is_file():
        records.extend(
            extract_contract_records_from_text(
                path.read_text(encoding="utf-8"),
                file_path=str(path),
            )
        )
    else:
        for file_path in path.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix not in {
                ".py", ".js", ".ts", ".cs", ".java", ".go", ".rs", ".md", ".yaml", ".yml",
                ".json", ".toml", ".sh", ".sql", ".html", ".css"
            } and file_path.name.lower() != "dockerfile":
                continue
            try:
                records.extend(
                    extract_contract_records_from_text(
                        file_path.read_text(encoding="utf-8"),
                        file_path=str(file_path.relative_to(path)),
                    )
                )
            except UnicodeDecodeError:
                continue

    data = [
        {
            "file": record.file_path,
            "line": record.start_line,
            "scope": record.contract.scope,
            "intent": record.contract.key,
            "priority": record.contract.priority,
            "domain": record.contract.domain,
        }
        for record in records
    ]

    if json_output:
        console.print_json(json.dumps(data, ensure_ascii=False))
        return

    table = Table(title="Intract contracts")
    table.add_column("File")
    table.add_column("Line")
    table.add_column("Scope")
    table.add_column("Intent")
    table.add_column("Priority")
    table.add_column("Domain")

    for item in data:
        table.add_row(
            item["file"],
            str(item["line"]),
            item["scope"],
            item["intent"],
            str(item["priority"]),
            item["domain"],
        )

    console.print(table)


@app.command()
def validate(
    path: Path = typer.Argument(Path("."), help="Project path."),
    manifest: Path | None = typer.Option(None, "--manifest", help="intent.yaml / intract.yaml."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON report."),
    planfile: bool = typer.Option(False, "--planfile", help="Generate planfile-compatible tickets."),
):
    """Validate project contracts."""
    report = validate_project(path, manifest_path=manifest)

    if planfile:
        tickets = tickets_from_report(report)
        paths = PlanfileExporter(Path(path) / ".intract").export(tickets)
        console.print(f"[yellow]Generated {len(tickets)} ticket(s):[/] {paths['yaml']}")

    if json_output:
        console.print_json(json.dumps(report.to_dict(), ensure_ascii=False))
        return

    _print_validation_report(report)


@app.command()
def tickets(
    path: Path = typer.Argument(Path("."), help="Project path."),
    manifest: Path | None = typer.Option(None, "--manifest", help="intent.yaml / intract.yaml."),
):
    """Validate and export failed/partial/violating results as planfile-style tickets."""
    report = validate_project(path, manifest_path=manifest)
    tickets_ = tickets_from_report(report)
    paths = PlanfileExporter(Path(path) / ".intract").export(tickets_)

    console.print(f"[bold]Tickets:[/] {len(tickets_)}")
    for name, p in paths.items():
        console.print(f"- {name}: {p}")


@app.command()
def watch(
    path: Path = typer.Argument(Path("."), help="Folder to watch."),
    manifest: Path | None = typer.Option(None, "--manifest", help="intent.yaml / intract.yaml."),
    interval: float = typer.Option(1.0, "--interval", help="Polling interval in seconds."),
    planfile: bool = typer.Option(False, "--planfile", help="Generate tickets when validation fails."),
    once: bool = typer.Option(False, "--once", help="Run one validation pass and exit."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON report on change."),
):
    """Watch folder and re-validate Intract contracts when logical files change."""
    def run_validation(changed: list[str] | None = None) -> None:
        if changed:
            console.print(f"[cyan]Changed:[/] {', '.join(changed)}")
        report = validate_project(path, manifest_path=manifest)

        if planfile:
            tickets_ = tickets_from_report(report)
            PlanfileExporter(Path(path) / ".intract").export(tickets_)
            if tickets_:
                console.print(f"[yellow]Generated {len(tickets_)} ticket(s) in .intract/[/]")

        if json_output:
            console.print_json(json.dumps(report.to_dict(), ensure_ascii=False))
        else:
            console.print(f"[bold]Status:[/] {report.status.value}  "
                          f"pass={len(report.passed)} partial={len(report.partial)} "
                          f"fail={len(report.failed)} violations={len(report.violations)}")

    if once:
        run_validation()
        return

    console.print(f"[green]Watching[/] {path}  interval={interval}s")
    run_validation()

    def on_change(changes):
        run_validation(changes_to_paths(changes))

    try:
        watch_tree(path, on_change, config=WatchConfig(interval=interval))
    except KeyboardInterrupt:
        console.print("[yellow]Stopped.[/]")


@engine_app.command("suggest")
def engine_suggest(
    path: Path = typer.Argument(Path("."), help="Project path."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON."),
):
    """Analyze codebase and suggest @intract.v1 contracts for logical fragments."""
    result = scan_suggest_and_validate(EngineConfig(root=path))
    suggestions = result["suggestions"]

    if json_output:
        console.print_json(json.dumps({"suggestions": suggestions}, ensure_ascii=False))
        return

    table = Table(title="Suggested Intract contracts")
    table.add_column("File")
    table.add_column("Line")
    table.add_column("Confidence")
    table.add_column("Contract")

    for item in suggestions:
        table.add_row(
            item["file_path"],
            str(item["line"]),
            str(round(item["confidence"], 2)),
            item["contract_line"],
        )

    console.print(table)


@engine_app.command("drift")
def engine_drift(
    path: Path = typer.Argument(Path("."), help="Project path."),
    manifest: Path | None = typer.Option(None, "--manifest", help="intent.yaml / intract.yaml."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON."),
):
    """Detect logical codebase drift since the previous engine scan."""
    result = scan_suggest_and_validate(
        EngineConfig(root=path, manifest=str(manifest) if manifest else None)
    )

    if json_output:
        console.print_json(json.dumps(result, ensure_ascii=False))
        return

    drift = result["drift"]
    console.print(f"[bold]Files:[/] {result['files']}")
    console.print(f"[bold]Fragments:[/] {result['fragments']}")
    console.print(f"[bold]Drift issues:[/] {len(drift)}")

    table = Table(title="Logic drift")
    table.add_column("Severity")
    table.add_column("Kind")
    table.add_column("File")
    table.add_column("Message")

    for item in drift:
        table.add_row(item["severity"], item["kind"], item["file_path"], item["message"])

    console.print(table)


@engine_app.command("run")
def engine_run(
    path: Path = typer.Argument(Path("."), help="Project path."),
    manifest: Path | None = typer.Option(None, "--manifest", help="intent.yaml / intract.yaml."),
    planfile: bool = typer.Option(False, "--planfile", help="Generate tickets."),
    json_output: bool = typer.Option(False, "--json", help="Print JSON."),
):
    """Run full engine: scan fragments, suggest contracts, detect drift and validate."""
    result = scan_suggest_and_validate(
        EngineConfig(root=path, manifest=str(manifest) if manifest else None)
    )

    if planfile:
        # Build tickets from validation only; drift tickets will be added later.
        report = validate_project(path, manifest_path=manifest)
        tickets_ = tickets_from_report(report)
        PlanfileExporter(Path(path) / ".intract").export(tickets_)

    if json_output:
        console.print_json(json.dumps(result, ensure_ascii=False))
        return

    console.print(f"[bold]Files:[/] {result['files']}")
    console.print(f"[bold]Fragments:[/] {result['fragments']}")
    console.print(f"[bold]Suggestions:[/] {len(result['suggestions'])}")
    console.print(f"[bold]Drift:[/] {len(result['drift'])}")
    console.print(f"[bold]Validation:[/] {result['validation']['status']}")


def _print_validation_report(report) -> None:
    console.print(f"[bold]Project:[/] {report.project_path}")
    console.print(f"[bold]Status:[/] {report.status.value}")

    table = Table(title="Validation results")
    table.add_column("Status")
    table.add_column("Scope")
    table.add_column("Contract")
    table.add_column("Score")
    table.add_column("File")
    table.add_column("Missing / Violations")

    for result in report.results:
        issues = []
        issues.extend(result.missing)
        issues.extend(issue.message for issue in result.violations)
        table.add_row(
            result.status.value,
            result.scope,
            result.contract,
            str(result.score),
            result.file_path or "",
            "\\n".join(issues),
        )

    console.print(table)
