
import boto3
import json

s3_bkt = "aws-bucket-testing-798"
s3_reg = "us-east-2"

s3 = boto3.client("s3", region_name=s3_reg)

# load_s3() loads a json from AWS s3 public bucket
def load_s3(file_name):
    try:
        resp = s3.get_object(Bucket=s3_bkt, Key=file_name)
        return json.loads(resp["Body"].read().decode("utf-8"))
    except Exception as e:
        print(f"Error loading {file_name}")

# save_s3() saves a json to an AWS s3 public bucket
def save_s3(file_name, data):
    try:
        s3.put_object(Bucket=s3_bkt, Key=file_name, Body=json.dumps(data))
    except Exception as e:
        print(f"Error saving {file_name}")
