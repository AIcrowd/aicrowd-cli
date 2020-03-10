import json
import os

import click

from aicrowd.context import pass_info, Info
from helpers.evalapi import Auth, Grader

@click.group(name="eval", short_help="Evaluations API commands")
def eval_command():
    pass


@click.command(help="Login into evaluations API")
@pass_info
def login(info: Info):
    email = click.prompt('Evaluations API email', type=str)    
    password = click.prompt('Evaluations API password', type=str)    
    if Auth.login(email, password):
        click.echo("Logged in successfully!")
    else:
        click.echo("Please try again!")

@click.command(help="Create Grader")
@pass_info
def new_grader(info: Info):
    grader_url = click.prompt('Enter Grader URL', type=str)    
    if Grader.create_grader(grader_url):
        click.echo("Logged in successfully!")
    else:
        click.echo("Please try again!")


eval_command.add_command(login)
eval_command.add_command(new_grader)
