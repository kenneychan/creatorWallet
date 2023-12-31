
import os
import environ
import requests
import json

environ.Env()
environ.Env.read_env()

def twitchStats(user):
    client_id = os.environ['TWITCH_CLIENT_ID']
    app_token = os.environ['TWITCH_APP_TOKEN']

    validateRequest = requests.get(f'https://api.twitch.tv/helix/users?login={user}', 
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
    # print ( validateRequest.json()['data'][0]  )
    context = {
        'stats': {
            'total followers': total,
        },
        'latest_stream' : {
            'title': validateRequest.json()['data'][0]['title'],
            'views': validateRequest.json()['data'][0]['view_count'],
            'thumbnail': (validateRequest.json()['data'][0]['thumbnail_url']).replace("%{width}","640").replace("%{height}","360"),
            'url': validateRequest.json()['data'][0]['url'],
            'duration': validateRequest.json()['data'][0]['duration'],
        }
    }
    return [context]