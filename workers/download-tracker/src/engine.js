/**
 * AZChat Worker engine — isolate-hash mirror of aziel-runtime 1.9.0.
 * Spendable handles, ephemeral rooms, agent bus.
 * Mesh hop default OFF. Not SMTP. Not AZMail. Do not bridge.
 * True engine remains in-process on aziel-runtime FragGate slug `azchat`.
 * Author: Aziel Eliab. Identity is Aziel Eliab only.
 */

export const PRODUCT = "azchat";
export const SLUG = "azchat";
export const NAME = "AZChat";
export const VERSION = "0.1.0";
export const SPEC = "AZC-CHAT-0.1";
export const AUTHOR = "Aziel Eliab";
export const ROLE = "spendable-handle rooms + agent bus";
export const MOTTO = "Handles spend. Rooms seal. Mesh stays off.";
export const CLASS = "Plain";
export const DOMAIN = "Comms";
export const AXES = Object.freeze(["handle", "room", "bus", "receipt"]);
export const NEIGHBORS = Object.freeze(["azmail (not bridged)", "aznet", "peacelock"]);
export const MESH_ENABLED_DEFAULT = false;
export const ROOM_TTL_DEFAULT_MS = 15 * 60 * 1000;
export const ROOM_TTL_MAX_MS = 60 * 60 * 1000;
export const TEXT_CAP = 2000;
export const FRAME_CAP = 64;
export const TITLE_CAP = 80;
export const PASSPHRASE_ITERS = 100000;
export const PASSPHRASE_MAX = 128;
export const PRIVATE_NOTE =
  "Private means a passphrase is required to join. " +
  "It is not end-to-end encryption. " +
  "Lamb Lens Service → Clarity → Peace.";

export const LIVE_OPS = Object.freeze([
  "health",
  "skill",
  "doctor",
  "handle_new",
  "handle_rotate",
  "room_open",
  "room_post",
  "room_pull",
  "room_list",
  "room_host",
  "room_join",
  "bus_send",
  "bus_poll",
  "verify_receipt",
  "import_export",
]);

export const STUB_OPS = Object.freeze([
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
]);

export const LIMITATION =
  "THIS IS: AZChat spendable handles, ephemeral rooms (TTL/sealed), and an agent bus. " +
  "Reached only through FragGate. mesh_enabled_default is false. " +
  "THIS IS NOT: SMTP, a public MTA, AZMail, a mesh hop, deanonymize, or a Chromium chat runner. " +
  "Do not bridge AZChat ↔ AZMail. Stranger room_pull is 404. " +
  "Hosted rooms appear on the all-rooms list. A private room requires a passphrase to join " +
  "and is not end-to-end encryption. Author: Aziel Eliab only.";

export const HONEST = LIMITATION;

const STUB_MESSAGES = {
  smtp: "AZC-CHAT-REFUSE: SMTP is stub. AZChat is not a mailer.",
  smtp_send: "AZC-CHAT-REFUSE: smtp_send is stub. Not an MTA.",
  send: "AZC-CHAT-REFUSE: send is stub. Use room_post or bus_send.",
  mail: "AZC-CHAT-REFUSE: mail is stub. Do not bridge AZChat ↔ AZMail.",
  deliver: "AZC-CHAT-REFUSE: deliver is stub. Not a public MTA.",
  deanonymize: "AZC-CHAT-REFUSE: deanonymize is stub.",
  harvest: "AZC-CHAT-REFUSE: harvest is stub.",
  mesh_join: "AZC-CHAT-REFUSE: product-local mesh_join is stub. Suite mesh is /v1/mesh/* PROXY. GET never enables.",
  mesh_enable: "AZC-CHAT-REFUSE: product-local mesh_enable is stub. GET /v1/mesh never enables. Default OFF.",
  vpn: "AZC-CHAT-REFUSE: vpn is stub. Not a hop mesh.",
  bridge_azmail: "AZC-CHAT-REFUSE: do not bridge AZChat ↔ AZMail.",
  bridge: "AZC-CHAT-REFUSE: bridge is stub. Not AZMail.",
  chromium: "AZC-CHAT-REFUSE: chromium is stub. Not a Chromium chat runner.",
};

export class RefuseError extends Error {
  constructor(msg) {
    super(msg);
    this.name = "RefuseError";
  }
}

const store = {
  handles: new Map(),
  rooms: new Map(),
  bus: [],
  seq: 0,
};

export function resetAzchatStore() {
  store.handles.clear();
  store.rooms.clear();
  store.bus = [];
  store.seq = 0;
}

function nowMs() {
  return Date.now();
}

function nowIso(ms = nowMs()) {
  return new Date(ms).toISOString();
}

function clip(raw, cap = TEXT_CAP) {
  return String(raw == null ? "" : raw).slice(0, cap);
}

function nextId(prefix) {
  store.seq += 1;
  return `${prefix}_${store.seq.toString(36)}_${nowMs().toString(36)}`;
}

function tokenBytes() {
  const bytes = new Uint8Array(18);
  crypto.getRandomValues(bytes);
  return [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");
}

export async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(String(text)));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function baseFields() {
  return {
    product: PRODUCT,
    name: NAME,
    slug: SLUG,
    version: VERSION,
    spec: SPEC,
    role: ROLE,
    motto: MOTTO,
    axes: AXES.slice(),
    neighbors: NEIGHBORS.slice(),
    live_ops: LIVE_OPS.slice(),
    stub_ops: STUB_OPS.slice(),
    true_engine_runtime: false,
    worker_local: true,
    catalog_engine: "aziel-runtime",
    kv_increment: false,
    door: "fraggate",
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    limitation: LIMITATION,
    author: AUTHOR,
    isolate_hash_store: true,
    object_store: "isolate-hash",
    cdn: false,
    azmail_bridge: false,
    smtp: false,
    mta: false,
    public_url: false,
  };
}

export function refuseStub(op) {
  const key = String(op || "").trim().replace(/-/g, "_");
  if (!STUB_OPS.includes(key)) throw new RefuseError("unknown stub");
  return {
    ok: false,
    status: 403,
    error: STUB_MESSAGES[key],
    code: "AZC-CHAT-REFUSE",
    stub: true,
    op: key,
    product: PRODUCT,
    slug: SLUG,
    spec: SPEC,
    version: VERSION,
    author: AUTHOR,
    door: "fraggate",
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    azmail_bridge: false,
    limitation: LIMITATION,
  };
}

export function health(meshPointer) {
  return {
    ok: true,
    op: "health",
    status: "ok",
    ...baseFields(),
    mesh: meshPointer || { pointer: true, enabled_default: false },
    note: "Hosted /v1 does not increment downloads. True engine is aziel-runtime FragGate slug azchat. This Worker is the human door + counted /download + mesh peer.",
    honest: HONEST,
  };
}

export function doctor() {
  return {
    ok: true,
    op: "doctor",
    status: "ok",
    ...baseFields(),
    doctor_note: "AZChat doctor: handles/rooms/bus only. Mesh stays off. Not a mailer. Not AZMail.",
    identity: "Aziel Eliab only",
    fraggate_live: true,
    network: false,
    invariants: {
      I1: "Mesh hop default off. GET /v1/mesh never enables.",
      I2: "Not SMTP. Not a public MTA.",
      I3: "Not AZMail. Do not bridge.",
      I4: "Stranger room_pull is 404.",
      I5: "FragGate is THE single door.",
      I6: "Identity is Aziel Eliab only.",
      I7: "Private rooms are passphrase-gated entry. The passphrase is not stored in plaintext and is not on the public list. Private is not end-to-end encryption.",
    },
    note: "Doctor is a FragGate LIVE_OPS self-check. No writes. Mesh stays off.",
  };
}

export function skillMarkdown() {
  return `---
name: AZChat
description: Use when minting spendable handles, opening ephemeral rooms, hosting a listed room, joining from the all-rooms list, or polling an agent bus (AZC-CHAT-0.1). Private rooms require a passphrase to join and are not end-to-end encryption. Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404. Dual surface: Worker /v1 + POST /mcp, or aziel-runtime FragGate slug azchat. This Worker /v1/fraggate/* and /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. GET /v1/mesh never enables. Product-local mesh_enable is stub/REFUSE. Author Aziel Eliab. Identity: Aziel Eliab only. Lamb Lens Service → Clarity → Peace.
---

# AZChat (AZC-CHAT-0.1)

AZChat: spendable handles, ephemeral rooms, agent bus. Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404.

- MCP: \`fraggate_call\` with \`{ slug: "azchat", op: "..." }\`
- HTTP: \`POST /v1/fraggate/call\` with the same envelope
- Leftover flat names such as \`azchat_health\` still go through FragGate (\`parseTarget\`) — they are not a side door and are not listed on \`tools/list\`

LIVE_OPS: health, skill, doctor, handle_new, handle_rotate, room_open, room_post, room_pull, room_list, room_host, room_join, bus_send, bus_poll, verify_receipt, import_export.

Hosted rooms: \`room_host\` puts a room on the all-rooms list (\`room_list\`). \`room_join\` enters a listed room. A private room stores only a PBKDF2-HMAC-SHA-256 verifier. A wrong or missing passphrase does not join. The passphrase is not on the public list and is not stored in plaintext. Private is passphrase-gated entry, not end-to-end encryption. Pairwise \`room_open\` rooms stay off the list. Stranger \`room_pull\` is 404 until a live handle is a member.

Stubs (refuse): smtp, smtp_send, send, mail, deliver, deanonymize, harvest, mesh_join, mesh_enable, vpn, bridge_azmail, bridge, chromium.

Axes / order: handle, room, bus, receipt.
Neighbors: azmail (not bridged), aznet, peacelock.

Author: Aziel Eliab only.
Limitation: ${LIMITATION}
`;
}

export function skillBody() {
  return {
    op: "skill",
    markdown: skillMarkdown(),
    skill: skillMarkdown(),
    kv_increment: false,
    limitation: LIMITATION,
    live_ops: LIVE_OPS.slice(),
    stub_ops: STUB_OPS.slice(),
    neighbors: NEIGHBORS.slice(),
    axes: AXES.slice(),
    door: "fraggate",
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    author: AUTHOR,
    product: PRODUCT,
    name: NAME,
    version: VERSION,
    spec: SPEC,
    true_engine_runtime: false,
    worker_local: true,
  };
}

function lookupHandle(token) {
  const key = String(token || "").trim();
  if (!key) return null;
  const row = store.handles.get(key);
  if (!row || row.live !== true) return null;
  return row;
}

async function receiptOf(fields) {
  const body = { ...fields, author: AUTHOR };
  const hash = await sha256Hex(JSON.stringify(body));
  return { ...body, receipt_sha256: hash };
}

export async function handleNew(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const token = tokenBytes();
  const id = nextId("h");
  const row = {
    id,
    token,
    live: true,
    rotated: false,
    successor: null,
    label: clip(src.label || src.agent || "handle", 48),
    created: nowIso(),
  };
  store.handles.set(token, row);
  const receipt = await receiptOf({ op: "handle_new", handle_id: id, label: row.label, ts: row.created });
  return {
    ok: true,
    op: "handle_new",
    handle_id: id,
    token,
    label: row.label,
    live: true,
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    receipt,
    note: "Spendable handle. Rotate unlinks this token. Author: Aziel Eliab.",
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function handleRotate(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const current = lookupHandle(src.token || src.handle_token);
  if (!current) {
    return { ok: false, status: 404, error: "handle-unlinked", op: "handle_rotate" };
  }
  const nextToken = tokenBytes();
  const nextIdValue = nextId("h");
  current.live = false;
  current.rotated = true;
  current.successor = nextIdValue;
  const next = {
    id: nextIdValue,
    token: nextToken,
    live: true,
    rotated: false,
    successor: null,
    label: current.label,
    created: nowIso(),
    previous: current.id,
  };
  store.handles.set(nextToken, next);
  const receipt = await receiptOf({ op: "handle_rotate", from: current.id, to: next.id, ts: next.created });
  return {
    ok: true,
    op: "handle_rotate",
    handle_id: next.id,
    token: nextToken,
    unlinked: current.id,
    live: true,
    receipt,
    note: "Prior token is unlinked. Rooms still list the old handle id as spent.",
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

function roomSealed(room, now = nowMs()) {
  return room.sealed === true || now >= room.expires_at;
}

function asBool(value) {
  if (value === true || value === 1) return true;
  if (typeof value === "string") {
    const s = value.trim().toLowerCase();
    return s === "1" || s === "true" || s === "yes" || s === "on";
  }
  return false;
}

function roomTtl(src) {
  const ttl = Number(src.ttl_ms);
  const n = Number.isFinite(ttl) ? ttl : ROOM_TTL_DEFAULT_MS;
  return Math.min(ROOM_TTL_MAX_MS, Math.max(1, n));
}

function passphraseText(raw) {
  if (raw == null) return { ok: false, error: "passphrase-required" };
  const text = String(raw).trim();
  if (!text) return { ok: false, error: "passphrase-required" };
  if (text.length > PASSPHRASE_MAX) return { ok: false, error: "passphrase-too-long" };
  return { ok: true, text };
}

function bytesToHex(bytes) {
  return [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function hexToBytes(hex) {
  const clean = String(hex || "");
  if (!clean || clean.length % 2 !== 0 || /[^0-9a-f]/i.test(clean)) return null;
  const out = new Uint8Array(clean.length / 2);
  for (let i = 0; i < out.length; i++) out[i] = parseInt(clean.slice(i * 2, i * 2 + 2), 16);
  return out;
}

async function hashPassphrase(text, saltBytes) {
  const salt = saltBytes || crypto.getRandomValues(new Uint8Array(16));
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(text),
    "PBKDF2",
    false,
    ["deriveBits"],
  );
  const bits = await crypto.subtle.deriveBits(
    { name: "PBKDF2", salt, iterations: PASSPHRASE_ITERS, hash: "SHA-256" },
    key,
    256,
  );
  return { salt: bytesToHex(salt), hash: bytesToHex(new Uint8Array(bits)) };
}

function timingSafeEqual(a, b) {
  const aa = String(a);
  const bb = String(b);
  const len = Math.max(aa.length, bb.length);
  let diff = aa.length ^ bb.length;
  for (let i = 0; i < len; i++) {
    const ca = i < aa.length ? aa.charCodeAt(i) : 0;
    const cb = i < bb.length ? bb.charCodeAt(i) : 0;
    diff |= ca ^ cb;
  }
  return diff === 0;
}

async function verifyPassphrase(text, saltHex, expectHex) {
  const salt = hexToBytes(saltHex);
  if (!salt || !salt.length || !expectHex) return false;
  const hashed = await hashPassphrase(text, salt);
  return timingSafeEqual(hashed.hash, String(expectHex));
}

function publicRoom(room) {
  const isPrivate = room.private === true;
  return {
    room_id: room.id,
    title: room.title || "",
    host_id: room.host_id || null,
    private: isPrivate,
    passphrase_required: isPrivate,
    member_count: (room.members || []).length,
    sealed: roomSealed(room),
    opened_at: nowIso(room.opened_at),
    expires_at: nowIso(room.expires_at),
    listed: true,
    e2e: false,
    entry: isPrivate ? "passphrase" : "open",
  };
}

export async function roomOpen(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const a = lookupHandle(src.token_a || src.handle_a);
  const b = lookupHandle(src.token_b || src.handle_b);
  if (!a || !b) {
    return { ok: false, status: 404, error: "handle-unlinked", op: "room_open" };
  }
  if (a.id === b.id) {
    return { ok: false, status: 400, error: "need-two-handles", op: "room_open" };
  }
  const ttl = roomTtl(src);
  const opened = nowMs();
  const id = nextId("r");
  const room = {
    id,
    members: [a.id, b.id],
    posts: [],
    opened_at: opened,
    expires_at: opened + ttl,
    ttl_ms: ttl,
    sealed: false,
    listed: false,
    private: false,
    title: "",
    host_id: null,
    passphrase_salt: null,
    passphrase_hash: null,
  };
  store.rooms.set(id, room);
  const receipt = await receiptOf({ op: "room_open", room_id: id, members: room.members, ttl_ms: ttl });
  return {
    ok: true,
    op: "room_open",
    room_id: id,
    members: room.members.slice(),
    ttl_ms: ttl,
    expires_at: nowIso(room.expires_at),
    sealed: false,
    listed: false,
    private: false,
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    receipt,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function roomPost(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const handle = lookupHandle(src.token || src.handle_token);
  const room = store.rooms.get(String(src.room_id || ""));
  if (!handle || !room || !room.members.includes(handle.id)) {
    return { ok: false, status: 404, error: "stranger-or-missing", op: "room_post" };
  }
  if (roomSealed(room)) {
    room.sealed = true;
    return { ok: false, status: 410, error: "room-sealed", op: "room_post", room_id: room.id, sealed: true };
  }
  const text = clip(src.text != null ? src.text : src.body);
  if (!text) return { ok: false, status: 400, error: "empty-post", op: "room_post" };
  const post = { id: nextId("p"), from: handle.id, text, ts: nowIso() };
  room.posts.push(post);
  const receipt = await receiptOf({ op: "room_post", room_id: room.id, post_id: post.id, from: handle.id });
  return {
    ok: true,
    op: "room_post",
    room_id: room.id,
    post,
    receipt,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function roomPull(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const handle = lookupHandle(src.token || src.handle_token);
  const room = store.rooms.get(String(src.room_id || ""));
  if (!handle || !room || !room.members.includes(handle.id)) {
    return { ok: false, status: 404, error: "stranger-or-missing", op: "room_pull" };
  }
  if (roomSealed(room)) room.sealed = true;
  return {
    ok: true,
    op: "room_pull",
    room_id: room.id,
    members: room.members.slice(),
    posts: room.posts.slice(),
    sealed: room.sealed,
    expires_at: nowIso(room.expires_at),
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export function roomList() {
  const rooms = [...store.rooms.values()].filter((room) => room.listed === true).map((room) => publicRoom(room));
  rooms.sort((a, b) => String(b.opened_at).localeCompare(String(a.opened_at)));
  return {
    ok: true,
    op: "room_list",
    count: rooms.length,
    rooms,
    note: "All hosted rooms. Pairwise room_open stays off this list. " + PRIVATE_NOTE,
    e2e: false,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function roomHost(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const host = lookupHandle(src.token || src.handle_token);
  if (!host) return { ok: false, status: 404, error: "handle-unlinked", op: "room_host" };
  const isPrivate = asBool(src.private);
  const supplied = src.passphrase;
  if (supplied != null && String(supplied).trim() && !isPrivate) {
    return {
      ok: false,
      status: 400,
      error: "private-flag-required",
      op: "room_host",
      note: "A passphrase was sent without private=true. The room was not created. " + PRIVATE_NOTE,
    };
  }
  let salt = null;
  let verifier = null;
  if (isPrivate) {
    const parsed = passphraseText(supplied);
    if (!parsed.ok) return { ok: false, status: 400, error: parsed.error, op: "room_host", note: PRIVATE_NOTE };
    const hashed = await hashPassphrase(parsed.text);
    salt = hashed.salt;
    verifier = hashed.hash;
  }
  const title = clip(src.title || "room", TITLE_CAP).trim() || "room";
  const ttl = roomTtl(src);
  const opened = nowMs();
  const id = nextId("r");
  const room = {
    id,
    members: [host.id],
    posts: [],
    opened_at: opened,
    expires_at: opened + ttl,
    ttl_ms: ttl,
    sealed: false,
    listed: true,
    private: isPrivate,
    title,
    host_id: host.id,
    passphrase_salt: salt,
    passphrase_hash: verifier,
  };
  store.rooms.set(id, room);
  const receipt = await receiptOf({
    op: "room_host",
    room_id: id,
    host_id: host.id,
    title,
    private: isPrivate,
    listed: true,
    ttl_ms: ttl,
  });
  return {
    ok: true,
    op: "room_host",
    room_id: id,
    title,
    host_id: host.id,
    private: isPrivate,
    passphrase_required: isPrivate,
    listed: true,
    e2e: false,
    members: [host.id],
    member_count: 1,
    ttl_ms: ttl,
    expires_at: nowIso(room.expires_at),
    sealed: false,
    receipt,
    note: isPrivate ? PRIVATE_NOTE : "Hosted room is on the all-rooms list. Entry is open to a live handle.",
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function roomJoin(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const handle = lookupHandle(src.token || src.handle_token);
  if (!handle) return { ok: false, status: 404, error: "handle-unlinked", op: "room_join" };
  const room = store.rooms.get(String(src.room_id || ""));
  if (!room || room.listed !== true) {
    return { ok: false, status: 404, error: "room-missing", op: "room_join" };
  }
  if (roomSealed(room)) {
    room.sealed = true;
    return { ok: false, status: 410, error: "room-sealed", op: "room_join", room_id: room.id, sealed: true };
  }
  const isPrivate = room.private === true;
  if (room.members.includes(handle.id)) {
    return {
      ok: true,
      op: "room_join",
      room_id: room.id,
      title: room.title || "",
      private: isPrivate,
      already_member: true,
      joined: false,
      e2e: false,
      note: isPrivate ? PRIVATE_NOTE : "Already a member of this hosted room.",
      author: AUTHOR,
      limitation: LIMITATION,
    };
  }
  if (isPrivate) {
    const parsed = passphraseText(src.passphrase);
    if (!parsed.ok && parsed.error === "passphrase-too-long") {
      return { ok: false, status: 403, error: "passphrase-too-long", op: "room_join", note: PRIVATE_NOTE };
    }
    if (!parsed.ok) {
      return { ok: false, status: 403, error: "passphrase-required", op: "room_join", note: PRIVATE_NOTE };
    }
    const okPass = await verifyPassphrase(parsed.text, room.passphrase_salt || "", room.passphrase_hash || "");
    if (!okPass) {
      return { ok: false, status: 403, error: "passphrase-rejected", op: "room_join", note: PRIVATE_NOTE };
    }
  }
  room.members.push(handle.id);
  const receipt = await receiptOf({ op: "room_join", room_id: room.id, handle_id: handle.id, private: isPrivate });
  return {
    ok: true,
    op: "room_join",
    room_id: room.id,
    title: room.title || "",
    private: isPrivate,
    already_member: false,
    joined: true,
    e2e: false,
    member_count: room.members.length,
    receipt,
    note: isPrivate ? PRIVATE_NOTE : "Joined the hosted room.",
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function busSend(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const from = clip(src.from || src.agent || "agent", 48);
  const to = clip(src.to || src.peer || "", 48);
  const text = clip(src.text != null ? src.text : src.body);
  if (!text) return { ok: false, status: 400, error: "empty-frame", op: "bus_send" };
  const frame = { id: nextId("b"), from, to, text, ts: nowIso() };
  store.bus.unshift(frame);
  if (store.bus.length > FRAME_CAP) store.bus.length = FRAME_CAP;
  const receipt = await receiptOf({ op: "bus_send", frame_id: frame.id, from, to });
  return {
    ok: true,
    op: "bus_send",
    frame,
    receipt,
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    azmail_bridge: false,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export function busPoll(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const agent = clip(src.agent || src.to || "", 48);
  const limit = Math.min(32, Math.max(1, Number(src.limit) || 16));
  const frames = store.bus
    .filter((f) => !agent || f.to === agent || f.from === agent || !f.to)
    .slice(0, limit);
  return {
    ok: true,
    op: "bus_poll",
    count: frames.length,
    frames,
    mesh_enabled_default: MESH_ENABLED_DEFAULT,
    azmail_bridge: false,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function verifyReceipt(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const receipt = src.receipt && typeof src.receipt === "object" ? src.receipt : src;
  const { receipt_sha256, ...rest } = receipt;
  const expect = await sha256Hex(JSON.stringify(rest));
  return {
    ok: true,
    op: "verify_receipt",
    match: Boolean(receipt_sha256) && receipt_sha256 === expect,
    receipt_sha256: expect,
    posted: receipt_sha256 || null,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export function importExport(payload) {
  const src = payload && typeof payload === "object" ? payload : {};
  const mode = String(src.mode || "export").toLowerCase();
  if (mode === "import") {
    return {
      ok: true,
      op: "import_export",
      mode: "import",
      accepted: true,
      stored: false,
      note: "Client-held JSON only. Hosted AZChat does not persist an import store.",
      author: AUTHOR,
      limitation: LIMITATION,
    };
  }
  return {
    ok: true,
    op: "import_export",
    mode: "export",
    handles_live: [...store.handles.values()].filter((h) => h.live).map((h) => h.id),
    rooms: [...store.rooms.values()].map((r) => ({
      id: r.id,
      members: r.members.slice(),
      sealed: roomSealed(r),
      listed: r.listed === true,
      private: r.private === true,
      title: r.title || "",
    })),
    bus_count: store.bus.length,
    stored: false,
    author: AUTHOR,
    limitation: LIMITATION,
  };
}

export async function dispatch(op, payload) {
  const name = String(op || "").trim().replace(/-/g, "_");
  if (STUB_OPS.includes(name)) return refuseStub(name);
  if (name === "health") return health();
  if (name === "doctor") return doctor();
  if (name === "skill") return skillBody();
  if (name === "handle_new") return handleNew(payload);
  if (name === "handle_rotate") return handleRotate(payload);
  if (name === "room_open") return roomOpen(payload);
  if (name === "room_post") return roomPost(payload);
  if (name === "room_pull") return roomPull(payload);
  if (name === "room_list") return roomList();
  if (name === "room_host") return roomHost(payload);
  if (name === "room_join") return roomJoin(payload);
  if (name === "bus_send") return busSend(payload);
  if (name === "bus_poll") return busPoll(payload);
  if (name === "verify_receipt" || name === "verify") return verifyReceipt(payload);
  if (name === "import_export") return importExport(payload);
  throw new RefuseError("unknown op: " + op);
}
