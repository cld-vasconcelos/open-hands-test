import pytest
from django.conf import settings

@pytest.fixture(scope='session', autouse=True)
def configure_settings():
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
    settings.AWS_S3_ENDPOINT_URL = 'http://localhost:4566'
    settings.AWS_DEFAULT_REGION = 'us-east-1'
    settings.AWS_STORAGE_BUCKET_NAME = 'test-bucket'
    settings.AWS_ACCESS_KEY_ID = 'test-access-key'
    settings.AWS_SECRET_ACCESS_KEY = 'test-secret-key'
    settings.AWS_QUERYSTRING_AUTH = False
    settings.AWS_S3_SIGNATURE_VERSION = 's3v4'
