from utils import validate_mime_type, resize_image, upload_file_to_s3


def test_validate_mime_type():
    assert validate_mime_type('image/png') is True
    assert validate_mime_type('text/csv') is False


def test_resize_image(s3_file_created):
    assert resize_image(s3_file_created, 100, 100) == 'https://testing.com/resized_images/100x100-testing_file.png'


def test_upload_file_to_s3(s3_test, test_file):
    assert upload_file_to_s3(test_file, 'test_file', 'png') is True
