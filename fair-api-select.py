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

    r = requests.post(f'{FAIR_API_ENDPOINT}/api/selection/select', headers=headers, json=payload)
    if r.status_code != 200:
        print(f'Failed to select: ({r.status_code}) {r.content}') 
    else:
        print(r.json())
