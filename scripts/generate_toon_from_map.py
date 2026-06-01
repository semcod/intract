#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urlencode

from intract.parsers.inline import parse_contract_line
from intract.propose_llm import propose_contracts_llm


@dataclass(frozen=True)
class FunctionTarget:
    file_path: str
    function_name: str


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", ".", value.strip().lower())
    cleaned = re.sub(r"\.+", ".", cleaned).strip(".")
    return cleaned or "item"


def _parse_intent_from_name(name: str) -> str:
    text = name.strip()
    if not text:
        return "implement:unknown"
    snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text).lower()
    parts = [p for p in re.split(r"[_\-\.]+", snake) if p]
    if len(parts) == 1:
        return f"implement:{parts[0]}"
    return f"{parts[0]}:{'_'.join(parts[1:])}"


def _parse_modules(lines: list[str]) -> list[str]:
    modules: list[str] = []
    in_modules = False
    for line in lines:
        if line.startswith("M["):
            in_modules = True
            continue
        if in_modules and line.startswith("D:"):
            break
        if not in_modules:
            continue
        if line.startswith("  "):
            value = line.strip()
            if not value:
                continue
            if "," in value:
                value = value.split(",", 1)[0]
            modules.append(value)
    return modules


def _parse_functions(lines: list[str]) -> list[FunctionTarget]:
    targets: list[FunctionTarget] = []
    in_details = False
    current_file: str | None = None

    def add_name(name: str) -> None:
        symbol = name.strip()
        if not symbol or not current_file:
            return
        if symbol.startswith("_"):
            return
        if symbol in {"if", "for", "while", "switch", "catch"}:
            return
        targets.append(FunctionTarget(file_path=current_file, function_name=symbol))

    for raw in lines:
        line = raw.rstrip("\n")
        if line.startswith("D:"):
            in_details = True
            continue
        if not in_details:
            continue
        file_match = re.match(r"^ {2}([^:\n]+):$", line)
        if file_match:
            current_file = file_match.group(1)
            continue
        if current_file is None:
            continue

        signature = re.match(r"^ {4}([A-Za-z_]\w*)\([^)]*\)", line)
        if signature:
            add_name(signature.group(1))
            continue

        class_methods = re.match(r"^ {4}([A-Za-z_]\w*):\s*(.+)$", line)
        if class_methods:
            methods_blob = class_methods.group(2)
            for chunk in methods_blob.split(","):
                method_match = re.match(r"\s*([A-Za-z_]\w*)\(", chunk)
                if method_match:
                    add_name(method_match.group(1))

    unique = {(item.file_path, item.function_name): item for item in targets}
    return list(unique.values())


def _contract_fragment(
    *,
    contract_id: str,
    intent: str,
    scope: str,
    priority: int,
    domain: str,
    forbid: tuple[str, ...] = (),
    req: tuple[str, ...] = (),
    validate: tuple[str, ...] = (),
    meaning: str = "",
) -> str:
    params: list[tuple[str, str]] = [
        ("id", contract_id),
        ("intent", intent),
        ("scope", scope),
        ("priority", str(priority)),
        ("domain", domain),
    ]
    if forbid:
        params.append(("forbid", ",".join(forbid)))
    if req:
        params.append(("req", ",".join(req)))
    if validate:
        params.append(("validate", ",".join(validate)))
    if meaning:
        params.append(("meaning", meaning))
    return urlencode(params, quote_via=quote, safe=",:_-.")


def _toon_uri(file_path: str, *, query: dict[str, str] | None = None, fragment: str) -> str:
    query_part = ""
    if query:
        query_part = "?" + urlencode(query, quote_via=quote, safe="/_-.")
    return f"intract://{file_path}{query_part}#{fragment}"


def _llm_contract_fragment(
    *,
    file_path: str,
    symbol: str,
    goal: str,
    model: str | None,
) -> str | None:
    pseudo_source = (
        f"# symbol from code2llm map\n"
        f"# file: {file_path}\n"
        f"def {symbol}(...):\n"
        f"    pass\n"
    )
    proposals = propose_contracts_llm(
        pseudo_source,
        goal=(
            goal
            or "Propose one strict function contract for this symbol; include id, intent, scope:function, domain,"
            " forbid/validate only when useful."
        ),
        fragment_name=f"{file_path}:{symbol}",
        model=model,
    )
    if not proposals:
        return None
    parsed = parse_contract_line(proposals[0].line, default_scope="function")
    if parsed is None:
        return None
    intent = f"{parsed.action}:{parsed.object}" if parsed.action and parsed.object else _parse_intent_from_name(symbol)
    contract_id = parsed.contract_id or f"fn.{_slug(file_path)}.{_slug(symbol)}"
    return _contract_fragment(
        contract_id=contract_id,
        intent=intent,
        scope="function",
        priority=parsed.priority,
        domain=parsed.domain or "auto",
        forbid=tuple(parsed.forbidden),
        req=tuple(parsed.required),
        validate=tuple(parsed.validators),
        meaning=parsed.meaning,
    )


def generate_toon_lines(
    *,
    map_file: Path,
    include_project: bool,
    include_files: bool,
    include_functions: bool,
    llm: bool,
    llm_goal: str,
    llm_model: str | None,
) -> list[str]:
    content = map_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    modules = _parse_modules(lines)
    functions = _parse_functions(lines)

    out: list[str] = []
    out.append("# Auto-generated from code2llm map.toon.yaml")
    out.append(f"# source: {map_file}")

    if include_project:
        fragment = _contract_fragment(
            contract_id="project.auto.overview",
            intent="analyze:project",
            scope="project",
            priority=2,
            domain="governance",
            validate=("required_intents",),
            meaning="project-level auto-generated governance contract",
        )
        out.append(_toon_uri(".", fragment=fragment))

    if include_files:
        for file_path in sorted(set(modules)):
            file_slug = _slug(file_path)
            fragment = _contract_fragment(
                contract_id=f"file.{file_slug}",
                intent="implement:file_module",
                scope="file",
                priority=3,
                domain="architecture",
                validate=("no_forbidden_effect",),
                meaning="auto-generated file contract",
            )
            out.append(_toon_uri(file_path, fragment=fragment))

    if include_functions:
        for target in sorted(functions, key=lambda x: (x.file_path, x.function_name)):
            fn_slug = _slug(target.function_name)
            file_slug = _slug(target.file_path)
            if llm:
                fragment = _llm_contract_fragment(
                    file_path=target.file_path,
                    symbol=target.function_name,
                    goal=llm_goal,
                    model=llm_model,
                )
                if fragment is None:
                    fragment = _contract_fragment(
                        contract_id=f"fn.{file_slug}.{fn_slug}",
                        intent=_parse_intent_from_name(target.function_name),
                        scope="function",
                        priority=3,
                        domain="auto",
                        validate=("return_value", "no_forbidden_effect"),
                        meaning="fallback auto-generated function contract",
                    )
            else:
                fragment = _contract_fragment(
                    contract_id=f"fn.{file_slug}.{fn_slug}",
                    intent=_parse_intent_from_name(target.function_name),
                    scope="function",
                    priority=3,
                    domain="auto",
                    validate=("return_value", "no_forbidden_effect"),
                    meaning="auto-generated function contract",
                )

            out.append(
                _toon_uri(
                    target.file_path,
                    query={"func": target.function_name},
                    fragment=fragment,
                )
            )

    return out


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate flat Intract .toon URI manifest from code2llm map.toon.yaml"
    )
    parser.add_argument("--map", dest="map_file", type=Path, required=True, help="Path to map.toon.yaml")
    parser.add_argument(
        "--output",
        dest="output_file",
        type=Path,
        default=Path("project/generated.intract.toon"),
        help="Output .toon file path",
    )
    parser.add_argument("--no-project", action="store_true", help="Skip project-level contract")
    parser.add_argument("--no-files", action="store_true", help="Skip file-level contracts")
    parser.add_argument("--no-functions", action="store_true", help="Skip function-level contracts")
    parser.add_argument("--llm", action="store_true", help="Use LLM enrichment for function contracts")
    parser.add_argument("--llm-goal", default="", help="Goal/context passed to LLM")
    parser.add_argument("--llm-model", default=None, help="Optional model override for LLM")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run `python -m intract validate <root> --manifest <output>` after generation",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Validation root path when --validate is used",
    )
    return parser


def _run_validate(root: Path, manifest: Path) -> int:
    import subprocess

    cmd = [sys.executable, "-m", "intract", "validate", str(root), "--manifest", str(manifest)]
    proc = subprocess.run(cmd)
    return int(proc.returncode)


def _ensure_parent(path: Path) -> None:
    if path.parent and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)


def main(argv: Iterable[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not args.map_file.exists():
        print(f"[error] map file not found: {args.map_file}", file=sys.stderr)
        return 2

    try:
        lines = generate_toon_lines(
            map_file=args.map_file,
            include_project=not args.no_project,
            include_files=not args.no_files,
            include_functions=not args.no_functions,
            llm=args.llm,
            llm_goal=args.llm_goal,
            llm_model=args.llm_model,
        )
    except RuntimeError as exc:
        print(f"[error] LLM enrichment failed: {exc}", file=sys.stderr)
        return 3

    _ensure_parent(args.output_file)
    args.output_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(f"[ok] generated: {args.output_file} ({len(lines)} lines)")

    if args.validate:
        return _run_validate(args.root, args.output_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
