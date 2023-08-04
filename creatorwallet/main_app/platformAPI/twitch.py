
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

    validateRequest = requests.get(f'https://api.twitch.tv/helix/videos?user_id={user_id}&broadcastType=null', 
            headers = {
                'Client-ID' : client_id, 
                'Authorization' : 'Bearer ' + app_token})
    print ( validateRequest.json()['data'][0]  )
    context = {
        'total': total,
        'title': validateRequest.json()['data'][0]['title'],
        'view_count': validateRequest.json()['data'][0]['view_count'],
        'thumbnail_url': validateRequest.json()['data'][0]['thumbnail_url'],
        'url': validateRequest.json()['data'][0]['url'],
        'duration': validateRequest.json()['data'][0]['duration'],
    }
    return [context]