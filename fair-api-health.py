import requests
import json
from common.constants import BASE_HEADERS, SSL_VERIFY, FAIR_API_ENDPOINT

health_endpoint = f'{FAIR_API_ENDPOINT}health'
print(f'Testing API endpoint: {health_endpoint}')

response = requests.get(
    health_endpoint, headers=BASE_HEADERS, verify=SSL_VERIFY)
if response.status_code != 200:
    print(
        f'Health check failed. Status code: {response.status_code} ({response.content})')
else:
    print(json.dumps(response.json(), indent=4))
    print(f'API health check succeeded')
