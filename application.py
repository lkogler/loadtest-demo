import random
import time
from tempfile import TemporaryFile

from flask import Flask, request, send_file
from uuid import uuid4
import os
import boto
from io import BytesIO
import math

application = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VIDEO_FILE_PATH = os.path.join(PROJECT_ROOT, "please_dont_ever_share_this.mov")
FILE_SEGMENT_SIZE = 5000 * 1024 * 1024
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', None)
S3_DOWNLOAD_EXAMPLE_FILENAME = os.environ.get('S3_DOWNLOAD_EXAMPLE_FILENAME', None)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', None)


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


@application.route('/s3_upload')
def my_s3_upload():
    s3_upload(VIDEO_FILE_PATH)

    return 'OK'


@application.route('/s3_download')
def my_s3_download():
    s3_download(S3_DOWNLOAD_EXAMPLE_FILENAME)

    return 'OK'


def s3_upload(file_path):
    with open(file_path, 'rb') as file_pointer:
        s3_connection = boto.connect_s3(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY)
        bucket = s3_connection.get_bucket(S3_BUCKET_NAME)

        multipart_upload = bucket.initiate_multipart_upload(str(uuid4()))

        bytes_io_object = BytesIO(file_pointer.read())
        file_size = bytes_io_object.getbuffer().nbytes

        chunks_count = int(math.ceil(file_size / float(FILE_SEGMENT_SIZE)))

        for i in range(chunks_count):
            byte_offset = i * FILE_SEGMENT_SIZE
            bytes_to_go = file_size - byte_offset
            byte_count = min([FILE_SEGMENT_SIZE, bytes_to_go])
            file_pointer.seek(byte_offset)
            multipart_upload.upload_part_from_file(fp=file_pointer, part_num=(i + 1), size=byte_count)
            file_pointer.seek(0)

        bytes_io_object.close()
        if len(multipart_upload.get_all_parts()) == chunks_count:
            multipart_upload.complete_upload()
        else:
            multipart_upload.cancel_upload()
            raise Exception('Failed to upload file \'{}\' to S3'.format(file_path))


def s3_download(s3_filename):
    file_pointer = BytesIO()
    s3_connection = boto.connect_s3(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_KEY)
    s3_connection.get_bucket(S3_BUCKET_NAME).get_key(
        s3_filename).get_contents_to_file(file_pointer)
    file_pointer.seek(0)

    return file_pointer
