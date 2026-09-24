"""AZChat CLI. Human text by default. --json keeps the machine fields.

Author: Aziel Eliab only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from azchat import __version__
from azchat.engine import (
    HONEST,
    LIVE_OPS,
    SPEC,
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
    skill_body,
    skill_markdown,
    verify_receipt,
)
from azchat.errors import AzChatError
from azchat.session import load_session, save_session, session_path

_AS_JSON = False

WELCOME = """AZChat opens short-lived rooms with spendable handles.

Open the local app:
  azchat ui

Then open http://127.0.0.1:8878/

From the terminal:
  azchat handle-new --label me
  azchat doctor

Handles and rooms from these commands stay in a session file on this computer.

Author: Aziel Eliab
"""


def main_help() -> str:
    return f"""usage: azchat [--help] [--version] [--json] <command> [<args>]

AZChat opens short-lived rooms with spendable handles.
Author: Aziel Eliab.

commands:
  ui              Open the local app on this computer
  handle-new      Create a spendable handle
  room-open       Open a room with two handles
  room-post       Send a message into a room
  room-pull       Read messages in a room
  doctor          Check this install
  health          Show whether AZChat is up
  skill           Print the skill notes
  help            Show this help

advanced:
  handle-rotate   Replace a handle token
  bus-send        Send a frame on the agent bus
  bus-poll        Read frames on the agent bus
  verify          Check a receipt hash
  export          Write a client-held export
  stub            Call a refused operation

options:
  -h, --help      Show this help
  --version       Show azchat {__version__}
  --json          Print machine JSON (same fields the tools already use)

examples:
  azchat
  azchat ui
  azchat handle-new --label me
  azchat doctor
  azchat health --json

`azchat <command> --help` explains one command.
"""


def _split_json(argv: list[str]) -> tuple[bool, list[str]]:
    as_json = False
    cleaned: list[str] = []
    for arg in argv:
        if arg == "--json":
            as_json = True
        else:
            cleaned.append(arg)
    return as_json, cleaned


def explain_usage(message: str) -> tuple[str, str]:
    choice = re.search(r"invalid choice: '([^']*)'", message)
    if choice:
        name = choice.group(1)
        return (f'Unknown command "{name}".', "Try: azchat ui   or   azchat --help")
    if "required" in message:
        if "--token-a" in message or "--token-b" in message:
            return (
                "A room needs two live handle tokens.",
                "Try: azchat handle-new --label me",
            )
        if "--token" in message:
            return ("A handle token is required.", "Try: azchat handle-new --label me")
        if "--room-id" in message and "--text" in message:
            return (
                "A room id and message text are required.",
                'Try: azchat room-post --token TOKEN --room-id ROOM --text "hello"',
            )
        if "--room-id" in message:
            return ("A room id is required.", "Try: azchat room-open --help")
        if "--text" in message:
            return (
                "Message text is required.",
                'Try: azchat bus-send --text "hello"',
            )
        if "--receipt" in message:
            return ("A receipt file is required.", "Try: azchat verify --receipt receipt.json")
        if re.search(r"\bcmd\b", message):
            return ("Choose a command to continue.", "Try: azchat ui   or   azchat --help")
    if message.startswith("unrecognized arguments"):
        return ("That option is not recognized.", "Try: azchat --help")
    if "expected one argument" in message or "invalid" in message:
        return ("That value is not usable.", "Try: azchat --help")
    return ("AZChat could not run that command.", "Try: azchat --help")


class AzChatParser(argparse.ArgumentParser):
    def format_help(self) -> str:
        if getattr(self, "_azchat_root", False):
            return main_help()
        return super().format_help()

    def error(self, message: str) -> None:
        reason, nxt = explain_usage(message)
        if _AS_JSON:
            sys.stdout.write(
                json.dumps({"ok": False, "error": reason, "next": nxt}, indent=2, ensure_ascii=True) + "\n"
            )
        else:
            sys.stderr.write(f"{reason}\n{nxt}\n")
        self.exit(2)


def _print_json(data: Any) -> int:
    sys.stdout.write(json.dumps(data, indent=2, ensure_ascii=True) + "\n")
    return 0 if data.get("ok", True) else 1


def _fail(reason: str, nxt: str, as_json: bool, code: int = 1) -> int:
    if as_json:
        sys.stdout.write(
            json.dumps({"ok": False, "error": reason, "next": nxt}, indent=2, ensure_ascii=True) + "\n"
        )
    else:
        sys.stderr.write(f"{reason}\n{nxt}\n")
    return code


def _welcome_body() -> dict[str, Any]:
    return {
        "ok": True,
        "product": "azchat",
        "name": "AZChat",
        "version": __version__,
        "spec": SPEC,
        "summary": "AZChat opens short-lived rooms with spendable handles.",
        "next": [
            "azchat ui",
            "azchat handle-new --label me",
            "azchat doctor",
            "azchat --help",
        ],
        "session_file": str(session_path() or ""),
        "author": "Aziel Eliab",
    }


def _mesh_word(data: dict[str, Any]) -> str:
    return "off" if data.get("mesh_enabled_default") is False else "on"


def _humanize(data: dict[str, Any]) -> str:
    if data.get("ok") is False:
        if data.get("code") == "AZC-CHAT-REFUSE" or "AZC-CHAT-REFUSE" in str(data.get("error") or ""):
            err = str(data.get("error") or "Refused.")
            return f"{err}\nTry: azchat --help\n"
        err = str(data.get("error") or "That did not work.")
        reasons = {
            "handle-unlinked": (
                "That handle is not live.",
                "Try: azchat handle-new --label me",
            ),
            "need-two-handles": (
                "A room needs two different handles.",
                "Try: azchat handle-new --label other",
            ),
            "stranger-or-missing": (
                "That room does not include this handle.",
                "Try: azchat room-open --help",
            ),
            "room-sealed": (
                "This room is sealed.",
                "Try: azchat room-open --help",
            ),
            "empty-post": (
                "The message was empty.",
                'Try: azchat room-post --token TOKEN --room-id ROOM --text "hello"',
            ),
            "empty-frame": (
                "The bus frame was empty.",
                'Try: azchat bus-send --text "hello"',
            ),
        }
        reason, nxt = reasons.get(err, (err, "Try: azchat --help"))
        return f"{reason}\n{nxt}\n"

    op = str(data.get("op") or "")
    if op == "health":
        return (
            "AZChat is up.\n"
            f"product: {data.get('product')}\n"
            f"spec: {data.get('spec')}\n"
            f"version: {data.get('version')}\n"
            f"mesh hop: {_mesh_word(data)}\n"
            f"author: {data.get('author')}\n"
            "\n"
            "Next: azchat ui\n"
        )
    if op == "doctor":
        passed = data.get("status") == "ok"
        lines = [
            "Doctor: pass" if passed else "Doctor: fail",
            "Handles, rooms, and the agent bus are on this computer."
            if passed
            else "This install did not pass the self-check.",
            f"Mesh hop: {_mesh_word(data)}",
            f"Author: {data.get('author')}",
            "",
        ]
        invariants = data.get("invariants") if isinstance(data.get("invariants"), dict) else {}
        if invariants:
            lines.append("Checks:")
            for key in sorted(invariants):
                lines.append(f"  {invariants[key]}")
            lines.append("")
        lines.append("Next: azchat ui")
        return "\n".join(lines) + "\n"
    if op == "handle_new":
        return (
            "Handle ready.\n"
            "op: handle_new\n"
            f"label: {data.get('label')}\n"
            f"handle id: {data.get('handle_id')}\n"
            f"token: {data.get('token')}\n"
            "\n"
            "Save this token. It stays in the session file on this computer.\n"
            "Next: azchat handle-new --label other\n"
        )
    if op == "handle_rotate":
        return (
            "Handle replaced.\n"
            "op: handle_rotate\n"
            f"handle id: {data.get('handle_id')}\n"
            f"token: {data.get('token')}\n"
            f"unlinked: {data.get('unlinked')}\n"
            "\n"
            "The previous token no longer works.\n"
            "Next: use the new token with room-open or room-post.\n"
        )
    if op == "room_open":
        return (
            "Room open.\n"
            "op: room_open\n"
            f"room id: {data.get('room_id')}\n"
            f"closes: {data.get('expires_at')}\n"
            f"sealed: {'yes' if data.get('sealed') else 'no'}\n"
            "\n"
            'Next: azchat room-post --token TOKEN --room-id ROOM --text "hello"\n'
        )
    if op == "room_post":
        post = data.get("post") if isinstance(data.get("post"), dict) else {}
        return (
            "Message sent.\n"
            "op: room_post\n"
            f"room id: {data.get('room_id')}\n"
            f"post id: {post.get('id')}\n"
            "\n"
            "Next: azchat room-pull --token TOKEN --room-id ROOM\n"
        )
    if op == "room_pull":
        posts = data.get("posts") if isinstance(data.get("posts"), list) else []
        lines = [
            "Room.\n"
            "op: room_pull\n"
            f"room id: {data.get('room_id')}\n"
            f"sealed: {'yes' if data.get('sealed') else 'no'}\n"
            f"closes: {data.get('expires_at')}\n"
            f"messages: {len(posts)}",
        ]
        for post in posts:
            if isinstance(post, dict):
                lines.append(f"  - {post.get('text')}")
        if not posts:
            lines.append("")
            lines.append('Next: azchat room-post --token TOKEN --room-id ROOM --text "hello"')
        return "\n".join(lines) + "\n"
    if op == "bus_send":
        frame = data.get("frame") if isinstance(data.get("frame"), dict) else {}
        return (
            "Bus frame sent.\n"
            "op: bus_send\n"
            f"from: {frame.get('from')}\n"
            f"to: {frame.get('to')}\n"
            "\n"
            "Next: azchat bus-poll --agent " + str(frame.get("to") or "") + "\n"
        )
    if op == "bus_poll":
        frames = data.get("frames") if isinstance(data.get("frames"), list) else []
        lines = [
            "Bus.",
            "op: bus_poll",
            f"frames: {data.get('count', len(frames))}",
        ]
        for frame in frames:
            if isinstance(frame, dict):
                lines.append(f"  - {frame.get('from')} → {frame.get('to')}: {frame.get('text')}")
        return "\n".join(lines) + "\n"
    if op == "verify_receipt":
        return (
            "Receipt check.\n"
            "op: verify_receipt\n"
            f"match: {'yes' if data.get('match') else 'no'}\n"
            f"sha256: {data.get('receipt_sha256')}\n"
        )
    if op == "import_export":
        if data.get("mode") == "import":
            return (
                "Import noted.\n"
                "op: import_export\n"
                "This copy does not store the import.\n"
                f"{data.get('note') or ''}\n"
            )
        handles = data.get("handles_live") if isinstance(data.get("handles_live"), list) else []
        rooms = data.get("rooms") if isinstance(data.get("rooms"), list) else []
        return (
            "Export.\n"
            "op: import_export\n"
            "mode: export\n"
            f"live handles: {len(handles)}\n"
            f"rooms: {len(rooms)}\n"
            f"bus frames: {data.get('bus_count')}\n"
            "stored on this host: no\n"
        )
    return json.dumps(data, indent=2, ensure_ascii=True) + "\n"


def emit(data: dict[str, Any], as_json: bool) -> int:
    if as_json:
        return _print_json(data)
    sys.stdout.write(_humanize(data))
    return 0 if data.get("ok", True) else 1


def _engine_error(exc: AzChatError, as_json: bool) -> int:
    if as_json:
        return _print_json({"ok": False, "error": str(exc), "honest": HONEST, "live_ops": list(LIVE_OPS)})
    return _fail(str(exc), "Try: azchat --help", False)


def build_parser() -> AzChatParser:
    p = AzChatParser(prog="azchat", description="AZChat opens short-lived rooms with spendable handles.")
    p._azchat_root = True  # noqa: SLF001
    p.add_argument("--version", action="version", version=f"azchat {__version__}")
    sub = p.add_subparsers(dest="cmd", required=False, metavar="<command>")

    sub.add_parser("help", help="Show the command list.")
    sub.add_parser("health", help="Show whether AZChat is up.")
    sub.add_parser("doctor", help="Check this install.")
    sub.add_parser("skill", help="Print the skill notes.")

    hn = sub.add_parser("handle-new", help="Create a spendable handle.")
    hn.add_argument("--label", default="handle", help="Name for this handle.")

    hr = sub.add_parser("handle-rotate", help="Replace a handle token. The previous token stops working.")
    hr.add_argument("--token", required=True, help="Live handle token.")

    ro = sub.add_parser("room-open", help="Open a room. Needs two live handle tokens.")
    ro.add_argument("--token-a", required=True, help="First handle token.")
    ro.add_argument("--token-b", required=True, help="Second handle token.")
    ro.add_argument("--ttl-ms", type=int, default=900000, help="How long the room stays open, in milliseconds.")

    rp = sub.add_parser("room-post", help="Send a message into a room as a member.")
    rp.add_argument("--token", required=True, help="Member handle token.")
    rp.add_argument("--room-id", required=True, help="Room id from room-open.")
    rp.add_argument("--text", required=True, help="Message text.")

    rpl = sub.add_parser("room-pull", help="Read messages in a room.")
    rpl.add_argument("--token", required=True, help="Member handle token.")
    rpl.add_argument("--room-id", required=True, help="Room id.")

    bs = sub.add_parser("bus-send", help="Send a frame on the agent bus.")
    bs.add_argument("--from-agent", dest="from_agent", default="agent-a", help="Sender name.")
    bs.add_argument("--to", default="agent-b", help="Recipient name.")
    bs.add_argument("--text", required=True, help="Frame text.")

    bp = sub.add_parser("bus-poll", help="Read frames on the agent bus.")
    bp.add_argument("--agent", default="", help="Only frames for this name. Empty reads the recent bus.")
    bp.add_argument("--limit", type=int, default=16, help="How many frames to show.")

    vr = sub.add_parser("verify", help="Check a receipt hash.")
    vr.add_argument("--receipt", required=True, help="Path to receipt JSON.")

    ie = sub.add_parser("export", help="Write a client-held export.")
    ie.add_argument("--mode", default="export", help="export or import. Import is not stored here.")

    stub = sub.add_parser("stub", help="Call a refused operation.")
    stub.add_argument("op", choices=list(STUB_OPS))

    ui = sub.add_parser("ui", help="Open the local app on this computer.")
    ui.add_argument("--host", default="127.0.0.1", help="Loopback address.")
    ui.add_argument("--port", type=int, default=8878, help="Loopback port.")

    return p


def _read_skill() -> str:
    skill = Path(__file__).resolve().parents[1] / "SKILL.md"
    if skill.exists():
        return skill.read_text(encoding="utf-8")
    return skill_markdown()


def main(argv: list[str] | None = None) -> int:
    global _AS_JSON
    raw = list(sys.argv[1:] if argv is None else argv)
    as_json, cleaned = _split_json(raw)
    _AS_JSON = as_json
    parser = build_parser()
    try:
        args = parser.parse_args(cleaned)
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        return code if isinstance(code, int) else 2

    if not args.cmd:
        if as_json:
            return _print_json(_welcome_body())
        sys.stdout.write(WELCOME)
        return 0
    if args.cmd == "help":
        sys.stdout.write(main_help())
        return 0

    session_cmds = {
        "handle-new",
        "handle-rotate",
        "room-open",
        "room-post",
        "room-pull",
        "bus-send",
        "bus-poll",
        "export",
    }
    persist = args.cmd in session_cmds
    if persist:
        problem = load_session()
        if problem:
            return _fail(problem, "Try: azchat doctor", as_json)

    try:
        if args.cmd == "health":
            return emit(health(), as_json)
        if args.cmd == "doctor":
            code = emit(doctor(), as_json)
            path = session_path()
            if code == 0 and path is not None and not as_json:
                sys.stdout.write(f"Session file: {path}\n")
            return code
        if args.cmd == "skill":
            if as_json:
                return emit(skill_body(), as_json)
            text = _read_skill()
            sys.stdout.write(text if text.endswith("\n") else text + "\n")
            return 0
        if args.cmd == "handle-new":
            return emit(handle_new({"label": args.label}), as_json)
        if args.cmd == "handle-rotate":
            return emit(handle_rotate({"token": args.token}), as_json)
        if args.cmd == "room-open":
            return emit(
                room_open({"token_a": args.token_a, "token_b": args.token_b, "ttl_ms": args.ttl_ms}),
                as_json,
            )
        if args.cmd == "room-post":
            return emit(
                room_post({"token": args.token, "room_id": args.room_id, "text": args.text}),
                as_json,
            )
        if args.cmd == "room-pull":
            return emit(room_pull({"token": args.token, "room_id": args.room_id}), as_json)
        if args.cmd == "bus-send":
            return emit(bus_send({"from": args.from_agent, "to": args.to, "text": args.text}), as_json)
        if args.cmd == "bus-poll":
            return emit(bus_poll({"agent": args.agent, "limit": args.limit}), as_json)
        if args.cmd == "verify":
            try:
                rec = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
            except FileNotFoundError:
                return _fail(
                    "Could not read that receipt file.",
                    "Try: azchat verify --receipt receipt.json",
                    as_json,
                )
            except json.JSONDecodeError:
                return _fail(
                    "That file is not receipt JSON.",
                    "Try: azchat verify --receipt receipt.json",
                    as_json,
                )
            if not isinstance(rec, dict):
                return _fail(
                    "That file is not receipt JSON.",
                    "Try: azchat verify --receipt receipt.json",
                    as_json,
                )
            return emit(verify_receipt(rec if "receipt" in rec else {"receipt": rec}), as_json)
        if args.cmd == "export":
            return emit(import_export({"mode": args.mode}), as_json)
        if args.cmd == "stub":
            return emit(dispatch(args.op, {}), as_json)
        if args.cmd == "ui":
            from azchat.ui import serve

            try:
                serve(host=args.host, port=args.port)
            except ValueError as exc:
                return _fail(str(exc), "Try: azchat ui", as_json)
            except OSError as exc:
                detail = exc.strerror or str(exc)
                return _fail(
                    f"Could not listen on {args.host}:{args.port}. {detail}",
                    "Try: azchat ui --port 8879",
                    as_json,
                )
            return 0
    except AzChatError as exc:
        return _engine_error(exc, as_json)
    finally:
        if persist:
            save_session()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
