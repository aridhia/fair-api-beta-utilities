import os
import sys


# Ensure we have set the endpoint before setting the constant for use elsewhere
def set_endpoint():
    if 'FAIR_API_ENDPOINT' not in os.environ:
        print('Please add FAIR_API_ENDPOINT to the environment')
        exit(1)

    provided = os.environ['FAIR_API_ENDPOINT']
    https = 'https://'
    if provided[:5] == 'https':
        https = ''

    return f'{https}{provided}'


# Endpoint of FAIR API, you can retrieve this from FAIR UI by viewing the "About" page
FAIR_API_ENDPOINT = set_endpoint()

# Dry run means we do not send requests, but you can review what would be sent
DRY_RUN = len(sys.argv) > 2 and sys.argv[2] == '--dry-run'

# FAIR_API_ENDPOINT but without the trailing "/api"
FAIR_URL = FAIR_API_ENDPOINT[:-4]

# Verify TLS/SSL requests, useful for disabling in local environment,
# should always be True in production so defaults to True
SSL_VERIFY = not(os.getenv('FAIR_API_DISABLE_SSL_VERIFY', False))

# Default authenticated headers for use against authenticated endpoints
BASE_HEADERS = {
    'Content-Type': 'application/json'
}

# Route to datasets methods
DATASETS_URL = f"{FAIR_API_ENDPOINT}datasets/"

# Route to dictionaries methods
DICTIONARIES_URL = f"{FAIR_API_ENDPOINT}dictionaries/"
