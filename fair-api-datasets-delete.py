import sys
import requests
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DRY_RUN, SSL_VERIFY, DATASETS_URL

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <code> <--dry-run>')
    exit(1)

dataset_code = sys.argv[1]
url = f"{DATASETS_URL}{dataset_code}"

print(f'API endpoint: {url}')
print(f'Deleting Dataset with code: {dataset_code}')
if DRY_RUN:
    print("DRY RUN - no requests sent")
    exit(0)

r = requests.delete(url, headers=AUTHENTICATED_HEADERS, verify=SSL_VERIFY)
if r.status_code != 204:
    data = r.json()
    print(
        f'Failed to delete dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
else:
    print(f'Deleted dataset with code: {dataset_code}')
