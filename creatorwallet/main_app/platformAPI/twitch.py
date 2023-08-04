
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

    context = []

    validateRequest = requests.get(f'https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}&broadcastType=null', 
            headers = {
                'Client-ID' : client_id, 
                'Authorization' : 'Bearer ' + app_token})
    total = validateRequest.json()['total']


    }
    return [context]