import sys
import requests
from common.auth import AUTHENTICATED_HEADERS
from common.constants import SSL_VERIFY, FAIR_API_ENDPOINT

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <search terms>')
    exit(1)

search_terms = " ".join(sys.argv[1:])

search_endpoint = f'{FAIR_API_ENDPOINT}search/search'

params = {
    'index': 'fair-index',
    'query': search_terms
}

response = requests.get(
    search_endpoint, headers=AUTHENTICATED_HEADERS, params=params, verify=SSL_VERIFY)

if response.status_code != 200:
    data = response.json()
    print(
        f'Failed to search: Status code: {response.status_code}, Error message: {data["error"]["message"]}')
else:
    results = response.json()
    hits = len(results["items"])
    print(f'Search for "{search_terms}" returns {hits} results')
    for i in results["items"]:
        # TODO: - why catalogue__title not name?
        print(f'{i["@search.score"]} - {i["code"]} - {i["catalogue__title"]}')
