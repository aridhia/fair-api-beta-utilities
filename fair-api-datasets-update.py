import requests
import json
import sys
from datasets.diff_helper import DiffHelper
from datasets.utilities import dataset_url, ensure_file_exists
from common.constants import BASE_HEADERS, SSL_VERIFY, FAIR_URL, DRY_RUN

def get_request(dataset_code):
    href = dataset_url(dataset_code)
    resp = requests.get(
        href, headers=BASE_HEADERS, verify=SSL_VERIFY
    )
    if resp.status_code != 200:
        data = resp.json()
        print(f'\nFailed to get dataset: Status code: {resp.status_code}, Error message: {data["error"]["message"]}')
        exit(1)
    return resp

def patch_request(data):
    dataset_code = data['catalogue']['id']
    resp = get_request(dataset_code)
    original = resp.json()
    diff = DiffHelper.dataset_diff(original, data)
    print (f'\nPATCH {dataset_url(dataset_code)} --data {json.dumps(diff, indent=2)}')
    if DRY_RUN: return
    print('Sending request...')
    r = requests.patch(dataset_url(dataset_code), headers=BASE_HEADERS, json=diff, verify=SSL_VERIFY)
    if r.status_code != 200:
        data = r.json()
        print(f'Failed to patch dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
    else:
        data = r.json()    
        if len(data) != 1:
            print(f'Patched dataset: {data["code"]}')
            print(f'View on the web at: {FAIR_URL}#/data/datasets/{data["code"]}')
        else:
            print(f'Expected 1 dataset in response - received {(data)}')

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <path to dataset definition json file> <--dry-run>')
    exit(1)
with open(ensure_file_exists(sys.argv[1])) as fh:
    payload=fh.read()
    data=json.loads(payload)
    patch_request(data)
