from io import BytesIO
from uuid import uuid4

import boto3
import requests

from amazon_authentication import AmazonAuthentication
from loadtest_env import S3_BUCKET_NAME, S3_DOWNLOAD_EXAMPLE_FILENAME, VIDEO_FILE_PATH


def http_upload(file_pointer, service_base_url, access_key, secret_key):
    unique_identifier = str(uuid4())
    s3_url = "https://{}/{}/{}".format(service_base_url, S3_BUCKET_NAME, unique_identifier)
    auth = AmazonAuthentication(access_key=access_key,
                                secret_key=secret_key,
                                service_base_url=service_base_url)
    requests.put(s3_url, data=file_pointer, auth=auth)


def http_download(service_base_url, access_key, secret_key):
    s3_url = "https://{}/{}/{}".format(service_base_url, S3_BUCKET_NAME, S3_DOWNLOAD_EXAMPLE_FILENAME)
    auth = AmazonAuthentication(access_key=access_key,
                                secret_key=secret_key,
                                service_base_url=service_base_url)
    requests.get(s3_url, auth=auth)


def boto_download():
    s3 = boto3.client('s3')
    file_pointer = BytesIO()
    s3.download_fileobj(S3_BUCKET_NAME, S3_DOWNLOAD_EXAMPLE_FILENAME, file_pointer)
    file_pointer.close()


def boto_upload():
    with open(VIDEO_FILE_PATH, 'rb') as file_pointer:
        s3_connection = boto3.resource('s3')

        unique_identifier = str(uuid4())
        s3_connection.Object(S3_BUCKET_NAME, unique_identifier).put(Body=file_pointer)
