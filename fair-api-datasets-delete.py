import requests
import sys
from common.constants import BASE_HEADERS, SSL_VERIFY
from datasets.utilities import require_args, dataset_url

require_args()

dataset_code = sys.argv[1]
url = dataset_url(dataset_code)

print(f'API endpoint: {url}')
print(f'Deleting Dataset with code: {dataset_code}')

r = requests.delete(url, headers=BASE_HEADERS, verify=SSL_VERIFY)
if r.status_code != 204:
    data = r.json()
    print(f'Failed to delete dataset: Status code: {r.status_code}, Error message: {data["error"]["message"]}')
else:
    print(f'Deleted dataset with code: {dataset_code}')

           
