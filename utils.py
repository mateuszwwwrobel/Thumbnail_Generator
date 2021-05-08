import logging
import io
import boto3
from botocore.exceptions import ClientError
from random import randint
from PIL import Image

CLOUDFRONT_URL = 'di9ryp57fjv5f.cloudfront.net/'
SOURCE_BUCKET = 'thumb-images-bucket'
RESIZED_BUCKET = 'resized-thumbnails-bucket'


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
def upload_file_to_s3(file: bytes, file_name: str, file_extension: str):
    """Upload a file to an S3 bucket

    :param file: File to upload(bytes)
    :param bucket: Bucket to upload to
    :param file_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    img = Image.open(io.BytesIO(file))
    buffer = io.BytesIO()
    img.save(buffer, file_extension)
    buffer.seek(0)
    try:
        save_image(buffer, SOURCE_BUCKET, file_name, file_extension)
    except:
        return False
    return True


# test
def resize_image(image, width: int, height: int):
    """"""
    image_body = image.get()['Body'].read()
    img = Image.open(io.BytesIO(image_body))
    img = img.resize((width, height), Image.ANTIALIAS)
    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    new_file_name = f'{width}x{height}-{image.key}'
    img_url = save_image(buffer, RESIZED_BUCKET, f'resized_images/{new_file_name}')
    return img_url


# test
def save_image(img, bucket, new_file_name, file_extension='png'):
    """"""
    s3 = boto3.resource('s3')
    obj = s3.Object(
        bucket_name=bucket,
        key=new_file_name,
    )
    obj.put(Body=img, ContentType=f'image/{file_extension}')
    return resized_image_url(new_file_name)


# test
def resized_image_url(resized_key):
    """"""
    return f'https://{CLOUDFRONT_URL}{resized_key}'


# test
def get_file_from_s3():
    """"""
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(SOURCE_BUCKET)

    count = len(list(s3bucket.objects.all()))
    if count != 0:
        random_int = randint(0, count-1)
        image = list(s3bucket.objects.all())[random_int]
        return image
    else:
        return None
