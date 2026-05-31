from pathlib import Path

from intract.integrations.redup import parse_policy_tokens, validate_for_redup


ROOT = Path(__file__).resolve().parents[1]
FULL_STACK = ROOT / "examples" / "full-stack"


def test_validate_for_redup_passes_full_stack():
    result = validate_for_redup(
        FULL_STACK,
        manifest=FULL_STACK / "intract.yaml",
        fail_on=["violation", "missing_required_p1"],
        warn_on=["partial"],
    )
    assert not result.should_fail
    assert result.validation_status == "pass"


def test_validate_for_redup_fails_on_intent_duplicate():
    groups = [
        {
            "group_id": "intent_0001",
            "evidence": {"contracts": ["parse.extensions", "parse.extension_list"]},
        }
    ]
    result = validate_for_redup(
        FULL_STACK,
        manifest=FULL_STACK / "intract.yaml",
        intent_groups=groups,
        fail_on=["intent_duplicate"],
        warn_on=[],
    )
    assert result.should_fail
    assert any("intent_duplicate" in reason for reason in result.reasons)


def test_parse_policy_tokens_csv():
    assert parse_policy_tokens("violation, intent_duplicate") == ["violation", "intent_duplicate"]
