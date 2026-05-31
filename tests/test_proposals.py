from intract.proposals import propose_ui_delta_contracts


def test_propose_ui_delta_delete_and_keep():
    proposals = propose_ui_delta_contracts(
        stage=0,
        keep=["screen"],
        delete=["Mod", "deg"],
        capsule="scientific_calc",
    )
    assert len(proposals) == 3
    kinds = {p.kind for p in proposals}
    assert kinds == {"delete", "keep"}
    delete_mod = next(p for p in proposals if p.element == "Mod")
    assert "@intract.v1" in delete_mod.line
    assert "ui:remove:Mod" in delete_mod.line
    assert "scientific_calc" in delete_mod.id
