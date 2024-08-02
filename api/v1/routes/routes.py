from fastapi import APIRouter

import api.v1.controllers.songs as SongController  # noqa: N812

router = APIRouter()

# /api/v1 -> GET
router.get("/")(SongController.root)

# /api/v1/songs -> GET
router.get("/songs")(SongController.get_all_songs_info)

# /api/v1/songs/add -> POST
router.post("/songs/add")(SongController.add_songs)

# /api/v1/song/add -> POST
router.post("/song/add")(SongController.add_song)

# /api/v1/song/{song_id} -> GET
router.get("/song/{song_id}")(SongController.get_song_info)
