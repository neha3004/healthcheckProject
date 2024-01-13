import argparse
from urllib.parse import urlparse
import requests
import yaml
import schedule
import time

from yaml.loader import SafeLoader


def read_yaml(healthcheck_yaml_file):
    with open(healthcheck_yaml_file, 'r') as f:
        yaml_data = list(yaml.load_all(f, Loader=SafeLoader))
        return yaml_data


def get_yaml():
    parser = argparse.ArgumentParser()
    parser.add_argument('healthcheck_yaml_file', type=str, help='Enter the path for healthcheck.yaml')
    args = parser.parse_args()
    return args.healthcheck_yaml_file


def store_response(response, url):
    domain = urlparse(url).netloc
    if domain in result:
        result[domain]["total"] = result[domain]["total"]+1
    else:
        result[domain] = {}
        result[domain]["success"] = 0
        result[domain]["total"] = 1
    if response.status_code > 199 and response.status_code < 300 and response.elapsed.total_seconds()*1000 < 500:
        result[domain]["success"] = result[domain]["success"]+1


def perform_actual_healthcheck(check):
    url = check["url"]

    method = "GET"
    if "method" in check:
        method = check["method"]

    headers= {}
    if "headers" in check:
        for header,value in check["headers"].items():
            headers[header] = value
    else:
        headers = None

    body = None
    if "body" in check:
        body = check["body"]

    if method.lower() == "get":
        response = requests.get(url, headers=headers)
        store_response(response, url)

    elif method.lower() == "post":
        response = requests.post(url, headers=headers, json=body)
        store_response(response, url)


def print_result():
    print(result)
    for key, domain in result.items():
        percent = (domain['success'] / domain['total'])*100
        print(key + " has "+ str(percent)+"% availability percentage")


def perform_healthcheck(healthcheck_data):
    for check in healthcheck_data[0]:
        perform_actual_healthcheck(check)
    print_result()

if __name__ == '__main__':
    global result
    result = {}
    yaml_path = get_yaml()
    healthcheck_data = read_yaml(yaml_path)
    print(healthcheck_data)
    #perform_healthcheck(healthcheck_data)

    schedule.every(5).seconds.do(perform_healthcheck, healthcheck_data)

    while True:
         schedule.run_pending()
         time.sleep(1)


