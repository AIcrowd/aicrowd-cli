import os
import time
import re
import yaml
import subprocess
import shutil
import wget
import platform
import time
import aicrowd_evaluations
from aicrowd.config import Config
from aicrowd import fmt
from helpers.evaluations.auth import api_configuration


def wait_to_complete(api, method, object_id, timeout=60 * 15):
    start_time = time.time()
    f = getattr(api, method)
    response = f(object_id)
    while response.status is not "Completed" and (
        start_time - time.time() < timeout
    ):
        time.sleep(15)
        response = f(object_id)
    return response


def create(grader_id, file_path, wait, auth_token):
    """Make post request to Evaluations API"""
    submission_code = open(file_path, "r").read()
    submission_type = file_path.split('.')[-1]
    configuration = api_configuration(auth_token)

    api_instance = aicrowd_evaluations.SubmissionsApi(
        aicrowd_evaluations.ApiClient(configuration)
    )
    payload = aicrowd_evaluations.Submissions(
        meta='{"round_id": 0, "participant_id": 0}',
        grader_id=grader_id,
        submission_data={"type": submission_type, "code": submission_code}
    )
    api_response = api_instance.create_submission(payload)
    if wait:
        api_response = wait_to_complete(api_instance, "get_submission", api_response.id)
    return api_response

