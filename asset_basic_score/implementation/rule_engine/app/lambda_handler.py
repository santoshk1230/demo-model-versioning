import json

from rule_engine.src.score_generator import ScoreGenerator
from rule_engine.schema.payload.DsScoreCalculator import DsScoreCalculator
from rule_engine.logger.cloudLogger import LambdaLogger


logger = LambdaLogger(service_name="asset_basic_score")


def _json_response(status_code: int, body: dict):
    return {"statusCode": status_code, "body": json.dumps(body)}


def lambda_handler(event, context):
    """
    Lambda handler
    - Expects event["body"] as JSON string or dict
    - Body should contain: client_name, m_version, response (dict), input (dict)
    """
    try:
        body = event.get("body")
        if body is None:
            return _json_response(400, {"error": "Missing 'body' in event"})

        payload_dict = json.loads(body) if isinstance(body, str) else body

        # Validate/normalize via pydantic
        payload = DsScoreCalculator(**payload_dict)

        data = payload.response or {}
        generator = ScoreGenerator(data=data, payload=payload)
        result = generator.get_data_as_per_rules()

        logger.log_entry(event, result, context)
        return _json_response(200, result)

    except Exception as e:
        # Avoid crashing lambda without a response
        try:
            logger.log_error(e, context)
        except Exception:
            pass
        return _json_response(500, {"error": str(e)})
