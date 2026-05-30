from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from intract.core.models import ContractRecord
from intract.parsers.manifest import contract_from_mapping


def parse_openapi_contracts(path: Path) -> list[ContractRecord]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    records: list[ContractRecord] = []
    paths = data.get("paths", {}) or {}

    for route, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            x = operation.get("x-intract")
            if not isinstance(x, dict):
                continue
            contract = contract_from_mapping({**x, "scope": x.get("scope", "endpoint")})
            records.append(
                ContractRecord(
                    contract=contract,
                    file_path=str(path),
                    start_line=1,
                    end_line=1,
                    owner=f"{str(method).upper()} {route}",
                )
            )
    return records


def parse_openapi_text(content: str, *, file_path: str = "openapi.yaml") -> list[ContractRecord]:
    data = yaml.safe_load(content) or {}
    records: list[ContractRecord] = []
    paths = data.get("paths", {}) or {}

    for route, methods in paths.items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            x = operation.get("x-intract")
            if not isinstance(x, dict):
                continue
            contract = contract_from_mapping({**x, "scope": x.get("scope", "endpoint")})
            records.append(
                ContractRecord(
                    contract=contract,
                    file_path=file_path,
                    start_line=1,
                    end_line=1,
                    owner=f"{str(method).upper()} {route}",
                )
            )
    return records
