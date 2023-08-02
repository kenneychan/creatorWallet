
import os
import environ
import requests
import json

environ.Env()
environ.Env.read_env()

def twitchStats(user):
    client_id = os.environ['TWITCH_CLIENT_ID']
    app_token = os.environ['TWITCH_APP_TOKEN']

    user_name = 'smacksmackk'

    validateRequest = requests.get(f'https://api.twitch.tv/helix/users?login={user_name}', 
            headers = {
                'Client-ID' : client_id, 
                'Authorization' : 'Bearer ' + app_token})
    user_id = validateRequest.json()['data'][0]['id']

    validateRequest = requests.get(f'https://api.twitch.tv/helix/videos?user_id={user_id}&broadcastType=null', 
            headers = {
                'Client-ID' : client_id, 
                'Authorization' : 'Bearer ' + app_token})
    print ( validateRequest.json()['data'][0:3]  )

    return validateRequest.json()['data'][0:3]