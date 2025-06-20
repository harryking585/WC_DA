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

    try:
        response = r.post(
            'https://oauth.battle.net/token',
            data=data,
            auth=(client_id, key),
        )
    except:
        print("Error has occurred: Unable to grab OAUTH token from battle.net. Ensure your Client ID and Secret are correct and still active.")

    return response


# def test_get_call(hostname, access_token):
#     headers = {
#         'Authorization':f'Bearer {access_token}'
#     }
#     response = r.get(
#         hostname,
#         headers=headers

#     )

#     return response

def get_mythicplus(hostname, access_token):
    namespace = "profile-us"
    realm = "emerald-dream"
    char_name = "vathren"
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
        print(f'Error has occurred: Unable to receive response from {hostname}profile/wow/character/{realm}/{char_name}/mythic-keystone-profile')
        return 0
    
    # Grabbing hostname for most recent participated mythic+ season
    char_seasons = response.json()['seasons']
    played_seasons = []
    for x in char_seasons:
        played_seasons.append(x['id'])
    current_season = max(played_seasons)
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
        print(f'Error has occurred: Unable to receive response from {hostname}profile/wow/character/{realm}/{char_name}/mythic-keystone-profile')
        return 0
    
    
    mplus_json = response.json()
    bestrun_df = pd.DataFrame(mplus_json['best_runs'])
    os.makedirs('WC_DA/testdata', exist_ok=True)
    bestrun_df.to_csv('WC_DA/testdata/raw_bestruns.csv')

    '''
        Multiple attributes we can decide to build tables for...
            i) All best runs per current weekly affix (IE if affix is void soaks we display all dungeon data where affix = void soaks. {IGNORE FORT AND TYRAN AS BOTH APPLY WITHIN +12})
                - AFter further consideration there is not affix except fort and tyran in +12 and above keys so this would be useless for players who play above this threshhold
            ii) Best runs per each dungeon (Say we have Darkflame cleft, display all of our top 10 runs and data associated for those runs)
            iii) Cross-Seasonal Data Analysis: We can look at the improvements and stack the data against each other for each season the player has ran Mythic+. !!! =< Like uper cool idea
            iv) 
    '''

    return 0


def main():
    print("****** Starting MAIN ******")
    hostname = "https://us.api.blizzard.com/"
    # append = "data/wow/achievement/index?namespace=static-us&locale=en_US"
    # hostname += append

    envs = initialize_enviromentals()
    client_id = envs[0]
    key = envs[1]

    resp = grab_OAUTH_cred(client_id, key)
    access_token = resp.json()['access_token']

    print(f"!OAUTH Credentials Obtained")

    get_mythicplus(hostname, access_token)
    print("****** Ending MAIN ******")

    


if __name__ =="__main__":
    main()
