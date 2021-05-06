import logging
import io
import boto3
from botocore.exceptions import ClientError
from random import randint
from PIL import Image


# test
def validate_mime_type(file_type: str):
    """Validation of the uploaded file MIME type.

    :param file_type: file content type
    :return: True if file content/type == 'image'
    """

    if file_type.split('/')[0] == 'image':
        return True
    return False


# test
def upload_file_to_s3(file: io.BytesIO, bucket: str, file_name: str):
    """Upload a file to an S3 bucket

    :param file: File to upload(bytes)
    :param bucket: Bucket to upload to
    :param file_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    s3_client = boto3.client(
        's3',
        aws_access_key_id='AKIATXKH6RANVQV55XHU',
        aws_secret_access_key='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',
    )

    try:
        response = s3_client.upload_fileobj(file, bucket, file_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# test
def resize_image(image, width: int, height: int):
    image_body = image.get()['Body'].read()
    img = Image.open(io.BytesIO(image_body))
    img = img.resize((width, height), Image.ANTIALIAS)
    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    new_file_name = f'{width}x{height}-{image.key}'
    new_path = save_resized_image(buffer, new_file_name)
    return new_path


def save_resized_image(img, new_file_name):
    s3 = boto3.resource('s3')
    obj = s3.Object(
        bucket_name='thumb-images-bucket',
        key=f'resized_images/{new_file_name}',
    )
    obj.put(Body=img, ContentType='image/png')
    return resized_image_url(f'resized_images/{new_file_name}', 'thumb-images-bucket', 'eu-west-2')


def resized_image_url(resized_key, bucket, region):
    return f'https://{bucket}.s3.{region}.amazonaws.com/{resized_key}'


# test
def get_file_from_s3(filename, bucket_name: str):
    """"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id='AKIATXKH6RANVQV55XHU',
        aws_secret_access_key='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',
    )

    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(bucket_name)

    count = count_files_in_s3(s3bucket)

    if count != 0:
        random_int = randint(0, count-1)
        image = list(s3bucket.objects.all())[random_int]
        return image
    else:
        return None


# test
def count_files_in_s3(s3bucket):
    total_count = 0
    for key in s3bucket.objects.all():
        total_count += 1
    return total_count
