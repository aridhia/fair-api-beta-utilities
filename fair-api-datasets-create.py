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
    print(f'Usage: {sys.argv[0]} <path to dataset defintion json file>')
    exit(1)

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']

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
    payload = {
        "datasets": [
            json.load(fh)
        ]
    }
        
    r = requests.post(dataset_list_endpoint, headers=headers, json=payload)
    if r.status_code != 201:
        data = r.json()
        print(f'Failed to create dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
    else:
        data = r.json()
        if len(data) != 1:
            print(f'Expected 1 dataset in response - received {ken(data)}')
            print(json.dumps(data))
        else:
            dataset = data[0]
            # TODO - dataset['id'] may be confusing here. Need to review API?
            print(f'Created dataset: {dataset["code"]} (Ref. {dataset["id"]})')
            print(f'View on the web at: {FAIR_API_ENDPOINT}/#/data/datasets/{dataset["code"]}')