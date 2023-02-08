from bs4 import BeautifulSoup

import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lxml

url="https://www.billboard.com/charts/hot-100/"
date=input("Enter the date you want the playlist for in YYYY-MM-DD format")

complete_url=url+date
response=requests.get(complete_url)
scrap=response.text
soup=BeautifulSoup(scrap,"html.parser")

songsList = soup.select("li ul li h3")
song_names = [song.get_text(strip=True) for song in songsList]
print(song_names)

year = date.split("-")[0]
scope="playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",client_secret="",redirect_uri="https://example.com",scope=scope,show_dialog=True,cache_path="token.txt"))
user_id=sp.current_user()['id']
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
