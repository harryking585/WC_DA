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


# def test_req(key):
#     print("starting request")

#     print("end request")
#     return 0


def main():
    envs = initialize_enviromentals()
    client_id = envs[0]
    key = envs[1]

    print("CLIENT == " + client_id)
    print("SECRET == " + key)


if __name__ =="__main__":
    main()
