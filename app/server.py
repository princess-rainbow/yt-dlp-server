#!/usr/bin/env python3
'''foo'''
# pylint: disable=W0702,C0301
import os
import sys
from flask import Flask, request
from worker import add

try:
    SSL_CERT_PATH = os.environ.get("SSL_CERT_PATH")
    SSL_KEY_PATH = os.environ.get("SSL_KEY_PATH")
    LISTEN_PORT = os.environ.get("LISTEN_PORT", 8801)
except:
    print("Variables not set")
    sys.exit(1)

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    '''index'''
    if request.method == 'POST':
        url = request.form.get('url')
        add.delay(url)
        return "OK\n"
    return "foo\n"


@app.after_request
def add_header(response):
    '''Access-Control-Allow-Origin'''
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == "__main__":
        app.run(host="0.0.0.0", port=LISTEN_PORT, debug=True,
                ssl_context=(SSL_CERT_PATH, SSL_KEY_PATH))
