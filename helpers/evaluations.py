import os
import click
from pprint import pprint
import subprocess
import shutil

import aicrowd_evaluations
from aicrowd_evaluations.rest import ApiException
from aicrowd.config import Config
from handlers.git_handler import Git


class Evaluations:

    def __init__(self, key = ''):
        self.configuration = aicrowd_evaluations.Configuration()
        self.configuration.host = 'https://evaluations-api-staging.internal.k8s.aicrowd.com/v1'
        self.configuration.verify_ssl = False
        self.configuration.api_key['AUTHORIZATION'] = key
    
    def login(self, email, password):
        payload = aicrowd_evaluations.Login(email=email, password=password)
        api_instance = aicrowd_evaluations.AuthApi(aicrowd_evaluations.ApiClient(self.configuration))
        try:
            api_response = api_instance.login(payload)
            config = Config()
            config_settings = config.settings
            config_settings['evalapi_auth_token'] = api_response.authorization
            config.dump(config_settings)
            return True
        except ApiException as e:
            return False


    def grader_create(self, grader_url):
        payload = aicrowd_evaluations.Grader(evaluator_repo=grader_url)
        api_instance = aicrowd_evaluations.GradersApi(aicrowd_evaluations.ApiClient(self.configuration))
        try:
            api_response = api_instance.create_grader(payload)
            return api_response
        except ApiException as e:
            print("Exception when calling GradersApi->post_grader_list_dao: %s\n" % e)

class Utils:

    def __init__(self):
        self.config = Config()
        self.templates_dir = os.path.join(os.path.expanduser('~'), self.config.settings['templates_dir'])
        self.examples_dir = os.path.join(os.path.expanduser('~'), self.config.settings['examples_dir'])

    def helm_validate(self, grader_url, repo_tag = 'master'):
        
        # Clone necessary repositories
        os.mkdir('.validate')
        os.chdir('.validate')
        Git().clone(f"{grader_url} evaluator-repository")
        os.chdir('evaluator-repository')
        subprocess.run(f"git checkout {repo_tag}".split(), stdout=subprocess.DEVNULL)
        Git().clone(f"{self.config.settings['templates_url']} evaluator-templates")

        # Get the template name from aicrowd.yaml
        with open('aicrowd.yaml', 'r') as infile:
            proc = subprocess.Popen('yq -r .challenge.template'.split(), stdin = infile, stdout=subprocess.PIPE)
        template = proc.stdout.read().decode('utf-8').strip()
        print(f"Detected template name as: {template}")

        # Copy the helm template to the directory having grader
        os.mkdir('.aicrowd')
        subprocess.run(f'cp -r evaluator-templates/{template} .aicrowd'.split())
        subprocess.run(f'mv .aicrowd/{template}/aicrowd.yaml .aicrowd/{template}/values.yaml'.split())
        subprocess.run(f'cd .aicrowd/{template} && chmod +x ./pre-start.sh && ./pre-start.sh && cd -'.split(), stdout=subprocess.DEVNULL, shell=True)
        subprocess.run(f'ls | xargs -n1 -I{{}} rm -rf .aicrowd/{template}/{{}}'.split(), shell = True, stdout=subprocess.DEVNULL)
        subprocess.run(f'cp -r * .aicrowd/{template}', shell=True)

        # Expand helm templates
        proc = subprocess.run(f'helm template --values aicrowd.yaml .aicrowd/{template} -f aicrowd.yaml > desired-fs.yaml', shell = True)
        os.chdir('../..')
        shutil.rmtree('./.validate')
        if proc.returncode is 0:
            return True
        
        return False


    def list_templates(self):
        if not os.path.exists(self.templates_dir):
            Git().clone(f"{self.config.settings['templates_url']} {self.templates_dir}")
            #subprocess.run(f"git clone {self.config.settings['templates_url']} {self.templates_dir}".split())
        templates = [ f.name for f in os.scandir(self.templates_dir) if f.is_dir() and f.name[0] is not '.']
        return templates
    
    def get_template(self, template):
        subprocess.run(f'cp -r {os.path.join(self.templates_dir, template)} .'.split())
        

    def list_examples(self):
        if not os.path.exists(self.examples_dir):
            Git().clone(f"{self.config.settings['examples_url']} {self.examples_dir}")
            #subprocess.run(f"git clone {self.config.settings['examples_url']} {self.examples_dir}".split())
        examples = [ f.name for f in os.scandir(self.examples_dir) if f.is_dir() and f.name[0] is not '.']
        return examples
    
    def get_example(self, example):
        subprocess.run(f'cp -r {os.path.join(self.examples_dir, example)} .'.split())
        
