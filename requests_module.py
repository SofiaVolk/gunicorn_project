from flask import request, jsonify
import marshmallow
import time

import logs
from flaskapp import app
# from model.ml import wish_handler


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    total_time = (time.time() - request.start_time) * 1000
    logs.api_logger.info(f'{request.method}\t {request.path}\t - Total time: {total_time}')
    return response


def setup_metrics(application):
    application.before_request(start_timer)
    application.after_request(stop_timer)


def log_decor(func):
    def wrapper(content):
        msg, status = func(content)
        logs.api_logger.info(f'{msg} <{status}>')
        return status
    return wrapper


class DataSchema(marshmallow.Schema):
    text = marshmallow.fields.Str(required=True)


def no_content(content):
    msg = 'no content'
    if not content:
        logs.api_logger.error('Request failed <400>:\t' + msg)
        return True
    else:
        return False


@log_decor
@app.route('/', methods=['POST'])
def index():
    content = request.json
    if no_content(content):
        return '', 400
    try:
        DataSchema(strict=True).load(content).data
        # wish_handler(content)
    except marshmallow.exceptions.ValidationError as e:
        return jsonify(e.messages), 400

    return '', 200


'''
@log_decor
@app.route('/vacancy', methods=['POST'])
def post_similar_vacancy():
    content = request.json
    if no_content(content):
        return '', 400

    try:
        DataSchema(strict=True).load(content).data

    except marshmallow.exceptions.ValidationError as e:
        return jsonify(e.messages), 400

    return '', 200


@log_decor
@app.route('/classvacancy', methods=['POST'])
def post_classify_vacancy():
    content = request.json
    if no_content(content):
        return '', 400
    try:
        DataSchema(strict=True).load(content).data

    except marshmallow.exceptions.ValidationError as e:
        return jsonify(e.messages), 400

    return '', 200


@log_decor
@app.route('/product', methods=['POST'])
def post_similar_product():
    content = request.json
    if no_content(content):
        return '', 400

    try:
        DataSchema(strict=True).load(content).data
        
    except marshmallow.exceptions.ValidationError as e:
        return jsonify(e.messages), 400

    return '', 200
'''

if __name__ == '__main__':
    setup_metrics(app)
    app.run(host="127.0.0.1", port="5000")

