import random
import time
from tempfile import TemporaryFile

from flask import Flask, request
from uuid import uuid4
import os

application = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
VIDEO_FILE_PATH = os.path.join(PROJECT_ROOT, "please_dont_ever_share_this.mov")


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
