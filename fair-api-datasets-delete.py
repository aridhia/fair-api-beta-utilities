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
    print(f'Usage: {sys.argv[0]} <path to dataset definition json file>')
    exit(1)

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']

dataset_code = sys.argv[1]
dataset_list_endpoint = f'{FAIR_API_ENDPOINT}/api/datasets/'+dataset_code

print(f'API endpoint: {dataset_list_endpoint}')
print(f'Deleting Dataset with code: {dataset_code}')

headers = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}',
    'Content-Type' : 'application/json'
}

r = requests.delete(dataset_list_endpoint, headers=headers)
if r.status_code != 204:
    data = r.json()
    print(f'Failed to delete dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
else:
    print(f'Deleted dataset with code: {dataset_code}')

           
