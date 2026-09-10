# AZC-CHAT-0.1 — AZChat

Spendable handles, ephemeral rooms, and an agent bus.

**Author:** Aziel Eliab only  
**Class:** Plain · slug `azchat` · domain Comms (07)  
**Door:** FragGate is THE single door.

## What this is

AZChat mints spendable handle tokens, opens ephemeral rooms between two
live handles, and carries an isolate-hash agent bus. Rooms seal on TTL.
A stranger `room_pull` is 404. Mesh hop default is off. GET `/v1/mesh`
never enables.

## What this is not

Not SMTP. Not a public MTA. Not AZMail. Do not bridge AZChat ↔ AZMail.
Not deanonymize. Not a Chromium chat runner. Not a hop mesh.

## Dual surface

The true engine is in-process on aziel-runtime 1.9.0 FragGate slug
`azchat`. This repository is the Softwares human door: Worker UI,
counted `/download`, Flutter `mobile/`, `install.sh`, and a thin
OpenAPI + MCP pointer at runtime FragGate.

## LIVE_OPS

health, skill, doctor, handle_new, handle_rotate, room_open, room_post,
room_pull, bus_send, bus_poll, verify_receipt, import_export.

Stubs refuse with `AZC-CHAT-REFUSE`.

## Neighbors

azmail (not bridged), aznet, peacelock.

Apache-2.0. Forks are welcome and always allowed.
