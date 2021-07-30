from common.constants import DRY_RUN, FAIR_URL, BASE_HEADERS, SSL_VERIFY
from datasets.utilities import *
import requests
import json

def post_request(data):
    print (f'\nPOST {dataset_url()} --data {json.dumps(data, indent=2)}')
    if DRY_RUN: 
        print("DRY RUN - no requests sent")
        exit(0)

    print('Sending request...')
    r = requests.post(dataset_url(), headers=BASE_HEADERS, json=data, verify=SSL_VERIFY)
    if r.status_code != 201:
        data = r.json()
        print(f'Failed to create dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
        return False
    data = r.json()

    if len(data) != 1:
        print(f'Created dataset: {data["code"]}')
        print(f'View on the web at: {FAIR_URL}#/data/datasets/{data["code"]}')
    else:
        print(f'Expected 1 dataset in response - received {(data)}')

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <path to dataset definition json file> <--dry-run>')
    exit(1)

with open(definition_file(sys.argv[1])) as fh:
    payload=fh.read()
    data=json.loads(payload)
    post_request(data)
