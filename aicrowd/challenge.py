import click

from aicrowd.context import pass_info, Info
from helpers.challenge import Challenge

@click.group(name="challenge", short_help="Manage challenges")
def challenge_command():
    pass

@click.command(help="Init the project structure for challenge")
@click.option('--challenge', '-c')
@pass_info
def init(_: Info, challenge):
    """Say 'hello' to the nice people."""
    click.echo(f"generating the directory for challenge %s" %(challenge))
    challenge_id = click.prompt('Please enter the challenge id', type=str)
    challenge_id = Challenge(challenge_id).get_challenge_project()
    click.echo(f"generated the directory for the challenge %s" % (challenge))

challenge_command.add_command(init)
