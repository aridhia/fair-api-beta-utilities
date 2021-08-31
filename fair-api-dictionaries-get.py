import sys
import json
import requests
from common.constants import DICTIONARIES_URL, SSL_VERIFY, BASE_HEADERS

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <code>')
    exit(1)
code = sys.argv[1]
dictionary_url = f"{DICTIONARIES_URL}{code}"
response = requests.get(dictionary_url, headers=BASE_HEADERS, verify=SSL_VERIFY)
if response.status_code != 200:
    error_data = response.json()
    print(f'Failed to retrieve dictionary. Status code: {response.status_code}, Error message: {error_data["error"]["message"]}')
else:
    data = response.json()
    print(f'Dictionary at endpoint: {dictionary_url}')
    print(json.dumps(data, indent=2))
    print()
