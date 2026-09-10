"""Engine receipts, rooms, bus, and stub refuses."""

from __future__ import annotations

from azchat.engine import (
    LIVE_OPS,
    STUB_OPS,
    bus_poll,
    bus_send,
    dispatch,
    doctor,
    handle_new,
    handle_rotate,
    health,
    import_export,
    reset_azchat_store,
    room_open,
    room_post,
    room_pull,
    verify_receipt,
)


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


def test_stubs_refuse() -> None:
    for op in STUB_OPS:
        out = dispatch(op, {})
        assert out["ok"] is False
        assert out["code"] == "AZC-CHAT-REFUSE"
        assert out["stub"] is True
        assert out["azmail_bridge"] is False
