from fastapi import Request
from sqlalchemy.orm import Session

from api.models.models import Song


def store_song_in_db(db: Session, metadata: dict, request: Request) -> Song:
    db_song = db.query(Song).filter(Song.url == metadata["url"]).first()
    if not db_song:
        db_song = Song(
            id=metadata["id"],
            name=metadata["name"],
            artists=", ".join(metadata["artists"]),
            album=metadata["album"],
            release_date=metadata["release_date"],
            duration=metadata["duration"],
            url=metadata["url"],
            thumbnail_url=metadata["thumbnail_url"],
            download_url=str(request.url_for("get_song", song_id=metadata["id"]))
        )
        db.add(db_song)
        db.commit()
        db.refresh(db_song)
    return db_song
