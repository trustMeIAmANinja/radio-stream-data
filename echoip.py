import requests
import json
import sys

def log_external_ip():
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        print('Status: ' + response.status_code + ' .Problem with the request. Exiting.')
    data = response.json()
    print("External Gateway IP Address is " + data['ip'])

log_external_ip()
