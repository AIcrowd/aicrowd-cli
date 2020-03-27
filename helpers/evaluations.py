import os
import click
from pprint import pprint
from aicrowd.config import Config

import aicrowd_evaluations
from aicrowd_evaluations.rest import ApiException


class Evaluations:

    def __init__(self, key = ''):
        self.configuration = aicrowd_evaluations.Configuration()
        self.configuration.host = 'https://evaluations-api-staging.internal.k8s.aicrowd.com/v1'
        self.configuration.verify_ssl = False
        self.configuration.api_key['AUTHORIZATION'] = key
    
    def login(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        api_instance = aicrowd_evaluations.AuthApi(aicrowd_evaluations.ApiClient(self.configuration))
        try:
            api_response = api_instance.post_user_login(payload)
            config = Config()
            config_settings = config.settings
            config_settings['evalapi_auth_token'] = api_response.authorization
            config.dump(config_settings)
            return True
        except ApiException as e:
            return False


    def grader_create(self, grader_url):

        payload = {
            "code_access_mode": "raw",
            "docker_username": "subsbot001",
            "docker_password": "subsbot001",
            "evaluation_code": grader_url
        }
        api_instance = aicrowd_evaluations.GradersApi(aicrowd_evaluations.ApiClient(self.configuration))
        try:
            api_response = api_instance.post_grader_list_dao(payload)
            return api_response
        except ApiException as e:
            print("Exception when calling GradersApi->post_grader_list_dao: %s\n" % e)



