import random
import time
from io import BytesIO
from tempfile import TemporaryFile

import boto3
import requests
from flask import Flask, request, send_file
from uuid import uuid4
import os

from amazon_authentication import AmazonAuthentication

application = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VIDEO_FILE_PATH = os.path.join(PROJECT_ROOT, "please_dont_ever_share_this.mov")
FILE_SEGMENT_SIZE = 5000 * 1024 * 1024
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', None)
S3_DOWNLOAD_EXAMPLE_FILENAME = os.environ.get('S3_DOWNLOAD_EXAMPLE_FILENAME', None)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)


@application.route('/upload', methods=['POST'])
def upload():
    if 'big_file' in request.files:
        return 'OK'
    return 'Not OK'


@application.route('/upload_and_save_tempfile', methods=['POST'])
def upload_and_save_tempfile():
    if 'big_file' in request.files:
        file = request.files['big_file']
        return 'OK'
    return 'Not OK'


@application.route('/upload_and_save_non_tempfile', methods=['POST'])
def upload_and_save_non_tempfile():
    if 'big_file' in request.files:
        file = request.files['big_file']

        unique_filename = os.path.join(PROJECT_ROOT, str(uuid4()))
        file.save(unique_filename)
        os.remove(unique_filename)

        return 'OK'
    return 'Not OK'


@application.route('/save_file')
def save_file():
    with open(VIDEO_FILE_PATH, 'rb') as video_file:
        unique_filename = os.path.join(PROJECT_ROOT, str(uuid4()))
        with open(unique_filename, 'wb') as saved_file:
            saved_file.write(video_file.read())
        os.remove(unique_filename)

    return 'OK'


@application.route('/download')
def download():
    return send_file(VIDEO_FILE_PATH,
                     attachment_filename='video.mov',
                     as_attachment=True,
                     mimetype='application/quicktime')


@application.route('/save_tempfile')
def save_tempfile():
    with open(VIDEO_FILE_PATH, 'rb') as video_file:
        temporary_file = TemporaryFile()
        temporary_file.write(video_file.read())
    return 'OK'


@application.route('/fast')
def fast():
    return 'OK'


@application.route('/slow')
def slow():
    time.sleep(20 + random.random() * 5.0)
    return 'OK'


@application.route('/cpu')
def cpu():
    for i in range(3000):
        for x in range(100000):
            x * x
    return 'OK'


@application.route('/s3_upload_http')
def s3_upload_http():
    with open(VIDEO_FILE_PATH, 'rb') as file_pointer:
        unique_identifier = str(uuid4())
        s3_url = "https://s3.amazonaws.com/{}/{}".format(S3_BUCKET_NAME, unique_identifier)
        auth = AmazonAuthentication(access_key=AWS_ACCESS_KEY_ID, secret_key=AWS_SECRET_ACCESS_KEY)
        requests.put(s3_url, data=file_pointer, auth=auth)

    return 'OK'


@application.route('/s3_download_http')
def s3_download_http():
    s3_url = "https://s3.amazonaws.com/{}/{}".format(S3_BUCKET_NAME, S3_DOWNLOAD_EXAMPLE_FILENAME)
    auth = AmazonAuthentication(access_key=AWS_ACCESS_KEY_ID, secret_key=AWS_SECRET_ACCESS_KEY)
    requests.get(s3_url, auth=auth)
    return 'OK'


@application.route('/s3_upload_boto')
def s3_upload_boto():
    with open(VIDEO_FILE_PATH, 'rb') as file_pointer:
        s3_connection = boto3.resource('s3')

        unique_identifier = str(uuid4())
        s3_connection.Object(S3_BUCKET_NAME, unique_identifier).put(Body=file_pointer)

    return 'OK'


@application.route('/s3_download_boto')
def s3_download_boto():
    s3 = boto3.client('s3')
    file_pointer = BytesIO()
    s3.download_fileobj(S3_BUCKET_NAME, S3_DOWNLOAD_EXAMPLE_FILENAME, file_pointer)
    file_pointer.close()

    return 'OK'
