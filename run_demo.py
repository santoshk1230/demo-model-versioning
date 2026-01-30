import json
from implementation.kyc_risk_score.inference.scorer import score_kyc


def main():
    with open("implementation/kyc_risk_score/artifacts/config.json", "r", encoding="utf-8") as f:
        cfg = json.load(f)

    samples = [
        {
            "name": "Clean user",
            "payload": {"age": 30, "pan_verified": True, "aadhaar_verified": True, "device_change_7d": 0}
        },
        {
            "name": "Risky user",
            "payload": {
                "age": 19, "pan_verified": False, "aadhaar_verified": False,
                "address_mismatch": True, "high_risk_pincode": True, "device_change_7d": 3
            }
        }
    ]

    for s in samples:
        res = score_kyc(s["payload"], cfg)
        print(f"\n--- {s['name']} ---")
        print("score:", res.score)
        print("band :", res.risk_band)
        print("reasons:", res.reasons)


if __name__ == "__main__":
    main()
