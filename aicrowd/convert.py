import json
import os

import click

from aicrowd.context import pass_info, Info
from helpers.nb_parser import parse


@click.command(name='convert', help="Convert a Python Notebook to AICrowd Submission")
@click.argument('notebook')
@pass_info
def convert_command(info: Info, notebook):
    #TODO: Generate a Dockerfile that can read run.sh and make the respective installations
    code_file = 'code.py'
    bash_file = 'shell.py'
    parse(notebook, code_file, bash_file)
