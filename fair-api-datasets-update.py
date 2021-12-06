import json
import sys
import os
import requests
from datasets.diff_helper import DiffHelper
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DATASETS_URL, EXIT_FAILED_REQUEST, EXIT_MISSING_ARGUMENTS, SSL_VERIFY, FAIR_URL, DRY_RUN

def dataset_url(code):
    return f"{DATASETS_URL}{code}"

def get_request(dataset_code):
    resp = requests.get(
        dataset_url(dataset_code), headers=AUTHENTICATED_HEADERS, verify=SSL_VERIFY
    )
    if resp.status_code != 200:
        data = resp.json()
        print(
            f'\nFailed to get dataset: Status code: {resp.status_code}, Error message: {data["error"]["message"]}')
        exit(EXIT_FAILED_REQUEST)
    return resp


def patch_request(data):
    dataset_code = data['code']
    resp = get_request(dataset_code)
    original = resp.json()
    diff = DiffHelper.dataset_diff(original, data)
    print(
        f'\nPATCH {dataset_url(dataset_code)} --data {json.dumps(diff, indent=2)}')
    if DRY_RUN:
        return  # In dry-run mode we do nothing past this point
    print('Sending request...')
    response = requests.patch(
        dataset_url(dataset_code),
        headers=AUTHENTICATED_HEADERS,
        json=diff,
        verify=SSL_VERIFY
    )
    data = response.json()
    if response.status_code != 200:
        print(
            f'Failed to patch dataset: Status code: {response.status_code}, Error message: {data["error"]["message"]}')
        exit(EXIT_FAILED_REQUEST)
    if len(data) != 1:
        print(f'Patched dataset: {data["code"]}')
        print(f'View on the web at: {FAIR_URL}#/data/datasets/{data["code"]}')
    else:
        print(f'Expected 1 dataset in response - received {(data)}')


# Script must be run with at least 1 argument
if len(sys.argv) < 2:
    print(
        f'Usage: {sys.argv[0]} <path to dataset definition json file> <--dry-run>')
    exit(EXIT_MISSING_ARGUMENTS)

# First argument must be a path to a file
definition_file = sys.argv[1]
if not os.path.isfile(definition_file):
    print(
        f'Provided path "{definition_file}" does not seem to be a file, ensure the path is correct and try again')
    exit(EXIT_MISSING_ARGUMENTS)

with open(definition_file) as fh:
    payload = fh.read()
    data = json.loads(payload)
    patch_request(data)
