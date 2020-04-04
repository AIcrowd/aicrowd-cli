import json
from urllib.parse import urljoin

import requests
from requests import HTTPError

headers = {'Content-Type': 'application/json'}

AICROWD_API = 'https://aicrowd-cli-api.herokuapp.com/api'
CHALLENGE_ROUTE = '/challenges/'
BASELINE_ROUTE = '/baselines/'
TEMPLATES_ROUTE = '/templates/'
DATASET_ROUTE = '/datasets/'

def request_handler(request_func):
    try:
        response = request_func()
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        return response.json()

class AIcrowdAPI:
    def __init__(self):
        self.api_endpoint = AICROWD_API

    def get_challenge(self, challengeid):
        request_url = ''.join((self.api_endpoint, CHALLENGE_ROUTE, challengeid))
        return request_handler(lambda: requests.get(request_url))

    def get_datasets(self, challengeid):
        return request_handler(lambda: requests.get(''.join((AICROWD_API, CHALLENGE_ROUTE, challengeid)), params={'fields': 'dataset'}))

    def get_baselines(self, challengeid):
        return request_handler(lambda: requests.get(''.join((AICROWD_API, CHALLENGE_ROUTE, challengeid)), params={'fields': 'baseline'}))

    def get_templates(self, challengeid):
        return request_handler(lambda: requests.get(''.join((AICROWD_API, CHALLENGE_ROUTE, challengeid)), params={'fields': 'challenge_template'}))
