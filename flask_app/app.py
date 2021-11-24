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


from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-albert-small-v2', device="cpu")
_test = model.encode(["warmup test"])

server = Flask(__name__)


@server.route('/health', methods=['GET'])
def health():

    response = {"status": "healthy"}

    return make_response(jsonify(response), 200)


@server.route('/comparenoauth', methods=['POST'])
def comparenoauth():

    payload = request.json
    api_key = request.headers.get("X-Api-Key")

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
