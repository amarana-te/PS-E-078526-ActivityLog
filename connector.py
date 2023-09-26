import time
import requests.adapters
from datetime import datetime

super_http = requests.Session()
adapter1 = requests.adapters.HTTPAdapter(pool_connections=35, pool_maxsize=77)

super_http.mount('https://api.thousandeyes.com/', adapter=adapter1)


def get_data(headers, endp_url):

    start = time.time()
    endpoint_data = super_http.get(url=endp_url, headers=headers)
    roundtrip = time.time() - start

    if endpoint_data.status_code == 429:

        dt_object = datetime.fromtimestamp(int(endpoint_data.headers.get('x-organization-rate-limit-reset'))) - datetime.now()
        time.sleep(dt_object.seconds + 1)
        endpoint_data = super_http.get(url=endp_url, headers=headers)

    else:

        print("Status Code ", str(endpoint_data.status_code) + ": " + endp_url + " time: ", str(roundtrip))

    endpoint_data = endpoint_data.json()

    return endpoint_data


def post_data(headers, endp_url, payload):

    start = time.time()
    endpoint_data = super_http.post(url=endp_url, headers=headers, data=payload)
    roundtrip = time.time() - start

    if endpoint_data.status_code == 429:

        dt_object = datetime.fromtimestamp(int(endpoint_data.headers.get('x-organization-rate-limit-reset'))) - datetime.now()
        time.sleep(dt_object.seconds + 1)
        endpoint_data = super_http.post(url=endp_url, headers=headers, data=payload)

    else:

        print("Status Code ", str(endpoint_data.status_code) + ": " + endp_url + " time: ", str(roundtrip))

    return endpoint_data