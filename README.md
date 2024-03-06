# README

Useful scripts and documentation for using the beta version of the API for [FAIR Data Services](https://www.aridhia.com/fair-data-services/). The API to the service is currently in beta. For more user guide material on the FAIR data services, please refer to the [knowledge base](https://knowledgebase.aridhia.io/kbcategory/fair-data-services/)

See also the [API specification](https://fair.preview.aridhia.io/api/docs/).

> Note: This repository provides **early access** functionality which may change over time. Feedback is welcome: Please log an issue in this github repository.

## Overview - interacting with the metadata service

The FAIR data services support the life cycle of creating and using metadata about research datasets. This service manages metadata and data for a dataset. Normally, a dataset comprises one or more tables of data. In some cases, for example when setting a standard for data, the dataset doesn't have data tables associated with it, just metadata:

In summary, a dataset entry in the FAIR Data Services is defined as:

- Catalogue (1 x dataset)
- Dictionary (1 x data table)
- Data table(s) if present

More information regarding the definition of a FAIR dataset can be found [here](https://knowledgebase.aridhia.io/article/what-is-a-dataset/).

As a Data Steward/Owner, you can deposit data and metadata. Specifically:

- Create a dataset entry - dataset-level (catalogue) and table-level (dictionary) metadata
- Upload data (API only, beta)
- Assume the permissions of a Standard user (i.e. data consumer)

As a Standard user (or data consumer), you can find and query data:

- Search for metadata
- Save searches
- Read and download metadata
- Query and download data (API only, beta)

More information regarding the user permissions in FAIR Data Services can be found [here](https://knowledgebase.aridhia.io/article/role-based-access-control-2/).

The service supports web-based access and API access where the full API documentation can be found [here](https://fair.preview.aridhia.io/api/docs/).
that includes the technical format for the catalogue and dictionary data structures (in JSON). However you can also use the examples provided that allow dataset searching, creation and uploading of data.

## Pre-requisites

In order to run these examples, you need to be a user of an Aridhia [FAIR Data service](https://www.aridhia.com/fair-data-services/) instance with the following permissions:

- Data steward permissions set
- In addition, `datasets upload` and `selection read` permissions are required

Please note the following assumptions:

- Web access is through a modern browser (Chrome or Firefox)
- Example of API access are given using `python` and the `requests` library but could be adapted to other tools such as `curl` or an API client like [Postman](https://www.postman.com/)
- [`jq`](https://stedolan.github.io/jq/) is a useful tool for processing JSON outputs.
- Examples are provided for a Linux environment but could be adapted to Windows environment.
- Where python is used, we assume Python 3.
- Uploading data and attachments requires the [`tusclient` library](https://github.com/tus/tus-py-client). This can be installed using `pip` or other tools. Ensure you have the right version for Python 3.

## Create a Dataset Entry (Web)

A Dataset entry in FAIR represents a findable dataset, potentially with multiple tables of data. The record comprises:

- a catalogue entry (aligned to the [DCAT](https://www.w3.org/TR/vocab-dcat-2/) standard)
- one or more data dictionaries (for each table)
- (optionally) attachments

In order to create metadata, a user must have permissions of a 'data steward'.

To create a new dataset entry:

- Log into the FAIR data services
- Select `Datasets` from the menu ribbon, and then click `New Dataset`.
- Provide a code (optional), name and brief description for the dataset. Click `Create`
- Provide further details by completing the form using `Click to Edit`.
- You can then upload attachments by dragging and dropping the files in the area at the bottom of the screen
- Create and edit dictionaries for the dataset

For more details - see the knowledge base pages on [Managing Data](https://knowledgebase.aridhia.io/kbcategory/managing-data-fair-data-services/)

## Search for a Dataset Entry (Web)

Using the Web interface, it is possible to find datasets using the search functionality:

- Use the search in the main navigation bar at the top of the page
- Use the 'Home' tab and and click 'Discover Data' or select 'Discover' from the menu ribbon bar to open up the search tab

From the search tab, you can:

- search for a whole word or a set of words: e.g. "Alzheimer's"
- search for words by prefix: e.g. "alz*"
- search for words using fuzzy matching: e.g. "alz~"

Click the name of the dataset to view the full entry.

For more details - see the knowledge base page on [Searching for Data](https://knowledgebase.aridhia.io/article/searching-for-data/)

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
- Rights
- Identifier (displayed as DOI)
- Created and updated data (of this record)
- Attachments - such as documentation or supplementary material which can be downloaded
- Dictionary by table

In addition, it is possible to download metadata records in JSON by clicking the download icons adjacent to the display of the catalogue entry and dictionary. Alternatively the JSON entry can be downloaded as a whole using the 'Download' tool in the menu ribbon.

For more details - see the knowledge base page on [What is a dataset](https://knowledgebase.aridhia.io/article/what-is-a-dataset/)

## Obtaining an API authorisation token

FAIR data services uses the OAuth2 framework for authentication and authorisation. All API calls require an API authorisation token, obtained as an authenticated user of the FAIR data service.

A temporary API token can be obtained via the FAIR web interface:

- Click the drop down menu top-right of the screen with your name on it, select the "About" option.
- The token will be displayed in the pop up dialogue.
- Copy the key to clipboard using the button provided.

The authorisation token is a [JWT](https://jwt.io/) token which is a long encrypted string and will look something like (this example has been redacted):

`eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZ...iFYQ84MQt0euCX9Gncb9YHBOAviRdlVTf0LmFkb9ZM3N-5B-0e4helQ4j99HAlcTqZKbK0iscsvQiYRbnxctYjz242cUb6hKZ_sGL5Suol1YE4NuWF6esOs9iWdM1GsjIYVfNpuw`

When copying the token, make sure the whole token is copied, with no spaces, e.g. use the Copy button. If you have a problem with the token, refresh the web browser and try again. These tokens expire approximately every 60 minutes.

In the examples below, we assume that a valid token is in the user's environment, as well an API endpoint. For example in a bash terminal, set the environment property:

```sh
export FAIR_API_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZ...iFYQ84MQt0euCX9Gncb9YHBOAviRdlVTf0LmFkb9ZM3N-5B-0e4helQ4j99HAlcTqZKbK0iscsvQiYRbnxctYjz242cUb6hKZ_sGL5Suol1YE4NuWF6esOs9iWdM1GsjIYVfNpuw
```

## The FAIR API endpoint

> Note your `FAIR_API_ENDPOINT` will vary - make sure it's pointing to the correct server for your use case.

Depending on the instance of the FAIR data service you are working with, you will be provided with a URL to the service, which acts as base URL of the API endpoint. This will be the bare URL without paths. In these examples, we use the fictional endpoint `https://fair.example.org/api/`.

You can find the FAIR API URL by following the steps below:

1. Log into the FAIR UI.
2. Hover over your name and a drop down will appear.
3. Click on About.
4. Click on the copy icon at the right hand side of the API textbox.

```sh
export FAIR_API_ENDPOINT=<as provided>
```

## Testing the API

Then, to test the API is up and running at all use the script [`fair-api-health.py`](fair-api-health.py):

```sh
python fair-api-health.py
```

The output should look something like:

```text
Testing API endpoint: https://fair.example.org/api/health
API health check succeeded
```

This will fail if the endpoint `/api/health` fails to return a HTTP success code of 200.

To test the token works, run the script [`fair-api-datasets-list.py`](fair-api-datasets-list.py):

```sh
python fair-api-datasets-list.py
```

The output should look something like:

```text
Datasets at endpoint: https://fair.example.org/api/datasets
Found 27 datasets
...
avocado_prices - Avocado Prices
...
```

## Create a Dataset Entry (API)

In order to create metadata using the API a JSON file should be created and made to conform to the standard set out in the API documentation, which can typically be found at your FAIR instance's domain with `/api/docs`, e.g. https://fair.example.org/api/docs. This can then be posted to the service to create the dataset. An example is provided below or you can use the [Excel to JSON FAIR converter](https://github.com/aridhia/fair-excel-to-json) to create the correct JSON to POST to the API.

Datasets are created using HTTP `POST` operations. The server validates the payload and looks for a dataset identifier in it - in the `catalogue.id` structure:

- If the `id` is present in the file posted it is tested for uniqueness: if it already exists an error will be returned.
- If the `id` is absent in the file posted a new one is generated by the server and is returned in the response from the server. The user should be careful not to create many copies of the same metadata

An example dataset JSON file has been provided, see [simulated_covid19_remdesivir_dataset.json](./examples/simulated_covid19_remdesivir_dataset.json), however the following attributes should be modified to something unique.

- `dataset.code`
- `catalogue.title`
- `dictionary.code` (this can be omitted and the FAIR API will generate a code for you, however we will refer to this in future examples)

For the purpose of these examples, we will assume that **<dataset_code>** will be the `catalogue.id` which you have just set in the JSON file.

We will also assume that **\<dictionary_code\>** will be the `dictionary.code` which you have also just set in the JSON file.

When you call the URLs in the examples you should replace **\<dataset_code\>** and **\<dictionary_code\>** with what has been set in the JSON file.

```sh
python fair-api-datasets-create.py ./examples/simulated_covid19_remdesivir_dataset.json
```

If successful, the output should look something like:

```text
API endpoint: https://fair.example.org/api/datasets
Posting definition: examples/simulated_covid19_remdesivir_dataset.json
Created dataset: simulated_covid19_remdesivir_test (Ref. 296)
View on the web at: https://fair.example.org/#/data/datasets/simulated_covid19_remdesivir_tes
```

> Tip: During the beta testing, it can be useful to create a dataset using the API but delete it using an HTTP `DELETE` call, using the web interface, or using the [`fair-api-datasets-delete.py`](fair-api-datasets-delete.py) script.

## Search for Metadata (API)

The search API can be used to find datasets based on search terms - see [`fair-api-search.py`](fair-api-search.py).

```sh
python fair-api-search.py <search terms>
```

Search terms are concatenated into a single search string.

Examples:

```sh
python fair-api-search.py alzheimer\'s
```

Will produce results like:

```text
Search for "alzheimer's" returns 4 results
2.1436093 - synthetic_alzheimers_profile - Synthetic Alzheimer's Profiles
1.8868049 - oasis_longitudinal - MRI and Alzheimer's
0.71022123 - sadd_subjects - Synthetic Alzheimer's Disease Data
0.4112628 - sadd_snipper - Synthetic Alzheimer's Disease Data
```

Try variant search terms like `alz*` (prefix match) or `alz~` (fuzzy match).

## Upload resources (beta API)

> This is an **early access** API and subject to change. Please send feedback so we can improved the experience.

It is possible to add attachments and data files to the dataset, so that they can be downloaded at the time of reading metadata. The API for this also provides the ability to upload tables of CSV data for storage and subsequent querying.

To upload an attachment or data file, it is important to know the **<dataset_code>**. For example to upload an image attachment to the `simulated_covid19_remdesivir` dataset use the script [fair-api-upload.py](./fair-api-upload.py) with dataset code for `entity_code` and either the `attachments` or `datafiles` switch:

Attachments can be any files you want to store against the dataset.

Data files must be in CSV format and can be converted to dictionary data at a later stage.

```sh
python fair-api-upload.py\
     <dataset_code>\
     attachments\
     examples/Covid-19-curves-graphic-social-v3-1.gif
```

Note the parameter is `attachments` not `attachment`.

The image used in this example is [“Flattening the curve” by Siouxsie Wiles and Toby Morris](https://creativecommons.org/2020/03/19/now-is-the-time-for-open-access-policies-heres-why/covid-19-curves-graphic-social-v3-1/) licensed CC BY-SA. Thanks!

## Upload data (beta API)

> This is an **early access** API and subject to change. Please send feedback so we can improved the experience.

The FAIR data services can store structured data for subsequent selection and query. (Remember that a FAIR dataset can have multiple tables.)

To upload data, use the script [fair-api-upload.py](fair-api-upload.py) with the dictionary code for `entity_code` and the `data` switch:

```sh
python fair-api-upload.py \
    <dictionary_code> \
    data \
    examples/<dictionary_code>.csv
```

Uploading a CSV will result in a database table being created and written to within the dataset previously created (i.e. named **<dataset_code>**). The system will attempt to load the CSV into the PostgreSQL database but may fail due to formatting errors. Also, please note that if a CSV is uploaded multiple times it will **overwrite** the original database table. (In future, appending may be supported - let us know if this is important).

## Selecting data (beta API)

> This is an **early access** API, is only available to selected users and is subject to change. For those with access, please send feedback so we can improved the experience.

When data has been uploaded, it can be queried or downloaded using [GraphQL](https://graphql.org/) queries. Specifying GraphQL is outside the scope of this documentation but a number of examples are provided.

The API allows queries to be validated (is the query formatted correctly) as well as checking whether the query would return results if executed (aka 'beacon') as well as selecting. The dialect of GraphQL used allows for filtering and aggregation. Examples are provided of each. The example script just shows the `/api/selection/select` endpoint, but could be adapted for the `/api/selection/validate` and `/api/selection/beacon` endpoints.

To run the example use the script [fair-api-select.py](fair-api-select.py) with a query file:

```sh
python fair-api-select.py examples/select-all.graphql
```

Examples:

- [selection](./examples/select-all.graphql)
- [filter](./examples/filter.graphql)
- [aggregate](./examples/aggregate.graphql)

Outputs are in JSON format, but can be easily converted to CSV if needed using a tool like [`jq`](https://stedolan.github.io/jq/).

## Updating a Dataset Entry (API)

This section describes how the update cycle in FAIR works.

To demonstrate how to update a dataset, the `fair-api-datasets-update.py` helper command can be used:

1. Create a patch file, which we will call `dataset.json`:
   - If you don't aleady have a dataset, create a JSON file conforming to the metadata specification set out in [Create a Dataset Entry](#create-a-dataset-entry-api). Post this to the API and make a note of the `dataset_code`, which we will assume is `test_dataset`.
   - For an existing dataset you can use the [`fair-api-datasets-get.py` script](fair-api-datasets-get.py) script and save the JSON output. You will have to remove some of the additional fields from this JSON, see your instance's API docs for more details.
2. Make a change to the metadata in `dataset.json`, for example add or remove a dictionary from the `dictionaries` list, or change some values in the `catalogue` attributes. Note that any modified dictionaries must include their `id` and `code` fields.
3. Now call the `fair-api-datasets-update.py` command with `--dry-run` enabled. This will calculate differences and print the appropriate PATCH call that should be used to update the dataset. Running witout --dry-run will apply the change to the database:

```sh
python fair-api-datasets-update.py test_dataset ~/path/to/dataset.json --dry-run
```

## Converting JSON output to CSV

JSON data can be converted to CSV with a tool like `jq`. For example, to select data and then convert it to CSV with headers, the following script will first select data to a file, then convert it to the target format:

```sh
python fair-api-select.py examples/select-all.graphql  > output/select-all.json

cat output/select-all.json\
    | jq -r '["study_name", "age", "comorbidity"], (.data[].simulated_covid19_remdesivir[] | [.study_name,.age,.comorbidity]) | @csv'\
    | less
```

Note that the `jq` pattern creates a row with the headers, then parses the array of nested values in the result JSON into a flat array of values, then formats it for CSV output with the `@csv` macro.

Results from selection are in the form:

```js
{
    "data": [
        {
            "tablename": [
                { ... record ... }
            ]
        }
    ]
}
```

The example above use the pattern `.data[].tablename[]` (in this case `.data[].simulated_covid19_remdesivir[]`) to extract the records into a list.

## Download a Dataset's Data Access Requests

For Data Access Request (DAR) enabled customers, a researcher or data owner can download a list of their requests using the script [`fair-api-requests-download.py`](fair-api-requests-download.py)

```sh
python fair-api-requests-download.py 
```

By default, the script will download a summary list of requests to a `requests_output` in the current directory. This summary files includes the dataset name, project name, requested tables and the request status.

By adding the `--detailed` flag, all contents of each request are downloaded as separate CSV files into the same `requests_output` folder.

Note: this script will extract existing requests in FAIR and not previously deleted requests (via audit)

## Deleting the Dataset

To delete your test dataset, use the script [`fair-api-datasets-delete.py`](fair-api-datasets-delete.py):

```sh
python fair-api-datasets-delete.py <dataset_code>
```

## Dictionaries

As above, ensure that the `FAIR_API_ENDPOINT` and `FAIR_API_TOKEN` are set in your environment.

### List all dictionaries

Run:

```sh
python fair-api-dictionaires-list.py
```

Result:

```text
Found 74 dictionaries

...
athlete_events - athlete_events
climate70 - climate70
golden_globe_awards - golden_globe_awards
...
```

### Get single dictionary

Run:

```sh
python fair-api-dictionaries-get.py <code>
```

Result:

```text
{
  "id": 127,
  "name": "synthetic_alzheimers_profile",
  "code": "synthetic_alzheimers_profile",
  "description": null,
  "created_at": "2021-04-21T15:57:16.968Z",
  "updated_at": "2021-11-09T15:00:08.262Z",
  "fields": [
    {
      "name": "study_id",
      "label": "Study ID",
      "description": "Participant Study ID",
      "constraints": "STUDY_ID",
      "uri": null,
      "pseudonymisation_rule": null,
      "type": "text"
    },
    {
      "name": "site",
      "label": "Site",
      "description": "Trial Delivery Centre",
      "constraints": "SITE",
      "uri": null,
      "pseudonymisation_rule": null,
      "type": "text"
    },
    ...
  ],
  "lookups": {},
  "dataset_id": 133
}
```

### Update a Dictionary

> Note this is separate from modifying dictionaries through datasets as described above

1. Use an existing dictionary or create one as above and note it's `code`, referred to hereafter as \<dictionary_code\>.
2. Create a JSON file which will describe your patch, we will call this the dictionary patch file.
3. Create a JSON object in the patch file representing your desired changes, for example:

    ```json
    {
        "description": "This is an update of the description field"
    }
    ```

4. Run the script:

    ```sh
    python fair-api-dictionaries-update.py <dictionary_code> /path/to/dictionary/patch/file
    ```

Result:

```text
Sending request...
Patched dictionary: simulated_covid19_remdesivir_00002
{
    "id": 340,
    "name": "Simulated Covid19 Remdesivir",
    "code": "simulated_covid19_remdesivir_00002",
    "description": "This is an updated description",
    ...
}
```

## License

Please contact Aridhia Informatics to license this code.

Copyright - All rights reserved (c) 2020 Aridhia Informatics.
