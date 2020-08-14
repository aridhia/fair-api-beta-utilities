import requests
import os
import json
import sys

if 'FAIR_API_TOKEN' not in os.environ:
    print('Please add FAIR_API_TOKEN to the environment')
    exit(1)

if 'FAIR_API_ENDPOINT' not in os.environ:
    print('Please add FAIR_API_ENDPOINT to the environment')
    exit(1)

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <graphql_file>')
    exit(1)

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']

graphql_file = sys.argv[1]
if not os.path.isfile(graphql_file):
    print(f'Data file missing: {graphql_file}')
    exit(1) 

with open(graphql_file) as fh:
    graphql = fh.read().strip()

    payload = {
        'query': graphql
    }
    headers = {
        'Authorization': f'Bearer {FAIR_API_TOKEN}',
        'Content-type': 'application/json'
    }

    selection_endpoint = f'{FAIR_API_ENDPOINT}/api/selection/select'

    r = requests.post(selection_endpoint, headers=headers, json=payload)
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
        print(r.json())
