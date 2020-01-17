import os

import click
import pyperclip

from aicrowd.context import pass_info, Info
from helpers.ssh import SSHHandler

@click.group(name="ssh", short_help="Manage SSH keys")
def ssh_command():
    pass

@click.command(name='create', help="Generate SSH keys")
@pass_info
def ssh_create(info: Info):
    click.echo(f"generating the ssh keys")
    home_user = os.path.expanduser('~')
    aicrowd_root = os.path.join(home_user, info.home_default)
    private_file = os.path.join(aicrowd_root, info.private_key)
    public_file = os.path.join(aicrowd_root, info.public_key)

    ssh_handler = SSHHandler(private_file, public_file)
    click.echo("generating SSH keys")
    pubkey = ssh_handler.generate_keys()
    click.echo('copied the public key to your clipboard, paste it at https://gitlab.aicrowd.com/profile/keys')
    pyperclip.copy(pubkey.decode('ascii'))
    click.echo('Incase of copying the public key manually, here is the public key')
    click.echo(pubkey)

ssh_command.add_command(ssh_create)
