import json
import requests
import sys
from common.constants import BASE_HEADERS, SSL_VERIFY, DRY_RUN
from dictionaries.utilities import dictionary_url, patch_file

def patch_request(data):
    code = data['code']
    url = dictionary_url(code)
    print (f'\nPATCH {url} --data {json.dumps(data, indent=2)}')
    if DRY_RUN:
        print("DRY RUN - no requests sent")
        return
    print('Sending request...')
    response = requests.patch(dictionary_url(code), headers=BASE_HEADERS, json=data, verify=SSL_VERIFY)
    if response.status_code != 200:
        data = response.json()
        print(f'Failed to patch dataset: Status code: {response.status_code}, Error message: {data["error"]["message"]}')
    else:
        data = response.json()    
        if len(data) != 1:
            print(f'Patched dictionary: {data["code"]}')
            print(json.dumps(data, indent=4))
        else:
            print(f'Expected 1 dictionary in response - received {(data)}')

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <path to dictionary patch json file> <--dry-run>')
    exit(1)
with open(patch_file()) as fh:
    payload=fh.read()
    data=json.loads(payload)
    patch_request(data)
