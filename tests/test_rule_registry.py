from intract.validators.engine import validate_contract_against_source
from intract.validators.registry import RuleRegistry, get_rule_registry


def test_rule_registry_lists_builtin_rules():
    registry = get_rule_registry(discover=False)
    names = {rule.name for rule in registry.rules()}
    assert "input_presence" in names
    assert "output_presence" in names
    assert "return_value" in names
    assert "no_forbidden_effect" in names


def test_rule_registry_reports_per_rule_status():
    source = (
        "# @intract.v1 scope:function intent:validate:user forbid:network\n"
        "import requests\n"
        "def validate_user():\n"
        "    return requests.get('https://example.com')\n"
    )
    from intract.core.signatures import build_signatures
    from intract.parsers.inline import extract_contract_records_from_text

    records = extract_contract_records_from_text(source, file_path="auth.py")
    signature = build_signatures(records)[0]
    result = validate_contract_against_source(signature, source)

    assert "rules" in result.evidence
    assert result.evidence["rules"]["no_forbidden_effect"] == "fail"


def test_rule_registry_discovers_entry_points():
    registry = get_rule_registry(discover=True)
    names = {rule.name for rule in registry.rules()}
    assert len(names) >= 4


def test_custom_rule_can_be_registered():
    from intract.validators.base import RuleResult, ValidationContext

    class AlwaysPassRule:
        name = "always_pass"

        def supports(self, validators):
            return True

        def validate(self, signature, source, context: ValidationContext) -> RuleResult:
            return RuleResult(name=self.name, score=1.0)

    registry = RuleRegistry()
    registry.register(AlwaysPassRule())
    assert "always_pass" in {rule.name for rule in registry.rules()}
