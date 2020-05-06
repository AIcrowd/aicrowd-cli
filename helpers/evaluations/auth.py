#!/usr/bin/env
import aicrowd_evaluations
from aicrowd.config import Config
from helpers.evaluations import API_HOST, AUTH_TOKEN_KEY


def api_configuration(auth_key=None):
    configuration = aicrowd_evaluations.Configuration()
    configuration.host = API_HOST
    if auth_key:
        configuration.api_key["AUTHORIZATION"] = auth_key
    return configuration


def login(email, password):
    api_instance = aicrowd_evaluations.AuthApi(
        aicrowd_evaluations.ApiClient(api_configuration())
    )
    payload = aicrowd_evaluations.Login(email=email, password=password)
    api_response = api_instance.login(payload)
    config = Config()
    config.settings[AUTH_TOKEN_KEY] = api_response.authorization
    config.dump(config.settings)
