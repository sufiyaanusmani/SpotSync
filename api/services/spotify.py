import os
from typing import Any

import spotipy

# Load environment variables
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

# Spotify credentials
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

def get_song_metadata(url: str) -> dict[str, Any]:
    try:
        track_id = url.split("/")[-1].split("?")[0]  # Extract track ID from URL
        track = sp.track(track_id)

        # Extract album images
        album_images = track["album"]["images"]
        thumbnail_url = album_images[0]["url"] if album_images else None

        return {
            "name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "duration": track["duration_ms"] // 1000,
            "url": track["external_urls"]["spotify"],
            "thumbnail_url": thumbnail_url
        }
    except Exception as e:
        return {"error": str(e)}
