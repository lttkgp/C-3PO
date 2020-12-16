import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from fetch_songs import get_songs


scope="playlist-modify-public"
username="Put your userid"
token = SpotifyOAuth(scope=scope,username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

# create the playlist
playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")
spotifyObject.user_playlist_create(user=username,name=playlist_name,public=True,description=playlist_description)

# fetch spotify uri
songs = get_songs()
list_of_songs =[]
for i in songs:
    result = spotifyObject.search(q=i)
    if(len(result['tracks']['items'])!=0):
        list_of_songs.append(result['tracks']['items'][0]['uri'])

# fetch latest created playlist id
prePlaylist = spotifyObject.current_user_playlists()
playlist = prePlaylist['items'][0]['uri']

# add songs to playlist
spotifyObject.user_playlist_add_tracks(user=username,playlist_id=playlist,tracks=list_of_songs)