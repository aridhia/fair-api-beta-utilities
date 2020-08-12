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
    print(f'Usage: {sys.argv[0]} <search terms>')
    exit(1)

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']

search_terms=" ".join(sys.argv[1:])

headers = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}'
}

search_endpoint=f'{FAIR_API_ENDPOINT}/api/search/search'

params = {
    'index': 'fair-index',
    'query': search_terms   
}

r = requests.get(search_endpoint, headers=headers, params=params)

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