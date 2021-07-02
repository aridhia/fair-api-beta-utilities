from datasets.diff_helper import DiffHelper
from datasets.command_base import *


def post_request(data):
    print (f'\nPOST {dataset_url()} --data {json.dumps(data, indent=2)}')

    if not DRY_RUN:
        print('Sending request...')
        r = requests.post(dataset_list_endpoint, headers=headers, json=data, verify=False)
        if r.status_code != 201:
            data = r.json()
            print(f'Failed to create dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
        else:
            data = r.json()
    
            if len(data) != 1:
                print(f'Created dataset: {data["code"]}')
                print(f'View on the web at: {FAIR_URL}#/data/datasets/{data["code"]}')
            else:
                print(f'Expected 1 dataset in response - received {(data)}')

with open(definition_file()) as fh:
    payload=fh.read()
    data=json.loads(payload)
    post_request(data)
