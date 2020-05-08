import click

from aicrowd.config import Config
from aicrowd.context import pass_info, Info

@click.group(name="keys", short_help="Manage keys to be used with cli")
def keys_command():
    pass

@click.command(name='add', help="Add a key")
@click.option("--key", "-k", help="Key to be passed")
@pass_info
def add(info: Info, key):
    key_name, value = key.split("=")
    config = Config()
    config_settings = config.settings
    config_settings[key_name] = value
    config.dump(config_settings)

keys_command.add_command(add)
