"""Engine receipts, rooms, bus, and stub refuses."""

from __future__ import annotations

import json

from azchat.engine import (
    LIVE_OPS,
    STUB_OPS,
    _store,
    bus_poll,
    bus_send,
    dispatch,
    doctor,
    handle_new,
    handle_rotate,
    health,
    import_export,
    reset_azchat_store,
    room_host,
    room_join,
    room_list,
    room_open,
    room_post,
    room_pull,
    verify_receipt,
)

SECRET = "correct-horse-battery-staple"


def setup_function() -> None:
    reset_azchat_store()


def test_health_and_doctor_live() -> None:
    h = health()
    d = doctor()
    assert h["ok"] is True
    assert h["slug"] == "azchat"
    assert h["spec"] == "AZC-CHAT-0.1"
    assert h["mesh_enabled_default"] is False
    assert h["azmail_bridge"] is False
    assert h["smtp"] is False
    assert d["fraggate_live"] is True
    assert d["identity"] == "Aziel Eliab only"
    for op in LIVE_OPS:
        assert op in h["live_ops"]
        assert op in d["live_ops"]


def test_handles_rooms_and_stranger_404() -> None:
    a = handle_new({"label": "agent-a"})
    b = handle_new({"label": "agent-b"})
    stranger = handle_new({"label": "stranger"})
    room = room_open({"token_a": a["token"], "token_b": b["token"]})
    assert room["ok"] is True
    posted = room_post({"token": a["token"], "room_id": room["room_id"], "text": "handles spend"})
    assert posted["ok"] is True
    pulled = room_pull({"token": b["token"], "room_id": room["room_id"]})
    assert pulled["ok"] is True
    assert pulled["posts"][0]["text"] == "handles spend"
    deny = room_pull({"token": stranger["token"], "room_id": room["room_id"]})
    assert deny["ok"] is False
    assert deny["status"] == 404
    assert deny["error"] == "stranger-or-missing"


def test_rotate_unlinks_prior_token() -> None:
    a = handle_new({"label": "agent-a"})
    rotated = handle_rotate({"token": a["token"]})
    assert rotated["ok"] is True
    again = handle_rotate({"token": a["token"]})
    assert again["ok"] is False
    assert again["error"] == "handle-unlinked"


def test_bus_send_poll_not_azmail() -> None:
    sent = bus_send({"from": "agent-a", "to": "agent-b", "text": "poll the bus"})
    assert sent["ok"] is True
    assert sent["azmail_bridge"] is False
    polled = bus_poll({"agent": "agent-b"})
    assert polled["count"] == 1
    assert polled["frames"][0]["text"] == "poll the bus"


def test_verify_receipt_hash() -> None:
    minted = handle_new({"label": "agent-a"})
    rec = minted["receipt"]
    ok = verify_receipt({"receipt": rec})
    assert ok["ok"] is True
    assert ok["match"] is True
    broken = dict(rec)
    broken["receipt_sha256"] = "0" * 64
    bad = verify_receipt({"receipt": broken})
    assert bad["match"] is False


def test_import_export_client_held() -> None:
    handle_new({"label": "a"})
    out = import_export({"mode": "export"})
    assert out["stored"] is False
    assert len(out["handles_live"]) == 1
    incoming = import_export({"mode": "import"})
    assert incoming["accepted"] is True
    assert incoming["stored"] is False


def _blob(payload: dict) -> str:
    return json.dumps(payload)


def test_host_appears_on_all_rooms_list_and_join() -> None:
    host = handle_new({"label": "host"})
    guest = handle_new({"label": "guest"})
    hosted = room_host({"token": host["token"], "title": "hall", "private": False})
    assert hosted["ok"] is True
    assert hosted["listed"] is True
    assert hosted["private"] is False
    assert hosted["e2e"] is False
    assert SECRET not in _blob(hosted)
    listed = room_list({})
    assert listed["count"] == 1
    card = listed["rooms"][0]
    assert card["room_id"] == hosted["room_id"]
    assert card["title"] == "hall"
    assert card["private"] is False
    assert card["entry"] == "open"
    assert "passphrase_hash" not in card
    assert "passphrase_salt" not in card
    before = room_pull({"token": guest["token"], "room_id": hosted["room_id"]})
    assert before["status"] == 404
    joined = room_join({"token": guest["token"], "room_id": hosted["room_id"]})
    assert joined["ok"] is True
    assert joined["joined"] is True
    posted = room_post({"token": guest["token"], "room_id": hosted["room_id"], "text": "joined from the list"})
    assert posted["ok"] is True
    pulled = room_pull({"token": host["token"], "room_id": hosted["room_id"]})
    assert pulled["posts"][0]["text"] == "joined from the list"


def test_pairwise_room_stays_off_the_list() -> None:
    a = handle_new({"label": "agent-a"})
    b = handle_new({"label": "agent-b"})
    stranger = handle_new({"label": "stranger"})
    room = room_open({"token_a": a["token"], "token_b": b["token"]})
    listed = room_list({})
    assert listed["count"] == 0
    assert listed["rooms"] == []
    denied = room_join({"token": stranger["token"], "room_id": room["room_id"]})
    assert denied["ok"] is False
    assert denied["status"] == 404
    assert denied["error"] == "room-missing"
    still = room_pull({"token": stranger["token"], "room_id": room["room_id"]})
    assert still["status"] == 404


def test_private_room_passphrase_fails_closed() -> None:
    host = handle_new({"label": "host"})
    guest = handle_new({"label": "guest"})
    missing_secret = room_host({"token": host["token"], "title": "quiet", "private": True})
    assert missing_secret["ok"] is False
    assert missing_secret["error"] == "passphrase-required"
    assert room_list({})["count"] == 0
    dropped = room_host({"token": host["token"], "title": "quiet", "passphrase": SECRET})
    assert dropped["ok"] is False
    assert dropped["error"] == "private-flag-required"
    assert room_list({})["count"] == 0
    blank = room_host({"token": host["token"], "title": "quiet", "private": True, "passphrase": "   "})
    assert blank["error"] == "passphrase-required"
    too_long = room_host({"token": host["token"], "title": "quiet", "private": True, "passphrase": "x" * 129})
    assert too_long["error"] == "passphrase-too-long"
    assert room_list({})["count"] == 0

    hosted = room_host({"token": host["token"], "title": "quiet", "private": True, "passphrase": SECRET})
    stored = _store["rooms"][hosted["room_id"]]
    assert stored["passphrase_hash"] != SECRET
    assert stored["passphrase_salt"]
    assert "passphrase" not in stored
    assert hosted["ok"] is True
    assert hosted["private"] is True
    assert hosted["e2e"] is False
    assert SECRET not in _blob(hosted)
    assert "passphrase_hash" not in _blob(hosted)
    assert "passphrase_salt" not in _blob(hosted)
    listed = room_list({"passphrase": SECRET})
    blob = _blob(listed)
    assert SECRET not in blob
    assert "passphrase_hash" not in blob
    assert "passphrase_salt" not in blob
    card = listed["rooms"][0]
    assert card["private"] is True
    assert card["passphrase_required"] is True
    assert card["entry"] == "passphrase"
    assert card["e2e"] is False

    no_pass = room_join({"token": guest["token"], "room_id": hosted["room_id"]})
    assert no_pass["ok"] is False
    assert no_pass["status"] == 403
    assert no_pass["error"] == "passphrase-required"
    assert SECRET not in _blob(no_pass)
    wrong = room_join({"token": guest["token"], "room_id": hosted["room_id"], "passphrase": "not-the-passphrase"})
    assert wrong["ok"] is False
    assert wrong["status"] == 403
    assert wrong["error"] == "passphrase-rejected"
    assert "not-the-passphrase" not in _blob(wrong)
    stranger = room_pull({"token": guest["token"], "room_id": hosted["room_id"]})
    assert stranger["status"] == 404
    assert room_post({"token": guest["token"], "room_id": hosted["room_id"], "text": "no"})["status"] == 404

    joined = room_join({"token": guest["token"], "room_id": hosted["room_id"], "passphrase": SECRET})
    assert joined["ok"] is True
    assert joined["joined"] is True
    assert SECRET not in _blob(joined)
    assert room_post({"token": guest["token"], "room_id": hosted["room_id"], "text": "inside"})["ok"] is True
    again = room_join({"token": host["token"], "room_id": hosted["room_id"]})
    assert again["ok"] is True
    assert again["already_member"] is True

    exported = import_export({"mode": "export"})
    export_blob = _blob(exported)
    assert SECRET not in export_blob
    assert "passphrase_hash" not in export_blob
    assert "passphrase_salt" not in export_blob
    for row in exported["rooms"]:
        assert "passphrase" not in row
        assert set(row) <= {"id", "members", "sealed", "listed", "private", "title"}


def test_sealed_hosted_room_refuses_join() -> None:
    host = handle_new({"label": "host"})
    guest = handle_new({"label": "guest"})
    hosted = room_host({"token": host["token"], "title": "old"})
    _store["rooms"][hosted["room_id"]]["expires_at"] = 0
    denied = room_join({"token": guest["token"], "room_id": hosted["room_id"]})
    assert denied["ok"] is False
    assert denied["status"] == 410
    assert denied["error"] == "room-sealed"
    assert room_pull({"token": guest["token"], "room_id": hosted["room_id"]})["status"] == 404


def test_stubs_refuse() -> None:
    for op in STUB_OPS:
        out = dispatch(op, {})
        assert out["ok"] is False
        assert out["code"] == "AZC-CHAT-REFUSE"
        assert out["stub"] is True
        assert out["azmail_bridge"] is False
