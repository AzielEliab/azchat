"""Localhost UI for AZChat. Binds 127.0.0.1. Author: Aziel Eliab only."""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from azchat import __version__
from azchat.engine import HONEST, LIVE_OPS, dispatch, doctor, health, skill_markdown
from azchat.errors import AzChatError

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8878
LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
MAX_BODY = 2 * 1024 * 1024

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AZChat</title>
<style>
  :root {
    --bg: #0b0b0b; --panel: #141414; --ink: #e8e0d0; --muted: #8a7219;
    --line: #2a2414; --gold: #c9a227; --focus: #e6d19a; --bad: #d4534b;
    --pass: #3dba7a;
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0; background: var(--bg); color: var(--ink);
    font-family: system-ui, "Segoe UI", sans-serif; line-height: 1.45;
  }
  body { max-width: 52rem; margin: 0 auto; padding: 2.1rem 1.2rem 4rem; }
  .tag {
    font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.72rem;
    letter-spacing: 0.14em; text-transform: uppercase; color: var(--gold);
  }
  h1 { font-size: 2rem; font-weight: 650; letter-spacing: 0.04em; margin: 0.35rem 0 0.25rem; }
  .motto { color: var(--gold); font-style: italic; margin: 0 0 0.85rem; font-size: 1.05rem; }
  .lede { color: #b8b09a; margin: 0 0 1.5rem; max-width: 44rem; }
  fieldset {
    border: 1px solid var(--line); border-radius: 10px; background: var(--panel);
    padding: 1.1rem 1.15rem 1.2rem; margin: 0 0 1rem;
  }
  legend {
    font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.72rem;
    letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold); padding: 0 0.4rem;
  }
  label { display: block; font-size: 0.92rem; margin: 0.85rem 0 0.3rem; }
  textarea, input[type="text"] {
    width: 100%; padding: 0.55rem 0.65rem; border: 1px solid var(--line);
    border-radius: 6px; background: #101010; color: var(--ink); font: inherit;
  }
  .row2 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; }
  .actions { display: flex; gap: 0.65rem; flex-wrap: wrap; margin: 0.9rem 0 0; }
  button {
    font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 0.85rem;
    letter-spacing: 0.04em; padding: 0.65rem 1rem; border-radius: 8px;
    border: 1px solid var(--gold); background: var(--gold); color: var(--bg);
    cursor: pointer; font-weight: 650;
  }
  button.ghost { background: transparent; color: var(--ink); border-color: var(--line); }
  .banner {
    border: 1px solid #5c4a1a; background: #241c0d; color: #f0d78c;
    padding: 0.85rem 1rem; border-radius: 10px; margin: 0 0 1.15rem; font-size: 0.92rem;
  }
  .status { margin: 0 0 0.8rem; padding: 0.75rem 0.85rem; border-radius: 10px; border: 1px solid var(--line); }
  .status.ok { color: var(--pass); border-color: #2f6b48; }
  .status.bad { color: var(--bad); border-color: #7a2f2c; }
  pre { background: #101010; padding: 0.75rem 0.9rem; overflow: auto; border-radius: 8px; font-size: 0.78rem; }
</style>
</head>
<body>
  <p class="tag">AZC-CHAT-0.1 · Plain · Comms · Aziel Eliab</p>
  <h1>AZChat</h1>
  <p class="motto">Handles spend. Rooms seal. Mesh stays off.</p>
  <p class="lede">Loopback only. FragGate LIVE_OPS: health, skill, doctor, handle_new, handle_rotate, room_open, room_post, room_pull, bus_send, bus_poll, verify_receipt, import_export. Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404.</p>
  <p class="banner">__HONEST__</p>
  <fieldset>
    <legend>Workspace</legend>
    <div class="row2">
      <div>
        <label>Handle A label</label>
        <input id="label_a" type="text" value="agent-a">
        <label>Handle A token</label>
        <input id="token_a" type="text" placeholder="minted token">
      </div>
      <div>
        <label>Handle B label</label>
        <input id="label_b" type="text" value="agent-b">
        <label>Handle B token</label>
        <input id="token_b" type="text" placeholder="second minted token">
      </div>
    </div>
    <label>Room id</label>
    <input id="room_id" type="text" placeholder="opened room">
    <label>Room / bus text</label>
    <textarea id="post_text" rows="3">handles spend</textarea>
    <div class="row2">
      <div>
        <label>Bus from</label>
        <input id="bus_from" type="text" value="agent-a">
      </div>
      <div>
        <label>Bus to</label>
        <input id="bus_to" type="text" value="agent-b">
      </div>
    </div>
    <div class="actions">
      <button type="button" id="btn-handle-a">New handle A</button>
      <button type="button" id="btn-handle-b">New handle B</button>
      <button type="button" class="ghost" id="btn-rotate">Rotate A</button>
      <button type="button" id="btn-room">Open room</button>
      <button type="button" class="ghost" id="btn-post">Room post</button>
      <button type="button" class="ghost" id="btn-pull">Room pull</button>
      <button type="button" class="ghost" id="btn-bus-send">Bus send</button>
      <button type="button" class="ghost" id="btn-bus-poll">Bus poll</button>
      <button type="button" class="ghost" id="btn-verify">Verify receipt</button>
      <button type="button" class="ghost" id="btn-export">Import/export</button>
      <button type="button" class="ghost" id="btn-health">Health</button>
      <button type="button" class="ghost" id="btn-skill">Skill</button>
      <button type="button" class="ghost" id="btn-doctor">Doctor</button>
    </div>
  </fieldset>
  <div class="status" id="status">No receipt yet. Mint two handles, then open a room. Mesh stays off.</div>
  <pre id="out">{}</pre>
  <script>
    var lastReceipt = null;
    function $(id) { return document.getElementById(id); }
    function show(data) {
      document.getElementById("out").textContent = JSON.stringify(data, null, 2);
      var el = document.getElementById("status");
      var ok = data && data.ok !== false;
      el.className = "status " + (ok ? "ok" : "bad");
      el.textContent = (data && (data.note || data.error || data.op || data.status)) || "done";
      if (data && data.receipt) lastReceipt = data.receipt;
      if (data && data.token && data.op === "handle_new") {
        if (!$("token_a").value) $("token_a").value = data.token;
        else if (!$("token_b").value) $("token_b").value = data.token;
      }
      if (data && data.token && data.op === "handle_rotate") $("token_a").value = data.token;
      if (data && data.room_id && data.op === "room_open") $("room_id").value = data.room_id;
    }
    async function api(path, body) {
      var get = path === "/v1/health" || path === "/v1/skill" || path === "/v1/doctor";
      var res = await fetch(path, {
        method: get ? "GET" : "POST",
        headers: { "content-type": "application/json", "user-agent": "Mozilla/5.0" },
        body: get ? undefined : JSON.stringify(body || {})
      });
      if (path === "/v1/skill") return { ok: true, op: "skill", skill: await res.text() };
      return res.json();
    }
    $("btn-handle-a").onclick = async function () { show(await api("/v1/handle_new", { label: $("label_a").value })); };
    $("btn-handle-b").onclick = async function () { show(await api("/v1/handle_new", { label: $("label_b").value })); };
    $("btn-rotate").onclick = async function () { show(await api("/v1/handle_rotate", { token: $("token_a").value })); };
    $("btn-room").onclick = async function () { show(await api("/v1/room_open", { token_a: $("token_a").value, token_b: $("token_b").value })); };
    $("btn-post").onclick = async function () { show(await api("/v1/room_post", { token: $("token_a").value, room_id: $("room_id").value, text: $("post_text").value })); };
    $("btn-pull").onclick = async function () { show(await api("/v1/room_pull", { token: $("token_a").value, room_id: $("room_id").value })); };
    $("btn-bus-send").onclick = async function () { show(await api("/v1/bus_send", { from: $("bus_from").value, to: $("bus_to").value, text: $("post_text").value })); };
    $("btn-bus-poll").onclick = async function () { show(await api("/v1/bus_poll", { agent: $("bus_to").value })); };
    $("btn-verify").onclick = async function () { show(await api("/v1/verify_receipt", { receipt: lastReceipt || {} })); };
    $("btn-export").onclick = async function () { show(await api("/v1/import_export", { mode: "export" })); };
    $("btn-health").onclick = async function () { show(await api("/v1/health")); };
    $("btn-skill").onclick = async function () { show(await api("/v1/skill")); };
    $("btn-doctor").onclick = async function () { show(await api("/v1/doctor")); };
  </script>
</body>
</html>
""".replace("__HONEST__", HONEST.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


class Handler(BaseHTTPRequestHandler):
    server_version = "AZChat/" + __version__

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write("azchat-ui: " + (fmt % args) + "\n")

    def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "private, no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data: Any, status: int = 200) -> None:
        raw = json.dumps(data, indent=2, ensure_ascii=True).encode("utf-8")
        self._send(raw, "application/json; charset=utf-8", status)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path.rstrip("/") or "/"
        if path == "/":
            self._send(PAGE.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/v1/health":
            self._json(health())
            return
        if path == "/v1/doctor":
            self._json(doctor())
            return
        if path == "/v1/skill":
            from pathlib import Path

            skill = Path(__file__).resolve().parents[1] / "SKILL.md"
            text = skill.read_text(encoding="utf-8") if skill.exists() else skill_markdown()
            self._send(text.encode("utf-8"), "text/markdown; charset=utf-8")
            return
        self._json({"error": "not found", "live_ops": list(LIVE_OPS)}, 404)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path.rstrip("/") or "/"
        length = int(self.headers.get("Content-Length") or "0")
        if length > MAX_BODY:
            self._json({"error": "payload too large"}, 413)
            return
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._json({"error": "JSON body required"}, 400)
            return
        op = path[4:] if path.startswith("/v1/") else ""
        try:
            self._json(dispatch(op, payload if isinstance(payload, dict) else {}))
        except AzChatError as exc:
            self._json({"ok": False, "error": str(exc)}, 400)


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    if host not in LOOPBACK:
        raise ValueError("AZChat UI binds loopback only")
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(f"AZChat UI http://{host}:{port}  (loopback only)")
    print("Author: Aziel Eliab. Mesh hop default off. Not SMTP. Not AZMail.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
