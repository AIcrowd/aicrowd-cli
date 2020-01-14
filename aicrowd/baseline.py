import click

from aicrowd.context import pass_info, Info
from aicrowd.utils import current_challenge

@click.group(name="baseline", short_help="Manage challenge baselines")
def baseline_command():
    pass

@click.command(help="Download the baseline")
@pass_info
def download(info: Info):
    challenge = current_challenge(info)
    baselines = challenge.list_baselines()
    for idx, baseline in enumerate(baselines):
        click.echo('[%d] %s' % (idx + 1, baseline['name']))
    confirm = True
    while confirm:
        value = click.prompt('Please enter the number for the baseline you want to download', type=int)
        challenge.clone_baseline(baselines[value-1])
        confirm = click.confirm('Do you want to download another baseline?', abort=True)


@click.command(help="List the baseline")
@pass_info
def list(info: Info):
    challenge = current_challenge(info)
    baselines = challenge.list_baselines()
    for idx, baseline in enumerate(baselines):
        click.echo('[%d] %s' % (idx + 1, baseline['name']))


baseline_command.add_command(download)
baseline_command.add_command(list)
