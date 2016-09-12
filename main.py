import random
import time
from flask import Flask
app = Flask(__name__)

@app.route('/fast')
def fast():
    return 'OK'

@app.route('/slow')
def slow():
    time.sleep(20 + random.random() * 5.0)
    return 'OK'

@app.route('/cpu')
def cpu():
    for x in range(300000000):
        x*x
    return 'OK'