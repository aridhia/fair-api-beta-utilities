from datasets.diff_helper import DiffHelper
from datasets.command_base import *


def get_request(dataset_code):
    href = dataset_url(dataset_code)
    resp = requests.get(
        href, headers=headers, verify=False
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
    if not DRY_RUN:
        print('Sending request...')
        r = requests.patch(dataset_url(dataset_code), headers=headers, json=diff, verify=False)
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

with open(definition_file()) as fh:
    payload=fh.read()
    data=json.loads(payload)
    patch_request(data)
