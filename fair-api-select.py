import os
import json
import sys
import requests
from common.constants import BASE_HEADERS, SSL_VERIFY, FAIR_API_ENDPOINT

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <graphql_file>')
    exit(1)

graphql_file = sys.argv[1]
if not os.path.isfile(graphql_file):
    print(f'Data file missing: {graphql_file}')
    exit(1)

with open(graphql_file) as fh:
    graphql = fh.read().strip()

    payload = {
        'query': graphql
    }

    selection_endpoint = f'{FAIR_API_ENDPOINT}selection/select'

    r = requests.post(selection_endpoint, headers=BASE_HEADERS, json=payload, verify=SSL_VERIFY)
    if r.status_code != 200:
        error = {
            'endpoint': selection_endpoint,
            'graphql_file': graphql_file,
            'error': f'Selection failed',
            'message':  str(r.content),
            'status_code': r.status_code
        }
        print(json.dumps(error))
    else:
        print(json.dumps(r.json()))
