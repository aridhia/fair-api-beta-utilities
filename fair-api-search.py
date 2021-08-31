import requests
import os
import json
import sys
from common.constants import BASE_HEADERS, SSL_VERIFY, FAIR_API_ENDPOINT

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <search terms>')
    exit(1)

search_terms=" ".join(sys.argv[1:])

search_endpoint=f'{FAIR_API_ENDPOINT}search/search'

params = {
    'index': 'fair-index',
    'query': search_terms   
}

r = requests.get(search_endpoint, headers=BASE_HEADERS, params=params, verify=SSL_VERIFY)

if r.status_code != 200:
     data = r.json()
     print(f'Failed to search: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
else:
    results = r.json()
    hits = len(results["items"])
    print(f'Search for "{search_terms}" returns {hits} results')
    for i in results["items"]:
        # TODO - why catalogue__title not name?
        print(f'{i["@search.score"]} - {i["code"]} - {i["catalogue__title"]}')
