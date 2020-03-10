import os

import click

from handlers.evalapi_handler import EvalAPI

aicrowd_api = EvalAPI()

class Login:
    def __init__(self):
        pass

    def login(email, password):
        response = aicrowd_api.login(email, password)
        return response
