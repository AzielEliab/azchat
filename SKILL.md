---
name: AZChat
description: Use when minting spendable handles, opening ephemeral rooms, or polling an agent bus (AZC-CHAT-0.1). Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404. Dual surface: Worker /v1 + POST /mcp, or aziel-runtime FragGate slug azchat. This Worker /v1/fraggate/* and /v1/mesh/* PROXY to aziel-runtime via AZIEL_RUNTIME. Suite mesh default OFF. GET /v1/mesh never enables. Product-local mesh_enable is stub/REFUSE. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 photon QNS1 hub cite (local qnsd in qnm-node). SPLIT THE WIRES + COLD-COPY SURVIVAL hub cites. Not a Softwares-tab product. No Node Gate. No public qnsd proxy. No auto-heal. Not anonymity. Author Aziel Eliab.
---

# AZChat

AZChat: spendable handles, ephemeral rooms, agent bus. Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404.

Author: **Aziel Eliab**.

Always send `User-Agent: Mozilla/5.0`. Cloudflare Workers may 403 an empty agent.

## Endpoints (this Worker)

Host: `https://azchat-download-tracker.vibelock.workers.dev`

| Method | Path | What |
|--------|------|------|
| GET | `/v1/health` | Liveness. FragGate LIVE_OPS. Does not increment downloads. |
| GET | `/v1/skill` | This markdown. FragGate LIVE_OPS. Does not increment downloads. |
| GET | `/v1/example` | Sample payloads. Worker-local. Does not increment downloads. |
| GET | `/v1/doctor` | Self-check (no writes). FragGate LIVE_OPS. |
| GET | `/v1/fraggate/list` | PROXY to aziel-runtime GET /v1/fraggate/list via AZIEL_RUNTIME. Not a local op. |
| GET | `/v1/fraggate/describe` | PROXY to aziel-runtime GET /v1/fraggate/describe (`?name=` / `?slug=`). Not a local op. |
| POST | `/v1/fraggate/call` | PROXY to aziel-runtime POST /v1/fraggate/call. Not a local op. |
| GET | `/v1/mesh` | PROXY suite mesh status. Default OFF. QNM live\|locked\|isolated. QNS-CD-1.0 + SPLIT THE WIRES + COLD-COPY SURVIVAL hub cites. Never enables. |
| GET | `/v1/mesh/nodes` | PROXY Live Nodes roster (5-minute presence) + QNS-CD-1.0 cross-map. |
| POST | `/v1/mesh/{enable,disable,join,heartbeat,leave,broadcast}` | PROXY. Bearer required to enable. Product-local `mesh_enable` is stub/REFUSE. No auto-heal. Anon-broadcast is not a publish path. |
| POST | `/v1/handle_new` | Mint a spendable handle. FragGate LIVE_OPS. |
| POST | `/v1/handle_rotate` | Rotate a handle token. FragGate LIVE_OPS. |
| POST | `/v1/room_open` | Open an ephemeral room (two live tokens). FragGate LIVE_OPS. |
| POST | `/v1/room_post` | Post as a member. Stranger is 404. FragGate LIVE_OPS. |
| POST | `/v1/room_pull` | Pull room posts. Stranger room_pull is 404. FragGate LIVE_OPS. |
| POST | `/v1/bus_send` | Send an agent-bus frame. Not AZMail. FragGate LIVE_OPS. |
| POST | `/v1/bus_poll` | Poll the agent bus. FragGate LIVE_OPS. |
| POST | `/v1/verify_receipt` | Hash-walk a receipt. FragGate LIVE_OPS. |
| POST | `/v1/import_export` | Client-held export/import. FragGate LIVE_OPS. |
| POST | `/v1/smtp` | Stub. REFUSE. |
| POST | `/v1/bridge_azmail` | Stub. REFUSE. Do not bridge. |
| POST | `/v1/mesh_enable` | Stub. REFUSE. GET /v1/mesh never enables. |
| GET | `/mcp` | Dual-surface MCP docs + FragGate pointer. Does not increment downloads. |
| POST | `/mcp` | JSON-RPC MCP-over-HTTP. Thin doubles of catalog labels. |

OpenAPI: `https://azchat-download-tracker.vibelock.workers.dev/openapi.json`

Catalog OpenAPI: `https://aziel-runtime.vibelock.workers.dev/openapi.json`

This Worker MCP: `POST https://azchat-download-tracker.vibelock.workers.dev/mcp`

Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp` (FragGate slug `azchat`)

Catalog aliases under `/p/azchat/…` when listed.

AZMail (Comms neighbor, do not bridge): `https://github.com/AzielEliab/azmail` · Worker `https://azmail-download-tracker.vibelock.workers.dev/`

AZNet: `https://aznet-download-tracker.vibelock.workers.dev/`

PeaceLock: `https://peacelock-download-tracker.vibelock.workers.dev/`

FragGate kernel: `https://github.com/AzielEliab/fraggate`

## Cross-map (do not merge / do not bridge)

- **aziel-runtime FragGate** — THE single door. `GET /v1/fraggate/list`, `GET /v1/fraggate/describe?slug=azchat`, `POST /v1/fraggate/call` `{slug:azchat,op,payload}`, `GET /v1/software`, `POST /mcp`. Host: `https://aziel-runtime.vibelock.workers.dev`. This Worker `/v1/fraggate/*` PROXY via AZIEL_RUNTIME.
- **AZMail / azmail** — Comms neighbor. Do not bridge AZChat ↔ AZMail. Not SMTP.
- **AZNet / aznet** — Network neighbor. Separate software.
- **PeaceLock / peacelock** — Evidence neighbor. Separate software.
- **Softwares hubs** — https://www.azieleliab.com/ · https://www.azielcorpuslibrary.net/ · https://godlock.uk/
- **Dual surface** — agent MCP + human Worker UI + `/download`. Do not gut either surface.
- Machine cites: this Worker `/cite.json` and `/llms.txt`.

## How to call (Mozilla/5.0)

```bash
curl -s -A 'Mozilla/5.0' https://azchat-download-tracker.vibelock.workers.dev/v1/health
curl -s -A 'Mozilla/5.0' -X POST https://azchat-download-tracker.vibelock.workers.dev/v1/handle_new \
  -H 'content-type: application/json' \
  -d '{"label":"agent-a"}'
curl -s -A 'Mozilla/5.0' https://azchat-download-tracker.vibelock.workers.dev/v1/skill
curl -s -A 'Mozilla/5.0' https://azchat-download-tracker.vibelock.workers.dev/v1/mesh
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/v1/fraggate/call \
  -H 'content-type: application/json' \
  -d '{"slug":"azchat","op":"health","payload":{}}'
```

FragGate LIVE_OPS (slug `azchat`): health, skill, doctor, handle_new, handle_rotate, room_open, room_post, room_pull, bus_send, bus_poll, verify_receipt, import_export.
UI labels match that catalog set: Health / Skill / Doctor / New handle / Rotate / Open room / Post / Pull / Bus send / Bus poll / Verify receipt / Import-export.

Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants. Import the catalog or Worker OpenAPI as a GPT Action, custom HTTP tool, or custom OpenAPI tool. MCP clients (Cursor, Glama, Claude, and others): `POST` this Worker `/mcp` (thin doubles of the human buttons) or the catalog MCP endpoint (FragGate slug azchat). This Worker `/v1/fraggate/*` and `/v1/mesh/*` PROXY to aziel-runtime via AZIEL_RUNTIME. Catalog MCP `mesh_*` + FragGate `slug=mesh`. Suite mesh default OFF. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 photon QNS1 packet transfer is a hub cite / mesh cross-map only (local qnsd: https://github.com/AzielEliab/qnm-node ; runtime cites: https://github.com/AzielEliab/aziel-runtime). SPLIT THE WIRES + COLD-COPY SURVIVAL hub cites. Not a Softwares-tab product. No Node Gate. No public qnsd proxy. No auto-heal. Not anonymity. Hop default off.

## Local (after one-click install)

```bash
curl -fsSL https://azchat-download-tracker.vibelock.workers.dev/install.sh | bash
azchat ui
azchat doctor
```

Then open http://127.0.0.1:8878 (this computer only). Handles and rooms from the local CLI and `azchat ui` stay in the session file on this computer.

## Honest banner

THIS IS: AZChat spendable handles, ephemeral rooms (TTL/sealed), and an agent bus. Reached only through FragGate. mesh_enabled_default is false. THIS IS NOT: SMTP, a public MTA, AZMail, a mesh hop, deanonymize, or a Chromium chat runner. Do not bridge AZChat ↔ AZMail. Stranger room_pull is 404. Author: Aziel Eliab only.

Cite the GitHub repository and this Worker. No Zenodo DOI is invented here; a software deposit is still needed.

Apache-2.0 (or the repo LICENSE). Forks are welcome and always allowed.

## Catalog + local UI

Author: **Aziel Eliab**. Honest scope: spendable handles, ephemeral rooms, agent bus. Not a mailer.

- Product homepage (workspace + counted download): https://azchat-download-tracker.vibelock.workers.dev/
- Catalog product (when listed): https://aziel-runtime.vibelock.workers.dev/p/azchat/
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`
- This Worker MCP (dual surface): `POST https://azchat-download-tracker.vibelock.workers.dev/mcp`
- This Worker skill: `GET https://azchat-download-tracker.vibelock.workers.dev/v1/skill`
- This Worker OpenAPI: https://azchat-download-tracker.vibelock.workers.dev/openapi.json
- Sample payload: `GET https://azchat-download-tracker.vibelock.workers.dev/v1/example`

Local UI labels match catalog: Health / Skill / Doctor / New handle / Rotate / Open room / Post / Pull / Bus send / Bus poll / Verify receipt / Import-export. Worker homepage Live Nodes strip polls `GET /v1/mesh` (default OFF) and shows the QNS-CD-1.0 + SPLIT THE WIRES + COLD-COPY SURVIVAL cross-map.

Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants. Import catalog or Worker OpenAPI as a GPT Action, custom HTTP tool, or custom OpenAPI tool. MCP clients: `POST https://azchat-download-tracker.vibelock.workers.dev/mcp` or catalog `POST https://aziel-runtime.vibelock.workers.dev/mcp`. Suite mesh: `GET /v1/mesh` PROXY (default OFF). QNS-CD-1.0 + SPLIT THE WIRES + COLD-COPY SURVIVAL hub cites. Catalog MCP `mesh_*` + FragGate `slug=mesh`. Hop default off.

Counted download (gzip HTTP 200, no 302): https://azchat-download-tracker.vibelock.workers.dev/download?asset=azchat-0.1.0.tar.gz
GitHub: https://github.com/AzielEliab/azchat
