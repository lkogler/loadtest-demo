import random
import time
from flask import Flask
app = Flask(__name__)

@app.route('/fast')
def fast():
    return 'OK'

@app.route('/slow')
def hello_world():
    time.sleep(20 + random.random() * 5.0)
    return 'OK'