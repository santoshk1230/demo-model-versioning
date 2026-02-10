# Confluence Documentation Structure for Models

This guide outlines how to structure the model documentation in Confluence to align with the Git-based metadata and README.

---

## Page Hierarchy

```
Confluence Space: Data Science Models
│
└── asset_basic_score — Model Overview (MAIN PAGE)
    ├── asset_basic_score — Validation Archive (optional)
    ├── asset_basic_score — Approval History (optional)
    └── asset_basic_score — Runbook (optional, ops-only)
```

Each model has **ONE primary page** with optional linked supporting pages.

---

## MAIN PAGE Template: `asset_basic_score — Model Overview`

### At-a-Glance (Top of page, always visible)

```
Model Name: Asset Basic Score
Owner: Data Science Team – [Name]
Current Production Version (Base Model): v1.0.0
Current Production Version (Client Configs): See table below
Model Type: Rule-based
Status: Active
Last Reviewed: [YYYY-MM-DD]
Confluence Page Link: [This page URL]
Git Repository: [GitHub repo link]
```

---

### 1. Model Identity

**Canonical Model ID:** asset_basic_score_001  
**Domain:** Credit Risk, Fraud Prevention, Customer Onboarding  
**Primary Objective:** Unified trust and risk scoring for multi-client lending and fintech partners  
**Output:** Composite score (0–1000, configurable per client) + rule-level transparency  
**Explainability:** Rule-level reason codes and trigger breakdowns  
**Consumers:** Lambda APIs, batch pipelines, downstream decisioning systems, dashboards  
**Deployment:** Real-time (API) + Batch (scheduled)  
**Risk Tier:** Medium

---

### 2. Business Context & Use Cases

**Problem Statement:**  
Raw signals (phone validity, address completeness, identity matches, financial indicators) are weak individually but collectively informative for customer risk. This model combines these signals into interpretable scores for different lending contexts.

**Primary Use Cases:**
- Pre-contact prioritization and verification workflow optimization
- Customer onboarding risk assessment
- Fraud prevention and account opening validation
- Operational confidence scoring for multiple lending partners

**Out of Scope:**
- Detailed fraud network detection
- Credit score prediction (independent)
- Customer intent or behavior modeling

---

### 3. Data & Inputs (High Level)

**Enriched Data Signals:**
- Email and phone vintage (years since first observed)
- Name matching across data sources
- Phone recency and reachability
- Address quality and verification status

**Social & Digital Signals:**
- WhatsApp presence and business registration
- Social platform presence (Flipkart, etc.)
- UPI availability
- Digital identity footprint

**Verification Signals:**
- PAN and GST status
- Tax payer information
- CDSL/Demat account presence

**Metadata:**
- Client name
- Product/use case
- Channel

---

### 4. Logic / Method

**Approach:**  
Deterministic, rule-based scoring with configurable thresholds per client.

1. **Rule Evaluation:** Each rule (e.g., "email_first_seen_year_trigger") evaluates input signals against thresholds.
2. **Trigger Scoring:** Rules produce positive or negative scores; sequential triggers (some rules skip depending on prior results).
3. **Aggregation:** Trigger scores are summed, plus base score (typically 350).
4. **Output:** Composite score + per-rule result explanation.

**Why Rule-Based:**
- Explainability required in regulated credit environments
- Deterministic behavior for reproducibility and audit
- Client customization without model retraining
- Rapid iteration on thresholds without data science overhead

**Extensibility:**
- New rules added as JSON entries; no code change required
- Base model supports any rule operator (between_1, token_ratio, null_check, etc.)
- Client-specific configs allow independent evolution

---

### 5. Validation & Performance (Summary Only)

| Metric | Value | Notes |
|--------|-------|-------|
| **Validation Type** | Backtesting + Shadow Run | |
| **Test Dataset** | Historical contact outcomes (Oct–Dec 2025) | 4,500+ records per client |
| **Rules Firing** | 20–25 per client | Varies by config |
| **Score Distribution Stability** | Stable across clients | PSI < 0.15 |
| **Known Limitations** | Sensitive to phone data freshness; address signals remain marginal | Monitor via data drift alerts |

**Link to Validation Archive:** [Confluence page for detailed validation evidence]

---

### 6. Monitoring & Alerts

**Monitored Metrics:**
- Score distribution drift (PSI)
- Input volume and quality
- Rule hit rates and trigger distribution
- High/low score band concentration

**Alerting:**
- Weekly checks for distribution drift
- Immediate alerts on input volume anomalies
- Monthly rule-level performance review

**Channels:** Data Science team Slack / email

---

### 7. Change Log & Versioning

#### Base Model (Rule Engine Core)
| Version | Change Type | What Changed | Why | Impact | Status |
|---------|-------------|--------------|-----|--------|--------|
| v1.0.0 | INITIAL | Initial rule engine implementation | Consolidate multi-client scoring logic | N/A | Production |

#### Client-Specific Configurations
| Client | Version | Change Type | What Changed | Impact | Status |
|--------|---------|-------------|--------------|--------|--------|
| **pocketly** | v1.0.0 | INITIAL | 21 rules, thresholds for age/phone/fintech signals | N/A | Production |
| **fibe** | v1.0.0 | INITIAL | 15 rules, tailored for FIBE onboarding | N/A | Production |
| **larsontubro** | v1.0.0 | INITIAL | 18 rules, focus on DI + digital vintage | N/A | Production |

**Versioning Policy:**
- **PATCH:** Threshold tuning, bug fixes (no output schema change)
- **MINOR:** New rules, enhanced logic (output distribution may shift)
- **MAJOR:** Rule removal, input contract changes (requires re-approval)

See README.md for full versioning details.

---

### 8. Approvals (Summary)

| Version | Reviewed By | Decision | Date | Notes |
|---------|-------------|----------|------|-------|
| Base Model v1.0.0 | [Reviewer Name] | Approved | [YYYY-MM-DD] | No exceptions |
| POCKETLY config v1.0.0 | [Reviewer Name] | Approved | [YYYY-MM-DD] | No exceptions |
| FIBE config v1.0.0 | [Reviewer Name] | Approved | [YYYY-MM-DD] | No exceptions |
| LARSONTUBRO config v1.0.0 | [Reviewer Name] | Approved | [YYYY-MM-DD] | No exceptions |

**Link to Approval History:** [Confluence page for detailed approval records]

---

### 9. Ops & Support (Summary)

**Execution Schedule (Batch):**
- Daily scheduled job
- Input availability: <timezone>
- Output delivery: <location>

**Real-Time API:**
- Serverless Lambda
- Latency: <SLA>
- Availability: <SLA>

**Determinism:**
- Fully deterministic (no randomness)
- Same input → same output (reproducible)

**Rollback:**
Revert to previous stable Git tag and redeploy.

**Link to Runbook:** [Confluence page for operational procedures, on-call contacts, troubleshooting]

---

## (Optional) Supporting Pages

### Validation Archive Page

**Purpose:** Store version-frozen validation evidence for audit and historical comparison.

**Sections (one per major release):**
- Validation scope (dataset, time window, methodology)
- Validation results (metrics, performance)
- Observations and limitations
- Validation conclusion (approved for use / approved with monitoring / not approved)
- Supporting artifacts (decile tables, ROC plots, sample outputs)

**Example subsection for v1.0.0 POCKETLY:**
```
Model: asset_basic_score — POCKETLY Config v1.0.0
Validation Date: [YYYY-MM-DD]
Dataset: Contact outcomes (Oct–Dec 2025), 4,500 records
Metrics: ROC-AUC 0.61, KS 0.18, Top-decile lift 1.6×
Result: Approved for production use
Artifacts: [Links to Excel, PDF, JSON samples]
```

---

### Approval History Page

**Purpose:** Audit trail of formal reviews and sign-offs.

**Sections:**
- Approval records (table: version, reviewer, decision, date, notes)
- Conditions and exceptions (if any)
- Approval summary (overall status, valid until date)
- Traceability (links to Model Overview and Git tags)

---

### Runbook Page (Ops-Only)

**Purpose:** Operational procedures for running, monitoring, and recovering the model.

**Sections:**
- Execution details (triggers, frequency, entry points)
- Input/output handling (sources, schemas, locations)
- Monitoring and health checks (key metrics, alerts)
- Common failure scenarios and resolution steps
- Rollback procedure (when, how, reference version)
- Escalation and support contacts
- Change safety notes (freeze windows, risks)

---

## Integration with Git

### Linking Git to Confluence

**In Confluence Model Overview:**
```
Git Repository: https://github.com/santoshk1230/demo-model-versioning
Branch: develop (production code) / main (stable releases)
Base Model Tags: rule-engine-v1.0.0, rule-engine-v1.1.0, ...
Client Config Tags: pocketly-config-v1.0.0, fibe-config-v1.0.0, ...
README: asset_basic_score/README.md
Metadata: asset_basic_score/registry/tags.yml
```

**In Confluence Change Log:**
```
Version v1.0.0 | Tag: rule-engine-v1.0.0 | Commit: [hash] | Date: [YYYY-MM-DD]
POCKETLY v1.0.0 | Tag: pocketly-config-v1.0.0 | Commit: [hash] | Date: [YYYY-MM-DD]
```

### Workflow

1. **Code change** → Git commit + tag
2. **Metadata update** → Edit `tags.yml` (version fields)
3. **Confluence update** → Add row to Change Log table, link to Git tag
4. **Approval** → Record in Approval History
5. **Validation** → Archive evidence in Validation Archive

---

## Key Principles Recap

1. **One Model Overview page** (not multiple pages per version)
2. **Versions are table entries**, not separate pages
3. **Git is source of truth** for code; Confluence for lifecycle
4. **Metadata in tags.yml** feeds both Git workflows and Confluence templates
5. **README.md in repo** is the starting point; Confluence expands with approvals and validation
6. **Same structure applies** to rule-based, heuristic, and ML models

---

**Last Updated:** [YYYY-MM-DD]  
**Maintained By:** Data Science Team
