"""AZChat engine — spendable handles, ephemeral rooms, agent bus.

Mesh hop default OFF. Not SMTP. Not AZMail. Do not bridge.
True engine remains in-process on aziel-runtime FragGate slug `azchat`.
This module is the local / isolate-hash mirror.

Author: Aziel Eliab only. Identity is Aziel Eliab only.
"""

from __future__ import annotations

import hashlib
import json
import secrets
import time
from typing import Any

from azchat.errors import RefuseError

PRODUCT = "azchat"
SLUG = "azchat"
NAME = "AZChat"
VERSION = "0.1.0"
SPEC = "AZC-CHAT-0.1"
AUTHOR = "Aziel Eliab"
ROLE = "spendable-handle rooms + agent bus"
MOTTO = "Handles spend. Rooms seal. Mesh stays off."
CLASS = "Plain"
DOMAIN = "Comms"
AXES = ("handle", "room", "bus", "receipt")
NEIGHBORS = ("azmail (not bridged)", "aznet", "peacelock")
MESH_ENABLED_DEFAULT = False
ROOM_TTL_DEFAULT_MS = 15 * 60 * 1000
ROOM_TTL_MAX_MS = 60 * 60 * 1000
TEXT_CAP = 2000
FRAME_CAP = 64

LIVE_OPS = (
    "health",
    "skill",
    "doctor",
    "handle_new",
    "handle_rotate",
    "room_open",
    "room_post",
    "room_pull",
    "bus_send",
    "bus_poll",
    "verify_receipt",
    "import_export",
)

STUB_OPS = (
    "smtp",
    "smtp_send",
    "send",
    "mail",
    "deliver",
    "deanonymize",
    "harvest",
    "mesh_join",
    "mesh_enable",
    "vpn",
    "bridge_azmail",
    "bridge",
    "chromium",
)

LIMITATION = (
    "THIS IS: AZChat spendable handles, ephemeral rooms (TTL/sealed), and an agent bus. "
    "Reached only through FragGate. mesh_enabled_default is false. "
    "THIS IS NOT: SMTP, a public MTA, AZMail, a mesh hop, deanonymize, or a Chromium chat runner. "
    "Do not bridge AZChat ↔ AZMail. Stranger room_pull is 404. Author: Aziel Eliab only."
)
HONEST = LIMITATION

STUB_MESSAGES = {
    "smtp": "AZC-CHAT-REFUSE: SMTP is stub. AZChat is not a mailer.",
    "smtp_send": "AZC-CHAT-REFUSE: smtp_send is stub. Not an MTA.",
    "send": "AZC-CHAT-REFUSE: send is stub. Use room_post or bus_send.",
    "mail": "AZC-CHAT-REFUSE: mail is stub. Do not bridge AZChat ↔ AZMail.",
    "deliver": "AZC-CHAT-REFUSE: deliver is stub. Not a public MTA.",
    "deanonymize": "AZC-CHAT-REFUSE: deanonymize is stub.",
    "harvest": "AZC-CHAT-REFUSE: harvest is stub.",
    "mesh_join": "AZC-CHAT-REFUSE: product-local mesh_join is stub. Suite mesh is /v1/mesh/* PROXY. GET never enables.",
    "mesh_enable": "AZC-CHAT-REFUSE: product-local mesh_enable is stub. GET /v1/mesh never enables. Default OFF.",
    "vpn": "AZC-CHAT-REFUSE: vpn is stub. Not a hop mesh.",
    "bridge_azmail": "AZC-CHAT-REFUSE: do not bridge AZChat ↔ AZMail.",
    "bridge": "AZC-CHAT-REFUSE: bridge is stub. Not AZMail.",
    "chromium": "AZC-CHAT-REFUSE: chromium is stub. Not a Chromium chat runner.",
}

_store: dict[str, Any] = {
    "handles": {},
    "rooms": {},
    "bus": [],
    "seq": 0,
}


def reset_azchat_store() -> None:
    _store["handles"] = {}
    _store["rooms"] = {}
    _store["bus"] = []
    _store["seq"] = 0


def session_snapshot() -> dict[str, Any]:
    return {
        "handles": _store["handles"],
        "rooms": _store["rooms"],
        "bus": _store["bus"],
        "seq": _store["seq"],
    }


def session_restore(data: dict[str, Any]) -> None:
    handles = data.get("handles")
    rooms = data.get("rooms")
    bus = data.get("bus")
    _store["handles"] = dict(handles) if isinstance(handles, dict) else {}
    _store["rooms"] = dict(rooms) if isinstance(rooms, dict) else {}
    _store["bus"] = list(bus) if isinstance(bus, list) else []
    try:
        _store["seq"] = int(data.get("seq") or 0)
    except (TypeError, ValueError):
        _store["seq"] = 0


def now_ms() -> int:
    return int(time.time() * 1000)


def now_iso(ms: int | None = None) -> str:
    stamp = (ms if ms is not None else now_ms()) / 1000.0
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(stamp))


def clip(raw: Any, cap: int = TEXT_CAP) -> str:
    return str("" if raw is None else raw)[:cap]


def next_id(prefix: str) -> str:
    _store["seq"] += 1
    return f"{prefix}_{_store['seq']:x}_{now_ms():x}"


def token_bytes() -> str:
    return secrets.token_hex(18)


def sha256_hex(text: str) -> str:
    return hashlib.sha256(str(text).encode("utf-8")).hexdigest()


def _canonical(obj: Any) -> str:
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=True, sort_keys=False)


def base_fields() -> dict[str, Any]:
    return {
        "product": PRODUCT,
        "name": NAME,
        "slug": SLUG,
        "version": VERSION,
        "spec": SPEC,
        "role": ROLE,
        "motto": MOTTO,
        "axes": list(AXES),
        "neighbors": list(NEIGHBORS),
        "live_ops": list(LIVE_OPS),
        "stub_ops": list(STUB_OPS),
        "true_engine_runtime": False,
        "worker_local": True,
        "catalog_engine": "aziel-runtime",
        "kv_increment": False,
        "door": "fraggate",
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "limitation": LIMITATION,
        "author": AUTHOR,
        "isolate_hash_store": True,
        "object_store": "isolate-hash",
        "cdn": False,
        "azmail_bridge": False,
        "smtp": False,
        "mta": False,
        "public_url": False,
    }


def refuse_stub(op: str) -> dict[str, Any]:
    key = str(op or "").strip().replace("-", "_")
    if key not in STUB_OPS:
        raise RefuseError("unknown stub")
    return {
        "ok": False,
        "status": 403,
        "error": STUB_MESSAGES[key],
        "code": "AZC-CHAT-REFUSE",
        "stub": True,
        "op": key,
        "product": PRODUCT,
        "slug": SLUG,
        "spec": SPEC,
        "version": VERSION,
        "author": AUTHOR,
        "door": "fraggate",
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "azmail_bridge": False,
        "limitation": LIMITATION,
    }


def health(mesh_pointer: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "ok": True,
        "op": "health",
        "status": "ok",
        **base_fields(),
        "mesh": mesh_pointer or {"pointer": True, "enabled_default": False},
        "note": "Hosted /v1 does not increment downloads. True engine is aziel-runtime FragGate slug azchat. This Worker is the human door + counted /download + mesh peer.",
        "honest": HONEST,
    }


def doctor() -> dict[str, Any]:
    return {
        "ok": True,
        "op": "doctor",
        "status": "ok",
        **base_fields(),
        "doctor_note": "AZChat doctor: handles/rooms/bus only. Mesh stays off. Not a mailer. Not AZMail.",
        "identity": "Aziel Eliab only",
        "fraggate_live": True,
        "network": False,
        "invariants": {
            "I1": "Mesh hop default off. GET /v1/mesh never enables.",
            "I2": "Not SMTP. Not a public MTA.",
            "I3": "Not AZMail. Do not bridge.",
            "I4": "Stranger room_pull is 404.",
            "I5": "FragGate is THE single door.",
            "I6": "Identity is Aziel Eliab only.",
        },
        "note": "Doctor is a FragGate LIVE_OPS self-check. No writes. Mesh stays off.",
    }


def skill_markdown() -> str:
    return f"""---
name: AZChat
description: Use when minting spendable handles, opening ephemeral rooms, or polling an agent bus (AZC-CHAT-0.1). Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404. Dual surface: Worker /v1 + POST /mcp, or aziel-runtime FragGate slug azchat. This Worker /v1/fraggate/* and /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. GET /v1/mesh never enables. Product-local mesh_enable is stub/REFUSE. Author Aziel Eliab.
---

# AZChat (AZC-CHAT-0.1)

AZChat: spendable handles, ephemeral rooms, agent bus. Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404.

- MCP: `fraggate_call` with `{{ slug: "azchat", op: "..." }}`
- HTTP: `POST /v1/fraggate/call` with the same envelope
- Leftover flat names such as `azchat_health` still go through FragGate (`parseTarget`) — they are not a side door and are not listed on `tools/list`

LIVE_OPS: health, skill, doctor, handle_new, handle_rotate, room_open, room_post, room_pull, bus_send, bus_poll, verify_receipt, import_export.

Stubs (refuse): smtp, smtp_send, send, mail, deliver, deanonymize, harvest, mesh_join, mesh_enable, vpn, bridge_azmail, bridge, chromium.

Axes / order: handle, room, bus, receipt.
Neighbors: azmail (not bridged), aznet, peacelock.

Author: Aziel Eliab only.
Limitation: {LIMITATION}
"""


def skill_body() -> dict[str, Any]:
    md = skill_markdown()
    return {
        "op": "skill",
        "markdown": md,
        "skill": md,
        "kv_increment": False,
        "limitation": LIMITATION,
        "live_ops": list(LIVE_OPS),
        "stub_ops": list(STUB_OPS),
        "neighbors": list(NEIGHBORS),
        "axes": list(AXES),
        "door": "fraggate",
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "author": AUTHOR,
        "product": PRODUCT,
        "name": NAME,
        "version": VERSION,
        "spec": SPEC,
        "true_engine_runtime": False,
        "worker_local": True,
    }


def lookup_handle(token: Any) -> dict[str, Any] | None:
    key = str(token or "").strip()
    if not key:
        return None
    row = _store["handles"].get(key)
    if not row or row.get("live") is not True:
        return None
    return row


def receipt_of(fields: dict[str, Any]) -> dict[str, Any]:
    body = {**fields, "author": AUTHOR}
    digest = sha256_hex(_canonical(body))
    return {**body, "receipt_sha256": digest}


def handle_new(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    token = token_bytes()
    hid = next_id("h")
    row = {
        "id": hid,
        "token": token,
        "live": True,
        "rotated": False,
        "successor": None,
        "label": clip(src.get("label") or src.get("agent") or "handle", 48),
        "created": now_iso(),
    }
    _store["handles"][token] = row
    receipt = receipt_of({"op": "handle_new", "handle_id": hid, "label": row["label"], "ts": row["created"]})
    return {
        "ok": True,
        "op": "handle_new",
        "handle_id": hid,
        "token": token,
        "label": row["label"],
        "live": True,
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "receipt": receipt,
        "note": "Spendable handle. Rotate unlinks this token. Author: Aziel Eliab.",
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def handle_rotate(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    current = lookup_handle(src.get("token") or src.get("handle_token"))
    if not current:
        return {"ok": False, "status": 404, "error": "handle-unlinked", "op": "handle_rotate"}
    next_token = token_bytes()
    next_id_value = next_id("h")
    current["live"] = False
    current["rotated"] = True
    current["successor"] = next_id_value
    nxt = {
        "id": next_id_value,
        "token": next_token,
        "live": True,
        "rotated": False,
        "successor": None,
        "label": current["label"],
        "created": now_iso(),
        "previous": current["id"],
    }
    _store["handles"][next_token] = nxt
    receipt = receipt_of({"op": "handle_rotate", "from": current["id"], "to": nxt["id"], "ts": nxt["created"]})
    return {
        "ok": True,
        "op": "handle_rotate",
        "handle_id": nxt["id"],
        "token": next_token,
        "unlinked": current["id"],
        "live": True,
        "receipt": receipt,
        "note": "Prior token is unlinked. Rooms still list the old handle id as spent.",
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def room_sealed(room: dict[str, Any], now: int | None = None) -> bool:
    stamp = now if now is not None else now_ms()
    return room.get("sealed") is True or stamp >= int(room["expires_at"])


def room_open(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    a = lookup_handle(src.get("token_a") or src.get("handle_a"))
    b = lookup_handle(src.get("token_b") or src.get("handle_b"))
    if not a or not b:
        return {"ok": False, "status": 404, "error": "handle-unlinked", "op": "room_open"}
    if a["id"] == b["id"]:
        return {"ok": False, "status": 400, "error": "need-two-handles", "op": "room_open"}
    try:
        ttl = int(src.get("ttl_ms") or ROOM_TTL_DEFAULT_MS)
    except (TypeError, ValueError):
        ttl = ROOM_TTL_DEFAULT_MS
    ttl = min(ROOM_TTL_MAX_MS, max(1, ttl))
    opened = now_ms()
    rid = next_id("r")
    room = {
        "id": rid,
        "members": [a["id"], b["id"]],
        "posts": [],
        "opened_at": opened,
        "expires_at": opened + ttl,
        "ttl_ms": ttl,
        "sealed": False,
    }
    _store["rooms"][rid] = room
    receipt = receipt_of({"op": "room_open", "room_id": rid, "members": list(room["members"]), "ttl_ms": ttl})
    return {
        "ok": True,
        "op": "room_open",
        "room_id": rid,
        "members": list(room["members"]),
        "ttl_ms": ttl,
        "expires_at": now_iso(room["expires_at"]),
        "sealed": False,
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "receipt": receipt,
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def room_post(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    handle = lookup_handle(src.get("token") or src.get("handle_token"))
    room = _store["rooms"].get(str(src.get("room_id") or ""))
    if not handle or not room or handle["id"] not in room["members"]:
        return {"ok": False, "status": 404, "error": "stranger-or-missing", "op": "room_post"}
    if room_sealed(room):
        room["sealed"] = True
        return {"ok": False, "status": 410, "error": "room-sealed", "op": "room_post", "room_id": room["id"], "sealed": True}
    text = clip(src["text"] if src.get("text") is not None else src.get("body"))
    if not text:
        return {"ok": False, "status": 400, "error": "empty-post", "op": "room_post"}
    post = {"id": next_id("p"), "from": handle["id"], "text": text, "ts": now_iso()}
    room["posts"].append(post)
    receipt = receipt_of({"op": "room_post", "room_id": room["id"], "post_id": post["id"], "from": handle["id"]})
    return {
        "ok": True,
        "op": "room_post",
        "room_id": room["id"],
        "post": post,
        "receipt": receipt,
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def room_pull(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    handle = lookup_handle(src.get("token") or src.get("handle_token"))
    room = _store["rooms"].get(str(src.get("room_id") or ""))
    if not handle or not room or handle["id"] not in room["members"]:
        return {"ok": False, "status": 404, "error": "stranger-or-missing", "op": "room_pull"}
    if room_sealed(room):
        room["sealed"] = True
    return {
        "ok": True,
        "op": "room_pull",
        "room_id": room["id"],
        "members": list(room["members"]),
        "posts": list(room["posts"]),
        "sealed": room["sealed"],
        "expires_at": now_iso(room["expires_at"]),
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def bus_send(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    frm = clip(src.get("from") or src.get("agent") or "agent", 48)
    to = clip(src.get("to") or src.get("peer") or "", 48)
    text = clip(src["text"] if src.get("text") is not None else src.get("body"))
    if not text:
        return {"ok": False, "status": 400, "error": "empty-frame", "op": "bus_send"}
    frame = {"id": next_id("b"), "from": frm, "to": to, "text": text, "ts": now_iso()}
    _store["bus"].insert(0, frame)
    if len(_store["bus"]) > FRAME_CAP:
        _store["bus"] = _store["bus"][:FRAME_CAP]
    receipt = receipt_of({"op": "bus_send", "frame_id": frame["id"], "from": frm, "to": to})
    return {
        "ok": True,
        "op": "bus_send",
        "frame": frame,
        "receipt": receipt,
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "azmail_bridge": False,
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def bus_poll(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    agent = clip(src.get("agent") or src.get("to") or "", 48)
    try:
        limit = int(src.get("limit") or 16)
    except (TypeError, ValueError):
        limit = 16
    limit = min(32, max(1, limit))
    frames = [f for f in _store["bus"] if (not agent or f["to"] == agent or f["from"] == agent or not f["to"])][:limit]
    return {
        "ok": True,
        "op": "bus_poll",
        "count": len(frames),
        "frames": frames,
        "mesh_enabled_default": MESH_ENABLED_DEFAULT,
        "azmail_bridge": False,
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def verify_receipt(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    receipt = src["receipt"] if isinstance(src.get("receipt"), dict) else src
    rest = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    expect = sha256_hex(_canonical(rest))
    posted = receipt.get("receipt_sha256")
    return {
        "ok": True,
        "op": "verify_receipt",
        "match": bool(posted) and posted == expect,
        "receipt_sha256": expect,
        "posted": posted or None,
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def import_export(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    src = payload if isinstance(payload, dict) else {}
    mode = str(src.get("mode") or "export").lower()
    if mode == "import":
        return {
            "ok": True,
            "op": "import_export",
            "mode": "import",
            "accepted": True,
            "stored": False,
            "note": "Client-held JSON only. Hosted AZChat does not persist an import store.",
            "author": AUTHOR,
            "limitation": LIMITATION,
        }
    return {
        "ok": True,
        "op": "import_export",
        "mode": "export",
        "handles_live": [h["id"] for h in _store["handles"].values() if h.get("live")],
        "rooms": [
            {"id": r["id"], "members": list(r["members"]), "sealed": room_sealed(r)}
            for r in _store["rooms"].values()
        ],
        "bus_count": len(_store["bus"]),
        "stored": False,
        "author": AUTHOR,
        "limitation": LIMITATION,
    }


def dispatch(op: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    name = str(op or "").strip().replace("-", "_")
    if name in STUB_OPS:
        return refuse_stub(name)
    if name == "health":
        return health()
    if name == "doctor":
        return doctor()
    if name == "skill":
        return skill_body()
    if name == "handle_new":
        return handle_new(payload)
    if name == "handle_rotate":
        return handle_rotate(payload)
    if name == "room_open":
        return room_open(payload)
    if name == "room_post":
        return room_post(payload)
    if name == "room_pull":
        return room_pull(payload)
    if name == "bus_send":
        return bus_send(payload)
    if name == "bus_poll":
        return bus_poll(payload)
    if name in ("verify_receipt", "verify"):
        return verify_receipt(payload)
    if name == "import_export":
        return import_export(payload)
    raise RefuseError("unknown op: " + str(op))
