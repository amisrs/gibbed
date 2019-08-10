#!/usr/bin/python3

import os
from flask import Flask, request, jsonify
from sample_queue import SampleQueue

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)

app.config.from_pyfile('config.py', silent=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass
buffer_max = 5
sample_queue = SampleQueue(buffer_max)
print("Queue initialised.")

@app.route('/death/<name>', methods=['GET'])
def die(name):
    # name = request.args.get('name', type=str)
    fake_name, primer, sentence = sample_queue.pop()
    return jsonify((primer + sentence).replace(fake_name, name))

@app.route('/death', methods=['POST'])
def change_length():
    data = request.get_json()
    sample_queue.length = int(data["length"])
    return "After " + str(sample_queue.queue.qsize()) +", new length: " + str(sample_queue.length)

@app.route('/buffer', methods=['GET', 'POST'])
def buffer():
    if request.method == 'GET':
        return "Sentence buffer: " + str(sample_queue.queue.qsize()) + " / " + str(sample_queue.buffer_max)
    elif request.method == 'POST':
        data = request.get_json()
        sample_queue.resize(int(data["size"]))
        return "Sentence buffer: " + str(sample_queue.queue.qsize()) + " / " + str(sample_queue.buffer_max)

