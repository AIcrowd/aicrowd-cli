#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

Itcan be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: aicrowd.cli
.. moduleauthor:: S.P. Mohanty <spmohanty91@gmail.com>
"""
import logging
import os

import click

from aicrowd.access_token import access_token_command
from aicrowd.baseline import baseline_command
from aicrowd.challenge import challenge_command
from aicrowd.config import Config
from aicrowd.context import pass_info, Info
from aicrowd.convert import convert_command
from aicrowd.dataset import dataset_command
from aicrowd.ssh import ssh_command
from aicrowd.status import status
from aicrowd.submit import submit_command
from aicrowd.template import template_command
from aicrowd.evaluations import evaluations_cmd
from aicrowd.keys import keys_command
from helpers.ssh import SSHHandler
from aicrowd.__init__ import __version__

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels




# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    """Run aicrowd."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    config = Config()
    info.verbose = verbose
    vars(info).update(config.settings)


cli.add_command(baseline_command)
cli.add_command(challenge_command)
cli.add_command(convert_command)
cli.add_command(dataset_command)
cli.add_command(ssh_command)
cli.add_command(submit_command)
cli.add_command(template_command)
cli.add_command(status)
cli.add_command(access_token_command)
cli.add_command(evaluations_cmd)
cli.add_command(keys_command)

@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))
