import requests
import sys
from common.constants import BASE_HEADERS, DRY_RUN, SSL_VERIFY
from datasets.utilities import dataset_url

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <code> <--dry-run>')
    exit(1)

dataset_code = sys.argv[1]
url = dataset_url(dataset_code)

print(f'API endpoint: {url}')
print(f'Deleting Dataset with code: {dataset_code}')
if DRY_RUN: 
    print("DRY RUN - no requests sent")
    exit(0)

r = requests.delete(url, headers=BASE_HEADERS, verify=SSL_VERIFY)
if r.status_code != 204:
    data = r.json()
    print(f'Failed to delete dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
else:
    print(f'Deleted dataset with code: {dataset_code}')

           
