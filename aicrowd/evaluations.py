import sys

import click
from aicrowd_evaluations.rest import ApiException
from aicrowd import fmt
from aicrowd.context import pass_info
from helpers.evaluations import AUTH_TOKEN_KEY, Errors, API_HOST
from helpers.evaluations.grader import (
    parse_secrets,
    validate as validate_grader,
    create as create_grader,
)
from helpers.evaluations.auth import login


@click.group(
    name="evaluations", short_help="Commands to interact with AIcrowd Evaluations API"
)
def evaluations_cmd():
    """Interact with AIcrowd Evaluations API"""
    pass


@click.group(name="grader")
def grader_cmd():
    """Create or delete a grader using AIcrowd Evaluations API"""
    pass


@click.group(name="submission")
def submission_cmd():
    """Create a submission using AIcrowd Evaluations API"""
    pass


@click.command(name="create")
@click.option(
    "--cluster-id", default=1, type=int, help="Cluster to use for evaluations"
)
@click.option("--repo", required=True, help="Git URL of the grader repo (SSH format)")
@click.option("--secrets", "-s", multiple=True, help="Secrets to be passed")
@click.option("--repo-tag", default="master", help="Git tag/branch to use")
@click.option("--meta", default="", help="Metadata to store along with the grader")
@click.option(
    "--validate", is_flag=True, help="Validate the grader setup without creating one"
)
@pass_info
def create_grader_cmd(info, cluster_id, repo, secrets, repo_tag, meta, validate):
    """Create a grader using AIcrowd Evaluations API"""
    parsed_secrets = parse_secrets(secrets)

    try:
        validate_grader(repo, parsed_secrets)
    except KeyError as e:
        fmt.echo_error(f"Attributes missing: {e}")
        sys.exit(Errors.keys)
    except ValueError as e:
        fmt.echo_error(f"Incorrect values: {e}")
        sys.exit(Errors.values)
    fmt.echo_info("Validation completed.")

    if not validate:
        try:
            auth_token = getattr(info, AUTH_TOKEN_KEY)
        except AttributeError:
            fmt.echo_error(
                "Incorrect credentials: Please login using `aicrowd evaluations login`"
            )
            sys.exit(Errors.auth)
        try:
            response = create_grader(cluster_id, repo, parsed_secrets, repo_tag, meta, auth_token)
            fmt.echo(f"Created grader: {API_HOST}/graders/{response.id}")
        except ApiException as e:
            fmt.echo_error(e)
            sys.exit(Errors.api)


@click.command(name="login", help="Login to AIcrowd Evaluations API")
@click.option("--email", "-e", required=True)
@click.option("--password", "-p", required=True)
@pass_info
def login_cmd(info, email, password):
    try:
        login(email, password)
    except ApiException as e:
        fmt.echo_error(e)
        sys.exit(Errors.api)
    fmt.echo_info("Logged in successfully!")


grader_cmd.add_command(create_grader_cmd)
evaluations_cmd.add_command(login_cmd)
evaluations_cmd.add_command(grader_cmd)
evaluations_cmd.add_command(submission_cmd)
