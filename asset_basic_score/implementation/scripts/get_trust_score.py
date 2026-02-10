import json
import argparse
import re
from pathlib import Path

from rule_engine.util.rule import get_score

# client rule classes
from rule_engine_config.model.pocketly.pocketly_1_0_0 import POCKETLY_1_0_0
from rule_engine_config.model.fibe.fibe_1_0_0 import FIBE_1_0_0
from rule_engine_config.model.larsontubro.larsontubro_1_0_0 import LARSONTUBRO_1_0_0

try:
    from rule_engine.src.score_generator import ScoreGenerator
    from rule_engine.schema.payload.DsScoreCalculator import DsScoreCalculator
except Exception:
    ScoreGenerator = None
    DsScoreCalculator = None


def camel_to_snake(camel_str):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", camel_str).lower()


def convert_keys_to_snake_case(data):
    if isinstance(data, dict):
        return {
            camel_to_snake(k): convert_keys_to_snake_case(v) for k, v in data.items()
        }
    elif isinstance(data, list):
        return [convert_keys_to_snake_case(item) for item in data]
    else:
        return data


CLIENT_MAP = {
    "pocketly": POCKETLY_1_0_0,
    "fibe": FIBE_1_0_0,
    "larsontubro": LARSONTUBRO_1_0_0,
}


def run_direct(client: str, ip_data: dict):
    client = client.lower()
    if client not in CLIENT_MAP:
        raise ValueError(f"Unknown client: {client}")
    rules = CLIENT_MAP[client]().rules
    result = get_score(ip_data or {}, rules)
    return result


def run_with_payload(payload: dict):
    if ScoreGenerator is None or DsScoreCalculator is None:
        raise RuntimeError("ScoreGenerator or DsScoreCalculator not available in import path")
    
    # Convert camelCase to snake_case (like Lambda handler does)
    transformed_payload = convert_keys_to_snake_case(payload)
    
    # Validate payload via pydantic model
    payload_model = DsScoreCalculator(**transformed_payload)
    data = transformed_payload["response"] or {}
    generator = ScoreGenerator(data=data, payload=payload_model)
    return generator.get_data_as_per_rules()


def main():
    parser = argparse.ArgumentParser(description="Get trust score for input using existing rule engine")
    parser.add_argument("--client", default="pocketly", help="client name: pocketly|fibe|larsontubro (used in direct mode)")
    parser.add_argument("--ip-data", help="JSON string of ip_data to pass directly to get_score")
    parser.add_argument("--ip-file", help="Path to JSON file containing ip_data")
    parser.add_argument("--payload-file", help="Path to full payload JSON (DsScoreCalculator schema). If provided, uses ScoreGenerator flow")

    args = parser.parse_args()

    if args.payload_file:
        payload_path = Path(args.payload_file)
        if not payload_path.exists():
            raise SystemExit(f"Payload file not found: {payload_path}")
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        result = run_with_payload(payload)
        print(json.dumps(result, indent=2))
        return

    # direct mode
    ip_data = {}
    if args.ip_file:
        p = Path(args.ip_file)
        if not p.exists():
            raise SystemExit(f"ip-data file not found: {p}")
        ip_data = json.loads(p.read_text(encoding="utf-8"))
    elif args.ip_data:
        ip_data = json.loads(args.ip_data)

    result = run_direct(args.client, ip_data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
