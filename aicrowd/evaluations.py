import json
import os

import click

from aicrowd.context import pass_info, Info
from helpers.evaluations import Evaluations


@click.group(name="evaluations", short_help="General commands for EvalAPI")
def evaluations_command():
    pass    

@click.command(help="Login to use evaluations")
@click.option('--email', '-e', required=True)
@click.option('--password', '-p', required=True)
@pass_info
def login(info: Info, email, password):
    evaluations = Evaluations()
    if evaluations.login(email, password):
        click.echo(f"Logged in successfully!")
    else:
        click.echo(f"Incorrect Credentials, Try again!")
        

evaluations_command.add_command(login)

