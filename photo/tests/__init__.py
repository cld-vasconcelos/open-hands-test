import boto3
from moto import mock_aws

@mock_aws
def setup_s3():
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")

setup_s3()
