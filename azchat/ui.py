"""Localhost UI for AZChat. Binds 127.0.0.1. Author: Aziel Eliab only."""

from __future__ import annotations

import html
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from azchat import __version__
from azchat.engine import HONEST, LIVE_OPS, dispatch, doctor, health, skill_markdown
from azchat.errors import AzChatError
from azchat.session import load_session, save_session, session_path, session_view

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8878
LOOPBACK = frozenset({"127.0.0.1", "localhost", "::1"})
MAX_BODY = 2 * 1024 * 1024

_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AZChat</title>
<style>
  :root {
    color-scheme: light;
    --bg: #f4f0e6;
    --panel: #fffdf8;
    --ink: #1a1814;
    --muted: #5e584e;
    --line: #e4d9c4;
    --gold: #c9a227;
    --gold-ink: #1a1408;
    --bad: #8c2f2a;
    --bad-bg: #f8ece8;
    --pass: #1d6b42;
    --pass-bg: #e7f4ec;
    --shadow: 0 1px 0 rgba(26, 24, 20, 0.04);
  }
  @media (prefers-color-scheme: dark) {
    :root {
      color-scheme: dark;
      --bg: #12110e;
      --panel: #1c1b17;
      --ink: #f4efe4;
      --muted: #cfc6b4;
      --line: #3c362c;
      --gold: #c9a227;
      --gold-ink: #1a1408;
      --bad: #f0b2ac;
      --bad-bg: #3a2422;
      --pass: #9ed8b6;
      --pass-bg: #1c3328;
      --shadow: none;
    }
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; max-width: 100%; overflow-x: hidden; }
  body {
    background: var(--bg);
    color: var(--ink);
    font-family: system-ui, "Segoe UI", sans-serif;
    line-height: 1.5;
    min-height: 100vh;
  }
  .wrap { max-width: 40rem; margin: 0 auto; padding: 1.25rem 1rem 3rem; }
  @media (min-width: 800px) {
    .wrap { padding: 2.5rem 1.5rem 4rem; }
  }
  .bar {
    display: flex; align-items: flex-end; justify-content: space-between;
    gap: 1rem; margin-bottom: 1.75rem;
  }
  .mark { margin: 0; font-size: 0.95rem; font-weight: 700; letter-spacing: 0.01em; }
  .by { margin: 0.1rem 0 0; color: var(--muted); font-size: 0.85rem; }
  .pill {
    margin: 0; color: var(--muted); font-size: 0.82rem;
    border: 1px solid var(--line); border-radius: 999px; padding: 0.2rem 0.65rem;
    background: var(--panel);
  }
  h1 { font-size: 1.85rem; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 0.4rem; }
  h2 { font-size: 1rem; margin: 0 0 0.35rem; }
  .lede { margin: 0 0 1.25rem; max-width: 36rem; color: var(--ink); }
  .status {
    margin: 0 0 1rem; padding: 0.8rem 0.9rem; border-radius: 12px;
    background: var(--panel); border: 1px solid var(--line); box-shadow: var(--shadow);
  }
  .status.ok { color: var(--pass); background: var(--pass-bg); border-color: transparent; }
  .status.bad { color: var(--bad); background: var(--bad-bg); border-color: transparent; }
  .actions { display: flex; flex-wrap: wrap; gap: 0.6rem; margin: 0 0 1.25rem; }
  button, summary {
    font: inherit; font-weight: 650; cursor: pointer;
  }
  button {
    min-height: 2.75rem; padding: 0.55rem 1rem; border-radius: 10px;
    border: 1px solid var(--line); background: var(--panel); color: var(--ink);
  }
  button.primary { background: var(--gold); border-color: var(--gold); color: var(--gold-ink); }
  button.ghost { background: transparent; }
  button:focus-visible, summary:focus-visible, a:focus-visible,
  input:focus-visible, textarea:focus-visible {
    outline: 3px solid #c9a227; outline-offset: 2px;
  }
  @media (max-width: 420px) {
    button.primary { width: 100%; }
  }
  input[type="password"] {
    width: 100%; max-width: 100%; padding: 0.6rem 0.7rem;
    border: 1px solid var(--line); border-radius: 8px;
    background: var(--bg); color: var(--ink); font: inherit;
  }
  label.check { display: flex; align-items: center; gap: 0.45rem; }
  label.check input { width: auto; }
  #room-list { list-style: none; margin: 0.7rem 0 0; padding: 0; }
  #room-list li {
    display: flex; flex-wrap: wrap; gap: 0.4rem 0.6rem; align-items: center;
    border: 1px solid var(--line); border-radius: 12px; padding: 0.55rem 0.7rem;
    margin: 0 0 0.4rem; background: var(--bg);
  }
  .cards { display: grid; gap: 0.75rem; margin: 0 0 1.25rem; }
  @media (min-width: 720px) {
    .cards { grid-template-columns: 1fr 1fr; }
  }
  article.card, .composer, details {
    background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
    padding: 0.9rem 1rem; box-shadow: var(--shadow);
  }
  .token {
    display: block; margin: 0.35rem 0 0; font-family: ui-monospace, Menlo, Consolas, monospace;
    font-size: 0.82rem; word-break: break-all;
  }
  label { display: block; font-size: 0.92rem; margin: 0.75rem 0 0.3rem; }
  textarea, input[type="text"], input[type="number"] {
    width: 100%; max-width: 100%; padding: 0.6rem 0.7rem;
    border: 1px solid var(--line); border-radius: 8px;
    background: var(--bg); color: var(--ink); font: inherit;
  }
  textarea { min-height: 5.5rem; resize: vertical; }
  .composer { margin: 0 0 1.25rem; }
  #thread { display: grid; gap: 0.6rem; margin: 0 0 1.25rem; }
  .post { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 0.75rem 0.9rem; }
  .post p { margin: 0; }
  .meta { color: var(--muted); font-size: 0.8rem; margin-bottom: 0.25rem !important; }
  details { margin: 0 0 0.8rem; }
  summary { padding: 0.15rem 0; }
  .stack { display: grid; gap: 0.75rem; }
  @media (min-width: 720px) {
    .stack.two { grid-template-columns: 1fr 1fr; }
  }
  .adv-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.9rem; }
  pre {
    margin: 0.8rem 0 0; padding: 0.75rem 0.85rem; border-radius: 10px;
    background: var(--bg); overflow: auto; white-space: pre-wrap; word-break: break-word;
    font-size: 0.78rem; max-width: 100%;
  }
  .about p { margin: 0.4rem 0; color: var(--muted); }
  [hidden] { display: none !important; }
</style>
</head>
<body>
  <div class="wrap">
    <header class="bar">
      <div>
        <p class="mark">AZChat</p>
        <p class="by">Aziel Eliab</p>
      </div>
      <p class="pill">On this computer</p>
    </header>
    <main>
      <h1>Open a room</h1>
      <p class="lede">Spendable handles let you open a short-lived room on this computer.</p>
      <p class="status" id="status" role="status" aria-live="polite">No handle yet. Create one to start.</p>
      <div class="actions">
        <button type="button" class="primary" id="btn-primary">New handle</button>
        <button type="button" class="ghost" id="btn-doctor">Doctor</button>
        <button type="button" class="ghost" id="btn-help">Help</button>
      </div>
      <section class="cards" id="handles" hidden>
        <article class="card" id="card-a" hidden>
          <h2>Your handle</h2>
          <p id="label-show-a"></p>
          <code class="token" id="token-show-a"></code>
        </article>
        <article class="card" id="card-b" hidden>
          <h2>Second handle</h2>
          <p id="label-show-b"></p>
          <code class="token" id="token-show-b"></code>
        </article>
      </section>
      <section class="composer" id="composer" hidden>
        <p class="meta" id="room-line"></p>
        <label for="message">Message</label>
        <textarea id="message">Hello</textarea>
      </section>
      <section id="thread" hidden></section>
      <section class="composer" id="rooms">
        <h2>All rooms</h2>
        <p class="meta">Host a room to put it on this list. Private means a passphrase is required to join. It is not end-to-end encryption. Lamb Lens Service → Clarity → Peace.</p>
        <label for="room_title">Room title</label>
        <input id="room_title" type="text" value="hall" maxlength="80">
        <label class="check" for="room_private"><input id="room_private" type="checkbox"> Private room — passphrase required to join</label>
        <label for="room_pass">Passphrase</label>
        <input id="room_pass" type="password" autocomplete="new-password" placeholder="required only when the room is private">
        <div class="adv-actions">
          <button type="button" id="btn-host">Host room</button>
          <button type="button" class="ghost" id="btn-rooms">Refresh list</button>
        </div>
        <ul id="room-list" aria-label="All rooms"></ul>
      </section>
      <details id="advanced">
        <summary>Advanced</summary>
        <div class="stack two">
          <div>
            <label for="label_a">Your label</label>
            <input id="label_a" type="text" value="me">
            <label for="token_a">Your token</label>
            <input id="token_a" type="text" autocomplete="off">
          </div>
          <div>
            <label for="label_b">Second label</label>
            <input id="label_b" type="text" value="other">
            <label for="token_b">Second token</label>
            <input id="token_b" type="text" autocomplete="off">
          </div>
        </div>
        <label for="room_id">Room id</label>
        <input id="room_id" type="text" autocomplete="off">
        <label for="post_text">Room or bus text</label>
        <textarea id="post_text" rows="3">Hello</textarea>
        <div class="stack two">
          <div>
            <label for="bus_from">Bus from</label>
            <input id="bus_from" type="text" value="me">
          </div>
          <div>
            <label for="bus_to">Bus to</label>
            <input id="bus_to" type="text" value="other">
          </div>
        </div>
        <div class="adv-actions">
          <button type="button" id="btn-handle-a">New handle</button>
          <button type="button" id="btn-handle-b">New second handle</button>
          <button type="button" id="btn-rotate">Rotate handle</button>
          <button type="button" id="btn-room">Open room</button>
          <button type="button" id="btn-post">Send message</button>
          <button type="button" id="btn-pull">Read room</button>
          <button type="button" id="btn-bus-send">Send on the bus</button>
          <button type="button" id="btn-bus-poll">Read the bus</button>
          <button type="button" id="btn-verify">Check receipt</button>
          <button type="button" id="btn-export">Export</button>
          <button type="button" id="btn-health">Health</button>
          <button type="button" id="btn-skill">Skill</button>
        </div>
        <details>
          <summary>Response details</summary>
          <pre id="out">No response yet.</pre>
        </details>
      </details>
      <details class="about" id="about">
        <summary>About</summary>
        <p>Author: Aziel Eliab. Spec AZC-CHAT-0.1. This page listens on 127.0.0.1 only.</p>
        <p id="session">__SESSION__</p>
        <p id="honest">__HONEST__</p>
      </details>
    </main>
  </div>
  <script>
    var lastReceipt = null;
    function $(id) { return document.getElementById(id); }
    function syncPrimary() {
      var hasA = !!$("token_a").value.trim();
      var hasB = !!$("token_b").value.trim();
      var hasRoom = !!$("room_id").value.trim();
      var btn = $("btn-primary");
      $("handles").hidden = !hasA && !hasB;
      $("card-a").hidden = !hasA;
      $("card-b").hidden = !hasB;
      $("label-show-a").textContent = $("label_a").value || "Handle";
      $("label-show-b").textContent = $("label_b").value || "Handle";
      $("token-show-a").textContent = $("token_a").value;
      $("token-show-b").textContent = $("token_b").value;
      if (!hasA) {
        btn.textContent = "New handle";
        btn.dataset.act = "handle-a";
        $("composer").hidden = true;
      } else if (!hasB) {
        btn.textContent = "New second handle";
        btn.dataset.act = "handle-b";
        $("composer").hidden = true;
      } else if (!hasRoom) {
        btn.textContent = "Open room";
        btn.dataset.act = "room";
        $("composer").hidden = true;
      } else {
        btn.textContent = "Send message";
        btn.dataset.act = "post";
        $("composer").hidden = false;
        if (!$("message").value) $("message").value = $("post_text").value || "Hello";
      }
    }
    function setStatus(text, kind) {
      var el = $("status");
      el.textContent = text;
      el.className = "status" + (kind ? " " + kind : "");
    }
    function plain(data) {
      if (!data || typeof data !== "object") return "Done.";
      if (data.ok === false) {
        var reasons = {
          "handle-unlinked": "That handle is not live. Create a new handle, then try again.",
          "need-two-handles": "A room needs two different handles. Create the second handle.",
          "stranger-or-missing": "That room does not include this handle. Use a member token, or open a room.",
          "room-sealed": "This room is sealed. Open a new room.",
          "room-missing": "That room is not on the all-rooms list.",
          "passphrase-required": "A private room needs a passphrase. No join.",
          "passphrase-rejected": "That passphrase did not match. No join.",
          "passphrase-too-long": "That passphrase is longer than 128 characters. No join.",
          "private-flag-required": "A passphrase was sent without marking the room private. No room was created.",
          "empty-post": "Write a message, then send it.",
          "empty-frame": "Write a message, then send it on the bus."
        };
        return reasons[data.error] || (data.error || "That did not work.") + " See About, or try the primary button.";
      }
      if (data.op === "handle_new") return "Handle ready. Save the token, then create the second handle.";
      if (data.op === "handle_rotate") return "Handle replaced. The previous token no longer works.";
      if (data.op === "room_open") return "Room is open. Write a message, then send it.";
      if (data.op === "room_post") return "Message sent.";
      if (data.op === "room_pull") return (data.posts ? data.posts.length : 0) + " message(s) in this room.";
      if (data.op === "room_list") return (data.count || 0) + " hosted room(s). Private means a passphrase is required to join. It is not end-to-end encryption.";
      if (data.op === "room_host") return data.private ? "Private room is on the list. A passphrase is required to join. It is not end-to-end encryption." : "Room is on the all-rooms list.";
      if (data.op === "room_join") return data.joined ? "Joined. You can send a message." : "You are already in this room.";
      if (data.op === "bus_send") return "Bus frame sent.";
      if (data.op === "bus_poll") return (data.count || 0) + " bus frame(s). Open Response details to read them.";
      if (data.op === "verify_receipt") return data.match ? "Receipt matches." : "Receipt does not match.";
      if (data.op === "import_export") return "Export stays on this computer. The host does not store it.";
      if (data.op === "doctor") return "Doctor: pass. Handles, rooms, and the bus are available.";
      if (data.op === "health") return "AZChat is up.";
      if (data.op === "skill") return "Skill notes are under Response details.";
      return data.note || "Done.";
    }
    function renderPosts(posts) {
      var el = $("thread");
      el.textContent = "";
      if (!posts || !posts.length) { el.hidden = true; return; }
      el.hidden = false;
      posts.forEach(function (p) {
        var item = document.createElement("article");
        item.className = "post";
        var meta = document.createElement("p");
        meta.className = "meta";
        meta.textContent = p.ts || "";
        var body = document.createElement("p");
        body.textContent = p.text || "";
        item.appendChild(meta);
        item.appendChild(body);
        el.appendChild(item);
      });
    }
    function show(data) {
      $("out").textContent = JSON.stringify(data, null, 2);
      var ok = data && data.ok !== false;
      setStatus(plain(data), ok ? "ok" : "bad");
      if (data && data.receipt) lastReceipt = data.receipt;
      if (data && data.token && data.op === "handle_new") {
        if (!$("token_a").value.trim()) {
          $("token_a").value = data.token;
          if (data.label) $("label_a").value = data.label;
        } else if (!$("token_b").value.trim()) {
          $("token_b").value = data.token;
          if (data.label) $("label_b").value = data.label;
        } else {
          $("token_a").value = data.token;
          if (data.label) $("label_a").value = data.label;
        }
      }
      if (data && data.token && data.op === "handle_rotate") $("token_a").value = data.token;
      if (data && data.room_id && (data.op === "room_open" || data.op === "room_host" || data.op === "room_join")) $("room_id").value = data.room_id;
      if (data && data.ok !== false && (data.op === "room_host" || data.op === "room_join") && $("room_pass")) $("room_pass").value = "";
      if (data && data.op === "room_pull") renderPosts(data.posts || []);
      if (data && data.op === "room_post" && data.post) renderPosts([data.post]);
      syncPrimary();
      if (data && data.op === "handle_new" && data.ok !== false) {
        if ($("token_a").value.trim() && $("token_b").value.trim()) {
          setStatus("Two handles are ready. Open a room when you want.", "ok");
        } else {
          setStatus("Handle ready. Save the token, then create the second handle.", "ok");
        }
      }
      if ($("room_id").value.trim()) $("room-line").textContent = "Room " + $("room_id").value.trim();
    }
    async function api(path, body) {
      var get = path === "/v1/health" || path === "/v1/skill" || path === "/v1/doctor" || path === "/v1/session";
      var res = await fetch(path, {
        method: get ? "GET" : "POST",
        headers: { "content-type": "application/json", "user-agent": "Mozilla/5.0" },
        body: get ? undefined : JSON.stringify(body || {})
      });
      if (path === "/v1/skill") return { ok: true, op: "skill", skill: await res.text() };
      return res.json();
    }
    function esc(s) {
      return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
    async function refreshRooms() {
      var data = await api("/v1/room_list", {});
      var list = $("room-list");
      var rooms = (data && data.rooms) || [];
      if (!rooms.length) {
        list.innerHTML = "<li>No hosted rooms yet.</li>";
        return data;
      }
      list.innerHTML = rooms.map(function (room) {
        var gate = room.private ? "private · passphrase required" : "open entry";
        return '<li><strong>' + esc(room.title || "room") + '</strong> <code>' + esc(room.room_id) + '</code> <span>' + esc(gate) + '</span> <span>' + esc(room.member_count) + ' members</span> <button type="button" data-join="' + esc(room.room_id) + '" data-private="' + (room.private ? "1" : "0") + '">Join</button></li>';
      }).join("");
      return data;
    }
    async function run(act) {
      var text = $("message").value || $("post_text").value;
      $("post_text").value = text;
      if (act === "handle-a") return show(await api("/v1/handle_new", { label: $("label_a").value }));
      if (act === "handle-b") return show(await api("/v1/handle_new", { label: $("label_b").value }));
      if (act === "rotate") return show(await api("/v1/handle_rotate", { token: $("token_a").value }));
      if (act === "room") return show(await api("/v1/room_open", { token_a: $("token_a").value, token_b: $("token_b").value }));
      if (act === "host") {
        var body = { token: $("token_a").value, title: $("room_title").value, private: $("room_private").checked };
        if ($("room_private").checked) body.passphrase = $("room_pass").value;
        var hosted = await api("/v1/room_host", body);
        show(hosted);
        await refreshRooms();
        return;
      }
      if (act === "rooms") return show(await refreshRooms());
      if (act === "post") {
        var posted = await api("/v1/room_post", { token: $("token_a").value, room_id: $("room_id").value, text: text });
        show(posted);
        if (posted && posted.ok !== false) {
          var pulled = await api("/v1/room_pull", { token: $("token_a").value, room_id: $("room_id").value });
          if (pulled && pulled.posts) renderPosts(pulled.posts);
        }
        return;
      }
      if (act === "pull") return show(await api("/v1/room_pull", { token: $("token_a").value, room_id: $("room_id").value }));
      if (act === "bus-send") return show(await api("/v1/bus_send", { from: $("bus_from").value, to: $("bus_to").value, text: text }));
      if (act === "bus-poll") return show(await api("/v1/bus_poll", { agent: $("bus_to").value }));
      if (act === "verify") return show(await api("/v1/verify_receipt", { receipt: lastReceipt || {} }));
      if (act === "export") return show(await api("/v1/import_export", { mode: "export" }));
      if (act === "health") return show(await api("/v1/health"));
      if (act === "skill") return show(await api("/v1/skill"));
      if (act === "doctor") return show(await api("/v1/doctor"));
    }
    $("btn-primary").dataset.act = "handle-a";
    $("btn-primary").onclick = function () { run($("btn-primary").dataset.act); };
    $("btn-doctor").onclick = function () { run("doctor"); };
    $("btn-help").onclick = function () {
      $("about").open = true;
      $("about").scrollIntoView({ behavior: "smooth", block: "start" });
    };
    $("btn-handle-a").onclick = function () { run("handle-a"); };
    $("btn-handle-b").onclick = function () { run("handle-b"); };
    $("btn-rotate").onclick = function () { run("rotate"); };
    $("btn-room").onclick = function () { run("room"); };
    $("btn-host").onclick = function () { run("host"); };
    $("btn-rooms").onclick = function () { run("rooms"); };
    $("room-list").addEventListener("click", function (ev) {
      var btn = ev.target.closest ? ev.target.closest("button[data-join]") : null;
      if (!btn) return;
      var body = { token: $("token_a").value, room_id: btn.getAttribute("data-join") };
      if (btn.getAttribute("data-private") === "1") body.passphrase = $("room_pass").value;
      api("/v1/room_join", body).then(function (data) {
        show(data);
        return refreshRooms();
      }).catch(function (err) { setStatus(String(err.message || err), "bad"); });
    });
    $("btn-post").onclick = function () { run("post"); };
    $("btn-pull").onclick = function () { run("pull"); };
    $("btn-bus-send").onclick = function () { run("bus-send"); };
    $("btn-bus-poll").onclick = function () { run("bus-poll"); };
    $("btn-verify").onclick = function () { run("verify"); };
    $("btn-export").onclick = function () { run("export"); };
    $("btn-health").onclick = function () { run("health"); };
    $("btn-skill").onclick = function () { run("skill"); };
    ["token_a", "token_b", "room_id", "label_a", "label_b"].forEach(function (id) {
      $(id).addEventListener("input", syncPrimary);
    });
    syncPrimary();
    async function hydrate() {
      var data = await api("/v1/session");
      if (!data || !data.handles) return;
      if (data.handles[0]) {
        $("token_a").value = data.handles[0].token || "";
        if (data.handles[0].label) $("label_a").value = data.handles[0].label;
      }
      if (data.handles[1]) {
        $("token_b").value = data.handles[1].token || "";
        if (data.handles[1].label) $("label_b").value = data.handles[1].label;
      }
      var rooms = data.rooms || [];
      var openRoom = null;
      rooms.forEach(function (room) { if (!room.sealed) openRoom = room; });
      if (openRoom && openRoom.id) $("room_id").value = openRoom.id;
      syncPrimary();
      if ($("token_a").value && $("token_b").value && !$("room_id").value) {
        setStatus("Two handles are ready. Open a room when you want.", "ok");
      }
      if ($("room_id").value && $("token_a").value) {
        var pulled = await api("/v1/room_pull", { token: $("token_a").value, room_id: $("room_id").value });
        if (pulled && pulled.posts) renderPosts(pulled.posts);
        if (pulled && pulled.ok !== false) setStatus("Room is open. Write a message, then send it.", "ok");
      }
      await refreshRooms();
    }
    hydrate().catch(function () {
      setStatus("The session could not be read. You can still create a handle.", "bad");
    });
  </script>
</body>
</html>
"""


def render_page(session_note: str | None = None) -> str:
    note = session_note
    if note is None:
        path = session_path()
        note = f"Session file: {path}" if path else ""
    page = _PAGE.replace("__HONEST__", html.escape(HONEST))
    return page.replace("__SESSION__", html.escape(note))


PAGE = render_page("")


def wants_json(accept: str | None) -> bool:
    header = (accept or "").lower()
    json_at = header.find("application/json")
    if json_at < 0:
        return False
    html_at = header.find("text/html")
    if html_at < 0:
        return True
    return json_at < html_at


def open_line(host: str, port: int) -> str:
    return f"Open http://{host}:{port}/"


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

    def _remember(self) -> str | None:
        problem = load_session()
        return problem

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path.rstrip("/") or "/"
        if path == "/":
            if wants_json(self.headers.get("Accept")):
                self._json(health())
                return
            problem = self._remember()
            note = problem or ""
            if not note:
                session = session_path()
                note = f"Session file: {session}" if session else ""
            page = render_page(note)
            if problem:
                page = page.replace(
                    "No handle yet. Create one to start.",
                    html.escape(problem),
                    1,
                )
            self._send(page.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/v1/session":
            problem = self._remember()
            if problem:
                self._json({"ok": False, "error": problem}, 400)
                return
            self._json(session_view())
            return
        if path == "/v1/health":
            self._json(health())
            return
        if path == "/v1/doctor":
            self._json(doctor())
            return
        if path == "/v1/room_list":
            problem = self._remember()
            if problem:
                self._json({"ok": False, "error": problem}, 400)
                return
            self._json(dispatch("room_list", {}))
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
        problem = self._remember()
        if problem:
            self._json({"ok": False, "error": problem}, 400)
            return
        try:
            self._json(dispatch(op, payload if isinstance(payload, dict) else {}))
        except AzChatError as exc:
            self._json({"ok": False, "error": str(exc)}, 400)
            return
        save_session()


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    if host not in LOOPBACK:
        raise ValueError("AZChat listens on this computer only (127.0.0.1).")
    httpd = ThreadingHTTPServer((host, port), Handler)
    print(open_line(host, port), flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
