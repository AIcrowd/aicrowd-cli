import os
import time
import re
import yaml
import subprocess
import shutil
import platform
import time
import aicrowd_evaluations
from aicrowd.config import Config
from aicrowd import fmt
from helpers.evaluations.auth import api_configuration
from helpers.evaluations import AICROWD_API_KEY


def wait_to_complete(api, method, object_id, timeout=60 * 15):
    start_time = time.time()
    f = getattr(api, method)
    response = f(object_id)
    while response.status != "Completed" and (
        start_time - time.time() < timeout
    ):
        time.sleep(15)
        response = f(object_id)
        print(response)
    return response


def create(grader_id, file_type, file_path, wait, auth_token):
    """Make post request to Evaluations API"""
    submission_code = open(file_path, "r").read()
    submission_type = file_type
    configuration = api_configuration(auth_token)

    api_instance = aicrowd_evaluations.SubmissionsApi(
        aicrowd_evaluations.ApiClient(configuration)
    )
    payload = aicrowd_evaluations.Submissions(
        meta=f'{{"round_id": 0, "participant_id": 0, "submission_id": 0, "challenge_client_name": "{grader_id}", "domain_name":"https://www.aicrowd.com", "aicrowd_token":"{AICROWD_API_KEY}"}}',
        grader_id=grader_id,
        submission_data={"type": submission_type, "code": submission_code}
    )
    api_response = api_instance.create_submission(payload)
    if wait:
        api_response = wait_to_complete(api_instance, "get_submission", api_response.id)
    return api_response

