import os
from common.constants import BASE_HEADERS, EXIT_MISSING_ARGUMENTS

# Ensure we have set the token before setting the constant for use elsewhere
def get_token():
    if 'FAIR_API_TOKEN' not in os.environ:
        print('Please add FAIR_API_TOKEN to the environment')
        exit(EXIT_MISSING_ARGUMENTS)
    return os.environ['FAIR_API_TOKEN']


# Authentication token to be passed with every authenticated endpoint in FAIR
FAIR_API_TOKEN = get_token()


def get_authorized_header():
    return {'Authorization': f'Bearer {FAIR_API_TOKEN}'}


AUTHORIZATION_HEADER = get_authorized_header()


def get_authenticated_headers():
    return {**BASE_HEADERS, **AUTHORIZATION_HEADER}


AUTHENTICATED_HEADERS = get_authenticated_headers()
