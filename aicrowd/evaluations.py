import sys

import click
from aicrowd_evaluations.rest import ApiException
from aicrowd import fmt
from aicrowd.context import pass_info
from helpers.evaluations import AUTH_TOKEN_KEY, AICROWD_API_KEY, Errors, API_HOST
from helpers.evaluations.grader import (
    parse_secrets,
    validate as validate_grader,
    create as create_grader,
    get as get_grader,
    deploy as deploy_grader

)
from helpers.evaluations.submission import (
    create as create_submission
)
from helpers.evaluations.auth import login

@click.group(
    name="evaluations", short_help="Commands to interact with AIcrowd Evaluations API"
)
def evaluations_cmd():
    """Interact with AIcrowd Evaluations API"""
    pass

@click.group(name="grader")
@pass_info
def grader_cmd(info):
    """Create or delete a grader using AIcrowd Evaluations API"""
    try:
        auth_token = getattr(info, AUTH_TOKEN_KEY)
    except AttributeError:
        fmt.echo_error(
            "Incorrect credentials: Please login using `aicrowd evaluations login`"
        )
        sys.exit(Errors.auth)


@click.group(name="submission")
def submission_cmd():
    """Create a submission using AIcrowd Evaluations API"""
    pass
    

@click.command(name="create")
@click.option(
    "--cluster-id", default=1, type=int, envvar="EVALUATION_CLUSTER_ID", help="Cluster to use for evaluations"
)
@click.option("--repo", required=True, help="Git URL of the grader repo (SSH format)")
@click.option("--secrets", "-s", multiple=True, help="Secrets to be passed")
@click.option("--repo-tag", default="master", help="Git tag/branch to use")
@click.option("--meta", default="", help="Metadata to store along with the grader")
@click.option(
    "--validate", is_flag=True, help="Validate the grader setup without creating one"
)
@click.option("--wait", is_flag=True, help="Wait for grader to complete")
@pass_info
def create_grader_cmd(info, cluster_id, repo, secrets, repo_tag, meta, validate, wait):
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
        auth_token = getattr(info, AUTH_TOKEN_KEY)
        try:
            response = create_grader(cluster_id, repo, parsed_secrets, repo_tag, meta, wait, auth_token)
            fmt.echo(f"Created grader: {API_HOST}/graders/{response.id}")
            if wait and response.status == "Failed":
                sys.exit(Errors.api)
        except ApiException as e:
            fmt.echo_error(e)
            sys.exit(Errors.api)

@click.command(name="status", help="Get status of the grader")
@click.option("--grader_id", "-g", required=True, help="ID of the grader")
@pass_info
def grader_status_cmd(info, grader_id):
    auth_token = getattr(info, AUTH_TOKEN_KEY)
    try:
        response = get_grader(grader_id, auth_token)
        fmt.echo(response.status)
    except ApiException as e:
        fmt.echo_error(e)
        sys.exit(Errors.api)   

@click.command(name="deploy", help="Deploy the grader on AIcrowd")
@click.option("--grader_id", "-g", required=True, help="ID of the grader")
@pass_info
def deploy_grader_cmd(info, grader_id):
    try:
        aicrowd_api_key = getattr(info, AICROWD_API_KEY)
    except AttributeError:
        fmt.echo_error(
            "AIcrowd API key not found: Please add it using `aicrowd keys add AICROWD_API_KEY=<key>`"
        )
        sys.exit(Errors.auth) 
    try:
        challenge_url = deploy_grader(grader_id, aicrowd_api_key)["url"]
        fmt.echo(f"Deployed Grader for challenge: {challenge_url}")
    except ApiException as e:
        fmt.echo_error(e)
 

@click.command(name="create")
@click.option("--url", "-f", required=True, help="Submission file")
@click.option("--grader_id", "-g", required=True, help="ID of the grader")
@click.option("--wait", is_flag=True, help="Wait for submission to complete")
@pass_info
def create_submission_cmd(info, url, grader_id, wait):
    """Create a submission using AIcrowd Evaluations API"""

    auth_token = getattr(info, AUTH_TOKEN_KEY)
    aicrowd_api_key = getattr(info, AICROWD_API_KEY)
    try:
        response = create_submission(grader_id, url, wait, auth_token, aicrowd_api_key)
        fmt.echo(f"Created submission: {API_HOST}/submissions/{response.id}")
        if wait and response.output == "Evaluation failed":
            sys.exit(Errors.api)
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
grader_cmd.add_command(deploy_grader_cmd)
grader_cmd.add_command(grader_status_cmd)
submission_cmd.add_command(create_submission_cmd)
evaluations_cmd.add_command(login_cmd)
evaluations_cmd.add_command(grader_cmd)
evaluations_cmd.add_command(submission_cmd)
