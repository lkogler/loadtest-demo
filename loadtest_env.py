import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_SEGMENT_SIZE = 5000 * 1024 * 1024
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
S34ME_ACCESS_KEY_ID = os.environ.get('S34ME_ACCESS_KEY_ID', None)
S34ME_SECRET_ACCESS_KEY = os.environ.get('S34ME_SECRET_ACCESS_KEY', None)
VIDEO_FILE_PATH = os.path.join(PROJECT_ROOT, "please_dont_ever_share_this.mov")
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', None)
S3_DOWNLOAD_EXAMPLE_FILENAME = os.environ.get('S3_DOWNLOAD_EXAMPLE_FILENAME', None)
