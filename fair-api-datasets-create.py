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

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <path to dataset defintion json file>')
    exit(1)

definition_file = sys.argv[1]
if not os.path.isfile(definition_file):
    print(f'Definition file not valid: {definition_file}')
    exit(1)

dataset_list_endpoint = f'{FAIR_API_ENDPOINT}/api/datasets'

print(f'API endpoint: {dataset_list_endpoint}')
print(f'Posting definition: {definition_file}')

headers = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}',
    'Content-Type' : 'application/json'
}

with open(definition_file) as fh:
    data = json.load(fh)

    r = requests.post(dataset_list_endpoint, headers=headers, json=data)

    if r.status_code != 200:
        data = r.json()
        print(f'Failed to create dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
    else:
        print(r.status_code)
        print(r.content)