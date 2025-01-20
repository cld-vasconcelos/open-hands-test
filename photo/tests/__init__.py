import os
from unittest.mock import patch

os.environ['AWS_S3_ENDPOINT_URL'] = 'http://localhost:4566'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['AWS_STORAGE_BUCKET_NAME'] = 'test-bucket'
os.environ['AWS_ACCESS_KEY_ID'] = 'test-access-key'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test-secret-key'
os.environ['AWS_QUERYSTRING_AUTH'] = 'False'
os.environ['AWS_S3_SIGNATURE_VERSION'] = 's3v4'

with patch('integrations.aws.s3.Client') as MockClient:
    client = MockClient()
    client.create_bucket()
