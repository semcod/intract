from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CacheEntry:
    code_hash: str
    contract_hash: str
    decision: str  # PASS, PARTIAL, VIOLATION
    rationale: str
    learned_rules: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class IntractDecisionCache:
    """Git-friendly, text-based JSON ledger cache for Intract's decision-making system.
    
    This cache stores compiled LLM facts and static analysis outcomes to guarantee:
    1. Zero cost/network calls on unchanged code.
    2. Version-controlled "learned" rules shared via Git.
    3. High auditability and easy manual verification by developers.
    """
    
    def __init__(self, cache_dir: Path | str):
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / "decision_ledger.json"
        self.entries: dict[str, CacheEntry] = {}
        self.load()

    def _hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _get_key(self, code_snippet: str, contract_rules: list[str]) -> str:
        code_h = self._hash(code_snippet.strip())
        rules_h = self._hash(",".join(sorted(contract_rules)))
        return f"{code_h}:{rules_h}"

    def load(self) -> None:
        if not self.cache_file.exists():
            return
        try:
            data = json.loads(self.cache_file.read_text(encoding="utf-8"))
            for k, v in data.items():
                self.entries[k] = CacheEntry(
                    code_hash=v["code_hash"],
                    contract_hash=v["contract_hash"],
                    decision=v["decision"],
                    rationale=v["rationale"],
                    learned_rules=v.get("learned_rules", []),
                    metadata=v.get("metadata", {}),
                )
        except Exception:
            # Tolerant loading
            self.entries = {}

    def save(self) -> None:
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        out = {k: asdict(v) for k, v in self.entries.items()}
        try:
            self.cache_file.write_text(
                json.dumps(out, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception:
            pass

    def get_decision(self, code_snippet: str, contract_rules: list[str]) -> CacheEntry | None:
        key = self._get_key(code_snippet, contract_rules)
        return self.entries.get(key)

    def set_decision(
        self,
        code_snippet: str,
        contract_rules: list[str],
        decision: str,
        rationale: str,
        learned_rules: list[str] = None,
        metadata: dict[str, Any] = None,
    ) -> CacheEntry:
        code_h = self._hash(code_snippet.strip())
        rules_h = self._hash(",".join(sorted(contract_rules)))
        key = f"{code_h}:{rules_h}"
        
        entry = CacheEntry(
            code_hash=code_h,
            contract_hash=rules_h,
            decision=decision,
            rationale=rationale,
            learned_rules=learned_rules or [],
            metadata=metadata or {},
        )
        self.entries[key] = entry
        self.save()
        return entry
