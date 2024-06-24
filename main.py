import yandex_music
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify
SPOTIPY_CLIENT_ID = '...'
SPOTIPY_CLIENT_SECRET = '...'
SPOTIPY_REDIRECT_URI = '...'
SPOTIPY_ACCESS_TOKEN = '...'
SPOTIPY_REFRESH_TOKEN = '...'

# Yandex Music
# You need to get your own Yandex Music OAuth token, visit https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d
# and copy the token from the URL (you need to do this fast)
# also, visit https://yandex-music.readthedocs.io/en/main/index.html for more information
YANDEX_OAUTH_TOKEN = '...'

# Авторизация в Яндекс Музыке
client = yandex_music.Client(YANDEX_OAUTH_TOKEN).init()

# Получение всех треков пользователя из Яндекс Музыки
likes_tracks = client.users_likes_tracks()
track_ids = [track.id for track in likes_tracks]
print(f"Total tracks: {len(track_ids)}")

# Авторизация в Spotify
sp = spotipy.Spotify(auth=SPOTIPY_ACCESS_TOKEN)

# Обновление токена при необходимости
sp.auth_manager = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                               client_secret=SPOTIPY_CLIENT_SECRET,
                               redirect_uri=SPOTIPY_REDIRECT_URI,
                               scope="playlist-modify-private playlist-modify-public",
                               cache_path=".cache")

# Создание плейлиста в Spotify
playlist_name = "My Yandex Music Tracks"
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user_id, playlist_name, public=False)

# Поиск и добавление треков в плейлист Spotify
for track_id in track_ids:
    track = client.tracks(track_id)[0]
    print(f"Track ID: {track_id}, Track Title: {track.title}, Artists: {track.artists}")
    if track and track.title and track.artists:
        search_query = f"{track.title} {track.artists[0].name}"
        search_result = sp.search(q=search_query, limit=1, type='track')
        if search_result['tracks']['items']:
            spotify_track_id = search_result['tracks']['items'][0]['id']
            sp.playlist_add_items(playlist['id'], [spotify_track_id])
            print(f"Added to playlist: {search_query}")

print("Треки успешно перенесены!")
