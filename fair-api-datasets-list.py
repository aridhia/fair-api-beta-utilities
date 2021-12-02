import requests
# import json
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DATASETS_URL, SSL_VERIFY

response = requests.get(DATASETS_URL, headers=AUTHENTICATED_HEADERS, verify=SSL_VERIFY)
if response.status_code != 200:
    error_data = response.json()
    print(f'Failed to retrieve dataset list. Status code: {response.status_code}, Error message: {error_data["error"]["message"]}')
else:
    data = response.json()
    # To output the JSON, use this
    # print(json.dumps(data))

    print(f'Datasets at endpoint: {DATASETS_URL}')
    print(f'Found {data["paging"]["total"]} datasets')
    print()

    #TODO: - handle paging (may need to run multiple calls)
    for d in data["items"]:
        print(f'{d["code"]} - {d["name"]}')
