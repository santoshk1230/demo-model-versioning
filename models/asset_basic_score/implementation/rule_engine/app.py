import json
from src.score_generator import ScoreGenerator
from schema.payload.DsScoreCalculator import DsScoreCalculator
from src.id_generator import generate_unique_id
from src.data_to_s3 import data_to_s3
from util.tags import get_tag_dict
from pydantic import ValidationError
import re
import logging
from logger.cloudLogger import LambdaLogger

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


def snake_to_camel(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def convert_keys_to_camel_case(data):
    if isinstance(data, dict):
        return {
            snake_to_camel(k): convert_keys_to_camel_case(v) for k, v in data.items()
        }
    elif isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    else:
        return data

def lambda_handler(event, context):
    logger = LambdaLogger(service_name="MyLambdaService", log_level=logging.INFO)

    payload = json.loads(event["body"])
    pan_id = payload['input']['pan']
    email_id = payload['input']['email']
    phone_id = payload['input']['phone']
    request_id = payload['input']['requestId']

    try: 
        unique_id_generated = None
        unique_id_generated = generate_unique_id(email=email_id,
                                                phone=phone_id,
                                                pan = pan_id)
      
    except Exception as e:
        print("unable to generate unique_id ",e)
    tags = get_tag_dict(payload['response'])
    transformed_payload = convert_keys_to_snake_case(payload)
                        
    try:
        payload = DsScoreCalculator(**transformed_payload)
    except ValidationError as e:
        errors = e.errors()
        formatted_errors = [
            {"field": err["loc"], "message": err["msg"]} for err in errors
        ]
        response = {"errors": formatted_errors, "statusCode": 400}
        return json.dumps(response)

    ds_client = ScoreGenerator(data=transformed_payload["response"], payload=payload)
    response = ds_client.get_data_as_per_rules()
    response = convert_keys_to_camel_case(response)
    
    response['requestId'] = request_id
    response['uniqueId'] = unique_id_generated

    try:
        ## storing scored data to s3 bucket 
        data_to_s3(data = response,
                bucket='data-science-ds',
                store_path = 'scores_store/cholamandalam/output_score/',
                data_type = 'score',
                file_name=unique_id_generated)

    except Exception as e:
        print("Not able to save score data to s3")
        print("Exception Occured: ",e)

    if 'ruleResponse' in response:
        # response.pop('ruleResponse')
        response.pop('tags')
        # response.pop('failedRules')
        response['tagIds'] = list(tags.keys())

    logger.log_entry(event, response, context)
    if "field_error" in response:
        return json.dumps({"statusCode": 400, "error": response["field_error"]}) 
    else:
        return json.dumps({"statusCode": 200, "data": response})
        

    


        

        
    




    

      
    