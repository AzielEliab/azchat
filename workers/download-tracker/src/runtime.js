/**
 * AZChat hosted runtime.
 * /v1 never touches DOWNLOADS KV.
 * Door paths (`/v1/fraggate/*`, `/v1/runtime/*`, `/v1/mesh/*`) PROXY to aziel-runtime via AZIEL_RUNTIME.
 * Local ops are single-segment `/v1/{op}` only.
 * Author: Aziel Eliab only.
 */
import { classifyV1Path, doorTargetUrl } from "./door.js";
import {
  LIVE_OPS,
  STUB_OPS,
  PRODUCT,
  SLUG,
  VERSION,
  SPEC,
  AUTHOR,
  MOTTO,
  ROLE,
  HONEST,
  LIMITATION,
  RefuseError,
  health as engineHealth,
  doctor as engineDoctor,
  skillMarkdown,
  skillBody,
  handleNew,
  handleRotate,
  roomOpen,
  roomPost,
  roomPull,
  busSend,
  busPoll,
  verifyReceipt,
  importExport,
  refuseStub,
} from "./engine.js";
import { attachMeshCites, attachQnsCd, meshOpenApiPaths, meshPointer } from "./mesh.js";

const HOST = "https://azchat-download-tracker.vibelock.workers.dev";
const CATALOG = "https://aziel-runtime.vibelock.workers.dev/";
const CATALOG_MCP = "https://aziel-runtime.vibelock.workers.dev/mcp";
const FRAGGATE_CALL = "https://aziel-runtime.vibelock.workers.dev/v1/fraggate/call";
const FRAGGATE_LIVE_OPS = LIVE_OPS.slice();
const FULL_CLIENTS =
  "Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.";

export const SKILL = skillMarkdown();

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, HEAD, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, MCP-Protocol-Version, mcp-session-id, User-Agent, Authorization",
  };
}

function json(body, status = 200) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...corsHeaders() },
  });
}

function examplePayload() {
  return {
    handle_new: { label: "agent-a" },
    room_open: { token_a: "<handle A token>", token_b: "<handle B token>", ttl_ms: 900000 },
    room_post: { token: "<member token>", room_id: "<room id>", text: "handles spend" },
    bus_send: { from: "agent-a", to: "agent-b", text: "poll the bus" },
    author: AUTHOR,
    spec: SPEC,
    note: "Mint two handles, then room_open with token_a + token_b. Stranger room_pull is 404. Mesh stays off.",
  };
}

function mcpInitialize() {
  return {
    protocolVersion: "2024-11-05",
    capabilities: { tools: {} },
    serverInfo: { name: "azchat", version: VERSION, title: "AZChat" },
    instructions: "AZChat is spendable handles, ephemeral rooms, and an agent bus. FragGate is THE single door. Prefer catalog POST " + CATALOG_MCP + " slug=azchat. Mesh hop default off. Not SMTP. Not AZMail. Do not bridge.",
  };
}

function mcpDocs() {
  return {
    product: PRODUCT,
    slug: SLUG,
    version: VERSION,
    author: AUTHOR,
    spec: SPEC,
    door: "fraggate",
    kv_increment: false,
    note: "GET /mcp documents the dual surface. POST /mcp is JSON-RPC thin doubles of catalog labels. Does not increment downloads. Canonical catalog MCP: " + CATALOG_MCP + " (FragGate slug azchat). Suite mesh: GET /v1/mesh PROXY (QNM-BUILD-1.0 live|locked|isolated; QNS-CD-1.0 hub cite; SPLIT THE WIRES; COLD-COPY SURVIVAL). Catalog MCP mesh_* + FragGate slug=mesh. Default OFF. GET never enables. No Node Gate. No auto-heal. No public qnsd proxy. Not anonymity.",
    catalog_mcp: CATALOG_MCP,
    agent_path: FRAGGATE_CALL,
    live_ops: FRAGGATE_LIVE_OPS,
    stub_ops: STUB_OPS.slice(),
    mesh: meshPointer(),
    clients: FULL_CLIENTS,
    honest: HONEST,
  };
}

const MCP_OPS = LIVE_OPS.slice().concat(["example"]);
const MCP_REFUSED = STUB_OPS.slice();

function mcpToolSchemas() {
  return [
    { name: "azchat_health", description: "Liveness. Same as GET /v1/health. FragGate LIVE_OPS.", inputSchema: { type: "object", properties: {} } },
    { name: "azchat_skill", description: "Skill markdown. Same as GET /v1/skill. FragGate LIVE_OPS.", inputSchema: { type: "object", properties: {} } },
    { name: "azchat_doctor", description: "Self-check. Same as GET /v1/doctor. FragGate LIVE_OPS.", inputSchema: { type: "object", properties: {} } },
    { name: "azchat_handle_new", description: "Mint a spendable handle. Same as POST /v1/handle_new.", inputSchema: { type: "object", properties: { label: { type: "string" }, agent: { type: "string" } } } },
    { name: "azchat_handle_rotate", description: "Rotate a handle token (unlinks the prior token).", inputSchema: { type: "object", properties: { token: { type: "string" }, handle_token: { type: "string" } } } },
    { name: "azchat_room_open", description: "Open an ephemeral room. Needs two live handle tokens.", inputSchema: { type: "object", properties: { token_a: { type: "string" }, token_b: { type: "string" }, handle_a: { type: "string" }, handle_b: { type: "string" }, ttl_ms: { type: "number" } } } },
    { name: "azchat_room_post", description: "Post into a room as a member. Stranger is 404.", inputSchema: { type: "object", properties: { token: { type: "string" }, handle_token: { type: "string" }, room_id: { type: "string" }, text: { type: "string" }, body: { type: "string" } } } },
    { name: "azchat_room_pull", description: "Pull room posts. Stranger room_pull is 404.", inputSchema: { type: "object", properties: { token: { type: "string" }, handle_token: { type: "string" }, room_id: { type: "string" } } } },
    { name: "azchat_bus_send", description: "Send an agent-bus frame. Not AZMail.", inputSchema: { type: "object", properties: { from: { type: "string" }, to: { type: "string" }, agent: { type: "string" }, peer: { type: "string" }, text: { type: "string" }, body: { type: "string" } } } },
    { name: "azchat_bus_poll", description: "Poll the agent bus.", inputSchema: { type: "object", properties: { agent: { type: "string" }, to: { type: "string" }, limit: { type: "number" } } } },
    { name: "azchat_verify_receipt", description: "Hash-walk a receipt. Same as POST /v1/verify_receipt.", inputSchema: { type: "object", properties: { receipt: { type: "object" }, receipt_sha256: { type: "string" } } } },
    { name: "azchat_import_export", description: "Client-held export/import. Hosted does not persist an import store.", inputSchema: { type: "object", properties: { mode: { type: "string" } } } },
    { name: "azchat_example", description: "Sample payloads. Same as GET /v1/example.", inputSchema: { type: "object", properties: {} } },
  ];
}

function resolveMcpOp(name) {
  if (typeof name !== "string" || !name) return null;
  const raw = name.trim();
  const stripped = raw.startsWith("azchat_") ? raw.slice("azchat_".length) : raw;
  if (MCP_OPS.includes(stripped)) return stripped;
  if (stripped === "verify") return "verify_receipt";
  return null;
}

function refusedMcpOp(name) {
  if (typeof name !== "string" || !name) return null;
  const raw = name.trim();
  const stripped = raw.startsWith("azchat_") ? raw.slice("azchat_".length) : raw;
  return MCP_REFUSED.includes(stripped) ? stripped : null;
}

async function runMcpOp(op, body) {
  const payload = body && typeof body === "object" ? body : {};
  if (op === "health") return engineHealth(meshPointer());
  if (op === "skill") return skillBody();
  if (op === "doctor") return engineDoctor();
  if (op === "example") return examplePayload();
  if (op === "handle_new") return handleNew(payload);
  if (op === "handle_rotate") return handleRotate(payload);
  if (op === "room_open") return roomOpen(payload);
  if (op === "room_post") return roomPost(payload);
  if (op === "room_pull") return roomPull(payload);
  if (op === "bus_send") return busSend(payload);
  if (op === "bus_poll") return busPoll(payload);
  if (op === "verify_receipt" || op === "verify") return verifyReceipt(payload);
  if (op === "import_export") return importExport(payload);
  throw new RefuseError("unknown op");
}

async function callMcpTool(name, args) {
  const refused = refusedMcpOp(name);
  if (refused) {
    const stub = refuseStub(refused);
    return {
      isError: true,
      content: [{ type: "text", text: JSON.stringify(stub, null, 2) }],
    };
  }
  const op = resolveMcpOp(name);
  if (!op) {
    return {
      isError: true,
      content: [{
        type: "text",
        text: JSON.stringify({
          ok: false,
          error: "Unknown MCP tool. Use azchat_health, azchat_skill, azchat_doctor, azchat_handle_new, azchat_handle_rotate, azchat_room_open, azchat_room_post, azchat_room_pull, azchat_bus_send, azchat_bus_poll, azchat_verify_receipt, azchat_import_export. Stub verbs refuse AZC-CHAT-REFUSE. Canonical catalog MCP: " + CATALOG_MCP + " slug=azchat.",
          door: "fraggate",
          slug: SLUG,
          agent_path: FRAGGATE_CALL,
        }, null, 2),
      }],
    };
  }
  try {
    if (op === "skill") return { content: [{ type: "text", text: SKILL }] };
    const data = await runMcpOp(op, args);
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  } catch (err) {
    return {
      isError: true,
      content: [{ type: "text", text: JSON.stringify({ ok: false, error: String(err.message || err), motto: MOTTO }, null, 2) }],
    };
  }
}

async function handleMcpJson(request) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }, 400);
  }
  const id = body && Object.prototype.hasOwnProperty.call(body, "id") ? body.id : null;
  const method = body && body.method;
  const params = (body && body.params) || {};
  if (method === "initialize") return json({ jsonrpc: "2.0", id, result: mcpInitialize() });
  if (method === "notifications/initialized" || method === "initialized") {
    return new Response(null, { status: 204, headers: corsHeaders() });
  }
  if (method === "ping") return json({ jsonrpc: "2.0", id, result: {} });
  if (method === "tools/list") return json({ jsonrpc: "2.0", id, result: { tools: mcpToolSchemas() } });
  if (method === "tools/call") {
    const name = params.name;
    const args = params.arguments && typeof params.arguments === "object" ? params.arguments : {};
    return json({ jsonrpc: "2.0", id, result: await callMcpTool(name, args) });
  }
  return json({
    jsonrpc: "2.0",
    id,
    error: { code: -32601, message: "Method not found. Use initialize, tools/list, tools/call." },
  });
}

async function handleMcp(request) {
  if (request.method === "GET" || request.method === "HEAD") {
    if (request.method === "HEAD") return new Response(null, { status: 200, headers: corsHeaders() });
    return json(mcpDocs());
  }
  if (request.method === "POST") return handleMcpJson(request);
  return json({ error: "method not allowed", hint: "GET or POST /mcp" }, 405);
}

function opPath(name) {
  return {
    post: {
      operationId: "azchat_" + name,
      summary: name.replace(/_/g, " "),
      tags: ["azchat"],
      requestBody: { content: { "application/json": { schema: { type: "object" } } } },
      responses: { "200": { description: "AZChat receipt" } },
    },
  };
}

function openapiSpec() {
  return {
    openapi: "3.0.3",
    info: {
      title: "AZChat",
      version: VERSION,
      description: HONEST + " " + FULL_CLIENTS + " FragGate slug azchat. Catalog MCP " + CATALOG_MCP + ". Suite mesh GET /v1/mesh PROXY (QNM-BUILD-1.0; QNS-CD-1.0 hub cite; SPLIT THE WIRES; COLD-COPY SURVIVAL; No Node Gate; No auto-heal; No public qnsd proxy).",
      contact: { name: AUTHOR, url: "https://github.com/AzielEliab/azchat" },
      license: { name: "Apache-2.0", url: "https://www.apache.org/licenses/LICENSE-2.0" },
    },
    servers: [{ url: HOST, description: "AZChat Worker" }, { url: CATALOG.replace(/\/$/, ""), description: "aziel-runtime catalog" }],
    paths: {
      "/v1/health": { get: { operationId: "azchat_health", summary: "Liveness. Does not increment downloads.", tags: ["azchat"], responses: { "200": { description: "health" } } } },
      "/v1/skill": { get: { operationId: "azchat_skill", summary: "Skill markdown. Does not increment downloads.", tags: ["azchat"], responses: { "200": { description: "markdown" } } } },
      "/v1/doctor": { get: { operationId: "azchat_doctor", summary: "Doctor self-check. FragGate LIVE_OPS.", tags: ["azchat"], responses: { "200": { description: "doctor" } } } },
      "/v1/example": { get: { operationId: "azchat_example", summary: "Sample payload.", tags: ["azchat"], responses: { "200": { description: "example" } } } },
      "/v1/handle_new": opPath("handle_new"),
      "/v1/handle_rotate": opPath("handle_rotate"),
      "/v1/room_open": opPath("room_open"),
      "/v1/room_post": opPath("room_post"),
      "/v1/room_pull": opPath("room_pull"),
      "/v1/bus_send": opPath("bus_send"),
      "/v1/bus_poll": opPath("bus_poll"),
      "/v1/verify_receipt": opPath("verify_receipt"),
      "/v1/import_export": opPath("import_export"),
      "/v1/smtp": opPath("smtp"),
      "/v1/bridge_azmail": opPath("bridge_azmail"),
      "/v1/mesh_enable": opPath("mesh_enable"),
      "/v1/fraggate/list": { get: { operationId: "azchat_fraggate_list_proxy", summary: "PROXY to aziel-runtime GET /v1/fraggate/list via AZIEL_RUNTIME. Not a local op.", tags: ["fraggate"], responses: { "200": { description: "catalog" } } } },
      "/v1/fraggate/describe": { get: { operationId: "azchat_fraggate_describe_proxy", summary: "PROXY to aziel-runtime GET /v1/fraggate/describe. Not a local op.", tags: ["fraggate"], responses: { "200": { description: "describe" } } } },
      "/v1/fraggate/call": { post: { operationId: "azchat_fraggate_call_proxy", summary: "PROXY to aziel-runtime POST /v1/fraggate/call. Not a local op.", tags: ["fraggate"], requestBody: { content: { "application/json": { schema: { type: "object" } } } }, responses: { "200": { description: "call" } } } },
      ...meshOpenApiPaths(),
    },
  };
}

function aiHtml() {
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>AZChat — AI assistants</title>
<meta name="author" content="Aziel Eliab">
<style>body{font:16px/1.5 system-ui;background:#0b0b0b;color:#e8e0d0;max-width:44rem;margin:0 auto;padding:2rem 1.2rem}a{color:#e6d19a}h2{color:#c9a227}</style>
</head><body>
<h1>AZChat</h1>
<p>Author: <strong>Aziel Eliab</strong> only. FragGate slug <code>azchat</code>.</p>
<h2>Use with AI assistants</h2>
<p>${FULL_CLIENTS}</p>
<h2>OpenAPI import</h2>
<p>Worker: <a href="/openapi.json">/openapi.json</a> · Catalog: <a href="https://aziel-runtime.vibelock.workers.dev/openapi.json">aziel-runtime OpenAPI</a></p>
<h2>MCP catalog</h2>
<p>This Worker <code>POST /mcp</code> or catalog <code>POST https://aziel-runtime.vibelock.workers.dev/mcp</code> (FragGate slug azchat). Agents prefer FragGate list → describe → call. Dual surface: do not gut the human UI.</p>
<p>${LIMITATION}</p>
</body></html>`;
}

function runtimeFetcher(env) {
  if (env && env.AZIEL_RUNTIME && typeof env.AZIEL_RUNTIME.fetch === "function") return env.AZIEL_RUNTIME;
  return null;
}

function isMeshCitePath(pathname) {
  const path = String(pathname || "").replace(/\/+$/, "") || "/";
  return path === "/v1/mesh" || path === "/v1/mesh/status" || path === "/v1/mesh/nodes";
}

async function decorateMeshCite(request, pathname, res, headers) {
  if (request.method === "HEAD" || request.method !== "GET") return null;
  if (!isMeshCitePath(pathname)) return null;
  const ctype = String(headers.get("content-type") || "").toLowerCase();
  if (!ctype.includes("json")) return null;
  try {
    const body = await res.clone().json();
    headers.delete("content-length");
    headers.set("X-Aziel-Qns-Cd", "QNS-CD-1.0");
    headers.set("X-Aziel-Stw", "STW-1.0");
    headers.set("X-Aziel-Ccs", "CCS-1.0");
    return new Response(JSON.stringify(attachMeshCites(body), null, 2), {
      status: res.status,
      statusText: res.statusText,
      headers,
    });
  } catch {
    return null;
  }
}

async function proxyDoor(request, url, env) {
  const dest = doorTargetUrl(url.pathname, request.url, env);
  if (!dest) return json({ ok: false, error: "not a door path", path: url.pathname, door: "fraggate" }, 404);
  const headers = new Headers();
  const pass = ["content-type", "accept", "authorization", "user-agent", "mcp-protocol-version", "mcp-session-id", "x-aziel-runtime-token"];
  for (const name of pass) {
    const v = request.headers.get(name);
    if (v) headers.set(name, v);
  }
  if (!headers.has("User-Agent")) headers.set("User-Agent", "Mozilla/5.0 AZChat/0.1.0");
  const init = { method: request.method, headers, redirect: "follow" };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = request.body;
    init.duplex = "half";
  }
  try {
    const fetcher = runtimeFetcher(env);
    const res = fetcher ? await fetcher.fetch(dest, init) : await fetch(dest, init);
    const outHeaders = new Headers(res.headers);
    for (const [k, v] of Object.entries(corsHeaders())) outHeaders.set(k, v);
    outHeaders.set("X-Aziel-Door", "proxy");
    outHeaders.set("X-Aziel-Door-Origin", dest);
    const decorated = await decorateMeshCite(request, url.pathname, res, outHeaders);
    if (decorated) return decorated;
    return new Response(res.body, { status: res.status, statusText: res.statusText, headers: outHeaders });
  } catch (exc) {
    return json({
      ok: false,
      error: "fraggate_proxy_failed",
      detail: String(exc).slice(0, 240),
      origin: dest,
      agent_path: FRAGGATE_CALL,
      door: "fraggate",
      slug: SLUG,
    }, 502);
  }
}

async function readBody(request) {
  try { return await request.json(); } catch { return {}; }
}

export async function handleRuntimeApi(request, url, env) {
  const stripped = url.pathname.replace(/\/+$/, "") || "/";
  if (stripped === "/mcp") {
    try {
      return await handleMcp(request);
    } catch (err) {
      return json({ error: String(err.message || err), motto: MOTTO, ok: false }, 400);
    }
  }
  const classified = classifyV1Path(url.pathname);
  if (classified.kind === "door") return proxyDoor(request, url, env);
  const path = url.pathname;
  const isApi = path === "/v1" || path.startsWith("/v1/") || path === "/openapi.json" || path === "/ai";
  if (!isApi) return null;
  if (classified.kind === "multi") {
    return json({
      ok: false,
      error: "not a local op",
      code: "NOT_LOCAL_OP",
      path: classified.path,
      hint: "Local ops are GET|POST /v1/{op} only (single segment). FragGate door is /v1/fraggate/list, /v1/fraggate/describe, /v1/fraggate/call (proxied to aziel-runtime via AZIEL_RUNTIME). Suite mesh is /v1/mesh/* (proxied to aziel-runtime; default OFF). Product-local mesh_enable is stub/REFUSE.",
      agent_path: FRAGGATE_CALL,
      live_ops: FRAGGATE_LIVE_OPS,
    }, 404);
  }
  try {
    if (path === "/v1/health" && request.method === "GET") return json(engineHealth(meshPointer()));
    if (path === "/v1/skill" && request.method === "GET") {
      return new Response(SKILL, { status: 200, headers: { "Content-Type": "text/markdown; charset=utf-8", "Cache-Control": "private, no-store", ...corsHeaders() } });
    }
    if (path === "/openapi.json" && request.method === "GET") return json(openapiSpec());
    if (path === "/ai" && request.method === "GET") {
      return new Response(aiHtml(), { headers: { "Content-Type": "text/html; charset=utf-8", ...corsHeaders() } });
    }
    if (path === "/v1/doctor" && request.method === "GET") return json(engineDoctor());
    if (path === "/v1/example" && request.method === "GET") return json(examplePayload());
    const localOp = classified.kind === "local" ? classified.op : null;
    if (localOp && STUB_OPS.includes(localOp) && (request.method === "POST" || request.method === "GET")) {
      return json(refuseStub(localOp));
    }
    if (path === "/v1/handle_new" && request.method === "POST") return json(await handleNew(await readBody(request)));
    if (path === "/v1/handle_rotate" && request.method === "POST") return json(await handleRotate(await readBody(request)));
    if (path === "/v1/room_open" && request.method === "POST") return json(await roomOpen(await readBody(request)));
    if (path === "/v1/room_post" && request.method === "POST") return json(await roomPost(await readBody(request)));
    if (path === "/v1/room_pull" && request.method === "POST") return json(await roomPull(await readBody(request)));
    if (path === "/v1/bus_send" && request.method === "POST") return json(await busSend(await readBody(request)));
    if (path === "/v1/bus_poll" && request.method === "POST") return json(busPoll(await readBody(request)));
    if ((path === "/v1/verify_receipt" || path === "/v1/verify") && request.method === "POST") return json(await verifyReceipt(await readBody(request)));
    if (path === "/v1/import_export" && request.method === "POST") return json(importExport(await readBody(request)));
    return json({
      error: "not found",
      hint: "GET /v1/health GET /v1/skill GET /v1/doctor POST /v1/{handle_new,handle_rotate,room_open,room_post,room_pull,bus_send,bus_poll,verify_receipt,import_export} GET /v1/fraggate/list GET /v1/fraggate/describe POST /v1/fraggate/call GET /v1/mesh",
      live_ops: FRAGGATE_LIVE_OPS,
      role: ROLE,
    }, 404);
  } catch (err) {
    return json({ error: String(err.message || err), motto: MOTTO, ok: false }, 400);
  }
}
