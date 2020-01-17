import os
import shutil

import click
import wget

from handlers.api_handler import AIcrowdAPI
from handlers.git_handler import Git

aicrowd_api = AIcrowdAPI()

class Challenge:
    def __init__(self, challenge_id):
        self.challenge_id = challenge_id

    def get_challenge_project(self):
        response = aicrowd_api.get_challenge(self.challenge_id)
        git_addr = response['git_addr']
        Git().clone('--progress ' + git_addr)
        return self.challenge_id

    def list_datasets(self):
        response = aicrowd_api.get_datasets(self.challenge_id)
        #replace with logging
        datasets = response['dataset']
        return datasets

    def download_dataset(self, dataset):
        os.makedirs('data', exist_ok=True)
        dataset_name = wget.download(dataset['download_link'])
        shutil.move(dataset_name, os.path.join('data', dataset_name))

    def list_baselines(self):
        response = aicrowd_api.get_baselines(self.challenge_id)
        #replace with logging
        baselines = response['baseline']
        return baselines

    def clone_baseline(self, baseline):
        Git().clone('--progress ' + baseline['git_addr'])

    def list_templates(self):
        response = aicrowd_api.get_templates(self.challenge_id)
        # replace with logging
        templates = response['challenge_template']
        return templates

    def clone_template(self, template):
        Git().clone('--progress ' + template['git_addr'])
