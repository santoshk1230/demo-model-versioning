# Equitas – Asset Basic Score Configuration

## Linked Canonical Model
- Model: asset_basic_score
- Canonical Model Tag: v1.0.0
- Validated Against Tag(s): v1.0.0
- Last Validation Date: ____________________

## Configuration Versions

### v1.0.0
Files (repo paths):
- models/asset_basic_score/implementation/rule_engine_config/config/equitas/Equitas_1_0_0.json
- models/asset_basic_score/implementation/rule_engine_config/model/equitas/Equitas_1_0_0.py

Config Intent:
- ____________________ (e.g., “Balanced risk thresholds for secured retail lending”)

Changes:
- Initial client configuration
- Client-specific thresholds and rule wiring

Change Log:
| Date | Change Summary | Reason | Done By | Approved By | Ticket/Ref |
|------|----------------|--------|---------|-------------|------------|
| ____ | Initial config | ____   | ____    | ____        | ____       |

## Ownership & Governance
- Team: Risk Analytics / Data Science
- Canonical Model Owner: Central DS Platform Team
- Client Config Owner: Equitas DS Team
- Changes Done By: ____________________
- Approved By: ____________________
- Audited By: ____________________

## Validation
- Smoke Test Payload Path: ____________________
- Expected Output Schema: score + reasons + metadata
- Notes: ____________________

## Rollback
- Revert to previous configuration version file if available.
- Otherwise, revert commit(s) introducing this configuration.

## Notes
- Client configuration versions are independent of canonical model versions.
- Config changes do not require canonical model retagging.
- Client adapters must not contain business logic.
