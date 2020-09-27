"""
For handling logins
"""
import sys
import click

from aicrowd.config import Config
from helpers.login import verify_api_key


@click.command(name="login")
@click.option(
    "--api-key",
    type=str,
    envvar="AICROWD_API_KEY",
    help="API Key from AIcrowd website",
)
def login_command(api_key):
    """
    Log in using AIcrowd API Key

    Saves the API Key to a file
    !! NOT ENCRYPTED
    """
    conf = Config()
    conf_settings = conf.settings

    if api_key is None:
        click.launch("https://www.aicrowd.com")
        click.echo(
            "Please login to the website and "
            + "Click on your profile picture -> View profile -> Copy paste the API Key"
        )
        api_key = click.prompt("API Key")

    click.echo("Verifying API Key...")
    if not verify_api_key(api_key):
        click.echo(
            click.style("Invalid API Key provided", fg="red", bold=True), err=True
        )
        sys.exit(1)

    click.echo(click.style("API Key valid", fg="green"))

    api_key_in_conf = conf_settings.get("aicrowd_api_key", "") != ""

    # if not defined or an older value, update
    if not api_key_in_conf or conf_settings["aicrowd_api_key"] != api_key:
        conf_settings["aicrowd_api_key"] = api_key

    conf.dump(conf_settings)
    click.echo(click.style("Saved API Key successfully!", fg="green"))
