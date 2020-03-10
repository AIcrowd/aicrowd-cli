import json
import os

import click

from aicrowd.context import pass_info, Info
from helpers.evalapi import Login

@click.group(name="eval", short_help="Evaluations API commands")
def eval_command():
    pass


@click.command(help="Login into evaluations API")
@pass_info
def login(info: Info):
    email = click.prompt('Evaluations API email', type=str)    
    password = click.prompt('Evaluations API password', type=str)    
    if Login.login(email, password):
        click.echo("Logged in successfully!")
    else:
        click.echo("Please try again!")


eval_command.add_command(login)
