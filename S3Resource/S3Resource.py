import os
import boto3
from random import randint


class S3Resource:
    """Class for making a connection to AWS S3 resources."""

    def __init__(self):
        self.s3 = boto3.resource('s3',
                                 aws_access_key_id=os.environ.get('AWS_ACCESS_ID'),
                                 aws_secret_access_key=os.environ.get('AWS_ACCESS_KEY'))

    def get_random_file(self, bucket_name):
        """Randomly choose a file from s3 bucket.

        :return: random image from s3 source bucket.
        """
        s3bucket = self.s3.Bucket(bucket_name)

        count = len(list(s3bucket.objects.all()))
        if count != 0:
            random_int = randint(0, count - 1)
            image = list(s3bucket.objects.all())[random_int]
            return image
        else:
            return None

    def save_image_to_bucket(self, image, bucket_name, new_file_name, file_extension='png'):

        obj = self.s3.Object(
            bucket_name=bucket_name,
            key=new_file_name,
        )

        obj.put(Body=image, ContentType=f'image/{file_extension}')
        return resized_image_url(new_file_name)


def resized_image_url(resized_key):
    """Create a url with to file with cloudfront and s3.

    :param resized_key: path to file in s3 bucket
    :return: URL to resized file
    """
    return f'https://{os.getenv("CLOUDFRONT_URL")}{resized_key}'
