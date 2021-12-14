import sys
import requests
from common.auth import AUTHENTICATED_HEADERS
from common.constants import DRY_RUN, EXIT_FAILED_REQUEST, EXIT_MISSING_ARGUMENTS, EXIT_SUCCESS, SSL_VERIFY, DATASETS_URL

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} <code> <--dry-run>')
    exit(EXIT_MISSING_ARGUMENTS)

dataset_code = sys.argv[1]
url = f"{DATASETS_URL}{dataset_code}"

print(f'API endpoint: {url}')
print(f'Deleting Dataset with code: {dataset_code}')
if DRY_RUN:
    print("DRY RUN - no requests sent")
    exit(EXIT_SUCCESS)

r = requests.delete(url, headers=AUTHENTICATED_HEADERS, verify=SSL_VERIFY)
if r.status_code != 204:
    data = r.json()
    print(
        f'Failed to delete dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
    exit(EXIT_FAILED_REQUEST)
else:
    print(f'Deleted dataset with code: {dataset_code}')
