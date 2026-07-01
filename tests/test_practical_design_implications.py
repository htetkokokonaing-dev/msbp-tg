from pathlib import Path


def test_practical_design_implications_are_present_and_conservative():
    text = Path("manuscript/MSBP_Tg_Journal_Manuscript.md").read_text(encoding="utf-8")
    assert "Implications for polymer design workflows" in text
    assert "early-stage screening and interpretation coordinate" in text
    assert "does not replace full materials qualification" in text
    assert "not a guaranteed cost or time saving" in text
    assert "not to replace experimental qualification" in text

    forbidden = [
        "reduce polymer design cost by",
        "save millions",
        "replaces experimental Tg testing",
        "replace experimental Tg testing",
        "guaranteed cost reduction",
    ]
    lower = text.lower()
    for phrase in forbidden:
        assert phrase not in lower
