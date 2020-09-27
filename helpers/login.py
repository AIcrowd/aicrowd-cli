"""
Helpers for the login command
"""

import os
import requests

AICROWD_API_ENDPOINT = os.getenv(
    "AICROWD_API_ENDPOINT", "https://www.aicrowd.com/api/v1"
)


def verify_api_key(api_key):
    """
    Verifies if the API Key is valid or not
    """
    return requests.get(
        f"{AICROWD_API_ENDPOINT}/api_user",
        headers={"Authorization": f"Token token={api_key}"},
    ).ok
