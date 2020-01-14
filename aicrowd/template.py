import click

from aicrowd.context import pass_info, Info
from aicrowd.utils import current_challenge

@click.group(name="template", short_help="Manage templates")
def template_command():
    pass


@click.command(help="Download the template")
@pass_info
def download(info: Info):
    challenge = current_challenge(info)
    templates = challenge.list_templates()
    confirm = True
    for idx, template in enumerate(templates):
        click.echo('[%d] %s' % (idx + 1, template['name']))
    while confirm:
        value = click.prompt('Please enter the number for the template you want to download', type=int)
        challenge.clone_template(templates[value-1])
        confirm = click.confirm('Do you want to download another template?', abort=True)

@click.command(help="List the template")
@pass_info
def list(info: Info):
    challenge = current_challenge(info)
    templates = challenge.list_templates()
    for idx, template in enumerate(templates):
        click.echo('[%d] %s' % (idx + 1, template['name']))


template_command.add_command(download)
template_command.add_command(list)







