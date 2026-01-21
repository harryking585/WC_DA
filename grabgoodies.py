import requests as r
import pandas as pd
import os
from pathlib import Path
import json
from json import loads, dumps
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import regex as re
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def end_kvpair_index(strrow, start_index):
    flags = 3 # indx0 = : encountered, indx1 = '1 encountered, indx2 = '2 encountered
    start_index += 7
    while(flags > 0):
        char = strrow[start_index]

        if(flags == 3 and char is ":"):
            flags-=1
        elif(flags <= 2 and char is "'"):
            flags -=1

        start_index += 1
    return start_index



def dfs_dataframe(dataframe):
    keys = list(dataframe.keys())

    for i in keys:
        us_start = 0
        us_stop = 0
        cn_start = 0
        cn_stop = 0
        element_type = type(dataframe[i][0])
        if(element_type is list or element_type is dict):   
            for j in range(0, len(dataframe[i])): 
                strcast_row = str(dataframe[i][j])
                if("'en_US'" in strcast_row):
                    for k in range(0, strcast_row.count("'zh_CN'")):
                        us_start = strcast_row.find("'en_US'")
                        cn_start = strcast_row.find("'zh_CN'")
                        
                        us_stop = end_kvpair_index(strcast_row, us_start)
                        cn_stop = end_kvpair_index(strcast_row, cn_start)
                        
                        strcast_row = strcast_row[0:us_stop] + strcast_row[cn_stop:len(strcast_row)]
                        dataframe[i][j] = str_to_dict(strcast_row)

                else:
                     break
        else:
            continue
            



    return dataframe
    

# Calls the mythic plus blizzard endpoint and formats the dataframe to ideal working state
# @return => dataframe || -1
def get_mythicplus(hostname, access_token, realm="emerald-dream",char_name="vathren"):
    df_list = []
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
    current_season = max(played_seasons)-2
    print(f"\n\nseasons list = {played_seasons}\n\n")
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
            df = dfs_dataframe(df)
            res = df.to_json()
            #parsed_df = loads(res)
            #dfjson = dumps(parsed_df, indent=4)

            #test regex expression
            res = re.find("[^(\\)]")
            #end regex expression
            df_list.append(res)
            df.to_csv(f'WC_DA/testdata/raw_{key}.csv')
            

    return df_list


# Calls the Blizzard Achievements endpoint 
# @return ; nil; pandas.DataFrame
def getAchievements(namespace, access_token):

    headers = {
        "Battlenet-Namespace": namespace,
        "Authorization": f"Bearer {access_token}",
    }
    endpoint = '/achievements'
    
    blacklist_attr=[]
    return 0 

# === FastAPI Endpoints ===

@app.get("/")
async def root():
    return {"status": "API is running"}


@app.get("/bestruns/{realm}/{name}")
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

# returns a list of all available realms
@app.get("/realms")
async def get_realms():
    hostname = "https://us.api.blizzard.com"
    envs = initialize_environmentals()
    client_id = envs[0]
    key = envs[1]

    resp = grab_OAUTH_cred(client_id, key)
    access_token = resp.json()['access_token']
    namespace = "profile-us"
    headers = {
        "Battlenet-Namespace": namespace,
        "Authorization": f"Bearer {access_token}",
    }

    try:
        response = r.get(
            hostname+"/data/wow/realm/index",
            headers
        )
        

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Purely for debugging purposes
# hostname = "https://us.api.blizzard.com/"
# envs = initialize_environmentals()
# client_id = envs[0]
# key = envs[1]
# resp = grab_OAUTH_cred(client_id, key)
# access_token = resp.json()['access_token']

# print(f"!OAUTH Credentials Obtained")

# get_mythicplus(hostname, access_token)


# ******** REALMS API CALL TESTING (SEQUENTIAL) ********
# hostname = "https://us.api.blizzard.com/"
# envs = initialize_environmentals()
# client_id = envs[0]
# key = envs[1]

# resp = grab_OAUTH_cred(client_id, key)
# access_token = resp.json()['access_token']
# namespace = "dynamic-us"
# headers = {
#     "Battlenet-Namespace": namespace,
#     "Authorization": f"Bearer {access_token}",
# }

# try:
#     response = r.get(
#         hostname+"data/wow/realm/index",
#         headers
#     )
        
#     print("complete")
# except Exception as e:
#     raise HTTPException(status_code=500, detail=str(e))