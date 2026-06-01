from pathlib import Path

from intract.core.cache import IntractDecisionCache


def test_decision_cache_lifecycle(tmp_path: Path):
    cache = IntractDecisionCache(tmp_path)
    
    code = "def process_payment(amount):\n    print('Charging', amount)"
    rules = ["forbid:network", "require:logging"]
    
    # Cache miss initially
    assert cache.get_decision(code, rules) is None
    
    # Store decision (learning phase)
    cache.set_decision(
        code_snippet=code,
        contract_rules=rules,
        decision="PASS",
        rationale="Function only logs locally using print, no network requests found.",
        learned_rules=["print_is_not_network"],
        metadata={"model": "qwen3-coder"}
    )
    
    # Cache hit
    entry = cache.get_decision(code, rules)
    assert entry is not None
    assert entry.decision == "PASS"
    assert "print_is_not_network" in entry.learned_rules
    
    # Reload from filesystem
    new_cache = IntractDecisionCache(tmp_path)
    loaded_entry = new_cache.get_decision(code, rules)
    assert loaded_entry is not None
    assert loaded_entry.rationale.startswith("Function only logs")
