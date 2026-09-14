# azchat download tracker

Isolated Worker `azchat-download-tracker`. Project `azchat`.
v0.1.0 serves spendable handles, ephemeral rooms, and an agent bus (AZC-CHAT-0.1).
Dedicated KV namespace `AZCHAT_DOWNLOADS` bound as `DOWNLOADS` (`01a3bbf8ad5e449eb0eb7648d75f8ae0`).
Do **not** reuse other products' KV ids.
Does **not** 302 to GitHub on `/download`. Serves gzip via `ASSETS.fetch`,
`Cache-Control: private, no-store`.

GET `/` is the product homepage (Use UI + counted download). Increments a **page-view** counter (separate from downloads).
GET `/download` increments **downloads**.
GET `/count` returns `{project, views, downloads, total}` (`total` = downloads).
`/v1` never increments DOWNLOADS KV.
GET `/install.sh` one-click install (does not increment; script curls `/download`).
GET `/v1/skill` returns skill markdown (`text/markdown`). Does not increment views or downloads.
GET `/v1/fraggate/list`, GET `/v1/fraggate/describe`, POST `/v1/fraggate/call` PROXY to aziel-runtime via the `AZIEL_RUNTIME` service binding. Not local ops. `/v1/runtime/{list,describe,call}` aliases map to those door paths.
`/v1/mesh/*` PROXY to aziel-runtime suite mesh (AZIEL_RUNTIME). Default OFF. GET never enables. Product-local `mesh_enable` is stub/REFUSE. QNM-BUILD-1.0 live|locked|isolated. QNS-CD-1.0 photon QNS1 hub cite (local qnsd in https://github.com/AzielEliab/qnm-node ; runtime catalog in https://github.com/AzielEliab/aziel-runtime). SPLIT THE WIRES (STW-1.0) + COLD-COPY SURVIVAL (CCS-1.0) hub cites. Not a Softwares-tab product. No Node Gate. No public qnsd proxy. No auto-heal. Not anonymity. Human UI Live Nodes strip polls `GET /v1/mesh`. Hop default off.
GET `/mcp` returns dual-surface MCP docs + FragGate pointer (`slug=azchat`). Does not increment.
POST `/mcp` is JSON-RPC MCP-over-HTTP (`initialize`, `tools/list`, `tools/call`) doubling catalog labels health/skill/doctor/handle_new/handle_rotate/room_open/room_post/room_pull/bus_send/bus_poll/verify_receipt/import_export.
UI Health / Skill / Doctor / New handle / Rotate / Open room / Post / Pull / Bus send / Bus poll / Verify receipt / Import-export map to catalog LIVE_OPS.
GET `/cite.json`, `/sitemap.xml`, `/robots.txt`, `/llms.txt` are SEO / cite surfaces (suite peers + FragGate door + dual-surface law). Do not increment downloads.
Human UI shows Softwares-style peer links (AZMail not bridged, AZNet, PeaceLock, aziel-runtime, hubs) and the runtime FragGate call path (`POST /v1/fraggate/call` PROXY). Dual surface: agent MCP + human Worker UI + `/download`.

Not SMTP. Not AZMail. Do not bridge. Mesh hop default off. FragGate only.

Host: https://azchat-download-tracker.vibelock.workers.dev

Account `ac575a9b822bea2bed97d0ab73aed238`. `workers_dev = true`.
Do not wrangler-deploy from CI if OAuth is missing — coordinator deploys.

Author: Aziel Eliab. Apache-2.0.
