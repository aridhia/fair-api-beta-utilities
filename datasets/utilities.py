from common.constants import FAIR_API_ENDPOINT

def dataset_url(code=None):
    if code: return f'{FAIR_API_ENDPOINT}datasets/{code}/'
    return f'{FAIR_API_ENDPOINT}datasets/'
