import datetime
import subprocess
import time
from pathlib import Path

from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.constants.directory import Directory
from api.constants.songs import (
    DOWNLOAD_MAX_RETRIES,
    DOWNLOAD_RETRY_INTERVAL_SEC,
    DOWNLOAD_TIMEOUT_SEC,
    NEXT_CHECK_TIME_INTERVAL_SEC,
    Status,
)
from api.services.db import get_undownloaded_songs, update_next_check_time, update_song_status


def download_song_with_spotdl(song_url: str) -> bool:
    song_file_path = Path(Directory.SONG_DIR) / "{track-id}"
    command = ["spotdl", song_url, "--output", str(song_file_path)]

    retries = DOWNLOAD_MAX_RETRIES
    for attempt in range(retries):
        try:
            subprocess.run(command, check=True, timeout=DOWNLOAD_TIMEOUT_SEC)
        except subprocess.CalledProcessError as e:  # noqa: PERF203
            print(f"Error downloading song {song_url}: {e.stderr.decode()}")
            print(f"Retrying... (attempt {attempt + 1}/{retries})")
            return False
        except Exception as e:
            print(f"An error occurred while downloading {song_url}: {e}")
            time.sleep(DOWNLOAD_RETRY_INTERVAL_SEC)
        else:
            return True
    return False

def process_undownloaded_songs(db: Session) -> JSONResponse:
    undownloaded_songs = get_undownloaded_songs(db)
    if not undownloaded_songs:
        return JSONResponse(content={"message": "No pending songs found."})

    for song in undownloaded_songs:
        update_song_status(db, song.id, Status.PROCESSING)
        update_next_check_time(db, song.id, datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=NEXT_CHECK_TIME_INTERVAL_SEC))
        if download_song_with_spotdl(song.url):
            update_song_status(db, song.id, Status.COMPLETED)
            update_next_check_time(db, song.id, None)
        else:
            update_song_status(db, song.id, Status.FAILED)

    return JSONResponse(content={"message": "Processed pending songs."})
