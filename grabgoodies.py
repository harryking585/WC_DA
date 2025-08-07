import requests as r
import pandas as pd
import os
from pathlib import Path
import json
from json import loads, dumps
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
app = FastAPI()

def initialize_environmentals():
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

    try:
        response = r.post(
            'https://oauth.battle.net/token',
            data=data,
            auth=(client_id, key),
        )
    except:
        print("Error has occurred: Unable to grab OAUTH token from battle.net. Ensure your Client ID and Secret are correct and still active.")

    return response


# checks a str to see if it can be converted to a dict
def check_isJson(p_str):
    return 0


# Takes unformatted_str and casts it to a dictionary using the json library
# @return => python dictionary || None
def str_to_dict(unformatted_str):
    formatted_str = unformatted_str.replace('\'', '\"')

    try:
        json_dict = json.loads(formatted_str)
    except:
        print("ERROR: String does not fully represent a dictionary, assumming type 'None'")
        return None
    
    return json_dict


    

# Calls the mythic plus blizzard endpoint and formats the dataframe to ideal working state
# @return => dataframe || -1
def get_mythicplus(hostname, access_token, realm="emerald-dream",char_name="vathren"):
    df_list = ['hee']
    namespace = "profile-us"
    headers = {
        "Battlenet-Namespace": namespace,
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = r.get(
            hostname+f"profile/wow/character/{realm}/{char_name}/mythic-keystone-profile",
            headers=headers
        )
    except:
        print(f'ERROR: Unable to receive response from {hostname}profile/wow/character/{realm}/{char_name}/mythic-keystone-profile')
        return -1
    
    # Grabbing hostname for most recent participated mythic+ season
    char_seasons = response.json()['seasons']
    played_seasons = []
    for x in char_seasons:
        played_seasons.append(x['id'])
    current_season = max(played_seasons)-1
    i = 0
    hostname = ''
    while(i < len(char_seasons)):
        if(char_seasons[i]['id'] == current_season):
            hostname = char_seasons[i]['key']['href']
            break
        i+=1
    print(hostname)
    headers.pop("Battlenet-Namespace")
    try:
        response = r.get(
            hostname,
            headers=headers
        )
    except:
        print(f'ERROR: Unable to receive response from {hostname}profile/wow/character/{realm}/{char_name}/mythic-keystone-profile')
        return -1
    
    
    mplus_json = response.json()
    # bestrun_df = pd.DataFrame(mplus_json['best_runs'])
    os.makedirs('WC_DA/testdata', exist_ok=True)
    blacklist_attr = ['_links', 'mythic_rating', 'character']
    # bestrun_df.to_csv('WC_DA/testdata/raw_bestruns.csv')
    for key in mplus_json.keys():
        df = pd.DataFrame(mplus_json[key])
        if key not in blacklist_attr:
            res = df.to_json(orient="split")
            parsed_df = loads(res)
            dfjson = dumps(parsed_df, indent=4)
            df_list.append(dfjson)
            df.to_csv(f'WC_DA/testdata/raw_{key}.csv')
            

    return df_list


# Calls the Blizzard Achievements endpoint 
# @return ; nil; pandas.DataFrame
def getAchievements(namespace, access_token):

    headers = {
        "Battlenet-Namespace": namespace,
        "Authorization": f"Bearer {access_token}",
    }
    endpoint = ''

    return 0 

# === FastAPI Endpoints ===


@app.get("/")
async def root():
    return {"status": "API is running"}


@app.get("/static_mythicplus")
async def get_staticmythicplus():
    try:
        hostname = "https://us.api.blizzard.com/"
        envs = initialize_environmentals()
        client_id = envs[0]
        key = envs[1]

        resp = grab_OAUTH_cred(client_id, key)
        access_token = resp.json()['access_token']

        print(f"!OAUTH Credentials Obtained")

        return get_mythicplus(hostname, access_token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/dynamic_mythicplus/{realm}/{name}")
async def get_dynamicmythicplus(realm, name):
    try:
        hostname = "https://us.api.blizzard.com/"
        envs = initialize_environmentals()
        client_id = envs[0]
        key = envs[1]

        resp = grab_OAUTH_cred(client_id, key)
        access_token = resp.json()['access_token']
        
        return get_mythicplus(hostname, access_token, realm, name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
