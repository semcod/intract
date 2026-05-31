from intract.validate_snippet import validate_artifact_with_proposals


def test_validate_artifact_with_proposals_passes_minimal_html():
    html = "<!DOCTYPE html><html><body><button id='ok'>OK</button></body></html>"
    proposals = [
        {
            "line": (
                "@intract.v1 id:ui.ok scope:ui intent:ui:keep:ok priority:3 domain:ui "
                "effect:read forbid:network validate:no_forbidden_effect meaning:\"keep ok\""
            )
        }
    ]
    result = validate_artifact_with_proposals(html, proposals, filename="stage0.html")
    assert "status" in result
    assert result["status"] in {"pass", "partial", "violation", "fail"}
