from fastapi import APIRouter

from api.v1.controllers.songs import add_song, get_song_info, root

router = APIRouter()

# /api/v1 -> GET
router.get("/")(root)

# /api/v1/song/{song_id} -> GET
router.get("/song/{song_id}")(get_song_info)

# /api/v1/add -> POST
router.post("/add")(add_song)
