import os
import random
import time
from tempfile import TemporaryFile
from uuid import uuid4

from flask import Flask, request, send_file

from s3_requests import http_upload, http_download, boto_upload, boto_download
from loadtest_env import VIDEO_FILE_PATH, PROJECT_ROOT, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S34ME_ACCESS_KEY_ID, \
    S34ME_SECRET_ACCESS_KEY

application = Flask(__name__)


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
        http_upload(file_pointer,
                    service_base_url='s3.amazonaws.com',
                    access_key=AWS_ACCESS_KEY_ID,
                    secret_key=AWS_SECRET_ACCESS_KEY)

        return 'OK'


@application.route('/s3_download_http')
def s3_download_http():
    http_download(service_base_url='s3.amazonaws.com',
                  access_key=AWS_ACCESS_KEY_ID,
                  secret_key=AWS_SECRET_ACCESS_KEY)
    return 'OK'


@application.route('/s34me_upload_http')
def s34me_upload_http():
    with open(VIDEO_FILE_PATH, 'rb') as file_pointer:
        http_upload(file_pointer,
                    service_base_url='rest.s3for.me',
                    access_key=S34ME_ACCESS_KEY_ID,
                    secret_key=S34ME_SECRET_ACCESS_KEY)

    return 'OK'


@application.route('/s34me_download_http')
def s34me_download_http():
    http_download(service_base_url='rest.s3for.me',
                  access_key=S34ME_ACCESS_KEY_ID,
                  secret_key=S34ME_SECRET_ACCESS_KEY)

    return 'OK'


@application.route('/s3_upload_boto')
def s3_upload_boto():
    boto_upload()

    return 'OK'


@application.route('/s3_download_boto')
def s3_download_boto():
    boto_download()

    return 'OK'
