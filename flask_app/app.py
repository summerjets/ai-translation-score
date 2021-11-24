from flask import Flask
from flask import request, jsonify
from random import sample

server = Flask(__name__)

@server.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        return 'This is a GET request'
    else:
        return "This is not a GET request"

