import requests
import os
import json
import sys
from datasets.diff_helper import DiffHelper

if 'FAIR_API_TOKEN' not in os.environ:
    print('Please add FAIR_API_TOKEN to the environment')
    exit(1)

if 'FAIR_API_ENDPOINT' not in os.environ:
    print('Please add FAIR_API_ENDPOINT to the environment')
    exit(1)

DRY_RUN = len(sys.argv) > 2 and sys.argv[2] == '--dry-run'

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <path to dataset definition json file> <--dry-run>')
    exit(1)
    
FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']
https = 'https://'

if FAIR_API_ENDPOINT[:5] == 'https':
    https = ''

dataset_list_endpoint = f'{https}{FAIR_API_ENDPOINT}datasets'
FAIR_URL = f'{https}{FAIR_API_ENDPOINT}'[:-4]

headers = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}',
    'Content-Type' : 'application/json'
}

def definition_file():
    definition_file = sys.argv[1]
    if not os.path.isfile(definition_file):
        print(f'Definition file not valid: {definition_file}')
        exit(1)
    return definition_file

def dataset_url(code=None):
  if code: return f'{https}{FAIR_API_ENDPOINT}datasets/{code}/'
  return f'{https}{FAIR_API_ENDPOINT}datasets/'
