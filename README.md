# README

Useful scripts and documentation for using the beta version of the [FAIR Data Services](https://www.aridhia.com/fair-data-services/). The API to the service is currently in beta. For more user guide material on the FAIR data services, please refer to the [knowledge base](https://knowledgebase.aridhia.io/kbcategory/fair-data-services/)

> Note: This repository provides **early access** functionality which may change over time. Feedback is welcome: Please log an issue in this github repository.

## Overview - interacting with the metadata service

The FAIR data services support the life cycle of creating and using metadata about research datasets.

As a data owner, depositing data and metadata:

- Create a dataset entry - dataset-level (catalogue) and table-level (dictionary)
- Upload data (API only, beta) 

As a data consumer, finding and querying data:

- Search for metadata
- Read and download metadata
- Query and download data (API only, beta)

The service supports web-based access and API access. The documentation for the catalogue and dictionary format is available in TODO/Knowledge Base.

## Pre-requisites

- Web access through a modern browser
- Example of API access are given using `python` and the `requests` library but could be adapted to other tools such as `curl` or an API client like [Postman](https://www.postman.com/)
- Examples are provided for a Linux environment but could be adapted to Windows environment.

## Create a Dataset Entry (Web)

A Dataset entry in FAIR represents a findable dataset, potentially with multiple tables of data. The record comprises:

- a catalogue entry (aligned to the [DCAT](https://www.w3.org/TR/vocab-dcat-2/) standard)
- one or more data dictionaries (for each table)
- (optionally) attachments

In order to create metadata, a user must have permissions of a 'data steward'. 

> Note: In version 1.0, data stewards have permission to create and edit *all* datasets. This will change in future versions.

To create a new data entry

- Log into the FAIR data services
- Select `Datasets` from the menu ribbon, and then click `New Dataset`.
- Provide a code (optional), name and brief description for the dataset. Click `Create`
- Provide further details by completing the using `Click to Edit`.
- You can then upload attachments by dragging and dropping the files in the area at the bottom of the screen
- Creating and editing the dictionary (TODO)

## Search for a Dataset Entry (Web)

Using the Web interface, it is possible to find datasets using the search functionality:

- Use the search in the main navigation bar at the top of the page
- Use the 'Home' tab and and click 'Discover Data' or select 'Discover' from the menu ribbon bar to open up the search tab

From the search tab, you can:

- search for a whole word or a set of words: e.g. "Alzheimer's"
- search for words by prefix: e.g. "alz*"
- search for words using fuzzy matching: e.g. "alz~"

Click the name of the dataset to view the full entry.

## View and download dataset metadata (Web)

The page for a dataset displays the metadata record:

- Name
- Description
- Keywords
- Author
- Contact email
- Publisher
- License
- Version
- Created and updated data (of this record)
- Attachments - such as documentation or supplementary material which can be downloaded
- Dictionary by table

In addition, it is possible to download metadata records in JSON by clicking the download icons adjacent to the display of the catalogue entry or and dictionary. Alternatively the JSON entry can be downloaded as a whole using the 'Download' tool in the menu ribbon.


## Obtaining an API authorisation token

FAIR data services uses the OAuth2 framework for authentication and authorisation. All API calls require an API authorisation token, obtained as an authenticated user of the FAIR data service.

> This is likely to change soon but for the beta programme, the API uses the same authorisation token as the web user interface, and subject to the same expiry.

**Option 1** Via the browser developer tools. Each browser is different (see below). The token is held in **Session Storage**, under the key `msal.idtoken`.  

To access the developer tools:

- On [Firefox](https://developer.mozilla.org/en-US/docs/Tools), you can toggle tools using Control+Shift+I on Windows or Command+Shift+I on macos.
- On [Chrome](https://developers.google.com/web/tools/chrome-devtools/), you can toggle tools using Command+Option+C (macos) or Control+Shift+C (Windows, Linux, Chrome OS). 

**Option 2** (coming soon!) Via the FAIR web interface: Click the drop down menu top-right of the screen with your name on it, select the "About" option. The token will be displayed in the pop up dialogue. Copy the key to clipboard.

The authorisation token is a [JWT](https://jwt.io/) token which is a long encrypted string and will look something like (this example has been redacted):
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZ...iFYQ84MQt0euCX9Gncb9YHBOAviRdlVTf0LmFkb9ZM3N-5B-0e4helQ4j99HAlcTqZKbK0iscsvQiYRbnxctYjz242cUb6hKZ_sGL5Suol1YE4NuWF6esOs9iWdM1GsjIYVfNpuw
```

When copying the token, make sure the whole token is copied, with no spaces. If you have a problem with the token, refresh the web browser and try again.

In the examples below, we assume that a valid token is in the user's environment, as well an API endpoint. For example in a bash terminal, set the environment property:
```sh
export FAIR_API_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZ...iFYQ84MQt0euCX9Gncb9YHBOAviRdlVTf0LmFkb9ZM3N-5B-0e4helQ4j99HAlcTqZKbK0iscsvQiYRbnxctYjz242cUb6hKZ_sGL5Suol1YE4NuWF6esOs9iWdM1GsjIYVfNpuw
export FAIR_API_ENDPOINT=https://fair.uksouth.preview-mca.aridhia.io
```

## Testing the API

Then, to test the API is up and running at all use the script [`fair-api-health.py`](fair-api-health.py):
```sh
python fair-api-health.py
```
The output should look something like:
```
Testing API endpoint: https://fair.uksouth.preview-mca.aridhia.io/api/health
API health check succeeded
```
This will fail if the endpoint `/api/health` fails to return a HTTP success code of 200.

To test the token works, run the script [`fair-api-datasets-list.py`](fair-api-datasets-list.py):
```sh
python fair-api-datasets-list.py
```
The output should look something like:
```
Datasets at endpoint: https://fair.uksouth.preview-mca.aridhia.io/api/datasets
Found 27 datasets
...
avocado_prices - Avocado Prices
...
```

## Create a Dataset Entry (API)

In order to create metadata using the API, a JSON file should be created, conformed to the standard. This can then be posted to the service to create the dataset.

Datasets are created using HTTP `POST` operations. The server validates the payload and looks for a dataset identifier in it - in the `catalogue` > `id` structure:

- If the `id` is present it is tested for uniqueness: if it already exists an error will be returned. 
- If the `id` is absent a new one is generated. The user should be careful not to create many copies of the same metadata

Technically the `POST` call can create multiple datasets, but the python script assumes that only one is created.

For example, see [simulated_covid19_remdesivir_dataset.json](./examples/simulated_covid19_remdesivir_dataset.json) - see [`fair-api-datasets-create.py`](fair-api-datasets-create.py).

```sh
python fair-api-datasets-create.py ./examples/simulated_covid19_remdesivir_dataset.json
```
If successful, the output should look something like:
```
API endpoint: https://fair.uksouth.preview-mca.aridhia.io/api/datasets
Posting definition: examples/simulated_covid19_remdesivir_dataset.json
Created dataset: simulated_covid19_remdesivir_test (Ref. 296)
View on the web at: https://fair.uksouth.preview-mca.aridhia.io/#/data/datasets/simulated_covid19_remdesivir_tes
```
> Tip: During the beta testing, it can be useful to create a dataset using the API but delete it either using an HTTP `DELETE` call or using the web interface

## Search for Metadata (API)

The search API be used to find datasets based on search terms - see [`fair-api-search.py`](fair-api-search.py).

```sh
python fair-api-search.py <search terms>
```
Search terms are concatenated into a single search string.

Examples:
```sh
python fair-api-search.py alzheimer\'s
```
Will produce results like:
```
Search for "alzheimer's" returns 4 results
2.1436093 - synthetic_alzheimers_profile - Synthetic Alzheimer's Profiles
1.8868049 - oasis_longitudinal - MRI and Alzheimer's
0.71022123 - sadd_subjects - Synthetic Alzheimer's Disease Data
0.4112628 - sadd_snipper - Synthetic Alzheimer's Disease Data
```

Try variant search terms like `alz*` (prefix match) or `alz~` (fuzzy match).






