from common.constants import FAIR_API_ENDPOINT

def dictionary_url(code=None):
    if code: return f'{FAIR_API_ENDPOINT}dictionaries/{code}/'
    return f'{FAIR_API_ENDPOINT}dictionaries/'