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
from .project import validate_project, validate_sources
from .signature import build_signature
from .validation import validate_contract_against_source

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
]

__version__ = "0.5.4"
