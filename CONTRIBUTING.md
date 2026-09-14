# Contributing to AZChat

**Forks are first-class.** This project is Apache-2.0; you do not need
permission to fork, patch, or redistribute. Pull requests are welcome
if you want a change upstream. Keep a fork forever if you do not.

**Forks are welcome and always allowed.**

## How to run tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q
```

Python 3.10+. Core is stdlib only (`hashlib`, `json`, `argparse`, `secrets`).
pytest is the dev extra. No network.

## Ground rules

1. **Identity is Aziel Eliab only.** Do not credit other names. Aziel Elroi Eliab is an allowed SEO aka.
2. **I1 Mesh hop default off.** GET `/v1/mesh` never enables.
3. **I2 Not SMTP.** Not a public MTA.
4. **I3 Not AZMail.** Do not bridge AZChat ↔ AZMail.
5. **I4** Stranger `room_pull` is 404.
6. **I5** FragGate is THE single door.
7. **I6** Identity is Aziel Eliab only.
8. **Door vs local op.** `/v1/fraggate/*`, `/v1/runtime/*`, and
    `/v1/mesh/*` PROXY to aziel-runtime. Local ops are `/v1/{op}` only.
    Never treat `fraggate/call` or `mesh/status` as a local op name.
    Suite mesh default OFF; QNM rollup live|locked|isolated; QNS-CD-1.0
    hub cite only (no public qnsd proxy); SPLIT THE WIRES + COLD-COPY
    SURVIVAL hub cites; no Node Gate; no auto-heal; not anonymity.
    Hop default off.
9. New behavior needs a test that fails without the change.

## Where to change things

- Engine: `azchat/engine.py`, `workers/download-tracker/src/engine.js`
- CLI: `azchat/cli.py`
- Local UI: `azchat/ui.py`
- Worker homepage: `workers/download-tracker/src/home.js`
- Suite mesh / QNM Live Nodes + QNS-CD-1.0 + SPLIT THE WIRES + COLD-COPY SURVIVAL: `workers/download-tracker/src/mesh.js`

## License of contributions

By submitting a change you agree it is licensed under Apache-2.0, the
same license as the rest of the tree. Keep the copyright lines honest.
Author: Aziel Eliab only.
