import sys
import os
from common.constants import FAIR_API_ENDPOINT

def require_args():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <path to dataset definition json file> <--dry-run>')
        exit(1)

def dataset_url(code=None):
    if code: return f'{FAIR_API_ENDPOINT}datasets/{code}/'
    return f'{FAIR_API_ENDPOINT}datasets/'

    
def definition_file(path):
    if not os.path.isfile(path):
        print(f'Provided path "{path}" does not seem to be a file')
        exit(1)
    return path