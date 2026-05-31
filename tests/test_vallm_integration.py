from pathlib import Path

from intract.integrations.vallm import validate_for_vallm, validate_proposal


ROOT = Path(__file__).resolve().parents[1]
WEB_APP = ROOT / "examples" / "web-app"
MANIFEST = WEB_APP / "intract.yaml"


def test_validate_for_vallm_web_app_v1_pass():
    result = validate_for_vallm(
        str(WEB_APP / "iterations/v1-pass"),
        manifest=str(MANIFEST),
    )
    assert result.status == "pass"
    assert result.score == 1.0


def test_validate_proposal_maps_violation():
    result = validate_proposal(
        "# @intract.v1 scope:function intent:auth:check forbid:network\n"
        "def check():\n"
        "    return requests.get('https://example.com')\n",
        filename="auth.py",
    )
    assert result.status == "violation"
    assert result.score == 0.0
    assert any(issue.severity == "error" for issue in result.issues)
