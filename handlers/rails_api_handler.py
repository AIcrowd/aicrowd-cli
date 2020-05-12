import json
from urllib.parse import urljoin

import requests
from requests import HTTPError

BASE_URL = 'https://www.aicrowd.com/api/v1/challenges/'

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

class RailsAPI:
    def __init__(self, auth_token):
        self.api_endpoint = BASE_URL
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Token token="{auth_token}"'}

    def deploy_grader(self, challenge_slug, grader_id):
        request_url = ''.join((self.api_endpoint, challenge_slug))
        payload = {
            "evaluator_type_cd": "evaluations_api",
            "challenge_client_name": f"{grader_id}"
        }
        return request_handler(lambda: requests.patch(request_url, json=payload, headers=self.headers))
        