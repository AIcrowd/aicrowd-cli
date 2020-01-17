import os

import click
import pyperclip

from aicrowd.config import Config
from aicrowd.context import pass_info, Info
from helpers.ssh import SSHHandler

@click.group(name="access_token", short_help="Manage datasets")
def access_token_command():
    pass

@click.command(name='create', help="Generate access token")
@pass_info
def create(info: Info):
    click.echo(f"Please navigate to https://gitlab.aicrowd.com/profile/personal_access_tokens and create an access token")
    access_token = click.prompt('Copy the generated access token here', type=str)
    config = Config()
    config_settings = config.settings
    config_settings['personal_access_token'] = access_token
    config.dump(config_settings)
    click.echo(
        f"successfully created the access_token Now you can push your code using http or know your submission status")



access_token_command.add_command(create)
