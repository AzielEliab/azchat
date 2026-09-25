# AZChat

Open short-lived rooms with spendable handles.

**Author:** Aziel Eliab only  
**Date:** September 2026 · v0.1.0  
**License:** [Apache-2.0](LICENSE)

## Start

1. Install: `python -m venv .venv && source .venv/bin/activate && pip install -e .`
2. Run: `azchat ui`
3. Open http://127.0.0.1:8878/

`azchat` with no arguments prints those next steps. `azchat doctor` checks this install.

## Commands

| Command | What it does |
| --- | --- |
| `azchat ui` | Open the local app on this computer |
| `azchat handle-new --label me` | Create a spendable handle |
| `azchat room-open` | Open a room with two handles |
| `azchat room-post` | Send a message into a room |
| `azchat room-pull` | Read messages in a room |
| `azchat doctor` | Check this install |
| `azchat --help` | Command list and examples |
| `azchat health --json` | Machine JSON |

Advanced commands stay available: `handle-rotate`, `bus-send`, `bus-poll`, `verify`, `export`, `stub`.

Commands share a session file on this computer (`~/.local/state/azchat/state.json`, or the `AZCHAT_STATE` path). `azchat ui` uses that same file. Set `AZCHAT_STATE=-` to keep a command from reading or writing it.

## One-click install

```bash
curl -fsSL https://azchat-download-tracker.vibelock.workers.dev/install.sh | bash
```

The script curls the **counted** tarball from this project's Worker
(`/download`, User-Agent `Mozilla/5.0`), extracts, makes a venv, and
`pip install -e .`. Then run `azchat ui` and open http://127.0.0.1:8878/.

Or use the live software homepage (workspace + counted download):
https://azchat-download-tracker.vibelock.workers.dev/

## Counted download (Cloudflare Worker)

**This is the counted download.** GitHub releases exist as a mirror.
The Worker serves the gzip itself (HTTP 200, no 302 to GitHub).

- Homepage: [https://azchat-download-tracker.vibelock.workers.dev/](https://azchat-download-tracker.vibelock.workers.dev/)
- Direct tarball: [azchat-0.1.0.tar.gz](https://azchat-download-tracker.vibelock.workers.dev/download?asset=azchat-0.1.0.tar.gz)
- One-click install: [https://azchat-download-tracker.vibelock.workers.dev/install.sh](https://azchat-download-tracker.vibelock.workers.dev/install.sh)
- Skill: [https://azchat-download-tracker.vibelock.workers.dev/v1/skill](https://azchat-download-tracker.vibelock.workers.dev/v1/skill)
- FragGate proxy: [list](https://azchat-download-tracker.vibelock.workers.dev/v1/fraggate/list) · describe · [call](https://azchat-download-tracker.vibelock.workers.dev/v1/fraggate/call) via AZIEL_RUNTIME
- Suite mesh proxy: [https://azchat-download-tracker.vibelock.workers.dev/v1/mesh](https://azchat-download-tracker.vibelock.workers.dev/v1/mesh) — default OFF; GET never enables; product-local `mesh_enable` is stub/REFUSE; QNM live / locked / isolated; QNS-CD-1.0 hub cite (photon QNS1; local qnsd in [qnm-node](https://github.com/AzielEliab/qnm-node); runtime catalog in [aziel-runtime](https://github.com/AzielEliab/aziel-runtime)). SPLIT THE WIRES (tip-only 0.5–1s tick; pull-only; update=proof; 777s dwell; 1s≠777s sockets). COLD-COPY SURVIVAL (multiply cold copies; refuse live body sync; tip expensive to erase; server pull cannot wipe cold replicas; hash-absolute poison refuse; data outlives creators). Not a Softwares-tab product. No public qnsd proxy. Hop default off.
- Worker MCP: [https://azchat-download-tracker.vibelock.workers.dev/mcp](https://azchat-download-tracker.vibelock.workers.dev/mcp) — GET docs / POST JSON-RPC (health/skill/doctor/handle_new/…)
- OpenAPI: [https://azchat-download-tracker.vibelock.workers.dev/openapi.json](https://azchat-download-tracker.vibelock.workers.dev/openapi.json)
- GitHub: [https://github.com/AzielEliab/azchat](https://github.com/AzielEliab/azchat)
- Cite: [cite.json](https://azchat-download-tracker.vibelock.workers.dev/cite.json) — Eliab, Aziel. (2026). AZChat 0.1.0 [Software]. Apache-2.0. No Zenodo DOI is invented here; a software deposit is still needed.

Isolated counter: Worker `azchat-download-tracker`, dedicated KV `AZCHAT_DOWNLOADS` (`01a3bbf8ad5e449eb0eb7648d75f8ae0`). Do not reuse other products' KV ids. `/v1` does not increment downloads.

Open http://127.0.0.1:8878 (loopback only). No CDN, no telemetry.

---

## Download

**Counted download page (this project only, ticks automatically):**

# → [https://azchat-download-tracker.vibelock.workers.dev/](https://azchat-download-tracker.vibelock.workers.dev/) ←

Direct tarball (also counted): [azchat-0.1.0.tar.gz](https://azchat-download-tracker.vibelock.workers.dev/download?asset=azchat-0.1.0.tar.gz)

- Live count JSON (`{project, views, downloads, total}`): [https://azchat-download-tracker.vibelock.workers.dev/count](https://azchat-download-tracker.vibelock.workers.dev/count)
- Stats: [https://azchat-download-tracker.vibelock.workers.dev/stats](https://azchat-download-tracker.vibelock.workers.dev/stats)
- GitHub releases: [https://github.com/AzielEliab/azchat/releases](https://github.com/AzielEliab/azchat/releases)

---

## Local UI

```bash
azchat ui
```

Open http://127.0.0.1:8878 on this computer only. The first screen has one
primary action. Rotate, the agent bus, receipt check, and export are under
Advanced. Hosted rooms are on the all-rooms list. A private room requires a
passphrase to join and is not end-to-end encryption. Catalog labels: Health /
Skill / Doctor / New handle / Rotate / Open room / Post / Pull / All rooms /
Host room / Join room / Bus send / Bus poll / Verify receipt / Import-export.

## Dual-surface law

1. **Agent / MCP.** The true engine is already live in-process on
   aziel-runtime 1.9.0 FragGate slug `azchat`. This repo Worker is the
   Softwares **human door** + counted `/download` + mesh peer.
2. **Human.** Complete Worker UI, Flutter sources under `mobile/`,
   `install.sh`, this README citing Worker `/download`. Forks allowed.
   OpenAPI + MCP are a thin door pointing at runtime FragGate.

Do not gut either surface. FragGate is THE single door.

## FragGate (catalog door + true engine)

Kernel: https://github.com/AzielEliab/fraggate  
Runtime: https://github.com/AzielEliab/aziel-runtime

```bash
curl -s -A 'Mozilla/5.0' https://aziel-runtime.vibelock.workers.dev/v1/fraggate/list
curl -s -A 'Mozilla/5.0' 'https://aziel-runtime.vibelock.workers.dev/v1/fraggate/describe?slug=azchat'
curl -s -A 'Mozilla/5.0' -X POST https://aziel-runtime.vibelock.workers.dev/v1/fraggate/call \
  -H 'content-type: application/json' \
  -d '{"slug":"azchat","op":"health","payload":{}}'
```

This Worker PROXY (same door, not a second door):
`GET /v1/fraggate/list`, `GET /v1/fraggate/describe`, `POST /v1/fraggate/call`
via service bind `AZIEL_RUNTIME` → `aziel-runtime`.

Hub Software tab: `GET https://aziel-runtime.vibelock.workers.dev/v1/software`

## LIVE_OPS

`health`, `skill`, `doctor`, `handle_new`, `handle_rotate`, `room_open`,
`room_post`, `room_pull`, `room_list`, `room_host`, `room_join`,
`bus_send`, `bus_poll`, `verify_receipt`, `import_export`.

`room_list`, `room_host`, and `room_join` are served by this Worker and
the local engine. This repository does not change the aziel-runtime
FragGate describe card.

Stubs (refuse `AZC-CHAT-REFUSE`): `smtp`, `smtp_send`, `send`, `mail`,
`deliver`, `deanonymize`, `harvest`, `mesh_join`, `mesh_enable`, `vpn`,
`bridge_azmail`, `bridge`, `chromium`.

Mesh default `false`. No bridge to AZMail. No SMTP.

## Use with AI assistants

Works with ChatGPT (GPT Actions / OpenAI), Grok (xAI), Venice, Claude (Anthropic), Cursor (MCP), Glama (MCP), Perplexity, Microsoft Copilot / Bing, Google Gemini / Vertex, Mistral, Meta AI, Apple Intelligence surfaces, Amazon Q tooling, DuckAssist, You.com, Cohere, and other MCP/OpenAPI-capable assistants.

Import the catalog or Worker `openapi.json` as a GPT Action, custom HTTP
tool, or custom OpenAPI tool. MCP clients (Cursor, Glama, Claude, and
others): `POST` this Worker `/mcp` (thin doubles of the human buttons) or
the catalog MCP endpoint (FragGate slug `azchat`).

- Worker OpenAPI: https://azchat-download-tracker.vibelock.workers.dev/openapi.json
- Catalog OpenAPI: https://aziel-runtime.vibelock.workers.dev/openapi.json
- Worker MCP: `POST https://azchat-download-tracker.vibelock.workers.dev/mcp`
- Catalog MCP: `POST https://aziel-runtime.vibelock.workers.dev/mcp`

Always send `User-Agent: Mozilla/5.0`.

## Suite peers — do not merge · do not bridge

- **aziel-runtime** — catalog + FragGate door + true AZChat engine.
  Paths: `/v1/fraggate/list`, `/v1/fraggate/describe`, `/v1/fraggate/call`,
  `/v1/software`, `/mcp`.
- **AZMail / azmail** — Comms neighbor. Mail airlock. **Do not bridge
  AZChat ↔ AZMail.** Not SMTP from this product.
  https://github.com/AzielEliab/azmail ·
  https://azmail-download-tracker.vibelock.workers.dev/
- **AZNet / aznet** — Network neighbor. Separate software.
- **PeaceLock / peacelock** — Evidence neighbor. Separate software.
- Softwares hubs: https://www.azieleliab.com/ ·
  https://www.azielcorpuslibrary.net/ · https://godlock.uk/

## Cloudflare

Worker name **must** be `azchat-download-tracker`.
Account `ac575a9b822bea2bed97d0ab73aed238`. `workers_dev = true`.
Dedicated DOWNLOADS KV `AZCHAT_DOWNLOADS` (`01a3bbf8ad5e449eb0eb7648d75f8ae0`)
— do not reuse other products' KV ids. Service bind `AZIEL_RUNTIME` →
`aziel-runtime`. Coordinator deploys if OAuth is missing.

## Scope

Not SMTP. Not AZMail. Do not bridge AZChat ↔ AZMail.

THIS IS: AZChat spendable handles, ephemeral rooms (TTL/sealed), and an
agent bus. Reached only through FragGate. mesh_enabled_default is false.
THIS IS NOT: SMTP, a public MTA, AZMail, a mesh hop, deanonymize, or a
Chromium chat runner. Do not bridge AZChat ↔ AZMail. Stranger room_pull
is 404. Hosted rooms appear on the all-rooms list. A private room requires
a passphrase to join and is not end-to-end encryption. Author: Aziel Eliab only.

Cite the GitHub repository and this Worker. No Zenodo DOI is invented
here; a software deposit is still needed.

Apache-2.0. Forks are welcome and always allowed.
