"""AZChat — spendable handles, ephemeral rooms, agent bus (AZC-CHAT-0.1).

Mesh hop default off. Not SMTP. Not AZMail. FragGate only.
Author: Aziel Eliab only.
"""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "Aziel Eliab"
SPEC = "AZC-CHAT-0.1"
SLUG = "azchat"
PRODUCT = "azchat"

from azchat.engine import (  # noqa: E402
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
    room_open,
    room_post,
    room_pull,
    verify_receipt,
)

__all__ = [
    "LIVE_OPS",
    "PRODUCT",
    "SLUG",
    "SPEC",
    "STUB_OPS",
    "__author__",
    "__version__",
    "bus_poll",
    "bus_send",
    "dispatch",
    "doctor",
    "handle_new",
    "handle_rotate",
    "health",
    "import_export",
    "room_open",
    "room_post",
    "room_pull",
    "verify_receipt",
]
