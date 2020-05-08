#!/usr/bin/env python

import os

AUTH_TOKEN_KEY = "aicrowd_evaluations_token"
AICROWD_API_KEY = "AICROWD_API_KEY"
API_HOST = os.getenv(
    "AICROWD_EVALUATION_API_ENDPOINT",
    "https://evaluations-api.internal.k8s.aicrowd.com/v1",
)
HELM_REPO = "https://gitlab.aicrowd.com/aicrowd/evaluator-templates/raw/charts/"


class Errors:
    """Error codes to return"""

    auth = 0
    keys = 1
    values = 2
    api = 3
    helm = 4
