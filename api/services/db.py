import datetime

from fastapi import HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from api.constants.songs import Status
from api.models.models import Song


def store_song_in_db(db: Session, metadata: dict) -> Song:
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
            thumbnail_url=metadata["thumbnail_url"]
        )
        db.add(db_song)
        db.commit()
        db.refresh(db_song)
    return db_song


def update_song_status(db: Session, song_id: str, status: str) -> dict:
    # Find the song by ID
    db_song = db.query(Song).filter(Song.id == song_id).first()

    # If the song doesn't exist, raise an exception
    if not db_song:
        raise HTTPException(status_code=404, detail="Song not found")

    # Update the status
    db_song.status = status
    db.commit()
    db.refresh(db_song)

    return {"song_id": song_id, "status": status}


def update_song_status_bulk(db: Session, song_ids: list[str], status: str) -> None:
    db.query(Song).filter(Song.id.in_(song_ids)).update({Song.status: status}, synchronize_session=False)
    db.commit()


def get_undownloaded_songs(db: Session) -> list[Song]:
    current_time = datetime.datetime.now(tz=datetime.timezone.utc)
    return db.query(Song).filter(
        and_(
            Song.status != Status.COMPLETED,
            or_(
                Song.status == Status.NOT_STARTED,
                Song.next_check_time is not None,
                Song.next_check_time < current_time
            )
        )
    ).all()


def update_next_check_time(db: Session, song_id: str, next_check_time: datetime.datetime) -> None:
    song = db.query(Song).filter(Song.id == song_id).first()
    if song:
        song.next_check_time = next_check_time
        db.commit()
        db.refresh(song)
