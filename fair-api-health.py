import requests
import os

if 'FAIR_API_TOKEN' not in os.environ:
    print('Please add FAIR_API_TOKEN to the environment')
    exit(1)

if 'FAIR_API_ENDPOINT' not in os.environ:
    print('Please add FAIR_API_ENDPOINT to the environment')
    exit(1)

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']

health_endpoint = f'{FAIR_API_ENDPOINT}/api/health'
print(f'Testing API endpoint: {health_endpoint}')

r = requests.get(health_endpoint)
if r.status_code != 200:
    print(f'Health check failed. Status code: {r.status_code} ({r.content})')
else:
    print(f'API health check succeeded')
