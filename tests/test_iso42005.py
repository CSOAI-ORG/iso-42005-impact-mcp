"""Smoke tests for iso-42005-impact-mcp."""
import sys, os, inspect, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    list_phases,
    impact_categories,
    assess_phase,
    run_full_impact_assessment,
    sign_attestation,
    cross_walk_eu_ai_act,
    cross_walk_iso_42001,
)


def test_phases_count_six():
    r = list_phases()
    assert len(r["phases"]) == 6
    assert {p["id"] for p in r["phases"]} == {"design", "development", "validation", "deployment", "monitoring", "decommissioning"}


def test_categories_count_seven():
    r = impact_categories()
    assert len(r["categories"]) == 7


def test_assess_phase_design():
    r = assess_phase("design", "credit scoring AI for personal loans")
    assert r["phase"]["id"] == "design"
    assert len(r["checklist"]) == 5


def test_assess_phase_unknown_returns_valid_list():
    r = assess_phase("WRONG", "anything")
    assert "error" in r
    assert len(r["valid"]) == 6


def test_full_assessment_high_risk_for_credit_scoring():
    r = run_full_impact_assessment(
        "AI credit scoring system using applicant demographic data and "
        "automated decisions for personal loan approvals"
    )
    assert r["overall_risk_level"] == "HIGH"
    assert any(c["category_id"] == "economic" and c["risk_score"] >= 50 for c in r["category_scores"])
    assert "signature" in r


def test_full_assessment_low_risk_for_innocuous():
    r = run_full_impact_assessment("AI tool that translates recipe ingredient quantities")
    assert r["overall_risk_level"] in ("LOW", "MEDIUM")


def test_sign_attestation_returns_id():
    fake = {"overall_risk_level": "HIGH", "category_scores": []}
    r = sign_attestation(fake)
    assert r["assessment_id"].startswith("iso42005_")
    assert "signature" in r and len(r["signature"]) > 5


def test_cross_walk_eu_ai_act_lists_articles():
    impact = {"high_risk_categories": ["Individual rights + freedoms"]}
    r = cross_walk_eu_ai_act(impact)
    arts = [m["article"] for m in r["article_mappings"]]
    assert any("Article 9" in a for a in arts)
    assert any("Article 10" in a for a in arts)
    assert any("Article 27" in a for a in arts)
    assert any("Article 5" in a for a in arts)  # added because of Individual rights flag


def test_cross_walk_iso_42001_includes_6_1_4():
    r = cross_walk_iso_42001({})
    clauses = [m["clause"] for m in r["clause_mappings"]]
    assert any("6.1.4" in c for c in clauses)


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    passed = failed = 0
    for fn in fns:
        try:
            fn()
            print(f"✓ {fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ {fn.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
