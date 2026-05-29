from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from . import __version__
from .parser import extract_contract_records_from_text
from .project import validate_project
from .yaml_manifest import create_sample_manifest

app = typer.Typer(help="Intract — intent contracts for codebases.")
console = Console()


@app.callback(invoke_without_command=True)
def main(version: bool = typer.Option(False, "--version", help="Show version.")):
    if version:
        console.print(f"intract {__version__}")
        raise typer.Exit()


@app.command()
def init(path: Path = typer.Argument(Path("."), help="Project path."), force: bool = typer.Option(False, "--force", help="Overwrite existing intent.yaml.")):
    """Create a sample intent.yaml manifest."""
    target = path / "intent.yaml"
    if target.exists() and not force:
        console.print(f"[red]File already exists:[/] {target}")
        raise typer.Exit(1)
    target.write_text(create_sample_manifest(), encoding="utf-8")
    console.print(f"[green]Created[/] {target}")


@app.command()
def scan(path: Path = typer.Argument(Path("."), help="File or directory."), json_output: bool = typer.Option(False, "--json", help="Print JSON.")):
    """Scan files for inline @intract contracts."""
    records = []
    if path.is_file():
        records.extend(extract_contract_records_from_text(path.read_text(encoding="utf-8"), file_path=str(path)))
    else:
        for file_path in path.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix not in {".py", ".js", ".ts", ".cs", ".java", ".go", ".rs", ".md"}:
                continue
            try:
                records.extend(extract_contract_records_from_text(file_path.read_text(encoding="utf-8"), file_path=str(file_path.relative_to(path))))
            except UnicodeDecodeError:
                continue

    data = [{"file": r.file_path, "line": r.start_line, "scope": r.contract.scope, "intent": r.contract.key, "priority": r.contract.priority, "domain": r.contract.domain} for r in records]
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
        table.add_row(item["file"], str(item["line"]), item["scope"], item["intent"], str(item["priority"]), item["domain"])
    console.print(table)


@app.command()
def validate(path: Path = typer.Argument(Path("."), help="Project path."), manifest: Path | None = typer.Option(None, "--manifest", help="intent.yaml / intract.yaml."), json_output: bool = typer.Option(False, "--json", help="Print JSON report.")):
    """Validate project contracts."""
    report = validate_project(path, manifest_path=manifest)
    if json_output:
        console.print_json(json.dumps(report.to_dict(), ensure_ascii=False))
        return

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
        table.add_row(result.status.value, result.scope, result.contract, str(result.score), result.file_path or "", "\\n".join(issues))
    console.print(table)
