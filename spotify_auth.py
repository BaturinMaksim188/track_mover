import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify
# You need to get your own Spotify API keys, create an app on Spotify Developer Dashboard
SPOTIPY_CLIENT_ID = '...'
SPOTIPY_CLIENT_SECRET = '...'
SPOTIPY_REDIRECT_URI = '...'

scope = "playlist-modify-private playlist-modify-public"
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=scope)

auth_url = sp_oauth.get_authorize_url()
print(f"Go to the following URL for Spotify authorization: {auth_url}")

# Enter the URL you were redirected to
redirected_url = input("Enter the URL you were redirected to: ")
code = sp_oauth.parse_response_code(redirected_url)
token_info = sp_oauth.get_access_token(code)

print("Access token:", token_info['access_token'])
print("Refresh token:", token_info['refresh_token'])