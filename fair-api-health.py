from common.constants import SSL_VERIFY, FAIR_API_ENDPOINT
import requests

health_endpoint = f'{FAIR_API_ENDPOINT}health'
headers = { 'Content-Type': 'application/json'}
print(f'Testing API endpoint: {health_endpoint}')

r = requests.get(health_endpoint, headers=headers, verify=SSL_VERIFY)
if r.status_code != 200:
    print(f'Health check failed. Status code: {r.status_code} ({r.content})')
else:
    print(f'API health check succeeded')
