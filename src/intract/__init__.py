"""Intract — intent contracts for codebases."""

from .models import (
    Contract,
    ContractRecord,
    ContractSignature,
    ProjectReport,
    ValidationResult,
    ValidationStatus,
)
from .parser import extract_contract_records_from_text, parse_contract_line
from .parsers.toon import parse_toon_uri_line, load_toon_records
from .project import validate_project, validate_sources
from .signature import build_signature
from .manifest_ops import ManifestApplyResult, apply_ledger_to_manifest
from .proposals import ProposedContract, propose_ui_delta_contract_dicts, propose_ui_delta_contracts
from .validate_snippet import validate_artifact_with_proposals
from .validation import validate_contract_against_source
from .integrations.nexu import (
    IntentContract,
    format_intract_v1_line,
    parse_intract_line,
    scan_contracts_in_text,
    scan_contracts_in_file,
    read_manifest_contracts,
    read_toon_manifest_contracts,
)

__all__ = [
    "Contract",
    "ContractRecord",
    "ContractSignature",
    "ProjectReport",
    "ValidationResult",
    "ValidationStatus",
    "parse_contract_line",
    "extract_contract_records_from_text",
    "build_signature",
    "validate_contract_against_source",
    "validate_project",
    "validate_sources",
    "ProposedContract",
    "propose_ui_delta_contracts",
    "propose_ui_delta_contract_dicts",
    "ManifestApplyResult",
    "apply_ledger_to_manifest",
    "validate_artifact_with_proposals",
    "IntentContract",
    "format_intract_v1_line",
    "parse_intract_line",
    "scan_contracts_in_text",
    "scan_contracts_in_file",
    "read_manifest_contracts",
    "read_toon_manifest_contracts",
    "parse_toon_uri_line",
    "load_toon_records",
]

__version__ = "0.5.9"
