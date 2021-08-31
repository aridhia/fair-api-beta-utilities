import requests
import os
import json

if 'FAIR_API_TOKEN' not in os.environ:
    print('Please add FAIR_API_TOKEN to the environment')
    exit(1)

if 'FAIR_API_ENDPOINT' not in os.environ:
    print('Please add FAIR_API_ENDPOINT to the environment')
    exit(1)

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']
https = 'https://'

if FAIR_API_ENDPOINT[:5] == 'https':
    https = ''

headers = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}'
}

dataset_list_endpoint = f'{https}{FAIR_API_ENDPOINT}datasets'
r = requests.get(dataset_list_endpoint, headers=headers)
if r.status_code != 200:
    error_data = r.json()
    print(f'Failed to retrieve dataset list. Status code: {r.status_code}, Error message: {error_data["error"]["message"]}')
else:
    data = r.json()
    # To output the JSON, use this 
    # print(json.dumps(data))
    
    print(f'Datasets at endpoint: {dataset_list_endpoint}')
    print(f'Found {data["paging"]["total"]} datasets')
    print()

    # TODO - handle paging (may need to run multiple calls)
    for d in data["items"]:
        print(f'{d["code"]} - {d["name"]}')

