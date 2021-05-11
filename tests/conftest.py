import os
import pytest
import datetime
import boto3

from fastapi.testclient import TestClient

from S3Resource.S3Resource import S3Resource
from main import app
from cache.cache import Cache
from moto import mock_s3, mock_sqs


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


# Cache class fixtures
@pytest.fixture()
def empty_cache():
    """Return an empty Cache instance."""
    return Cache()


@pytest.fixture()
def cache_within_hour():
    """Return a Cache instance with a cached data created within last hour."""
    time_30_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=30)
    cache = Cache()
    cache.add_key('100x100', 'test_file_url')
    cache.memory['100x100'][0] = time_30_minutes_ago
    return cache


@pytest.fixture()
def cache_not_within_hour():
    """Return a Cache instance with a cached data created more then hour ago."""
    time_90_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=90)
    cache = Cache()
    cache.add_key('100x100', 'test_file_url')
    cache.memory['100x100'][0] = time_90_minutes_ago
    return cache
