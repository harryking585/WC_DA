import requests as r
import pandas as pd
import os
from pathlib import Path


def initialize_enviromentals():
    # Get path to .env file in parent directory
    env_path = Path(__file__).resolve().parent.parent / ".env"

    # Load each line into environment
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                os.environ[key] = value
    client = os.getenv("CLIENT_ID")
    secret = os.getenv("SECRET")

    return [client, secret]


def grab_OAUTH_cred(client_id, key):
    data = {
    'grant_type': 'client_credentials',
    }

    response = r.post(
        'https://oauth.battle.net/token',
        data=data,
        auth=(client_id, key),
    )

    return response


def main():
    hostname = "us.api.blizzard.com"
    envs = initialize_enviromentals()
    client_id = envs[0]
    key = envs[1]

    resp = grab_OAUTH_cred(client_id, key)
    access_token = resp.json()['access_token']
    sub = resp.json()['sub']

    


if __name__ =="__main__":
    main()
