import os

import click

from handlers.evalapi_handler import EvalAPI

aicrowd_api = EvalAPI()

class Auth:
    def __init__(self):
        pass

    def login(email, password):
        response = aicrowd_api.login(email, password)
        return response
    
class Grader:
    def create_grader(grader_url, auth_token):
        response = aicrowd_api.create_grader(grader_url, auth_token)
        return response
