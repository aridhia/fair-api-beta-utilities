import sys
import json
import requests
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DICTIONARIES_URL, EXIT_FAILED_REQUEST, EXIT_MISSING_ARGUMENTS, SSL_VERIFY

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <code>')
    exit(EXIT_MISSING_ARGUMENTS)
code = sys.argv[1]
dictionary_url = f"{DICTIONARIES_URL}{code}"
response = requests.get(
    dictionary_url, headers=AUTHENTICATED_HEADERS, verify=SSL_VERIFY)
if response.status_code != 200:
    error_data = response.json()
    print(
        f'Failed to retrieve dictionary. Status code: {response.status_code}, Error message: {error_data["error"]["message"]}')
    exit(EXIT_FAILED_REQUEST)
else:
    data = response.json()
    print(f'Dictionary at endpoint: {dictionary_url}')
    print(json.dumps(data, indent=2))
    print()
