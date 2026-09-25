"""Client-held session file for the local CLI and loopback UI.

Hosted import/export stays unstored. This file lives on the person's computer.
Author: Aziel Eliab only.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from azchat.engine import room_sealed, session_restore, session_snapshot

_DISABLED = {"-", "off", "none"}


def session_path() -> Path | None:
    raw = os.environ.get("AZCHAT_STATE")
    if raw is not None and raw.strip().lower() in _DISABLED:
        return None
    if raw is not None and raw.strip():
        return Path(raw).expanduser()
    return Path.home() / ".local" / "state" / "azchat" / "state.json"


def load_session() -> str | None:
    path = session_path()
    if path is None or not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return f"Could not read the session file at {path}. Move it aside, then try again."
    if not isinstance(data, dict):
        return f"Could not read the session file at {path}. Move it aside, then try again."
    session_restore(data)
    return None


def save_session() -> None:
    path = session_path()
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(session_snapshot(), indent=2, ensure_ascii=True) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    tmp.replace(path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def session_view() -> dict[str, Any]:
    snap = session_snapshot()
    handles: list[dict[str, Any]] = []
    for token, row in snap["handles"].items():
        if isinstance(row, dict) and row.get("live") is True:
            handles.append(
                {
                    "token": token,
                    "label": row.get("label"),
                    "id": row.get("id"),
                    "live": True,
                }
            )
    rooms: list[dict[str, Any]] = []
    for room in snap["rooms"].values():
        if not isinstance(room, dict):
            continue
        rooms.append(
            {
                "id": room.get("id"),
                "sealed": room_sealed(room) if room.get("expires_at") is not None else bool(room.get("sealed")),
            }
        )
    path = session_path()
    return {
        "ok": True,
        "op": "session",
        "handles": handles,
        "rooms": rooms,
        "session_file": str(path) if path else "",
    }
