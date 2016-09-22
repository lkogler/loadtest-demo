import os
from queue import Empty

import time
from typing import Tuple

import subprocess
from kombu import BrokerConnection
from kombu.exceptions import MessageStateError
from kombu.simple import SimpleQueue

from s3_requests import boto_download

DEV_NULL = open(os.devnull, 'w')


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


def traceroute(domain) -> Tuple[float, float]:
    output_byte_string = subprocess.check_output('traceroute {} | head -n 3'.format(domain), shell=True,
                                                 stderr=DEV_NULL)
    output_byte_string = output_byte_string.decode("utf-8")
    hop_strings = output_byte_string.strip().split('\n')[1:]
    hop_averages = ()
    for h in hop_strings:
        try:
            hop_values = [float(s.strip()) for s in h.split(')')[-1].split('ms') if s]
            hop_average = (sum(hop_values) / len(hop_values)) / 1000.0
        except ValueError:
            hop_average = "TIMEOUT"
        hop_averages += (hop_average,)

    return hop_averages


def listen():
    queue = get_queue()
    while 1:
        try:
            request = queue.get(block=True, timeout=1)
            request.ack()

            decoded_request = request.decode()
            message_index = decoded_request["i"]

            download_time = timing(boto_download)
            nat_hop_1, nat_hop_2 = traceroute('s3.amazonaws.com')
            print(",QUEUE NUMBER,{},DOWNLOAD TIME,{},NAT_HOP_1,{},NAT_HOP_2,{}".format(
                message_index,
                download_time,
                nat_hop_1,
                nat_hop_2))
        except Empty:
            pass
        except MessageStateError:
            pass


if __name__ == "__main__":
    listen()
