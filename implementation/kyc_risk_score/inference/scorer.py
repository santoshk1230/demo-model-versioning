from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ScoreResult:
    score: int
    risk_band: str
    reasons: list[str]


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def score_kyc(payload: Dict[str, Any], config: Dict[str, Any]) -> ScoreResult:
    """
    Simple rule-based KYC risk score (0-100).
    Higher = higher risk.
    """
    reasons: list[str] = []
    score = 0

    # 1) Age rule
    age = payload.get("age")
    if age is None:
        score += config["weights"]["missing_age"]
        reasons.append("missing_age")
    else:
        if age < 21:
            score += config["weights"]["age_lt_21"]
            reasons.append("age_lt_21")
        elif age > 65:
            score += config["weights"]["age_gt_65"]
            reasons.append("age_gt_65")

    # 2) Docs
    pan_verified = bool(payload.get("pan_verified", False))
    aadhaar_verified = bool(payload.get("aadhaar_verified", False))

    if not pan_verified:
        score += config["weights"]["pan_not_verified"]
        reasons.append("pan_not_verified")
    if not aadhaar_verified:
        score += config["weights"]["aadhaar_not_verified"]
        reasons.append("aadhaar_not_verified")

    # 3) Risk signals
    address_mismatch = bool(payload.get("address_mismatch", False))
    high_risk_pincode = bool(payload.get("high_risk_pincode", False))
    device_change_7d = int(payload.get("device_change_7d", 0) or 0)

    if address_mismatch:
        score += config["weights"]["address_mismatch"]
        reasons.append("address_mismatch")
    if high_risk_pincode:
        score += config["weights"]["high_risk_pincode"]
        reasons.append("high_risk_pincode")

    # Device change: add weight per change with cap
    per = config["weights"]["device_change_each"]
    cap = config["caps"]["device_change_cap"]
    device_points = int(clamp(device_change_7d * per, 0, cap))
    if device_points > 0:
        score += device_points
        reasons.append(f"device_change_points_{device_points}")

    # Final clamp + banding
    score = int(clamp(score, 0, 100))

    bands = config["bands"]
    if score >= bands["high_min"]:
        band = "HIGH"
    elif score >= bands["medium_min"]:
        band = "MEDIUM"
    else:
        band = "LOW"

    return ScoreResult(score=score, risk_band=band, reasons=reasons)
