import requests
import os
from os.path import basename
import json
import sys
from tusclient import client

if 'FAIR_API_TOKEN' not in os.environ:
    print('Please add FAIR_API_TOKEN to the environment')
    exit(1)

if 'FAIR_API_ENDPOINT' not in os.environ:
    print('Please add FAIR_API_ENDPOINT to the environment')
    exit(1)

if len(sys.argv) < 4:
    print(f'Usage: {sys.argv[0]} <dataset_code> <upload_type> <upload_type>')
    exit(1)

FAIR_API_TOKEN=os.environ['FAIR_API_TOKEN']
FAIR_API_ENDPOINT=os.environ['FAIR_API_ENDPOINT']

dataset_code=sys.argv[1]
upload_type=sys.argv[2]
file_to_upload=sys.argv[3]

if upload_type not in ('data', 'attachments'):
    print(f'Invalid upload_type: {upload_type}')
    exit(1)

if not os.path.isfile(file_to_upload):
    print(f'Data file missing: {file_to_upload}')
    exit(1) 

headers = {
    'Authorization': f'Bearer {FAIR_API_TOKEN}',
    'ARIDHIA-FAIR-Parent-Model-ID': f'{dataset_code}',
     # TODO - one could guess mime type here
    'filetype': ''
}
filename=os.path.basename(file_to_upload)
metadata = {
    'filename': filename
}

if upload_type == 'attachments':
    url = f'{FAIR_API_ENDPOINT}/api/files/datasets/{dataset_code}/attachments'
elif upload_type == 'data':
    url = f'{FAIR_API_ENDPOINT}/api/files/datasets/{dataset_code}/data'

print(f'Dataset code: {dataset_code}')
print(f'File: {file_to_upload}')
print(f'Upload type: {upload_type}')
print(f'Destination: {url}')

# Documentation on tusclient: https://tus-py-client.readthedocs.io/en/latest/
try:
    print(f'Uploading file ... {filename} ...')
    client = client.TusClient(url, headers=headers)
    client.set_headers(headers)

    uploader = client.uploader(file_to_upload, chunk_size=5242880, metadata=metadata)
    uploader.upload()
    print(f'Uploading file ... {filename} ... Done')
except Exception as e:
    print(f'Problem uploading: {e} ({type(e)})')

