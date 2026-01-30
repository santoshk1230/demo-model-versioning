# kyc_risk_score — Model README

---

## 1. Model Overview

The KYC Risk Score model is designed to generate a simple, explainable risk score that represents potential KYC risk based on basic customer verification and behavioral signals.
It supports internal training and demonstration of standardized model onboarding, governance, and Git-based versioning by producing a deterministic risk score and associated reason codes.
The model is deterministic and fully explainable, making it suitable for regulated and audit-sensitive environments, although it is intended only for demonstration purposes.

---

## 2. Model Classification

* **Model Category**: Rule-based
* **Primary Objective**: Scoring
* **Current Status**: Active (Demo / Training)

---

## 3. Implementation Reference (Source of Truth)

This directory does not contain the core model execution logic.
It acts as an index pointing to the actual implementation and related artifacts in the repository.

### 3.1 Execution / Engine

* **Framework / Engine**: Custom Python-based rule execution (standalone demo implementation)

### 3.2 Model Artifacts

* **Configuration / Parameters**:
  `implementation/kyc_risk_score/artifacts/config.json`

* **Model Logic / Artifact**:
  `implementation/kyc_risk_score/inference/scorer.py`

* **Training Code / Notebooks**:
  NA (rule-based model)

* **Validation / Tests**:
  `implementation/kyc_risk_score/tests/`

(Mark fields as NA if they are not applicable.)

---

## 4. Interfaces (Contract Summary)

* **Input Definition**:
  Customer verification and behavioral signals including age, document verification flags, address risk indicators, and recent device activity.
  (Complete input schema documented in Confluence.)

* **Output Definition**:
  Risk score with categorical risk band and rule-level reason codes.

* **Output Scale**:
  0–100

* **Thresholding / Calibration**:
  Configuration-driven

---

## 5. Deployment Context (Reference Only)

* **Execution Environment**:
  Offline / Local execution (demo)

* **Deployment Stages**:
  Development only

* **Deployment Reference**:
  Git tag corresponding to the approved release (for example: `kyc_risk_score/v1.0.0`)

* **Rollback Reference**:
  Previous stable Git tag

(Deployment infrastructure and orchestration are managed externally.)

---

## 6. Documentation (Authoritative Source)

All detailed documentation, design decisions, approvals, and release lineage are maintained in Confluence.

* **Model Lineage Page**:
  KYC Risk Score — Model Overview
  (Confluence URL to be added)

* **Current Production Release**:
  Not applicable — demo model

* **Historical Releases**:
  Documented within the same Model Overview page under the Change Log & Versioning section

---

## 7. Ownership and Support

* **Owning Team**: Data Science
* **Primary Contact**: Model Owner (Data Science)
* **Support and Escalation**: Standard Data Science support process

---

## 8. Change and Versioning Policy

* **PATCH** (e.g., v1.0.0 → v1.0.1):
  Bug fixes, parameter tuning, or refactoring without intended behavior change

* **MINOR** (e.g., v1.0.1 → v1.1.0):
  Rule additions or behavior changes without contract changes

* **MAJOR** (e.g., v1.2.0 → v2.0.0):
  Input/output contract changes, objective redefinition, or architecture changes

---

## 9. Governance Note

This document serves as a Git-level model index and reference.
Confluence is the authoritative source for detailed design decisions, validation evidence, approvals, and release history.

---

### Usage Rule

Every new model must have this README and a corresponding `registry/tags.yml` created at model inception.

---

