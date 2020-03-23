import json
from urllib.parse import urljoin

import requests
from requests import HTTPError
from aicrowd.config import Config

headers = {'Content-Type': 'application/json'}

EVAL_API = 'http://evaluations-api-staging.internal.k8s.aicrowd.com/v1'
LOGIN_ROUTE = '/auth/login'
GRADER_ROUTE = '/graders/'

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

class EvalAPI:
    def __init__(self):
        self.api_endpoint = EVAL_API

    def login(self, email, password):
        request_url = ''.join((self.api_endpoint, LOGIN_ROUTE))
        payload = {
            'email': email,
            'password': password
        }
        response = request_handler(lambda: requests.post(request_url, json = payload, headers = headers))
        try:
            config = Config()
            config_settings = config.settings
            config_settings['evalapi_auth_token'] = response['Authorization']
            config.dump(config_settings)
        except:
            pass
        return response
    
    def create_grader(self, grader_url, auth_token):
        headers['Authorization'] = auth_token
        request_url = ''.join((self.api_endpoint, GRADER_ROUTE))
        payload = {
            "code_access_mode": "raw",
            "docker_username": "subsbot001",
            "docker_password": "subsbot001",
            "evaluation_code": grader_url
        }
        response = request_handler(lambda: requests.post(request_url, json = payload, headers = headers))
        return response 