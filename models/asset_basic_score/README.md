# Asset Basic Score — Model README

---

## 1. Model Overview

The Asset Basic Score model is designed to generate a standardized credit risk score for retail lending use cases.  
It evaluates core borrower signals related to income stability, bureau behaviour, address verification, and employment continuity.

The model is intended to be used across multiple lending clients with **client-specific configuration overrides**, while maintaining a single shared scoring engine.

---

## 2. Model Classification

- **Model Category**: Rule-Based / Heuristic  
- **Primary Objective**: Credit Risk Scoring  
- **Current Status**: Active (Demo / Training)

---

## 3. Implementation Reference (Source of Truth)

This directory acts as a **model identity and index**.  
The actual execution logic and artifacts are maintained under the implementation sub-folder.

### 3.1 Execution / Engine

- **Framework / Engine**: Custom Python rule engine  
- **Execution Style**: Configuration-driven scoring

### 3.2 Model Artifacts

- **Scoring Logic**  
  `models/asset_basic_score/implementation/inference/`

- **Feature Logic**  
  `models/asset_basic_score/implementation/features/`

- **Configuration / Weights**  
  `models/asset_basic_score/implementation/artifacts/`

- **Client-Specific Overrides**  
  `models/asset_basic_score/implementation/artifacts/clients/<client_name>/`

- **Tests**  
  `models/asset_basic_score/implementation/tests/`

---

## 4. Interfaces (Contract Summary)

### Input Definition

Borrower and application-level attributes including, but not limited to:
- Income information  
- Bureau score and delinquency indicators  
- Address verification status  
- Employment stability indicators  

(Exact input schema is documented in Confluence.)

### Output Definition

- Risk score (0–100)  
- Risk band (LOW / MEDIUM / HIGH)  
- Rule-level reason codes  

### Output Scale

0–100 (higher score indicates higher credit risk)

---

## 5. Deployment Context (Reference Only)

- **Execution Environment**: API / Batch (logical reference)  
- **Deployment Scope**: Multi-client  
- **Deployment Reference**: Git tag corresponding to approved release  
  (e.g. `asset_basic_score/v1.0.0`)

Rollback is performed by reverting to a previous Git tag.

---

## 6. Documentation (Authoritative Source)

Detailed documentation, validation notes, and release lineage are maintained in Confluence.

- **Model Overview Page**: Asset Basic Score — Model Overview  
- **Release History**: Maintained within the same Confluence page  

This README serves as the **Git-level technical index**.

---

## 7. Ownership and Support

- **Owning Team**: Data Science  
- **Primary Contact**: Santosh Kamble 
- **Support Model**: Standard DS support and escalation process

---

## 8. Change and Versioning Policy

- **PATCH**: Parameter tuning or bug fixes without behaviour change  
- **MINOR**: Rule additions or behaviour changes without contract change  
- **MAJOR**: Input/output contract changes or scoring objective changes  

All approved releases are tracked via **Git annotated tags**.

---

## 9. Governance Note

This model follows the standard model governance and versioning strategy:
- Model identity is fixed  
- Implementation evolves over time  
- Releases are immutable and traceable via Git tags
