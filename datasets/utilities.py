import sys
import os
from common.constants import FAIR_API_ENDPOINT

def dataset_url(code=None):
    if code: return f'{FAIR_API_ENDPOINT}datasets/{code}/'
    return f'{FAIR_API_ENDPOINT}datasets/'
    
def definition_file(path):
    if not os.path.isfile(path):
        print(f'Provided path "{path}" does not seem to be a file')
        exit(1)
    return path
