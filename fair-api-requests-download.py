import argparse
from pathlib import Path
import requests
import pandas as pd
import xlsxwriter
from common.constants import BASE_HEADERS, SSL_VERIFY, FAIR_API_ENDPOINT

script_args=''

def parse_arguments():
    global script_args
    parser = argparse.ArgumentParser()

    parser.add_argument('-d','--detailed', action='store_true', help='download all requests as separate CSVs', required=False)

    script_args = parser.parse_args()

def parse_request_json(request_data):
    request_json={}
    for item in request_data:
        # Due to JSON structure, parse out required info that is nested
        if item=='dictionaries':
            request_json['dataset_name']=request_data[item][0]['dataset']['name']
            request_json['dataset_owner']=request_data[item][0]['dataset']['approvers'][0]['email']
            tables=[]
            for table in request_data[item]:
                tables.append(table['name'])
            request_json['tables']=tables
        elif item=='requester':
            request_json[item]=request_data[item]['email']
        else:
            request_json[item]=request_data[item]

    return request_json

def get_requests():
    # Call /requests to get a list of all requests
    requests_list_endpoint = f'{FAIR_API_ENDPOINT}requests'
    r = requests.get(requests_list_endpoint, headers=BASE_HEADERS, verify=SSL_VERIFY)
    requests_array=[]

    if r.status_code != 200:
        error_data = r.json()
        print(f'Failed to retrieve request list. Status code: {r.status_code}, Error message: {error_data["error"]["message"]}')
        return False
    data = r.json()
    for req in data["items"]:
        request_code=req["code"]
        # Call /requests/{code} to get request specific information
        request_endpoint=f'{FAIR_API_ENDPOINT}requests/{request_code}'
        print("Retrieving data for request: " + request_code)
        r = requests.get(request_endpoint, headers=BASE_HEADERS, verify=SSL_VERIFY)
        if r.status_code != 200:
            try:
                error_data = r.json()
                print(f'Failed to retrieve request. Status code: {r.status_code}, Error message: {error_data["error"]["message"]}')
            except Exception:
                print(f'Failed to retrieve request. Status code: {r.status_code}')
        else:
            request_data = r.json()
            requests_array.append(parse_request_json(request_data))

    return requests_array

# Generate summary request CSV
def generate_summary_output(requests_array):
    output_folder='requests_output/'
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    fields=['dataset_name','requester','project_name','tables','status']
    request_summaries=[]
    for request in requests_array:
        request_summary={}
        for field in fields:
            request_summary[field]=request[field]
        request_summaries.append(request_summary)

    df = pd.DataFrame(request_summaries)
    df.to_csv(output_folder+'request_summary.csv', index=False)


def generate_detailed_output(requests_array):
    output_folder='requests_output/'
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    for request in requests_array:
        print(request)
        df=pd.DataFrame.from_dict(request, orient='index')
        print(df)
        df.to_csv(output_folder+request['code']+'.csv',header=False)

parse_arguments()
requests_array=get_requests()
generate_summary_output(requests_array)

if script_args.detailed:
    generate_detailed_output(requests_array)

print(f'Download data for {len(requests_array)} requests')
print()
