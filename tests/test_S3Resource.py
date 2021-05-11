import pytest
from S3Resource.S3Resource import S3Resource, resized_image_url


def test_empty_bucket(s3_test, bucket_name):
    my_client = S3Resource()
    bucket = my_client.get_random_file(bucket_name)
    assert bucket is None


def test_non_empty_bucket(s3_test, bucket_name, test_file):
    my_client = S3Resource()
    bucket = my_client.save_image_to_bucket(test_file, bucket_name, 'testing_file.png')
    assert bucket == resized_image_url('testing_file.png')
    random_file = my_client.get_random_file(bucket_name)
    assert random_file is not None


def test_save_item_to_bucket(s3_test, bucket_name, test_file):
    my_client = S3Resource()
    bucket = my_client.save_image_to_bucket(test_file, bucket_name, 'testing_file.png')
    assert bucket == resized_image_url('testing_file.png')


def test_resize_img_url():
    assert resized_image_url('testing_file.png') == 'https://testing.com/testing_file.png'

