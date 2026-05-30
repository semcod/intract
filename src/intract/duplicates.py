"""Backward-compatible re-exports. Prefer `intract.duplicates`."""

from intract.duplicates import DuplicateContract, find_duplicate_contracts

__all__ = ["DuplicateContract", "find_duplicate_contracts"]
