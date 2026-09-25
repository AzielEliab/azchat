# AZChat MCP notes

Agents do **not** treat MCP chrome as the product. FragGate is THE
single door.

## Canonical catalog door

1. `fraggate_list` or `GET https://aziel-runtime.vibelock.workers.dev/v1/software`
2. `fraggate_describe` slug `azchat`
3. `fraggate_call` `{ slug: "azchat", op, payload }`

Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`

Kernel: https://github.com/AzielEliab/fraggate

## This Worker (thin double)

`GET` / `POST` https://azchat-download-tracker.vibelock.workers.dev/mcp

JSON-RPC: `initialize`, `tools/list`, `tools/call`, `ping`.

Tools: `azchat_health`, `azchat_skill`, `azchat_doctor`,
`azchat_handle_new`, `azchat_handle_rotate`, `azchat_room_open`,
`azchat_room_post`, `azchat_room_pull`, `azchat_room_list`,
`azchat_room_host`, `azchat_room_join`, `azchat_bus_send`,
`azchat_bus_poll`, `azchat_verify_receipt`, `azchat_import_export`.

`room_list` returns hosted-room metadata only. `room_host` creates a
listed room. `room_join` fails closed on a private room when the
passphrase is missing or wrong. The passphrase is not returned and is
not on the public list. Private is not end-to-end encryption.

Stub tools (`smtp`, `bridge_azmail`, `mesh_enable`, …) refuse with
`AZC-CHAT-REFUSE`.

`/v1/fraggate/*` and `/v1/mesh/*` PROXY to aziel-runtime via the
`AZIEL_RUNTIME` service binding. GET `/v1/mesh` never enables.
SPLIT THE WIRES + COLD-COPY SURVIVAL are hub cites. Hop default off.

## Dual surface

Agent MCP (`POST /mcp` + catalog FragGate) **and** the human Worker UI
**and** counted `/download`. Agent output stays in the AI client
(`display.title` / `display.summary`). Humans keep the complete Worker
UI, Flutter `mobile/`, and counted `/download`. Do not gut either
surface.

## Cross-map (do not merge / do not bridge)

- aziel-runtime FragGate: `/v1/fraggate/list`, `/v1/fraggate/describe`,
  `/v1/fraggate/call`, `/v1/software`, `/mcp`
- AZMail / `azmail` — Comms neighbor, not bridged, not SMTP
- AZNet / `aznet` — Network neighbor
- PeaceLock / `peacelock` — Evidence neighbor
- Softwares hubs: azieleliab.com, azielcorpuslibrary.net, godlock.uk

Machine cites: `/cite.json`, `/llms.txt`.

Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude
(Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot /
Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence
surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other
MCP/OpenAPI-capable assistants.

Author: Aziel Eliab only.
