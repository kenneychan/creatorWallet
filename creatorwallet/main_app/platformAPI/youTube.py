
import os
import environ
from googleapiclient.discovery import build

environ.Env()
environ.Env.read_env()

def youTubeStats(user):
    api_key = os.environ['YOUTUBE_API_KEY']
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)
    MAX_RESULTS = 10

    resp = youtube.search().list(
        q = user,
        part = 'id',
        type = 'channel',
        fields = 'items(id(kind,channelId))',
        maxResults = MAX_RESULTS
    ).execute()

    items = resp['items']
    assert len(items) <= MAX_RESULTS

    ch = []
    for item in items:
        assert item['id']['kind'] == 'youtube#channel'
        ch.append(item['id']['channelId'])

    if not len(ch):
        return print ('No channels found.')

    print ('ch', ch)

    id = ch[0]

    request_yt = youtube.channels().list(
        part="statistics",
        id=id
    )
    response = request_yt.execute()
    statistics = response['items'][0]['statistics']
    print(statistics)

    context = {
        'view_count': statistics['viewCount'],
        'subscriber_count': statistics['subscriberCount'],
        'video_count': statistics['videoCount']
    }

    return statistics
    