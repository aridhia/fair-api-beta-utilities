import sys
import requests
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DICTIONARIES_URL, SSL_VERIFY

if len(sys.argv) != 1:
    print(f'Usage: {sys.argv[0]}')
    exit(1)
url = DICTIONARIES_URL
r = requests.get(url, headers=AUTHENTICATED_HEADERS, verify=SSL_VERIFY)
if r.status_code != 200:
    error_data = r.json()
    print(f'Failed to retrieve dictionary list. Status code: {r.status_code}, Error message: {error_data["error"]["message"]}')
else:
    data = r.json()
    # To output the JSON, use this 
    # print(json.dumps(data))
    
    print(f'dictionaries at endpoint: {url}')
    print(f'Found {data["paging"]["total"]} dictionaries')
    print()

    # TODO - handle paging (may need to run multiple calls)
    for d in data["items"]:
        print(f'{d["code"]} - {d["name"]}')
