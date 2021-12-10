from flask import Flask
from flask import request, jsonify, make_response, abort
from random import sample
import json
import scipy
import os
import torch

torch.set_num_threads(1)

## START CONFIG
MATCH_THRESHOLD = 0.8
## END CONFIG

API_KEY = os.environ.get("TRANSLATION_API_KEY", None)

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-albert-small-v2', device="cpu")
_test = model.encode(["warmup test"])

server = Flask(__name__)


@server.route('/health', methods=['GET'])
def health():

    response = {"status": "healthy"}

    return make_response(jsonify(response), 200)


@server.route('/compare', methods=['POST'])
def compare():

    payload = request.json
    api_key_passed = request.headers.get("X-Api-Key")

    invalid_auth_return = json.dumps({"status": "error",
                           "payload": {
                               "message": "invalid authentication"}
                           }
                        )

    # Check authentication keys
    if api_key_passed is None:

    	return invalid_auth_return

    elif API_KEY != api_key_passed:

    	return invalid_auth_return

    # Check payload is well constructed
    if payload == None:
        return json.dumps({"status": "error",
                           "payload": {
                               "message": "payload is empty"}
                           }
                        )

    exemplar = payload.get("exemplar", None)
    submission = payload.get("submission", None)

    if exemplar == None:
        return json.dumps({"status": "error",
                           "payload": {
                               "message": "exemplar not in payload"
                               }
                           }
                        )
    elif type(exemplar) != list:
        return json.dumps({"status": "error",
                           "payload": {
                               "message": "exemplar not of type array"
                               }
                           }
                        )

    if submission == None:
        return json.dumps({"status": "error",
                           "payload": {
                               "message": "submission not in payload"
                               }
                           }
                        )

    try:
        # Convert into separate sentences
        exemplar_embeddings = model.encode(exemplar)
        query_embeddings = model.encode([submission])

        distances = scipy.spatial.distance.cdist(query_embeddings, exemplar_embeddings, "cosine")[0]
        distances = [1-x for x in distances]

        score = max(distances)

        if any([x >= MATCH_THRESHOLD for x in distances]):
            accept = True
        else:
            accept = False

        response = json.dumps({"status": "success",
                               "payload": {
                                    "comparison_score": score,
                                    "accept_solution": accept,
                                          }
                                }
                              )
    except:
        response = json.dumps({"status": "error",
                           "payload": {
                               "message": "error running AI module."
                               }
                           }
                        )

    return response


# For debugging
if __name__ == '__main__':

    server.run()
