import json
import sys
import os
import requests
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DRY_RUN, FAIR_URL, SSL_VERIFY, DATASETS_URL


def post_request(data):
    print(f'\nPOST {DATASETS_URL} --data {json.dumps(data, indent=2)}')
    if DRY_RUN:
        print("DRY RUN - no requests sent")
        exit(0)

    print('Sending request...')
    response = requests.post(
        DATASETS_URL, headers=AUTHENTICATED_HEADERS, json=data, verify=SSL_VERIFY)
    if response.status_code != 201:
        data = response.json()
        print(
            f'Failed to create dataset: Status code: {response.status_code}, Error message: {data["error"]["message"]}')
        exit(1)
    data = response.json()

    if len(data) != 1:
        print(f'Created dataset: {data["code"]}')
        print(f'View on the web at: {FAIR_URL}#/data/datasets/{data["code"]}')
    else:
        print(f'Expected 1 dataset in response - received {(data)}')


# Script must be run with at least 1 argument
if len(sys.argv) < 2:
    print(
        f'Usage: {sys.argv[0]} <path to dataset definition json file> <--dry-run>')
    exit(1)

# First argument must be a path to a file
definition_file = sys.argv[1]
if not os.path.isfile(definition_file):
    print(
        f'Provided path "{definition_file}" does not seem to be a file, ensure the path is correct and try again')
    exit(1)

with open(definition_file) as fh:
    payload = fh.read()
    data = json.loads(payload)
    post_request(data)
