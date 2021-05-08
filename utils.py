import io
import os
import boto3
from random import randint
from PIL import Image


CLOUDFRONT_URL = os.environ.get('CLOUDFRONT_URL')
SOURCE_BUCKET = os.environ.get('SOURCE_BUCKET')
RESIZED_BUCKET = os.environ.get('RESIZED_BUCKET')
AWS_ACCESS_ID = os.environ.get('AWS_ACCESS_ID')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')


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
    :param file_name: S3 object name. If not specified then file_name is used
    :param file_extension: file extension
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
    """Resize image with PIL library

    :param image: binary representation of image
    :param width: target image width
    :param height: target image height
    :return: ready image url
    """

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
    """Save image to s3 with boto3.

    :param img: binary representation of image
    :param bucket: target bucket name
    :param new_file_name: target file name
    :param file_extension: file extension
    :return: URL to resized file
    """
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_ID,
                        aws_secret_access_key=AWS_ACCESS_KEY)
    obj = s3.Object(
        bucket_name=bucket,
        key=new_file_name,
    )
    obj.put(Body=img, ContentType=f'image/{file_extension}')
    return resized_image_url(new_file_name)


# test
def resized_image_url(resized_key):
    """Create a url with to file with cloudfront and s3.

    :param resized_key: path to file in s3 bucket
    :return: URL to resized file
    """
    return f'https://{CLOUDFRONT_URL}{resized_key}'


# test
def get_file_from_s3():
    """Randomly choose a file from s3 bucket.

    :return: random image from s3 source bucket.
    """
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_ID,
                        aws_secret_access_key=AWS_ACCESS_KEY)
    s3bucket = s3.Bucket(SOURCE_BUCKET)

    count = len(list(s3bucket.objects.all()))
    if count != 0:
        random_int = randint(0, count-1)
        image = list(s3bucket.objects.all())[random_int]
        return image
    else:
        return None
