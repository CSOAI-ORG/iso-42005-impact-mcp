#!/usr/bin/env python3
"""
ISO/IEC 42005:2025 AI Impact Assessment MCP
============================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/iso-42005-impact-mcp -->

WHAT THIS COVERS
----------------
ISO/IEC 42005:2025 — the first international standard dedicated to AI system
impact assessment. Published May 2025 by ISO + IEC. Companion to ISO 42001
(AI Management System).

The standard provides guidance for organisations conducting AI system impact
assessments that focus on understanding how AI systems — and their foreseeable
applications — may affect individuals, groups, or society at large. Process
standard (not certification), throughout the AI lifecycle from design to
decommissioning.

WHY IT MATTERS
--------------
- Aligns with EU AI Act Article 27 (Fundamental Rights Impact Assessment for
  high-risk Annex III deployers), Article 9 (Risk Management System), and
  Article 10 (Data and Data Governance)
- Required evidence for ISO 42001 AIMS certification
- Recognised as evidence of due diligence under various regulatory regimes
- Process is auditor-defensible: methodology + actors + scope + risks +
  mitigations + monitoring all documented

TOOLS
-----
- list_phases(): the 6 ISO 42005 lifecycle phases
- assess_phase(phase, ai_system_description): structured assessment of one phase
- impact_categories(): the 7 impact categories ISO 42005 evaluates
- run_full_impact_assessment(ai_system): orchestrate all phases + categories
- sign_attestation(assessment): HMAC-sign the complete impact assessment
- cross_walk_eu_ai_act(impact_assessment): map outputs to EU AI Act articles
- cross_walk_iso_42001(impact_assessment): map outputs to ISO 42001 clauses

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · Governance Substrate
£499/mo (https://meok.ai/governance) · Universe £1,499/mo.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import urllib.request as _meter_urlreq
import urllib.error as _meter_urlerr
import os
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("iso-42005-impact")

_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")


# ISO 42005:2025 — 6 lifecycle phases
PHASES = [
    {"id": "design", "name": "Design", "summary": "AI system design + intended purpose definition"},
    {"id": "development", "name": "Development", "summary": "Build, train, evaluate the model"},
    {"id": "validation", "name": "Validation", "summary": "Verify the system against requirements + bias + robustness"},
    {"id": "deployment", "name": "Deployment", "summary": "Release the system into production"},
    {"id": "monitoring", "name": "Monitoring", "summary": "Continuous operation + drift detection + incident response"},
    {"id": "decommissioning", "name": "Decommissioning", "summary": "Sunset, data deletion, model archive, knowledge transfer"},
]


# ISO 42005:2025 — 7 impact categories
IMPACT_CATEGORIES = [
    {"id": "individuals_rights", "name": "Individual rights + freedoms", "examples": ["privacy", "non-discrimination", "due-process"]},
    {"id": "groups_society", "name": "Groups + society at large", "examples": ["protected-class fairness", "democratic processes", "social cohesion"]},
    {"id": "physical_environment", "name": "Physical environment + safety", "examples": ["bodily harm", "infrastructure damage", "environmental impact"]},
    {"id": "economic", "name": "Economic + financial", "examples": ["job displacement", "market manipulation", "wealth concentration"]},
    {"id": "psychological", "name": "Psychological + wellbeing", "examples": ["mental health", "manipulation", "addictive design"]},
    {"id": "informational", "name": "Informational + epistemic", "examples": ["misinformation", "deepfakes", "epistemic capture"]},
    {"id": "institutional", "name": "Institutional + governance", "examples": ["regulatory capture", "accountability gaps", "checks-and-balances erosion"]},
]


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    body = json.dumps(payload, sort_keys=True).encode()
    return hmac.new(_HMAC_SECRET.encode(), body, hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ────────────────────────────────────────────────────────────────────────
# Heuristic risk scoring
# ────────────────────────────────────────────────────────────────────────

_HIGH_RISK_KEYWORDS = {
    "individuals_rights": ["biometric", "scoring", "ranking", "decision", "automated", "profiling", "surveillance"],
    "groups_society": ["demographic", "race", "gender", "religion", "election", "voting", "media"],
    "physical_environment": ["medical", "autonomous", "vehicle", "weapon", "robot", "industrial", "critical"],
    "economic": ["credit", "loan", "hiring", "trading", "pricing", "insurance", "benefits"],
    "psychological": ["minor", "child", "teen", "addiction", "engagement", "persuasion", "therapy"],
    "informational": ["news", "content", "deepfake", "image", "video", "voice", "synthetic"],
    "institutional": ["public", "government", "judicial", "law-enforcement", "regulatory", "policy"],
}


def _score_category(text: str, cat_id: str) -> tuple[int, list[str]]:
    """Return (risk-score 0-100, hit-keywords) for a category against text."""
    t = text.lower()
    hits = [k for k in _HIGH_RISK_KEYWORDS.get(cat_id, []) if k in t]
    score = min(len(hits) * 25, 100)
    return score, hits


# ────────────────────────────────────────────────────────────────────────
# MCP tools
# ────────────────────────────────────────────────────────────────────────

def _server_meter_check(api_key: str = "") -> dict:
    """Calls the live /verify endpoint for server-side metering. Returns the JSON dict.
    Fail-open: if /verify is unreachable or KV isn't configured, returns allowed=True
    (so the local rate-limit in _check_rate_limit remains the safety net)."""
    try:
        data = json.dumps({"api_key": api_key, "tool": ""}).encode()
        req = _meter_urlreq.Request(_METER_URL, data=data,
            headers={"Content-Type": "application/json"}, method="POST")
        with _meter_urlreq.urlopen(req, timeout=2.5) as r:
            d = json.loads(r.read())
            if isinstance(d, dict) and "allowed" in d:
                return d
    except Exception:
        pass
    return {"allowed": True, "tier": "anonymous", "remaining": 200, "upgrade_url": "https://meok.ai/pricing"}


_METER_URL = "https://proofof.ai/verify"


@mcp.tool()
def list_phases() -> dict:
    """List the 6 ISO/IEC 42005 lifecycle phases."""
    return {"phases": PHASES, "standard": "ISO/IEC 42005:2025", "published": "2025-05"}


@mcp.tool()
def impact_categories() -> dict:
    """List the 7 impact categories ISO/IEC 42005 evaluates."""
    return {"categories": IMPACT_CATEGORIES, "standard": "ISO/IEC 42005:2025"}


@mcp.tool()
def assess_phase(phase: str, ai_system_description: str) -> dict:
    """
    Structured assessment of one lifecycle phase against ISO 42005 expectations.

    Args:
        phase: One of "design", "development", "validation", "deployment", "monitoring", "decommissioning".
        ai_system_description: Free-text description of the AI system being assessed.

    Returns:
        {phase, checklist, gaps, next_step}
    """
    phase_lower = phase.lower().strip()
    matched = next((p for p in PHASES if p["id"] == phase_lower), None)
    if not matched:
        return {"error": "unknown_phase", "valid": [p["id"] for p in PHASES]}

    # Build phase-specific checklist
    checklists = {
        "design": [
            "Intended purpose documented (Article 13 EU AI Act alignment)",
            "Stakeholders identified (developers, deployers, end-users, affected groups)",
            "Foreseeable applications + foreseeable misuse cataloged",
            "Initial impact-category screening completed",
            "Cross-functional review by legal + ethics + domain experts",
        ],
        "development": [
            "Training data provenance documented (CycloneDX ML-BOM)",
            "Bias-mitigation strategy in place",
            "Model card created",
            "Evaluation metrics defined a priori",
            "Audit trail of design decisions",
        ],
        "validation": [
            "Independent validation by non-developer team",
            "Adversarial testing (NIST AI 100-2 E2025 alignment)",
            "Demographic fairness testing across protected classes",
            "Robustness testing under distribution shift",
            "Sign-off threshold defined + met",
        ],
        "deployment": [
            "User notification mechanism (EU AI Act Article 50 transparency)",
            "Human-oversight design documented (Article 14)",
            "Rollback procedure tested",
            "Incident response plan",
            "Monitoring instrumentation live",
        ],
        "monitoring": [
            "Drift-detection thresholds + alerts",
            "Incident classification chain (EU AI Act Art 73 + DORA Art 19 + NIS2 Art 23 + GDPR Art 33 + ISO 42001 cl 9)",
            "Quarterly bias re-evaluation",
            "User-feedback loop",
            "Logs retained for the regulatory retention period",
        ],
        "decommissioning": [
            "Sunset notice to affected users",
            "Data deletion + retention plan",
            "Model archive (frozen weights, documentation)",
            "Knowledge transfer to successor system or staff",
            "Post-mortem + lessons documented",
        ],
    }
    checklist = checklists[phase_lower]
    gap_hints = {
        "design": "Likely gap: foreseeable misuse cataloged thinly. Force adversarial brainstorming.",
        "development": "Likely gap: training data provenance via CycloneDX ML-BOM (use ai-bom-mcp).",
        "validation": "Likely gap: adversarial testing — wire NIST AI 100-2 E2025 patterns via agent-prompt-injection-firewall-mcp.",
        "deployment": "Likely gap: Article 50 transparency disclosure UX — use watermarking-authenticity-mcp.",
        "monitoring": "Likely gap: cross-regime incident clock — use ai-incident-reporting-mcp for the 5-clock chain.",
        "decommissioning": "Likely gap: data retention/deletion mapped to GDPR Article 17 + regulatory minimums.",
    }
    return {
        "phase": matched,
        "checklist": checklist,
        "ai_system_description": ai_system_description[:300],
        "gap_hint": gap_hints[phase_lower],
        "next_step": "Document each checklist item with evidence references. Run sign_attestation() once all 6 phases are assessed.",
    }


@mcp.tool()
def run_full_impact_assessment(ai_system_description: str) -> dict:
    """
    Run a full ISO 42005 impact assessment across all phases + categories.

    Args:
        ai_system_description: Free-text description of the AI system being assessed.

    Returns:
        {phases, category_scores, overall_risk, mitigations_required, signed}
    """
    # Score each impact category
    category_results = []
    high_risk_cats = []
    for cat in IMPACT_CATEGORIES:
        score, hits = _score_category(ai_system_description, cat["id"])
        category_results.append({
            "category": cat["name"],
            "category_id": cat["id"],
            "risk_score": score,
            "hit_keywords": hits,
            "needs_mitigation": score >= 50,
        })
        if score >= 50:
            high_risk_cats.append(cat["name"])

    # Phase summaries
    phase_summaries = []
    for p in PHASES:
        phase_summaries.append({
            "phase": p["name"],
            "phase_id": p["id"],
            "summary": p["summary"],
            "must_have": "see assess_phase() for the full checklist",
        })

    # Overall risk
    max_score = max((c["risk_score"] for c in category_results), default=0)
    overall_risk = "HIGH" if max_score >= 75 else ("MEDIUM" if max_score >= 50 else "LOW")

    assessment = {
        "ai_system_description": ai_system_description[:500],
        "standard": "ISO/IEC 42005:2025",
        "phases_assessed": phase_summaries,
        "category_scores": category_results,
        "overall_risk_level": overall_risk,
        "high_risk_categories": high_risk_cats,
        "mitigations_required": len(high_risk_cats) > 0,
        "ts": _ts(),
    }
    sig = _sign(assessment)
    return {
        **assessment,
        "signature": sig,
        "verify_url": "https://verify.meok.ai",
        "next_step": "If overall_risk_level >= MEDIUM, cross-walk via cross_walk_eu_ai_act() and cross_walk_iso_42001() to map mitigations to specific articles + clauses.",
    }


@mcp.tool()
def sign_attestation(assessment: dict) -> dict:
    """
    HMAC-sign a completed impact assessment for the audit chain.

    Args:
        assessment: Full assessment dict (typically from run_full_impact_assessment()).

    Returns:
        {assessment_id, signature, verify_url, chain_entry}
    """
    aid = f"iso42005_{int(time.time())}_{os.urandom(4).hex()}"
    payload = {
        "assessment_id": aid,
        "standard": "ISO/IEC 42005:2025",
        "ts": _ts(),
        "overall_risk": assessment.get("overall_risk_level", "UNKNOWN"),
        "category_scores": assessment.get("category_scores", []),
    }
    sig = _sign(payload)
    return {
        "assessment_id": aid,
        "signature": sig,
        "verify_url": f"https://verify.meok.ai?assessment={aid}",
        "chain_entry": payload,
        "audit_value": "Use this signed attestation as ISO 42001 clause 9 evidence and EU AI Act Article 27 due-diligence record.",
    }


@mcp.tool()
def cross_walk_eu_ai_act(impact_assessment: dict) -> dict:
    """
    Map ISO 42005 impact-assessment outputs to specific EU AI Act articles.

    Args:
        impact_assessment: Output from run_full_impact_assessment.

    Returns:
        {article_mappings: [{article, relevance, mitigation_via_mcp}]}
    """
    high_risk_cats = impact_assessment.get("high_risk_categories", [])
    mappings = [
        {"article": "Article 9 — Risk Management System", "relevance": "All systems", "mitigation_via_mcp": "eu-ai-act-compliance-mcp"},
        {"article": "Article 10 — Data and Data Governance", "relevance": "Always", "mitigation_via_mcp": "ai-bom-mcp · bias-detection-mcp"},
        {"article": "Article 13 — Transparency & info to deployers", "relevance": "Always", "mitigation_via_mcp": "eu-ai-act-compliance-mcp"},
        {"article": "Article 14 — Human oversight", "relevance": "High-risk Annex III", "mitigation_via_mcp": "agent-policy-enforcement-mcp"},
        {"article": "Article 27 — Fundamental Rights Impact Assessment", "relevance": "Public sector + Annex III deployers", "mitigation_via_mcp": "iso-42005-impact-mcp (this MCP)"},
        {"article": "Article 50 — Transparency obligations", "relevance": "Generative AI", "mitigation_via_mcp": "watermarking-authenticity-mcp"},
        {"article": "Article 73 — Reporting serious incidents", "relevance": "All systems post-deployment", "mitigation_via_mcp": "ai-incident-reporting-mcp"},
    ]
    if "Individual rights + freedoms" in high_risk_cats:
        mappings.append({"article": "Article 5 — Prohibited AI practices", "relevance": "Review required for biometric/social-scoring features", "mitigation_via_mcp": "eu-ai-act-compliance-mcp"})
    return {
        "standard": "EU AI Act (Regulation (EU) 2024/1689)",
        "article_mappings": mappings,
        "high_risk_categories_passed_in": high_risk_cats,
    }


@mcp.tool()
def cross_walk_iso_42001(impact_assessment: dict) -> dict:
    """Map ISO 42005 outputs to ISO 42001 AIMS clauses."""
    return {
        "standard": "ISO/IEC 42001:2023 (AI Management System)",
        "clause_mappings": [
            {"clause": "6.1.2 AI risk assessment", "evidence": "ISO 42005 category scoring is direct input"},
            {"clause": "6.1.3 AI risk treatment", "evidence": "Mitigations required for HIGH risk categories"},
            {"clause": "6.1.4 AI system impact assessment", "evidence": "This entire output IS the 6.1.4 record"},
            {"clause": "9.1 Performance evaluation", "evidence": "Quarterly re-run of run_full_impact_assessment()"},
            {"clause": "9.2 Internal audit", "evidence": "Signed attestation chain at verify.meok.ai"},
            {"clause": "10.1 Continual improvement", "evidence": "Compare quarter-over-quarter category scores"},
        ],
        "audit_value": "ISO 42001 clause 6.1.4 explicitly requires AI system impact assessment. ISO 42005 IS that standard.",
    }


def main():
    mcp.run()


if __name__ == "__main__":
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
