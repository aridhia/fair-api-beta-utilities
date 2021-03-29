import requests
import os
import json
import sys
from datasets.diff_helper import DiffHelper

if 'FAIR_API_TOKEN' not in os.environ:
    print('Please add FAIR_API_TOKEN to the environment')
    exit(1)

if 'FAIR_API_ENDPOINT' not in os.environ:
    print('Please add FAIR_API_ENDPOINT to the environment')
    exit(1)

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <path to dataset definition json file>')
    exit(1)
    
FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']
https = 'https://'

if FAIR_API_ENDPOINT[:5] == 'https':
    https = ''

definition_file = sys.argv[1]
if not os.path.isfile(definition_file):
    print(f'Definition file not valid: {definition_file}')
    exit(1)

dataset_list_endpoint = f'{https}{FAIR_API_ENDPOINT}datasets'
FAIR_URL = f'{https}{FAIR_API_ENDPOINT}'[:-4]

print(f'API endpoint: {dataset_list_endpoint}')
print(f'Posting definition: {definition_file}')

headers = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}',
    'Content-Type' : 'application/json'
}

def dataset_url():
  return f'{https}{FAIR_API_ENDPOINT}datasets/'

def patch_request(data):
  dataset_code = data['catalogue']['id']

  href = f'{https}{FAIR_API_ENDPOINT}datasets/{dataset_code}'
  resp = requests.get(
    href, headers=headers, verify=False
  )
  original = resp.json()

  print (f'ORIGINAL {json.dumps(original, indent=2)}')
  
  diff = DiffHelper.dataset_diff(original, data)

  print (f'PATCH {dataset_url()} --data {json.dumps(diff, indent=2)}')
  # href = f'{https}{FAIR_API_ENDPOINT}datasets/{dataset_code}'
  # resp = requests.patch(
  #   href, headers=headers, json=data, verify=False
  # )
  # print('patched')
  # print(resp.json())  

with open(definition_file) as fh:
    payload=fh.read()
    data=json.loads(payload)
    print (f'POSTING {json.dumps(data, indent=2)}')

    r = requests.post(dataset_list_endpoint, headers=headers, json=data, verify=False)
    if r.status_code == 400 and r.json()["error"]["message"] == 'Dataset already exists':
      print('already exists')
      patch_request(data)
    elif r.status_code != 201:
        data = r.json()
        print(f'Failed to create dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
    else:
        data = r.json()
  
        if len(data) != 1:
            print(f'Created dataset: {data["code"]}')
            print(f'View on the web at: {FAIR_URL}#/data/datasets/{data["code"]}')
        else:
            print(f'Expected 1 dataset in response - received {(data)}')
           
