import random
import time
from flask import Flask

application = Flask(__name__)


@application.route('/fast')
def fast():
    return 'OK'


@application.route('/slow')
def slow():
    time.sleep(20 + random.random() * 5.0)
    return 'OK'


@application.route('/cpu')
def cpu():
    for i in range(3):
        for x in range(100000000):
            x * x
    return 'OK'
