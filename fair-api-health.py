import requests
from common.constants import SSL_VERIFY, FAIR_API_ENDPOINT

health_endpoint = f'{FAIR_API_ENDPOINT}health'
headers = { 'Content-Type': 'application/json'}
print(f'Testing API endpoint: {health_endpoint}')

response = requests.get(health_endpoint, headers=headers, verify=SSL_VERIFY)
if response.status_code != 200:
    print(f'Health check failed. Status code: {response.status_code} ({response.content})')
else:
    print(f'API health check succeeded')
