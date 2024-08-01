from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Base directory of the application
MEDIA_DIR = BASE_DIR / "media"  # Base media directory
SONG_DIR = MEDIA_DIR / "songs"  # Directory for songs

# Ensure MEDIA_DIR and SONG_DIR exist
MEDIA_DIR.mkdir(parents=True, exist_ok=True)
SONG_DIR.mkdir(parents=True, exist_ok=True)

class Directory:
    BASE_DIR = BASE_DIR
    MEDIA_DIR = MEDIA_DIR
    SONG_DIR = SONG_DIR
