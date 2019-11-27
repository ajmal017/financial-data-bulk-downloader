import requests
import json
import os
from urllib import request


def post_request(url, json_query, file_output):
    with open(json_query) as json_file:
        query = json.load(json_file)
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(query), headers=headers)
        with open(file_output, "w") as f:
            f.write(r.text)
