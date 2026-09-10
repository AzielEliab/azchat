"""AZChat CLI. Author: Aziel Eliab only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from azchat import __version__
from azchat.engine import (
    HONEST,
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
    skill_markdown,
    verify_receipt,
)
from azchat.errors import AzChatError


def _print(data: Any) -> int:
    sys.stdout.write(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
    return 0 if data.get("ok", True) else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="azchat",
        description="AZChat — spendable handles, ephemeral rooms, agent bus (AZC-CHAT-0.1). Author: Aziel Eliab.",
    )
    p.add_argument("--version", action="version", version=f"azchat {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("health", help="Liveness. FragGate LIVE_OPS.")
    sub.add_parser("doctor", help="Self-check. FragGate LIVE_OPS.")
    sub.add_parser("skill", help="Print skill markdown.")

    hn = sub.add_parser("handle-new", help="Mint a spendable handle.")
    hn.add_argument("--label", default="handle")

    hr = sub.add_parser("handle-rotate", help="Rotate a handle token (unlinks the prior token).")
    hr.add_argument("--token", required=True)

    ro = sub.add_parser("room-open", help="Open an ephemeral room. Needs two live handle tokens.")
    ro.add_argument("--token-a", required=True)
    ro.add_argument("--token-b", required=True)
    ro.add_argument("--ttl-ms", type=int, default=900000)

    rp = sub.add_parser("room-post", help="Post into a room as a member. Stranger is 404.")
    rp.add_argument("--token", required=True)
    rp.add_argument("--room-id", required=True)
    rp.add_argument("--text", required=True)

    rpl = sub.add_parser("room-pull", help="Pull room posts. Stranger room_pull is 404.")
    rpl.add_argument("--token", required=True)
    rpl.add_argument("--room-id", required=True)

    bs = sub.add_parser("bus-send", help="Send an agent-bus frame. Not AZMail.")
    bs.add_argument("--from-agent", dest="from_agent", default="agent-a")
    bs.add_argument("--to", default="agent-b")
    bs.add_argument("--text", required=True)

    bp = sub.add_parser("bus-poll", help="Poll the agent bus.")
    bp.add_argument("--agent", default="")
    bp.add_argument("--limit", type=int, default=16)

    vr = sub.add_parser("verify", help="Verify a receipt hash.")
    vr.add_argument("--receipt", required=True, help="Path to receipt JSON.")

    ie = sub.add_parser("export", help="Client-held export.")
    ie.add_argument("--mode", default="export")

    stub = sub.add_parser("stub", help="Call a refused stub op (expect REFUSE).")
    stub.add_argument("op", choices=list(STUB_OPS))

    ui = sub.add_parser("ui", help="Loopback UI (127.0.0.1 only).")
    ui.add_argument("--host", default="127.0.0.1")
    ui.add_argument("--port", type=int, default=8878)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "health":
            return _print(health())
        if args.cmd == "doctor":
            return _print(doctor())
        if args.cmd == "skill":
            from pathlib import Path

            skill = Path(__file__).resolve().parents[1] / "SKILL.md"
            if skill.exists():
                sys.stdout.write(skill.read_text(encoding="utf-8"))
            else:
                sys.stdout.write(skill_markdown())
            return 0
        if args.cmd == "handle-new":
            return _print(handle_new({"label": args.label}))
        if args.cmd == "handle-rotate":
            return _print(handle_rotate({"token": args.token}))
        if args.cmd == "room-open":
            return _print(room_open({"token_a": args.token_a, "token_b": args.token_b, "ttl_ms": args.ttl_ms}))
        if args.cmd == "room-post":
            return _print(room_post({"token": args.token, "room_id": args.room_id, "text": args.text}))
        if args.cmd == "room-pull":
            return _print(room_pull({"token": args.token, "room_id": args.room_id}))
        if args.cmd == "bus-send":
            return _print(bus_send({"from": args.from_agent, "to": args.to, "text": args.text}))
        if args.cmd == "bus-poll":
            return _print(bus_poll({"agent": args.agent, "limit": args.limit}))
        if args.cmd == "verify":
            rec = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
            return _print(verify_receipt(rec if "receipt" in rec else {"receipt": rec}))
        if args.cmd == "export":
            return _print(import_export({"mode": args.mode}))
        if args.cmd == "stub":
            return _print(dispatch(args.op, {}))
        if args.cmd == "ui":
            from azchat.ui import serve

            serve(host=args.host, port=args.port)
            return 0
    except AzChatError as exc:
        return _print({"ok": False, "error": str(exc), "honest": HONEST, "live_ops": list(LIVE_OPS)})
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
