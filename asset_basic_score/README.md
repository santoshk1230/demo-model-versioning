# Asset Basic Score Model

## 1. Model Overview

The **asset_basic_score** model is a rule-based scoring engine that generates a unified trust and risk score for customer assets (phone, address, identity, financial indicators) across multiple lending and fintech partners.

The model supports customer onboarding, fraud prevention, credit risk decisioning, and operational verification workflows by combining deterministic rules and heuristic aggregation of weak signals into interpretable confidence and risk scores.

The model is **deterministic, explainable, and rule-driven**, making it suitable for regulated and audit-sensitive environments where transparency and traceability are critical.

---

## 2. Model Classification

| Property | Value |
|----------|-------|
| **Model Category** | Rule-based |
| **Primary Objective** | Scoring (Trust/Risk) |
| **Current Status** | Active |
| **Approach** | Deterministic rule engine with client-specific configurations |

---

## 3. Implementation Reference (Source of Truth)

This directory acts as an index pointing to the actual implementation and related artifacts.

### 3.1 Execution / Engine

**Framework / Engine:**  
Internal rule-based scoring engine (`rule_engine/util/rule.py`)

**Design:**
- Core rule evaluation logic is **model-version-agnostic**
- Client-specific rules and thresholds are **configuration-driven**
- Supports multi-client deployments with isolated rule sets

---

### 3.2 Model Artifacts

| Artifact | Location | Type |
|----------|----------|------|
| **Rule Engine Core** | `rule_engine/util/rule.py` | Source code |
| **Client Rule Models** | `rule_engine_config/model/{client}/{client}_1_0_0.py` | Python classes (rules dict) |
| **Client Rule Configs** | `rule_engine_config/config/{client}/{client}_1_0_0.json` | JSON (field mappings) |
| **Score Generator** | `rule_engine/src/score_generator.py` | Orchestration logic |
| **Lambda Handlers** | `rule_engine/app/{client}_app.py` | Serverless entry points |
| **Validation / Tests** | `rule_engine_config/test/{client}_test_1_0_0.py` | Pytest suite |
| **Utilities** | `rule_engine/util/name_match.py`, `rule_engine/logger/cloudLogger.py` | Supporting functions |

---

## 4. Interfaces (Contract Summary)

### Input Definition
**Schema:** `DsScoreCalculator`  
**Format:** JSON (camelCase)

```json
{
  "response": {
    "enrichedData": { ... },
    "phoneSocial": { ... },
    "phoneVpa": { ... },
    "phoneIntelligence": { ... },
    "panVerificationBasic": { ... },
    "ageOnNetwork": { ... },
    "cdsl": { ... },
    "gst": { ... }
  },
  "m_version": "1_0_0",
  "client_name": "pocketly",
  "input": {
    "email": "...",
    "phone": "...",
    "name": "...",
    "pan": "..."
  }
}
```

*(Complete input schema documented in Confluence)*

### Output Definition
**Format:** JSON with rule responses, total score, base score, tags, and metadata

```json
{
  "ruleResponse": {
    "{trigger_name}": { "score": <int>, "type": "Success|Exception" },
    ...
  },
  "totalScore": <int>,
  "baseScore": <int>,
  "tags": [<tag_ids>],
  "tagIds": [<tag_ids>],
  "failedRules": [<rule_names>]
}
```

### Output Scale
**Score Range:** 0–1000 (configurable per client)  
**Base Score:** 350 (configurable)  
**Trigger Scores:** Positive or negative integers

### Thresholding / Calibration
**Type:** Configuration-driven (stored in `rule_engine_config/config/{client}/*.json`)  
**Flexibility:** Client-specific rules and thresholds without core model changes

---

## 5. Deployment Context (Reference Only)

| Property | Value |
|----------|-------|
| **Execution Environment** | AWS Lambda + Batch |
| **Deployment Stages** | Development, UAT, Production |
| **Latency Sensitivity** | Medium (API: <1s, Batch: async) |
| **Cost Sensitivity** | Medium (serverless, event-driven) |
| **Determinism** | Fully deterministic (no randomness) |

**Deployment Reference:**  
Git tag corresponds to rule engine base version (e.g., `rule-engine-v1.0.0`)  
Client-specific config versions tracked separately (see versioning policy below)

**Rollback Reference:**  
Previous stable Git tag for base model; client configs can be reverted independently

---

## 6. Documentation (Authoritative Source)

All detailed documentation, evaluations, approvals, and release lineage are maintained in Confluence.

| Documentation | Location |
|----------------|----------|
| **Model Overview Page** | Confluence: `asset_basic_score — Model Overview` |
| **Current Production Release** | Change Log & Versioning section of Model Overview |
| **Historical Releases** | Archived in Model Overview or linked pages |
| **Validation Archive** | Confluence: `asset_basic_score — Validation Archive` |
| **Approval History** | Confluence: `asset_basic_score — Approval History` |
| **Runbook (Ops)** | Confluence: `asset_basic_score — Runbook` |

---

## 7. Ownership and Support

| Role | Team / Contact |
|------|----------------|
| **Owning Team** | Data Science Team |
| **Primary Contact** | [Model Owner Name / Role] |
| **Business Owner** | [Risk / Product / Operations] |
| **Support & Escalation** | Standard Data Science support and change management process |

---

## 8. Change and Versioning Policy

### Versioning Strategy

The model uses **semantic versioning** with distinct tracks for **base model** and **client-specific configurations**:

#### A. Base Model Versioning (Rule Engine Core)
Tracks changes to `rule_engine/util/rule.py`, `rule_engine/src/score_generator.py`, and utilities.

| Type | Example | Trigger | Impact |
|------|---------|---------|--------|
| **PATCH** | v1.0.0 → v1.0.1 | Bug fixes, refactoring, parameter tuning without logic change | No breaking changes to outputs or contracts |
| **MINOR** | v1.0.1 → v1.1.0 | New rule operators, enhanced score aggregation, new utilities | May affect output distribution; backward compatible |
| **MAJOR** | v1.2.0 → v2.0.0 | Redefine rule evaluation, change operator semantics, restructure output | Breaking changes to output schema or interpretation |

**Git Tag Format:** `rule-engine-vX.Y.Z`

#### B. Client Configuration Versioning (Config + Rules)
Tracks changes to `rule_engine_config/config/{client}/*.json` and `rule_engine_config/model/{client}/{client}_vX_Y_Z.py`.

| Type | Example | Trigger | Impact |
|------|---------|---------|--------|
| **PATCH** | v1.0.0 → v1.0.1 | Rule threshold tuning, parameter adjustment | Score shifts expected; no rule additions/removals |
| **MINOR** | v1.0.1 → v1.1.0 | New rules added, existing rules modified | Output distribution changes; improved discrimination |
| **MAJOR** | v1.2.0 → v2.0.0 | Rule removal, input schema changes, contract redefinition | Breaking changes; requires re-approval |

**Git Tag Format:** `{client}-config-vX.Y.Z` (e.g., `pocketly-config-v1.2.0`)

#### Independence
- Base model and client configs version **independently**
- A PATCH to base model does **not** require new client config versions
- A MINOR change to POCKETLY config does **not** affect FIBE or LARSONTUBRO

#### Coordination
- Client configs must specify compatible base model version range in their metadata (see `tags.yml`)
- Example: POCKETLY config v1.2.0 requires `rule-engine >= v1.0.0 AND < v2.0.0`

---

## 9. Governance Note

This document serves as the **Git-level model index and reference**.

**Confluence is the authoritative source** for:
- Detailed design decisions
- Validation evidence
- Approval records
- Release change logs
- Operational runbooks

---

## 10. Quick Start

### Local Testing (Development)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run scoring with sample payload:**
   ```powershell
   $env:PYTHONPATH = 'C:\path\to\asset_basic_score\implementation'
   python .\scripts\get_trust_score.py --payload-file .\payload.json
   ```

3. **Run tests:**
   ```bash
   pytest rule_engine_config/test/pocketly_test_1_0_0.py -v
   pytest rule_engine_config/test/fibe_test_1_0_0.py -v
   pytest rule_engine_config/test/larsontubro_test_1_0_0.py -v
   ```

### Adding a New Client

1. Create rule model:
   ```
   rule_engine_config/model/{client_name}/{client_name}_1_0_0.py
   ```
   (Class with `rules` dict following established pattern)

2. Create rule config:
   ```
   rule_engine_config/config/{client_name}/{client_name}_1_0_0.json
   ```
   (Field mappings from enriched data to rule inputs)

3. Create tests:
   ```
   rule_engine_config/test/{client_name}_test_1_0_0.py
   ```

4. The runner (`scripts/get_trust_score.py`) will auto-detect the new client.

---

## 11. References

- **Git Repository:** [GitHub link]
- **Confluence Model Overview:** [Confluence URL]
- **Rule Engine Utilities:** See `rule_engine/util/rule.py` for rule operators and logic
- **Score Generator:** See `rule_engine/src/score_generator.py` for orchestration
- **Lambda Handlers:** See `rule_engine/app/{client}_app.py` for serverless entry points

---

**Last Updated:** [YYYY-MM-DD]  
**Maintained By:** Data Science Team
