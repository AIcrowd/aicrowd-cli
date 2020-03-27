import json
import os

import click

from aicrowd.context import pass_info, Info
from helpers.evaluations import Evaluations


@click.group(name="grader", short_help="Grader related commands for the evaluations API")
@pass_info
def grader_command(info: Info):
    try:
        info.evalapi_auth_token
    except AttributeError:
        click.echo(f"Login to continue")
        evaluations = Evaluations()
        while True:
            email = click.prompt('Email', type=str)
            password = click.prompt('Password', type=str)
            if evaluations.login(email, password):
                break
            click.echo("Please try again!")            
        click.echo(f"Logged in successfully!")
        
        

@click.command(help="Create Grader")
@pass_info
def create(info: Info):
    grader_url = click.prompt('Enter Grader URL', type=str)
    evaluations = Evaluations(info.evalapi_auth_token)
    grader = evaluations.grader_create(grader_url)
    if grader:
        click.echo(f"Grader queued successfully with ID: {grader.id}")
    else:
        click.echo("Please try again!")


grader_command.add_command(create)
