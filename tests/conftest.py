import os
import pytest
import boto3

from fastapi.testclient import TestClient

from S3Resource.S3Resource import S3Resource
from main import app
from moto import mock_s3


@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client


# AWS S3 Resources class fixtures
@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing_key"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing_id"
    os.environ["AWS_SECURITY_TOKEN"] = "testing_security_token"
    os.environ["AWS_SESSION_TOKEN"] = "testing_session_token"
    os.environ["CLOUDFRONT_URL"] = "testing.com/"
    os.environ["SOURCE_BUCKET"] = 'my_bucket_name'
    os.environ["RESIZED_BUCKET"] = 'my_bucket_name'


@pytest.fixture
def s3_client(aws_credentials):
    with mock_s3():
        conn = boto3.client("s3", region_name='us-east-1')
        yield conn


@pytest.fixture
def s3_file_created(s3_test, test_app, test_file, bucket_name):
    my_client = S3Resource()
    my_client.save_image_to_bucket(test_file, bucket_name, 'testing_file.png')
    file = my_client.get_random_file(bucket_name)
    return file


@pytest.fixture
def test_file():
    with open(f"{os.getcwd()}/tests/test_image.png", 'rb') as file:
        r_file = file.read()
    return r_file


@pytest.fixture
def bucket_name():
    return 'my_bucket_name'


@pytest.fixture
def s3_test(s3_client, bucket_name):
    s3_client.create_bucket(Bucket=bucket_name)
    yield
