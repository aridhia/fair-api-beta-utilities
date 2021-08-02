from common.constants import SSL_VERIFY, BASE_HEADERS
from dictionaries.utilities import dictionary_url
import requests
import sys
import json

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <code>')
    exit(1)
code = sys.argv[1]
r = requests.get(dictionary_url(code), headers=BASE_HEADERS, verify=SSL_VERIFY)
if r.status_code != 200:
    error_data = r.json()
    print(f'Failed to retrieve dictionary. Status code: {r.status_code}, Error message: {error_data["error"]["message"]}')
else:
    data = r.json()
    print(f'Dictionary at endpoint: {dictionary_url(code)}')
    print(json.dumps(data, indent=2))
    print()
