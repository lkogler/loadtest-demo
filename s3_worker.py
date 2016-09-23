from functools import partial
from queue import Empty

import time
from kombu import BrokerConnection
from kombu.exceptions import MessageStateError
from kombu.simple import SimpleQueue

from loadtest_env import S34ME_ACCESS_KEY_ID, S34ME_SECRET_ACCESS_KEY
from s3_requests import http_download


def timing(f):
    time1 = time.time()
    f()
    time2 = time.time()
    return time2 - time1


_queue = None


def get_queue() -> SimpleQueue:
    global _queue
    if _queue is not None:
        return _queue

    sqs_uri = "sqs://sqs.us-east-1.amazonaws.com/425153808285/loadtest-demo"
    connection = BrokerConnection(sqs_uri, transport_options={'confirm_publish': True})
    connection.ensure_connection(errback=lambda exception, interval: print(exception),
                                 max_retries=5,
                                 interval_start=1,
                                 interval_step=1,
                                 callback=lambda exception, interval: print(exception))
    _queue = connection.SimpleQueue('loadtest-demo')
    _queue.consumer.qos(prefetch_count=1)
    return _queue


def publish(message_count):
    for message_index in range(message_count):
        queue = get_queue()
        queue.put({"i": message_index}, serializer='json')


def listen():
    queue = get_queue()
    while 1:
        try:
            request = queue.get(block=True, timeout=1)
            request.ack()

            decoded_request = request.decode()
            message_index = decoded_request["i"]
            download = partial(http_download, **{'service_base_url': 'rest.s3for.me',
                                                 'access_key': S34ME_ACCESS_KEY_ID,
                                                 'secret_key': S34ME_SECRET_ACCESS_KEY})

            download_time = timing(download)
            print(",QUEUE NUMBER,{},DOWNLOAD TIME,{}".format(message_index, download_time))
        except Empty:
            pass
        except MessageStateError:
            pass


if __name__ == "__main__":
    listen()
