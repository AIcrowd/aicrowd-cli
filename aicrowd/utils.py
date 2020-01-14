import json
import os

from helpers.challenge import Challenge


def current_challenge(info):
    challenge_config = os.path.join(os.getcwd(), info.challenge_config)
    with open(challenge_config) as f:
        challenge_id = json.load(f)['challenge_id']
    challenge = Challenge(challenge_id)
    return challenge

def edit_challenge_config(info, challenge_json):
    challenge_config = os.path.join(os.getcwd(), info.challenge_config)
    os.remove(challenge_config)
    with open(challenge_config, 'w') as f:
        json.dump(challenge_json, f, indent=4)
