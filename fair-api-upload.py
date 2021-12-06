import os
import sys
from tusclient import client
from common.auth import AUTHORIZATION_HEADER
from common.constants import EXIT_FAILED_REQUEST, EXIT_MISSING_ARGUMENTS, FAIR_API_ENDPOINT

if len(sys.argv) < 4:
    print(f'Usage: {sys.argv[0]} <entity_code> <upload_type> <file_to_upload>')
    print('Where <entity_code> is the dataset code for attachments or dictionary code for csv upload.')
    print('<upload_type> can be one of: data, attachments, datafiles.')
    print('<file_to_upload> path to a file to upload as part of this request.')
    exit(EXIT_MISSING_ARGUMENTS)

entity_code = sys.argv[1]
upload_type = sys.argv[2]
file_to_upload = sys.argv[3]

if upload_type not in ('data', 'attachments', 'datafiles'):
    print(f'Invalid upload_type: {upload_type}')
    exit(EXIT_MISSING_ARGUMENTS)

if not os.path.isfile(file_to_upload):
    print(f'Data file missing: {file_to_upload}')
    exit(EXIT_MISSING_ARGUMENTS)

headers = {
    **AUTHORIZATION_HEADER,
    'ARIDHIA-FAIR-Parent-Model-ID': f'{entity_code}',
    # TODO: - one could guess mime type here
    'filetype': ''
}
filename = os.path.basename(file_to_upload)
metadata = {
    'filename': filename
}

if upload_type == 'attachments':
    url = f'{FAIR_API_ENDPOINT}files/datasets/{entity_code}/attachments'
elif upload_type == 'datafiles':
    url = f'{FAIR_API_ENDPOINT}files/datasets/{entity_code}/datafiles'
elif upload_type == 'data':
    url = f'{FAIR_API_ENDPOINT}files/dictionaries/{entity_code}/data'

print(f'Entity code: {entity_code}')
print(f'File: {file_to_upload}')
print(f'Upload type: {upload_type}')
print(f'Destination: {url}')

# Documentation on tusclient: https://tus-py-client.readthedocs.io/en/latest/
try:
    print(f'Uploading file ... {filename} ...')
    client = client.TusClient(url, headers=headers)
    client.set_headers(headers)

    uploader = client.uploader(
        file_to_upload, chunk_size=5242880, metadata=metadata)
    uploader.upload()
    print(f'Uploading file ... {filename} ... Done')
except Exception as e:
    print(f'Problem uploading: {e} ({type(e)})')
    exit(EXIT_FAILED_REQUEST)
