from common.auth import AUTHENTICATED_HEADERS
import json
from common.constants import SSL_VERIFY


def request_as_curl(url, method, data=None, headers=AUTHENTICATED_HEADERS, verify_ssl=SSL_VERIFY):
    """
    Translate a request to the equivalent curl command

    url: Fully qualified URL to send the request to
    method: HTTP method to use for the request, eg GET, PATCH, POST
    data: Any data to be sent with the request, assumed to be json
    headers: Any headers to send with the request
    verify_ssl: When false, adds the `-k`, ie disable ssl verification, flag to the curl command, nothing otherwise
    """
    ssl_verify_curl_flag = " -k" if verify_ssl else ""
    curl_headers = ""
    for header in headers:
        curl_headers += f'-H "{header}: {headers[header]}" '
    curl_data = ""
    if data:
        curl_data += f' --data \'{json.dumps(data, indent=2)}\''
    return f'curl{ssl_verify_curl_flag} -X {method} {url} {curl_headers}{curl_data}'