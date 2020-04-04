import json
import os

import click

from aicrowd.context import pass_info, Info
from aicrowd.utils import edit_challenge_config
from helpers.submission import Submission


@click.command(name='submit', help="Make a Submission")
@click.argument('version_number')
@click.option('--http', type=bool, default=False)
@click.option('--dummy', type=bool, default=False)
@pass_info
def submit_command(info: Info, version_number, http, dummy):
    challenge_config = os.path.join(os.getcwd(), info.challenge_config)
    with open(challenge_config) as f:
        challenge_json = json.load(f)
    if not 'username' in challenge_json and not 'project_slug' in challenge_json:
        # click.echo('Please create a gitlab project at https://gitlab.aicrowd.com/projects/new')
        username = click.prompt('Please enter your aicrowd username:', type=str)
        project_slug = click.prompt('Please enter your gitlab project:', type=str)
        challenge_json['username'] = username
        challenge_json['project_slug'] = project_slug
        edit_challenge_config(info, challenge_json)
    home_user = os.path.expanduser('~')
    aicrowd_root = os.path.join(home_user, info.home_default)
    if(http):
        challenge_json['personal_access_token'] = info.personal_access_token
        challenge_json['ssh_private_key'] = None
    else:
        challenge_json['personal_access_token'] = None
        challenge_json['ssh_private_key'] = os.path.join(aicrowd_root, info.private_key)

    submission = Submission(**challenge_json)
    submission.submit_current_project(version_number, http, dummy)
