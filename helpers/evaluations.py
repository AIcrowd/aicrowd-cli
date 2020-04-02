import os
import click
from pprint import pprint
from aicrowd.config import Config
import subprocess

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
            "evaluator_repo": grader_url
        }
        api_instance = aicrowd_evaluations.GradersApi(aicrowd_evaluations.ApiClient(self.configuration))
        try:
            api_response = api_instance.post_grader_list_dao(payload)
            return api_response
        except ApiException as e:
            print("Exception when calling GradersApi->post_grader_list_dao: %s\n" % e)

class Utils:

    def __init__(self):
        self.home = '~/.aicrowd/'
        self.examples_url = 'http://gitlab.aicrowd.com/aicrowd/evaluator-examples.git'
        self.examples_dir = os.path.join(self.home, 'evaluator-examples')
        self.templates_url = 'http://gitlab.aicrowd.com/aicrowd/evaluator-templates.git'
        self.templates_dir = os.path.join(self.home, 'evaluator-templates')
    

    def list_templates(self):
        if not os.path.exists(self.templates_dir):
            subprocess.run(f"git clone {self.templates_url} {self.templates_dir}".split())
        templates = [ f.name for f in os.scandir(self.templates_dir) if f.is_dir() and f.name[0] is not '.']
        return templates
    
    def get_template(self, template):
        subprocess.run(f'cp -r {os.path.join(self.templates_dir, template)} .'.split())
        

    def list_examples(self):
        if not os.path.exists(self.examples_dir):
            subprocess.run(f"git clone {self.examples_url} {self.examples_dir}".split())
        examples = [ f.name for f in os.scandir(self.examples_dir) if f.is_dir() and f.name[0] is not '.']
        return examples
    
    def get_example(self, example):
        subprocess.run(f'cp -r {os.path.join(self.examples_dir, example)} .'.split())
        
