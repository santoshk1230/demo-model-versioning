import boto3
import json
from botocore.exceptions import NoCredentialsError, ClientError

def data_to_s3(data,bucket,store_path,file_name,data_type):
    """
    Upload a Python object (e.g., string, JSON, bytes) directly to an S3 bucket.

    :param data: Data to upload (string, JSON, bytes, etc.).
    :param bucket: The S3 bucket to upload to.
    :param store_path: The path inside S3 bucket
    :param file_name : unique_id generated for each incoming request.
    :param data_type : is enriched_data or score
    :return: True if upload succeeded, False otherwise.
    """
    
    # Create an S3 client
    s3_client = boto3.client('s3')
    if data_type != None:
        if data_type == 'score':
            object_name = store_path + file_name + '_score.json'
            print('object_name :',object_name)
        elif data_type == 'enrichment':
            object_name = store_path + file_name + '_enrichment.json'
            print('object_name :',object_name)        
        try:
            # If data is a dictionary (JSON-like), convert it to a string
            if isinstance(data, dict):
                data = json.dumps(data)
            
            # Upload the data to S3 (using put_object)
            print('here 1 ')
            s3_client.put_object(Body=data, Bucket=bucket, Key=object_name)
            print('here 2')
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
        
    elif data_type == None:
        print("Data type not specified for storing. Please make sure it either enrichment or score")