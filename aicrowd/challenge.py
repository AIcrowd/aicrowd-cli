import click

from aicrowd.context import pass_info, Info
from helpers.challenge import Challenge

@click.group(name="challenge", short_help="Manage challenges")
def challenge_command():
    pass

@click.command(help="Init the project structure for challenge")
@click.argument('challenge')
@pass_info
def init(_: Info, challenge):
    """Say 'hello' to the nice people."""
    click.echo(f"generating the directory for challenge %s" %(challenge))
    Challenge(challenge).get_challenge_project()
    click.echo(f"generated the directory for the challenge %s" % (challenge))

challenge_command.add_command(init)
