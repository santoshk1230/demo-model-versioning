import boto3
import json
from botocore.exceptions import NoCredentialsError, ClientError


def data_to_s3(data, bucket, store_path, file_name, data_type):
    """
    Upload a Python object directly to an S3 bucket.
    """
    s3_client = boto3.client("s3")

    if data_type is None:
        print("Data type not specified for storing. Please make sure it either enrichment or score")
        return False

    if data_type == "score":
        object_name = store_path + file_name + "_score.json"
    elif data_type == "enrichment":
        object_name = store_path + file_name + "_enrichment.json"
    else:
        print("Invalid data_type")
        return False

    try:
        if isinstance(data, dict):
            data = json.dumps(data)

        s3_client.put_object(Body=data, Bucket=bucket, Key=object_name)
        print(f"Data uploaded to '{bucket}/{object_name}'")
        return True

    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except ClientError as e:
        print(f"Client error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
