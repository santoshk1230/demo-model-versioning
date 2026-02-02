# Asset Basic Score — Model README

---

## 1. Model Overview

**Asset Basic Score** is a canonical **rule-based credit risk scoring model** designed for retail lending use cases.

The model generates a standardized risk score using deterministic business rules and heuristics. It supports **multiple lending clients** through client-specific configuration and adapters, while maintaining **one shared canonical scoring engine**.

---

## 2. Model Classification

- **Model Type**: Rule-Based / Heuristic  
- **Primary Use Case**: Credit Risk Scoring  
- **Execution Mode**: Configuration-driven  
- **Current Status**: Active (Demo / Reference Implementation)

---

## 3. Architecture & Source of Truth

This directory represents the **model identity**. All executable logic and configuration are maintained under the `implementation/` folder.

---

## 3.1 Canonical Rule Engine (Model Identity)

**Path** - models/asset_basic_score/implementation/rule_engine_config/


This layer customizes scoring behaviour **without changing the model**.

**Structure**
- `config/<client>/`  
  Client-specific parameters (thresholds, weights, toggles) in JSON
- `model/<client>/`  
  Client adapters (`*.py`) that wire config to the canonical engine
- `model/<client>/README.md`  
  Ownership, approvals, audit trail, and client config version history
- `test/`  
  Client-level validation and sanity tests

Changes in this layer **do NOT create a new model version**.

---

## 4. Execution Model

The model is designed to run as an **AWS Lambda-based rule engine**.

**Entrypoint**


## Client Configuration Structure (Quick Access)

Client-specific wiring is maintained under:

- `models/asset_basic_score/implementation/rule_engine_config/model/<client>/`

Each client directory contains:
- A versioned Python adapter (e.g. `<Client>_1_0_0.py`) responsible only for connecting client configuration to the canonical rule engine.  
  No business rules or scoring logic are implemented at this layer.

Current client adapters present in the repository:

- `models/asset_basic_score/implementation/rule_engine_config/model/cholamandalam/Cholamandalam_1_0_0.py`
- `models/asset_basic_score/implementation/rule_engine_config/model/equitas/Equitas_1_0_0.py`
- `models/asset_basic_score/implementation/rule_engine_config/model/fibe/Fibe_1_0_0.py`
- `models/asset_basic_score/implementation/rule_engine_config/model/incred/Incred_1_0_0.py`
- `models/asset_basic_score/implementation/rule_engine_config/model/larsontubro/Larsontubro_1_0_0.py`
- `models/asset_basic_score/implementation/rule_engine_config/model/poonawala/Poonawala_1_0_0.py`

Client-level README files (covering ownership, approvals, and configuration change history) are planned and will be added as part of the governance hardening phase.
