#!python

import sys
import json

from ytmusicapi import YTMusic

ytmusic = YTMusic('headers_auth.json')
print(ytmusic.auth)

try:
    # playlistId = ytmusic.create_playlist("Hôtel Costes", "Lounge electronica playlist")
    # search_results = ytmusic.search(query="Costes", filter='uploads', limit=250, ignore_spelling=False) # 'songs', 'videos', 'albums', 'artists', 'playlists', 'uploads'

    # playlistId = ytmusic.create_playlist("Café del Mar", "Chillout playlist")

    # playlistId = ytmusic.create_playlist("Chill", "Lounge electronica playlist")
    # search_results = ytmusic.search(query="chill", filter='uploads', limit=250, ignore_spelling=False) # 'songs', 'videos', 'albums', 'artists', 'playlists', 'uploads'

    # playlistId = ytmusic.create_playlist("Hed Kandi", "Hed Kandi playlist")
    # search_results = ytmusic.search(query="kandi", filter='uploads', limit=250, ignore_spelling=False) # 'songs', 'videos', 'albums', 'artists', 'playlists', 'uploads'

    # playlistId = ytmusic.create_playlist("Chilled + Distilled", "Chilled + Distilled playlist")
    # print(playlistId)
    # search_results = ytmusic.search(query="chilled", filter='uploads', limit=250, ignore_spelling=False) # 'songs', 'videos', 'albums', 'artists', 'playlists', 'uploads'

    # playlistId = ytmusic.create_playlist("Lounge", "Lounge playlist")
    # print(playlistId)
    # search_results = ytmusic.search(query="lounge", filter='uploads', limit=250, ignore_spelling=False)  # 'songs', 'videos', 'albums', 'artists', 'playlists', 'uploads'

    playlistId = ytmusic.create_playlist("José Padilla", "DJ playlist")
    # print(playlistId)
    search_results = ytmusic.search(query="padilla", filter='uploads', limit=20, ignore_spelling=False)  # 'songs', 'videos', 'albums', 'artists', 'playlists', 'uploads'
except Exception as e:
    # print(search_results)
    sys.exit(e)

playlist = []
print(search_results)
for result in search_results:

    try:
        if result['resultType'] == 'playlist':
            print('[{}] {} {} {}'.format(result['browseId'], result['resultType'], result['title'], result['author']))
        elif result['resultType'] == 'song':
            print('[{}] {} {} {} {}'.format(result['videoId'], result['resultType'], result['title'], result.get('album'), result.get('artists', result['artist'])))
        elif result['resultType'] == 'artist':
            print('[{}] {} {}'.format(result['browseId'], result['resultType'], result.get('artist', 'none')))
        elif result['resultType'] == 'album':
            print('[{}] {} {}'.format(result['browseId'], result['resultType'], result['title'], result['artist']))
        elif result['resultType'] == 'video':
            print('[{}] {} {}'.format(result['videoId'], result['resultType'], result['title'], result['artists']))
    except Exception as e:
        print(json.dumps(result, indent=2))
        sys.exit(e)

    if result['resultType'] == 'song':
        playlist.append(result['videoId'])

print(len(playlist))

# print(search_results)
response = ytmusic.add_playlist_items(playlistId, playlist)
print(response)



