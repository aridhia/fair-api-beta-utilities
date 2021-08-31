import requests
import json
from datasets.utilities import dataset_url
from common.constants import BASE_HEADERS, SSL_VERIFY

r = requests.get(dataset_url(), headers=BASE_HEADERS, verify=SSL_VERIFY)
if r.status_code != 200:
    error_data = r.json()
    print(f'Failed to retrieve dataset list. Status code: {r.status_code}, Error message: {error_data["error"]["message"]}')
else:
    data = r.json()
    # To output the JSON, use this 
    # print(json.dumps(data))
    
    print(f'Datasets at endpoint: {dataset_url()}')
    print(f'Found {data["paging"]["total"]} datasets')
    print()

    # TODO - handle paging (may need to run multiple calls)
    for d in data["items"]:
        print(f'{d["code"]} - {d["name"]}')

