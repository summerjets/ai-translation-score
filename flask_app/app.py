from flask import Flask
from flask import request, jsonify
from random import sample

import torch
torch.set_num_threads(1)

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-albert-small-v2', device="cpu")

server = Flask(__name__)

@server.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'GET':
        _test = model.encode(["warmup test"])
        return f"This is a GET request {_test}"
    else:
        return "This is not a GET request"

