# ISO/IEC 42005:2025 AI Impact Assessment MCP

> ## 🧱 Part of the MEOK Governance Substrate
>
> 10 governance MCPs as one signed pipeline for **£499/mo** with full
> EU AI Act + DORA + NIS2 + CRA + UK AI Bill coverage.
> See [meok.ai/governance](https://meok.ai/governance).

# First international standard for AI impact assessment

<!-- mcp-name: io.github.CSOAI-ORG/iso-42005-impact-mcp -->

[![PyPI](https://img.shields.io/pypi/v/iso-42005-impact-mcp)](https://pypi.org/project/iso-42005-impact-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io)

## What this standardises

ISO/IEC 42005:2025 was published in May 2025 as **the first international standard dedicated to AI system impact assessment**. It's a companion to ISO/IEC 42001:2023 (AI Management System) and provides the methodology that satisfies ISO 42001 clause 6.1.4.

It also produces evidence that satisfies:

- **EU AI Act Article 27** — Fundamental Rights Impact Assessment for high-risk Annex III deployers
- **EU AI Act Article 9** — Risk Management System
- **EU AI Act Article 10** — Data and Data Governance
- **GDPR Article 35** — Data Protection Impact Assessment (parts of)
- **UK ICO AI Auditing Framework** — recognised methodology

If you're pursuing ISO 42001 certification, you cannot skip ISO 42005 — clause 6.1.4 explicitly requires it. If you're an Annex III deployer under the EU AI Act, Article 27 effectively requires it.

## What this MCP does

7 tools that automate the ISO 42005 process across **6 lifecycle phases × 7 impact categories** = 42 assessment cells per AI system:

| Tool | Purpose |
|---|---|
| `list_phases()` | The 6 lifecycle phases (design → development → validation → deployment → monitoring → decommissioning) |
| `impact_categories()` | The 7 impact categories (individual rights · groups/society · physical · economic · psychological · informational · institutional) |
| `assess_phase(phase, ai_system)` | Structured checklist for one phase + gap hints |
| `run_full_impact_assessment(ai_system)` | Orchestrate all 6 × 7 cells + score categories + tag high-risk |
| `sign_attestation(assessment)` | HMAC-sign the result for the audit chain |
| `cross_walk_eu_ai_act(assessment)` | Map outputs to specific EU AI Act articles |
| `cross_walk_iso_42001(assessment)` | Map outputs to specific ISO 42001 clauses |

Output is auditor-defensible JSON with signed attestations verifiable at `verify.meok.ai`.

## Quick install

```bash
uvx iso-42005-impact-mcp
pip install iso-42005-impact-mcp
```

```json
{
  "mcpServers": {
    "iso-42005-impact": {
      "command": "uvx",
      "args": ["iso-42005-impact-mcp"]
    }
  }
}
```

## Worked example

```python
{"tool": "run_full_impact_assessment", "args": {
  "ai_system_description":
    "AI credit-scoring system for personal loans, deployed by a UK bank. "
    "Uses applicant demographic + transaction history. Automated decision "
    "with human-in-loop review for borderline cases."
}}
```

→ returns category scores (Economic = 100/100 HIGH, Individual rights = 75/100 HIGH, Institutional = 25/100 LOW), overall risk HIGH, mitigations required across Article 9 + 10 + 14 + 27, signed attestation, verify URL.

Pipe that into `cross_walk_eu_ai_act()` to get the article-by-article mitigation map pointing to specific sibling MCPs.

## Sister MCPs

Part of the MEOK **Governance** pack:

- `eu-ai-act-compliance-mcp` — Article 9 / 10 / 13 / 14 / 50 / 73 coverage
- `dora-compliance-mcp` — financial-sector ICT risk
- `nis2-compliance-mcp` — essential entities incident reporting
- `ai-bom-mcp` — CycloneDX 1.6 ML-BOM training data provenance
- `bias-detection-mcp` — Article 10 fairness metrics
- `watermarking-authenticity-mcp` — Article 50 transparency
- `ai-incident-reporting-mcp` — 5-clock incident chain (Art 73 / DORA Art 19 / NIS2 Art 23 / GDPR Art 33 / ISO 42001 cl 9)

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Protocol coverage + Universal PAYG

- ✅ **MCP** (Anthropic) — native
- ✅ **A2A** (Google + LF) — native
- ✅ **IBM ACP** — covered via A2A merge
- ◐ **Stripe ACP** (Agentic Commerce) — bridge via `agent-commerce-protocol-mcp`
- ◐ **AP2** (Google Payments) — bridge via `agent-commerce-payments-mcp`
- ◐ **x402** (Coinbase HTTP 402) — gateway support

| Option | Price | Best for |
|---|---|---|
| Self-host (this MCP) | £0 — MIT | Devs |
| Universal PAYG | £29/mo + £0.0002/call | Spiky usage |
| Governance Substrate | £499/mo | All 10 governance MCPs |
| Universe | £1,499/mo | All 48 MEOK MCPs |
| Defence | £4,990/mo | Enterprise + on-prem |

Buy: https://meok.ai/governance

## Wire it up — full stack

Pair this with the MEOK chain that turns one agent action into ONE signed compliance event:

1. **bft-progress-council-mcp** — anti-loop guardrail
2. **agent-token-budget-mcp** — hard spend cap
3. **agent-prompt-injection-firewall-mcp** — OWASP LLM01 scan
4. **agent-audit-logger-mcp** — hash-chained evidence
5. **a2a-governance-bridge-mcp** — fold N attestations → 1 signed event
6. **agent-incident-relay-mcp** — broadcast incidents to 5 regimes simultaneously

See [meok.ai/mcp-stack](https://meok.ai/mcp-stack) for the full architecture and [meok.ai/mcp-stack/demo](https://meok.ai/mcp-stack/demo) for the live in-browser demo.

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677). Not legal advice — pair with qualified counsel for production deployments.
