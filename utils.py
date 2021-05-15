import io
import os
from typing import Optional

import botocore

from PIL import Image
from S3Resource.S3Resource import S3Resource


def validate_mime_type(file_type: str) -> bool:
    """Validation of the uploaded file MIME type.

    :param file_type: file content type
    :return: True if file content/type == 'image/...'
    """

    if file_type.split('/')[0] == 'image':
        return True
    return False


def upload_file_to_s3(file: bytes, file_name: str, file_extension: str) -> Optional[bool]:
    """Upload a file to an S3 bucket

    :param file: File to upload(bytes)
    :param file_name: S3 object name. If not specified then file_name is used
    :param file_extension: file extension
    :return True if no errors occur
    """

    img = Image.open(io.BytesIO(file))
    buffer = io.BytesIO()
    img.save(buffer, file_extension)
    buffer.seek(0)

    try:
        s3_resource = S3Resource()
        s3_resource.save_image_to_bucket(buffer,
                                         os.getenv('SOURCE_BUCKET'),
                                         file_name,
                                         file_extension)
    except botocore.exceptions.ClientError as error:
        raise error
    except botocore.exceptions.ParamValidationError as error:
        raise error
    return True


def resize_image(image, width: int, height: int) -> str:
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
    s3_resource = S3Resource()
    img_url = s3_resource.save_image_to_bucket(buffer,
                                               os.getenv('RESIZED_BUCKET'),
                                               f'resized_images/{new_file_name}')
    return img_url
