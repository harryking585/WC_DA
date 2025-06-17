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


def test_get_call(hostname, access_token):
    headers = {
        'Authorization':f'Bearer {access_token}'
    }
    response = r.get(
        hostname,
        headers=headers

    )

    return response

def main():
    print("****** Starting MAIN ******")
    hostname = "https://us.api.blizzard.com/"
    append = "data/wow/achievement/index?namespace=static-us&locale=en_US"
    hostname += append

    envs = initialize_enviromentals()
    client_id = envs[0]
    key = envs[1]
    print(f"!Client Credentials Obtained\nCLIENT_ID={client_id}\nSECRET={key}")
    resp = grab_OAUTH_cred(client_id, key)
    access_token = resp.json()['access_token']
    sub = resp.json()['sub']
    print(f"!OAUTH Credentials Obtained\nACCESS_TOKEN={access_token}\nSUB_TOKEN={sub}")

    test = test_get_call(hostname, access_token)

    print(test)

    print("****** Ending MAIN ******")

    


if __name__ =="__main__":
    main()
