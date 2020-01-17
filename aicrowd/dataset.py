import json
import os

import click

from aicrowd.context import pass_info, Info
from aicrowd.utils import current_challenge

@click.group(name="dataset", short_help="Manage datasets")
def dataset_command():
    pass


@click.command(help="Download the dataset")
@pass_info
def download(info: Info):
    challenge = current_challenge(info)
    datasets = challenge.list_datasets()
    confirm = True
    while confirm:
        for idx, dataset in enumerate(datasets):
            click.echo('[%d] %s' %(idx+1, dataset['dataset_name']))
        value = click.prompt('Please enter the number for the dataset you want to download', type=int)
        challenge.download_dataset(datasets[value-1])
        confirm = click.confirm('\nDo you want to download another dataset?', abort=True)

@click.command(help="List the dataset")
@pass_info
def list(info: Info):
    challenge = current_challenge(info)
    datasets = challenge.list_datasets()
    for idx, dataset in enumerate(datasets):
        click.echo('[%d] %s' % (idx + 1, dataset['dataset_name']))

dataset_command.add_command(download)
dataset_command.add_command(list)
