import os
import sys

def set_token():
    if 'FAIR_API_TOKEN' not in os.environ:
        print('Please add FAIR_API_TOKEN to the environment')
        exit(1)
    return os.environ['FAIR_API_TOKEN']

def set_endpoint():
    if 'FAIR_API_ENDPOINT' not in os.environ:
        print('Please add FAIR_API_ENDPOINT to the environment')
        exit(1)

    provided = os.environ['FAIR_API_ENDPOINT']
    https = 'https://'
    if provided[:5] == 'https':
        https = ''

    return f'{https}{provided}'

FAIR_API_TOKEN = set_token()
FAIR_API_ENDPOINT = set_endpoint()
DRY_RUN = len(sys.argv) > 2 and sys.argv[2] == '--dry-run'
FAIR_URL = FAIR_API_ENDPOINT[:-4]

# Verify TLS/SSL requests, useful for disabling in local environment,
# should always be True in production so defaults to True
SSL_VERIFY=not(os.getenv('FAIR_API_DISABLE_SSL_VERIFY', False))

BASE_HEADERS = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}',
    'Content-Type' : 'application/json'
}
