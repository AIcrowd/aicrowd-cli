import json
import os
import re

import click
import emoji
import gitlab

from aicrowd.context import pass_info, Info

@click.command(name='status', help="Status of Recent Submission")
@pass_info
def status(info: Info):
    challenge_config = os.path.join(os.getcwd(), info.challenge_config)
    with open(challenge_config) as f:
        challenge_json = json.load(f)
    aicrowd_replies = gitlab_information('%s%%2F%s' %(challenge_json['username'], challenge_json['project_slug']), info.personal_access_token)
    click.echo(emoji.emojize(aicrowd_replies.replace('broken\_heart', 'broken_heart'), use_aliases=True))

def gitlab_information(gitlab_project, access_token):
    aicrowd_reply = None
    gl = gitlab.Gitlab('https://gitlab.aicrowd.com', private_token = access_token)
    project = gl.projects.get(gitlab_project)
    latest_issue = project.issues.list()[0].iid
    issue = project.issues.get(latest_issue)
    discussions = issue.discussions.list()
    if len(discussions) < 2:
        return ["Gitlab comment from aicrowd-bot is still pending, submission probably in image_build step"]

    discussion = discussions[1]
    for discussion in discussions:
        for note in discussion.attributes['notes']:
            if note['author']['username'] == 'aicrowd-bot':
                aicrowd_reply = re.sub('\|  \[|\:  \[', '\n[', re.sub('\n\n\n|`|\n__Note(.*)|\nThis is(.*)|\n Please(.*)', '', note['body']))

    if aicrowd_reply is None:
        return ["Gitlab comment from aicrowd-bot is still pending, submission probably in image_build step"]

    return aicrowd_reply

