"""Mint two handles, open a room, post, pull. Author: Aziel Eliab only."""

from azchat.engine import handle_new, reset_azchat_store, room_open, room_post, room_pull

if __name__ == "__main__":
    reset_azchat_store()
    a = handle_new({"label": "agent-a"})
    b = handle_new({"label": "agent-b"})
    room = room_open({"token_a": a["token"], "token_b": b["token"]})
    posted = room_post({"token": a["token"], "room_id": room["room_id"], "text": "handles spend"})
    pulled = room_pull({"token": b["token"], "room_id": room["room_id"]})
    print(room["room_id"], posted["post"]["id"], len(pulled["posts"]))
