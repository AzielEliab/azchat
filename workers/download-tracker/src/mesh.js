/**
 * Suite node mesh — QNM-BUILD-1.0 Live Nodes contract.
 * QNS-CD-1.0 hub cite: photon QNS1 packet transfer (local qnsd in qnm-node).
 * Default OFF. Public rollup is live|locked|isolated counts only.
 * No Node Gate. No public qnsd proxy. No auto-heal. Not an anonymity network.
 * /v1/mesh/* PROXY to aziel-runtime (AZIEL_RUNTIME binding).
 * Not a Softwares-tab product — hub cite / Worker mesh cross-map only.
 * Product-local mesh_enable is stub/REFUSE. AZChat mesh hop default off.
 * SPLIT THE WIRES (STW-1.0) + COLD-COPY SURVIVAL (CCS-1.0) are hub cites.
 * Author: Aziel Eliab only.
 */

const RUNTIME = "https://aziel-runtime.vibelock.workers.dev";
const FRAGGATE_MCP = "https://aziel-runtime.vibelock.workers.dev/mcp";
const FRAGGATE_CALL = "https://aziel-runtime.vibelock.workers.dev/v1/fraggate/call";
const IDENTITY = "Aziel Eliab";

export const QNM_SPEC = "QNM-BUILD-1.0";
export const MESH_KERNEL = "NM-0.1";
export const MESH_DEFAULT_OFF = true;
export const MESH_ANONYMITY_NETWORK = false;
export const MESH_NODE_GATE = false;
export const MESH_AUTO_HEAL = false;
export const MESH_IDENTITY = IDENTITY;
export const MESH_SLUG = "mesh";
export const MESH_PRODUCT = "azchat";
export const MESH_PATH = "/v1/mesh";
export const MESH_STATUS_PATH = "/v1/mesh/status";
export const MESH_NODES_PATH = "/v1/mesh/nodes";
export const MESH_ENABLE_PATH = "/v1/mesh/enable";
export const MESH_DISABLE_PATH = "/v1/mesh/disable";
export const MESH_JOIN_PATH = "/v1/mesh/join";
export const MESH_HEARTBEAT_PATH = "/v1/mesh/heartbeat";
export const MESH_LEAVE_PATH = "/v1/mesh/leave";
export const MESH_BROADCAST_PATH = "/v1/mesh/broadcast";
export const ANON_BROADCAST = "https://github.com/AzielEliab/anon-broadcast";

/** QNS-CD-1.0 — photon QNS1 packet transfer. Hub cite / Worker mesh cross-map only. */
export const QNS_CD_SPEC = "QNS-CD-1.0";
export const QNS_CD_NAME = "photon QNS1 packet transfer";
export const QNS_PHOTON = "QNS1 1.3";
export const QNS_MAGIC = "QNS1";
export const QNS_PROCESS = "qnsd";
export const QNSD_REPO = "https://github.com/AzielEliab/qnm-node";
export const QNS_CD_RUNTIME = "https://github.com/AzielEliab/aziel-runtime";
export const QNS_CD_DESIGNS = "https://github.com/AzielEliab/aziel-runtime/tree/main/docs/designs";
export const QNS_CD_PAPER = "https://github.com/AzielEliab/aziel-runtime/blob/main/docs/designs/QNS-CD-1.0.md";
export const QNS_CD_MESH_DOCS = "https://github.com/AzielEliab/aziel-runtime/blob/main/docs/NODE_MESH.md";
export const QNS_CD_PAIR_CUSTODY = "https://github.com/AzielEliab/azinterface";
export const QNS_CD_PUBLIC_PROXY = false;
export const QNS_CD_SOFTWARE_TAB = false;

export const QNS_CD = Object.freeze({
  spec: QNS_CD_SPEC,
  name: QNS_CD_NAME,
  kind: "hub_cite",
  local: QNSD_REPO,
  note: "Photon vias on local qnsd; Worker cites only",
  photon: QNS_PHOTON,
  magic: QNS_MAGIC,
  process: QNS_PROCESS,
  bind: "127.0.0.1",
  companion: Object.freeze(["QNM-BUILD-1.0", "AIH-WP-1.3"]),
  hub_companion: "AIH-WP-1.1",
  software_tab: false,
  softwares_tab: false,
  fraggate_slug: false,
  public_proxy: false,
  public_qnsd_proxy: false,
  emit: false,
  wipe: false,
  control_plane: false,
  loopback_only: true,
  qnsd: false,
  node_gate: false,
  default_off: true,
  paper: "docs/designs/QNS-CD-1.0.md",
  paper_url: QNS_CD_PAPER,
  path: "/v1/qns",
  local_qnsd: "qnm-node/",
  qnsd_repo: QNSD_REPO,
  runtime: QNS_CD_RUNTIME,
  runtime_docs: QNS_CD_MESH_DOCS,
  runtime_designs: QNS_CD_DESIGNS,
  qnm_docs: QNSD_REPO + "/blob/main/docs/QNM-BUILD-1.0.md",
  pair_custody: QNS_CD_PAIR_CUSTODY,
  identity: IDENTITY,
  author: IDENTITY,
});

/** SPLIT THE WIRES — two sockets. Tip tick ≠ dwell. Hop default off. Cite only. */
export const STW_SPEC = "STW-1.0";
export const STW_NAME = "SPLIT THE WIRES";
export const STW_TIP_TICK_MS_MIN = 500;
export const STW_TIP_TICK_MS_MAX = 1000;
export const STW_DWELL_S = 777;
export const STW_DWELL_MS = 777000;
export const STW_TIP_ONLY = true;
export const STW_PULL_ONLY = true;
export const STW_UPDATE_IS_PROOF = true;
export const STW_UPDATE_IS_TIMER = false;
export const STW_EQUIVOCATION_ENDS_PEER = true;
export const STW_EMIT_LAST_LOCAL = true;
export const STW_PHOENIX_LOCAL_ONLY = true;
export const STW_AUTO_SPLICE = false;
export const STW_HEARTBEAT_LOSS_IS_POISON = false;
export const STW_SOCKETS_EQUAL = false;
export const STW_HOP_DEFAULT_OFF = true;
export const STW_TIP_SOCKET = "tip";
export const STW_DWELL_SOCKET = "dwell";

export const STW_LAW = Object.freeze([
  "tip-only 0.5–1s tick",
  "pull-only payload",
  "update=proof not timer",
  "777s dwell after valid cite",
  "equivocation ends peer",
  "emit last locally",
  "Phoenix local only",
  "partition no auto-splice",
  "heartbeat loss≠poison",
  "1s≠777s sockets",
]);

export const STW = Object.freeze({
  spec: STW_SPEC,
  name: STW_NAME,
  kind: "hub_cite",
  software_tab: false,
  hop_default_off: true,
  tip_only: true,
  tip_tick_ms_min: STW_TIP_TICK_MS_MIN,
  tip_tick_ms_max: STW_TIP_TICK_MS_MAX,
  pull_only: true,
  update_is_proof: true,
  update_is_timer: false,
  dwell_s: STW_DWELL_S,
  dwell_ms: STW_DWELL_MS,
  equivocation_ends_peer: true,
  emit_last_local: true,
  phoenix_local_only: true,
  auto_splice: false,
  heartbeat_loss_is_poison: false,
  sockets_equal: false,
  tip_socket: STW_TIP_SOCKET,
  dwell_socket: STW_DWELL_SOCKET,
  law: STW_LAW,
  identity: IDENTITY,
  author: IDENTITY,
  note: "SPLIT THE WIRES. Tip-only 0.5–1s tick. Pull-only payload. Update=proof not timer. 777s dwell after valid cite. Equivocation ends peer. Emit last locally. Phoenix local only. Partition no auto-splice. Heartbeat loss≠poison. 1s≠777s sockets. AZChat mesh hop default off. Cite only.",
});

/** COLD-COPY SURVIVAL — replicas outlive the live body and the creators. Cite only. */
export const CCS_SPEC = "CCS-1.0";
export const CCS_NAME = "COLD-COPY SURVIVAL";
export const CCS_MULTIPLY_COLD_COPIES = true;
export const CCS_MIN_COLD_COPIES = 2;
export const CCS_LIVE_BODY_SYNC = false;
export const CCS_TIP_EXPENSIVE_TO_ERASE = true;
export const CCS_SERVER_PULL_WIPES_COLD = false;
export const CCS_HASH_ABSOLUTE_POISON_REFUSE = true;
export const CCS_DATA_OUTLIVES_CREATORS = true;
export const CCS_HOP_DEFAULT_OFF = true;

export const CCS_LAW = Object.freeze([
  "multiply cold copies",
  "refuse live body sync",
  "tip expensive to erase",
  "server pull cannot wipe cold replicas",
  "hash-absolute poison refuse",
  "data outlives creators",
]);

export const CCS = Object.freeze({
  spec: CCS_SPEC,
  name: CCS_NAME,
  kind: "hub_cite",
  software_tab: false,
  hop_default_off: true,
  multiply_cold_copies: true,
  min_cold_copies: CCS_MIN_COLD_COPIES,
  live_body_sync: false,
  tip_expensive_to_erase: true,
  server_pull_wipes_cold: false,
  hash_absolute_poison_refuse: true,
  data_outlives_creators: true,
  law: CCS_LAW,
  companion: Object.freeze(["STW-1.0", "QNM-BUILD-1.0"]),
  keeps_split_wires: true,
  identity: IDENTITY,
  author: IDENTITY,
  note: "COLD-COPY SURVIVAL. Multiply cold copies. Refuse live body sync. Tip expensive to erase. Server pull cannot wipe cold replicas. Hash-absolute poison refuse. Data outlives creators. Keeps SPLIT THE WIRES. AZChat mesh hop default off. Cite only.",
});

export const MESH_NOTE =
  "QNM-BUILD-1.0. QNS-CD-1.0 photon QNS1 packet transfer (hub cite / Worker mesh cross-map only). SPLIT THE WIRES (STW-1.0). COLD-COPY SURVIVAL (CCS-1.0). Suite mesh default off. Live|locked|isolated counts only. No Node Gate. No public qnsd proxy. No auto-heal. Not an anonymity network. AZChat mesh hop default off. Author: Aziel Eliab only.";

export const MESH_OPS = Object.freeze([
  "status",
  "enable",
  "disable",
  "join",
  "heartbeat",
  "leave",
  "nodes",
  "broadcast",
]);

export const MESH_PROXY_ROUTES = Object.freeze([
  { path: MESH_PATH, methods: ["get", "head"], op: "status", summary: "PROXY to aziel-runtime GET /v1/mesh. Suite mesh status. Default OFF. QNS-CD-1.0 hub cite attached. Not a local op. Not a qnsd proxy." },
  { path: MESH_STATUS_PATH, methods: ["get"], op: "status", summary: "PROXY alias of GET /v1/mesh. QNS-CD-1.0 hub cite attached. Not a local op." },
  { path: MESH_NODES_PATH, methods: ["get"], op: "nodes", summary: "PROXY to aziel-runtime GET /v1/mesh/nodes. Live Nodes (5-minute presence) + QNS-CD-1.0 cross-map. Not a local op. Not a qnsd proxy." },
  { path: MESH_ENABLE_PATH, methods: ["post"], op: "enable", summary: "PROXY to aziel-runtime POST /v1/mesh/enable. Operator bearer required. Rate-limited. Not a local op." },
  { path: MESH_DISABLE_PATH, methods: ["post"], op: "disable", summary: "PROXY to aziel-runtime POST /v1/mesh/disable. Always allowed. Not a local op." },
  { path: MESH_JOIN_PATH, methods: ["post"], op: "join", summary: "PROXY to aziel-runtime POST /v1/mesh/join. Body {product, node_id?, label?, presence?}. Refused while OFF. Not a local op." },
  { path: MESH_HEARTBEAT_PATH, methods: ["post"], op: "heartbeat", summary: "PROXY to aziel-runtime POST /v1/mesh/heartbeat. Body {node_id}. Not a local op." },
  { path: MESH_LEAVE_PATH, methods: ["post"], op: "leave", summary: "PROXY to aziel-runtime POST /v1/mesh/leave. Body {node_id}. Not a local op." },
  { path: MESH_BROADCAST_PATH, methods: ["post"], op: "broadcast", summary: "PROXY to aziel-runtime POST /v1/mesh/broadcast. SHA-256 receipt only. Not AnonBroadcast upload. Not a local op." },
]);

function firstNum(...vals) {
  for (const raw of vals) {
    if (raw == null || raw === "") continue;
    const n = typeof raw === "number" ? raw : Number(String(raw).replace(/,/g, ""));
    if (Number.isFinite(n) && n >= 0) return Math.floor(n);
  }
  return null;
}

function asList(value) {
  if (!value) return [];
  if (Array.isArray(value)) return value;
  if (typeof value === "object") return Object.values(value);
  return [];
}

function truthyEnabled(value) {
  if (value === true || value === 1) return true;
  const s = String(value || "").trim().toLowerCase();
  return s === "on" || s === "enabled" || s === "true" || s === "live";
}

export function emptyRollup() {
  return { live: 0, locked: 0, isolated: 0 };
}

export function meshRollup(mesh) {
  const m = mesh && typeof mesh === "object" ? mesh : {};
  const r = m.rollup && typeof m.rollup === "object" && !Array.isArray(m.rollup) ? m.rollup : {};
  return {
    live: firstNum(r.live, m.live_nodes, m.live) ?? 0,
    locked: firstNum(r.locked, m.locked_nodes, m.locked) ?? 0,
    isolated: firstNum(r.isolated, m.isolated_nodes, m.isolated) ?? 0,
  };
}

function parseRollup(inner, listedLive) {
  const r = inner.rollup && typeof inner.rollup === "object" && !Array.isArray(inner.rollup)
    ? inner.rollup
    : {};
  const live = firstNum(
    r.live,
    r.live_nodes,
    r.live_count,
    inner.live,
    inner.live_nodes,
    inner.mesh_live_nodes,
    inner.live_count,
    inner.count,
    inner.n,
    inner.node_count,
    listedLive,
  );
  const locked = firstNum(r.locked, r.locked_nodes, r.locked_count, inner.locked, inner.locked_nodes, inner.locked_count);
  const isolated = firstNum(r.isolated, r.isolated_nodes, r.isolated_count, inner.isolated, inner.isolated_nodes, inner.isolated_count);
  return {
    live: live != null ? live : 0,
    locked: locked != null ? locked : 0,
    isolated: isolated != null ? isolated : 0,
  };
}

export function emptyMesh(extra = {}) {
  const rollup = extra.rollup && typeof extra.rollup === "object"
    ? { ...emptyRollup(), ...extra.rollup }
    : emptyRollup();
  return {
    ok: true,
    spec: QNM_SPEC,
    kernel: MESH_KERNEL,
    enabled: false,
    default_off: true,
    live_nodes: 0,
    status: extra.status || "off",
    source: extra.source || "fallback",
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    note: MESH_NOTE,
    door: MESH_PATH,
    qns_cd_spec: QNS_CD_SPEC,
    qns_cd: QNS_CD,
    stw_spec: STW_SPEC,
    split_the_wires: STW,
    ccs_spec: CCS_SPEC,
    cold_copy_survival: CCS,
    ...extra,
    spec: QNM_SPEC,
    rollup,
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    qns_cd_spec: QNS_CD_SPEC,
    qns_cd: QNS_CD,
    stw_spec: STW_SPEC,
    split_the_wires: STW,
    ccs_spec: CCS_SPEC,
    cold_copy_survival: CCS,
  };
}

export function compactMeshNode(raw) {
  if (raw == null) return null;
  if (typeof raw === "string") {
    const id = raw.trim();
    return id ? { id } : null;
  }
  if (typeof raw !== "object") return null;
  const id = String(raw.id || raw.node_id || raw.session_id || raw.peer || raw.name || "").trim();
  const product = String(raw.product || raw.slug || raw.suite || "").trim();
  const seen = raw.last_utc || raw.last_seen || raw.seen_utc || raw.heartbeat_utc || "";
  if (!id && !product && !seen) return null;
  const out = {};
  if (id) out.id = id;
  if (product) out.product = product;
  if (seen) out.last_utc = String(seen);
  return out;
}

export function parseMeshDoc(body) {
  if (body == null) return emptyMesh({ status: "unavailable", source: "empty" });
  if (typeof body !== "object" || Array.isArray(body)) {
    return emptyMesh({ status: "unavailable", source: "empty" });
  }
  const inner = body.result && typeof body.result === "object" && !Array.isArray(body.result)
    ? { ...body, ...body.result }
    : (body.mesh && typeof body.mesh === "object" && !Array.isArray(body.mesh)
      ? { ...body, ...body.mesh }
      : body);
  const listed = asList(inner.nodes || inner.list || inner.peers || inner.live_nodes_list)
    .map(compactMeshNode)
    .filter(Boolean);
  const rollup = parseRollup(inner, listed.length ? listed.length : null);
  const enabled = truthyEnabled(inner.enabled)
    || truthyEnabled(inner.mesh_enabled)
    || String(inner.status || "").toLowerCase() === "on";
  const unavailable = inner.ok === false
    && !enabled
    && (inner.error || inner.status === "unavailable" || inner.status === "not_found");
  const status = enabled ? "on" : (unavailable ? "unavailable" : "off");
  const live = enabled ? rollup.live : 0;
  const locked = enabled ? rollup.locked : 0;
  const isolated = enabled ? rollup.isolated : 0;
  const products = asList(inner.products_present || inner.products)
    .map((p) => (typeof p === "string" ? p : (p && (p.product || p.slug || p.name)) || ""))
    .map((s) => String(s).trim())
    .filter(Boolean);
  return emptyMesh({
    ok: inner.ok !== false,
    enabled,
    default_off: inner.default_off !== false,
    live_nodes: live,
    rollup: { live, locked, isolated },
    products_present: products,
    nodes: listed,
    status,
    source: inner.source || "parsed",
    door: inner.door || MESH_PATH,
    note: enabled
      ? "QNM-BUILD-1.0. QNS-CD-1.0 photon QNS1 packet transfer. SPLIT THE WIRES. COLD-COPY SURVIVAL. Suite mesh is on. Live|locked|isolated counts only. No Node Gate. No public qnsd proxy. No auto-heal. Not an anonymity network. AZChat hop stays off unless suite radios are on."
      : MESH_NOTE,
  });
}

export function publicMesh(mesh) {
  const m = mesh && typeof mesh === "object" ? mesh : emptyMesh();
  const enabled = !!m.enabled;
  const rollup = enabled ? meshRollup(m) : emptyRollup();
  return {
    spec: QNM_SPEC,
    kernel: MESH_KERNEL,
    enabled,
    default_off: m.default_off !== false,
    live_nodes: enabled ? rollup.live : 0,
    rollup,
    status: enabled ? "on" : (m.status === "unavailable" ? "unavailable" : "off"),
    source: m.source || "fallback",
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    door: MESH_PATH,
    status_path: MESH_STATUS_PATH,
    nodes_path: MESH_NODES_PATH,
    join: MESH_JOIN_PATH,
    heartbeat: MESH_HEARTBEAT_PATH,
    enable: MESH_ENABLE_PATH,
    disable: MESH_DISABLE_PATH,
    leave: MESH_LEAVE_PATH,
    broadcast: MESH_BROADCAST_PATH,
    mcp: FRAGGATE_MCP,
    fraggate: FRAGGATE_CALL,
    slug: MESH_SLUG,
    product: MESH_PRODUCT,
    ops: MESH_OPS.slice(),
    origin: RUNTIME + MESH_PATH,
    note: m.note || MESH_NOTE,
    qns_cd_spec: QNS_CD_SPEC,
    qns_cd: QNS_CD,
    stw_spec: STW_SPEC,
    split_the_wires: STW,
    ccs_spec: CCS_SPEC,
    cold_copy_survival: CCS,
  };
}

export function meshStatusLine(mesh) {
  const m = mesh && typeof mesh === "object" ? mesh : emptyMesh();
  if (m.enabled) {
    const r = meshRollup(m);
    return "Suite mesh: on · live " + r.live + " · locked " + r.locked + " · isolated " + r.isolated + ". QNS-CD-1.0. SPLIT THE WIRES. COLD-COPY SURVIVAL. Not an anonymity network.";
  }
  if (m.status === "unavailable") {
    return "Suite mesh: off (unavailable). QNM-BUILD-1.0. QNS-CD-1.0. SPLIT THE WIRES. COLD-COPY SURVIVAL. Not an anonymity network.";
  }
  return "Suite mesh: off (default). QNM-BUILD-1.0. QNS-CD-1.0. SPLIT THE WIRES. COLD-COPY SURVIVAL. Not an anonymity network.";
}

/** Public Live Nodes count. Never auto-heal a visiting floor. */
export function alignLiveNodes({ mesh } = {}) {
  if (mesh && mesh.enabled) return meshRollup(mesh).live;
  return 0;
}

/** Hub cite only. Does not start qnsd or enable mesh. */
export function attachQnsCd(doc) {
  if (doc == null || typeof doc !== "object" || Array.isArray(doc)) {
    return { qns_cd_spec: QNS_CD_SPEC, qns_cd: QNS_CD };
  }
  return { ...doc, qns_cd_spec: QNS_CD_SPEC, qns_cd: QNS_CD };
}

/** Hub cite only. Does not enable hop radios. */
export function attachSplitTheWires(doc) {
  if (doc == null || typeof doc !== "object" || Array.isArray(doc)) {
    return { stw_spec: STW_SPEC, split_the_wires: STW };
  }
  return { ...doc, stw_spec: STW_SPEC, split_the_wires: STW };
}

/** Hub cite only. Does not wipe cold replicas. Does not enable hop radios. */
export function attachColdCopySurvival(doc) {
  if (doc == null || typeof doc !== "object" || Array.isArray(doc)) {
    return { ccs_spec: CCS_SPEC, cold_copy_survival: CCS };
  }
  return { ...doc, ccs_spec: CCS_SPEC, cold_copy_survival: CCS };
}

export function attachMeshCites(doc) {
  return attachColdCopySurvival(attachSplitTheWires(attachQnsCd(doc)));
}

export function stwTipTickOk(ms) {
  const n = Number(ms);
  return Number.isFinite(n) && n >= STW_TIP_TICK_MS_MIN && n <= STW_TIP_TICK_MS_MAX;
}

export function stwPayloadOk(mode) {
  return String(mode || "").trim().toLowerCase() === "pull";
}

export function stwUpdateOk(kind) {
  const k = String(kind || "").trim().toLowerCase();
  return k === "proof" || k === "cite";
}

export function stwDwellOpen(citeUtc, nowUtc) {
  const cite = Date.parse(citeUtc);
  const now = nowUtc == null ? Date.now() : Date.parse(nowUtc);
  if (!Number.isFinite(cite) || !Number.isFinite(now)) return false;
  return (now - cite) >= 0 && (now - cite) < STW_DWELL_MS;
}

export function stwEquivocationEndsPeer(tipA, tipB) {
  if (tipA == null || tipB == null) return false;
  const a = String(tipA).trim();
  const b = String(tipB).trim();
  return a !== "" && b !== "" && a !== b;
}

export function stwEmitLastScope(scope) {
  return String(scope || "").trim().toLowerCase() === "local";
}

export function stwPhoenixOk(scope) {
  return String(scope || "").trim().toLowerCase() === "local";
}

export function stwPartitionSpliceOk() {
  return false;
}

export function stwHeartbeatLossIsPoison() {
  return false;
}

export function stwSocketsSplit(tipSocket, dwellSocket) {
  const tip = String(tipSocket || "").trim();
  const dwell = String(dwellSocket || "").trim();
  if (!tip || !dwell) return false;
  return tip !== dwell;
}

export function stwHopDefaultOff() {
  return STW_HOP_DEFAULT_OFF && MESH_DEFAULT_OFF;
}

function stwRefuse(code, reason) {
  return {
    ok: false,
    refuse: true,
    spec: STW_SPEC,
    name: STW_NAME,
    code,
    reason,
    hop_default_off: true,
    author: IDENTITY,
  };
}

function stwPass(code, extra = {}) {
  return {
    ok: true,
    refuse: false,
    spec: STW_SPEC,
    name: STW_NAME,
    code,
    hop_default_off: true,
    author: IDENTITY,
    ...extra,
  };
}

export function evaluateSplitTheWires(event = {}) {
  const e = event && typeof event === "object" && !Array.isArray(event) ? event : {};
  const kind = String(e.kind || e.op || "").trim().toLowerCase();
  if (e.hop === true || e.enable_hop === true || kind === "hop") {
    return stwRefuse("STW-HOP-DEFAULT-OFF", "AZChat mesh hop default off.");
  }
  if (kind === "tick" || kind === "tip_tick") {
    if (!stwTipTickOk(e.ms != null ? e.ms : e.tick_ms)) {
      return stwRefuse("STW-TIP-TICK", "tip-only 0.5–1s tick");
    }
    if (e.payload && String(e.payload).toLowerCase() !== "tip") {
      return stwRefuse("STW-TIP-ONLY", "tip-only 0.5–1s tick");
    }
    return stwPass("STW-TIP-TICK");
  }
  if (kind === "payload" || kind === "body") {
    if (!stwPayloadOk(e.mode || e.payload_mode)) {
      return stwRefuse("STW-PULL-ONLY", "pull-only payload");
    }
    return stwPass("STW-PULL-ONLY");
  }
  if (kind === "update") {
    const via = e.update || e.via || e.proof_kind;
    if (String(via || "").toLowerCase() === "timer") {
      return stwRefuse("STW-UPDATE-PROOF", "update=proof not timer");
    }
    if (!stwUpdateOk(via)) {
      return stwRefuse("STW-UPDATE-PROOF", "update=proof not timer");
    }
    return stwPass("STW-UPDATE-PROOF");
  }
  if (kind === "dwell") {
    if (!e.cite) return stwRefuse("STW-DWELL", "777s dwell after valid cite");
    return stwPass("STW-DWELL", { dwell_open: stwDwellOpen(e.cite, e.now) });
  }
  if (kind === "equivocation") {
    if (stwEquivocationEndsPeer(e.tip_a, e.tip_b)) {
      return stwPass("STW-EQUIVOCATION-END-PEER", { end_peer: true });
    }
    return stwPass("STW-EQUIVOCATION-NONE", { end_peer: false });
  }
  if (kind === "emit_last") {
    if (!stwEmitLastScope(e.scope)) return stwRefuse("STW-EMIT-LAST-LOCAL", "emit last locally");
    return stwPass("STW-EMIT-LAST-LOCAL");
  }
  if (kind === "phoenix") {
    if (!stwPhoenixOk(e.scope)) return stwRefuse("STW-PHOENIX-LOCAL", "Phoenix local only");
    return stwPass("STW-PHOENIX-LOCAL");
  }
  if (kind === "splice" || kind === "partition_splice") {
    return stwRefuse("STW-NO-AUTO-SPLICE", "partition no auto-splice");
  }
  if (kind === "heartbeat_loss") {
    return stwPass("STW-HEARTBEAT-LOSS-NOT-POISON", { poison: false, suspect: true });
  }
  if (kind === "socket") {
    if (!stwSocketsSplit(e.tip_socket || e.tip, e.dwell_socket || e.dwell)) {
      return stwRefuse("STW-SOCKETS-SPLIT", "1s≠777s sockets");
    }
    return stwPass("STW-SOCKETS-SPLIT");
  }
  return stwRefuse("STW-UNKNOWN", "unknown SPLIT THE WIRES event");
}

export function ccsColdCopiesOk(copies) {
  if (!Array.isArray(copies)) return false;
  const ids = copies.map((c) => {
    if (c == null) return "";
    if (typeof c === "string") return c.trim();
    return String(c.id || c.hash || c.path || "").trim();
  }).filter(Boolean);
  return new Set(ids).size >= CCS_MIN_COLD_COPIES;
}

export function ccsLiveBodySyncOk() {
  return false;
}

export function ccsTipEraseOk(effort) {
  const e = String(effort || "").trim().toLowerCase();
  if (!e || e === "cheap" || e === "timer" || e === "server_pull" || e === "wipe") return false;
  return e === "local_operator" || e === "expensive";
}

export function ccsServerPullWipesCold() {
  return false;
}

export function ccsHashAbsolutePoisonRefuse(hash, poisonSet) {
  const h = String(hash || "").trim().toLowerCase();
  if (!h) return true;
  const set = Array.isArray(poisonSet) ? poisonSet : (poisonSet ? [poisonSet] : []);
  return set.map((p) => String(p).trim().toLowerCase()).includes(h);
}

export function ccsDataOutlivesCreators() {
  return true;
}

function ccsRefuse(code, reason) {
  return {
    ok: false,
    refuse: true,
    spec: CCS_SPEC,
    name: CCS_NAME,
    code,
    reason,
    hop_default_off: true,
    keeps_split_wires: true,
    author: IDENTITY,
  };
}

function ccsPass(code, extra = {}) {
  return {
    ok: true,
    refuse: false,
    spec: CCS_SPEC,
    name: CCS_NAME,
    code,
    hop_default_off: true,
    keeps_split_wires: true,
    author: IDENTITY,
    ...extra,
  };
}

export function evaluateColdCopySurvival(event = {}) {
  const e = event && typeof event === "object" && !Array.isArray(event) ? event : {};
  const kind = String(e.kind || e.op || "").trim().toLowerCase();
  if (e.hop === true || e.enable_hop === true || kind === "hop") {
    return ccsRefuse("CCS-HOP-DEFAULT-OFF", "AZChat mesh hop default off.");
  }
  if (kind === "live_body_sync" || kind === "sync_live") {
    return ccsRefuse("CCS-NO-LIVE-BODY-SYNC", "refuse live body sync");
  }
  if (kind === "multiply" || kind === "cold_copies") {
    if (!ccsColdCopiesOk(e.copies || e.replicas)) {
      return ccsRefuse("CCS-MULTIPLY-COLD", "multiply cold copies");
    }
    return ccsPass("CCS-MULTIPLY-COLD");
  }
  if (kind === "erase_tip" || kind === "tip_erase") {
    if (!ccsTipEraseOk(e.effort || e.via)) {
      return ccsRefuse("CCS-TIP-EXPENSIVE", "tip expensive to erase");
    }
    return ccsPass("CCS-TIP-EXPENSIVE");
  }
  if (kind === "server_pull" || kind === "pull_wipe") {
    if (e.wipe === true || e.wipe_cold === true || kind === "pull_wipe") {
      return ccsRefuse("CCS-SERVER-PULL-NO-WIPE", "server pull cannot wipe cold replicas");
    }
    return ccsPass("CCS-SERVER-PULL-NO-WIPE", { wipe_cold: false });
  }
  if (kind === "poison") {
    if (ccsHashAbsolutePoisonRefuse(e.hash, e.poison || e.poison_set)) {
      return ccsRefuse("CCS-HASH-ABSOLUTE-POISON", "hash-absolute poison refuse");
    }
    return ccsPass("CCS-POISON-MISS");
  }
  if (kind === "creator_gone" || kind === "outlive") {
    return ccsPass("CCS-DATA-OUTLIVES-CREATORS", { outlives: true });
  }
  return ccsRefuse("CCS-UNKNOWN", "unknown COLD-COPY SURVIVAL event");
}

export function meshPointer() {
  return {
    pointer: true,
    path: MESH_PATH,
    enabled_default: false,
    spec: QNM_SPEC,
    kernel: MESH_KERNEL,
    rollup: "live|locked|isolated",
    node_gate: false,
    auto_heal: false,
    anonymity_network: false,
    author: MESH_IDENTITY,
    identity: MESH_IDENTITY,
    catalog_mcp: FRAGGATE_MCP,
    fraggate_slug: MESH_SLUG,
    origin: RUNTIME + MESH_PATH,
    note: "PROXY to aziel-runtime /v1/mesh/* via AZIEL_RUNTIME. Not a local op. Not AnonBroadcast. Not AZMail's product-local ring. AZChat mesh hop default off. Product-local mesh_enable is stub/REFUSE. GET /v1/mesh never enables. Full node process is local qnm-node/. QNS-CD-1.0 photon QNS1 packet transfer is a hub cite only — local qnsd lives in qnm-node; no public qnsd proxy. SPLIT THE WIRES + COLD-COPY SURVIVAL hub cites. " + MESH_NOTE,
    anon_broadcast: ANON_BROADCAST,
    anon_broadcast_publish_path: false,
    qns_cd_spec: QNS_CD_SPEC,
    qns_cd: QNS_CD,
    stw_spec: STW_SPEC,
    split_the_wires: STW,
    ccs_spec: CCS_SPEC,
    cold_copy_survival: CCS,
  };
}

export function meshOpenApiPaths() {
  const paths = {};
  for (const route of MESH_PROXY_ROUTES) {
    const entry = paths[route.path] || {};
    for (const method of route.methods) {
      entry[method] = {
        operationId: "azchat_mesh_" + route.op + (method === "head" ? "_head" : "") + "_proxy",
        summary: route.summary,
        tags: ["mesh"],
        responses: { "200": { description: "aziel-runtime mesh envelope" } },
      };
      if (method === "post") {
        entry[method].requestBody = { content: { "application/json": { schema: { type: "object" } } } };
      }
    }
    paths[route.path] = entry;
  }
  return paths;
}
