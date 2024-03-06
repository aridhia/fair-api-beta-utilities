import json
import sys
import os
import requests
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DICTIONARIES_URL, EXIT_FAILED_REQUEST, EXIT_MISSING_ARGUMENTS, SSL_VERIFY, DRY_RUN
from common.utilities import request_as_curl


def patch_request(code, data):
    url = f"{DICTIONARIES_URL}{code}"
    print(request_as_curl(url, 'PATCH', data))
    if DRY_RUN:
        print("DRY RUN - no requests sent")
        return
    print('Sending request...')
    response = requests.patch(
        url, headers=AUTHENTICATED_HEADERS, json=data, verify=SSL_VERIFY)
    data = response.json()
    if response.status_code != 200:
        print(
            f'Failed to patch dataset: Status code: {response.status_code}, Error message: {data["error"]["message"]}')
        exit(EXIT_FAILED_REQUEST)
    else:
        if len(data) != 1:
            print(f'Patched dictionary: {data["code"]}')
            print(json.dumps(data, indent=4))
        else:
            print(f'Expected 1 dictionary in response - received {(data)}')


# Script must be run with at least 1 argument
if len(sys.argv) < 3:
    print(
        f'Usage: {sys.argv[0]} <code> <path to dictionary patch json file> <--dry-run>')
    exit(EXIT_MISSING_ARGUMENTS)

# First argument must be a path to a file
patch_file = sys.argv[2]
if not os.path.isfile(patch_file):
    print(
        f'Provided path "{patch_file}" does not seem to be a file, ensure the path is correct and try again')
    exit(EXIT_MISSING_ARGUMENTS)

code = sys.argv[1]

with open(patch_file) as fh:
    payload = fh.read()
    data = json.loads(payload)
    patch_request(code, data)
