import os
from common.constants import BASE_HEADERS

# Ensure we have set the token before setting the constant for use elsewhere
def set_token():
    if 'FAIR_API_TOKEN' not in os.environ:
        print('Please add FAIR_API_TOKEN to the environment')
        exit(1)
    return os.environ['FAIR_API_TOKEN']


# Authentication token to be passed with every authenticated endpoint in FAIR
FAIR_API_TOKEN = set_token()


def set_authorized_header():
    return {'Authorization': f'Bearer {FAIR_API_TOKEN}'}


AUTHORIZATION_HEADER = set_authorized_header()


def set_authenticated_headers():
    return {**BASE_HEADERS, **AUTHORIZATION_HEADER}


AUTHENTICATED_HEADERS = set_authenticated_headers()
