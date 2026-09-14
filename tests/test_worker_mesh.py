"""Suite mesh Live Nodes + QNM-BUILD-1.0 + QNS-CD-1.0 cross-map.

Default OFF. live|locked|isolated. No Node Gate. No public qnsd proxy.
No auto-heal. Not anonymity. Hub cite only — not a Softwares-tab product.
AZChat hop default off.
SPLIT THE WIRES + COLD-COPY SURVIVAL hub cites.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MESH = (ROOT / "workers/download-tracker/src/mesh.js").read_text(encoding="utf-8")
DOOR = (ROOT / "workers/download-tracker/src/door.js").read_text(encoding="utf-8")
RUNTIME = (ROOT / "workers/download-tracker/src/runtime.js").read_text(encoding="utf-8")
HOME = (ROOT / "workers/download-tracker/src/home.js").read_text(encoding="utf-8")
INDEX = (ROOT / "workers/download-tracker/src/index.js").read_text(encoding="utf-8")
WRANGLER = (ROOT / "workers/download-tracker/wrangler.toml").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
WORKER_README = (ROOT / "workers/download-tracker/README.md").read_text(encoding="utf-8")


def test_mesh_contract_default_off_qnm_law() -> None:
    assert 'QNM_SPEC = "QNM-BUILD-1.0"' in MESH
    assert "MESH_DEFAULT_OFF = true" in MESH
    assert "MESH_ANONYMITY_NETWORK = false" in MESH
    assert "MESH_NODE_GATE = false" in MESH
    assert "MESH_AUTO_HEAL = false" in MESH
    assert 'MESH_IDENTITY = IDENTITY' in MESH or '"Aziel Eliab"' in MESH
    assert 'MESH_PRODUCT = "azchat"' in MESH
    assert 'MESH_PATH = "/v1/mesh"' in MESH
    assert "live|locked|isolated" in MESH
    assert "enabled_default: false" in MESH
    assert "anon_broadcast_publish_path: false" in MESH
    assert "Aziel Eliab" in MESH
    assert 'QNS_CD_SPEC = "QNS-CD-1.0"' in MESH
    assert "export const QNS_CD" in MESH
    assert "photon QNS1 packet transfer" in MESH
    assert "QNS1 1.3" in MESH
    assert "https://github.com/AzielEliab/qnm-node" in MESH
    assert "https://github.com/AzielEliab/aziel-runtime" in MESH
    assert "https://github.com/AzielEliab/azinterface" in MESH
    assert "docs/designs/QNS-CD-1.0.md" in MESH
    assert "QNS-CD-1.0" in MESH
    assert "QNS_CD_PUBLIC_PROXY = false" in MESH
    assert "QNS_CD_SOFTWARE_TAB = false" in MESH
    assert "public_qnsd_proxy: false" in MESH
    assert "public_proxy: false" in MESH
    assert "software_tab: false" in MESH
    assert "softwares_tab: false" in MESH
    assert "Photon vias on local qnsd" in MESH
    assert "No public qnsd proxy" in MESH
    assert "QNS-CD-1.0" in MESH.split("export const MESH_NOTE")[1].split("export const MESH_OPS")[0]


def test_mesh_pointer_and_openapi_helpers() -> None:
    assert "export function meshPointer" in MESH
    assert "export function meshOpenApiPaths" in MESH
    assert "export function parseMeshDoc" in MESH
    assert "export function emptyMesh" in MESH
    assert "export function alignLiveNodes" in MESH
    assert "export function attachQnsCd" in MESH
    assert "export function attachSplitTheWires" in MESH
    assert "export function attachColdCopySurvival" in MESH
    assert "export function attachMeshCites" in MESH
    assert "fraggate_slug: MESH_SLUG" in MESH
    assert "azchat_mesh_" in MESH
    assert "qns_cd_spec: QNS_CD_SPEC" in MESH
    assert "qns_cd: QNS_CD" in MESH


def test_door_proxies_mesh_via_aziel_runtime() -> None:
    assert '"mesh"' in DOOR
    assert 'path === "/v1/mesh"' in DOOR
    assert 'path.startsWith("/v1/mesh/")' in DOOR
    assert "AZIEL_RUNTIME" in WRANGLER
    assert "aziel-runtime" in WRANGLER
    assert "/v1/mesh/*" in WRANGLER or "/v1/mesh" in WRANGLER


def test_runtime_advertises_mesh_proxy_and_pointer() -> None:
    assert 'from "./mesh.js"' in RUNTIME
    assert "meshPointer" in RUNTIME
    assert "meshOpenApiPaths" in RUNTIME
    assert "...meshOpenApiPaths()" in RUNTIME
    assert "mesh: meshPointer()" in RUNTIME
    assert "/v1/mesh" in RUNTIME
    assert "QNM-BUILD-1.0" in RUNTIME
    assert "QNS-CD-1.0" in RUNTIME
    assert "attachQnsCd" in RUNTIME
    assert "decorateMeshCite" in RUNTIME
    assert "No Node Gate" in RUNTIME
    assert "No auto-heal" in RUNTIME
    assert "No public qnsd proxy" in RUNTIME
    assert "handleRuntimeApi(request, url, env)" in INDEX
    assert "/v1/qnsd" not in RUNTIME
    assert "/v1/qnsd" not in MESH
    assert "/v1/qnsd" not in DOOR


def test_home_live_nodes_strip_no_node_gate() -> None:
    assert 'id="meshStrip"' in HOME
    assert 'id="meshLiveCount"' in HOME
    assert 'id="meshLine"' in HOME
    assert "Live Nodes" in HOME
    assert "QNM-BUILD-1.0" in HOME
    assert "QNS-CD-1.0" in HOME
    assert "No Node Gate" in HOME
    assert "No public qnsd proxy" in HOME
    assert "No auto-heal" in HOME
    assert "Not an anonymity network" in HOME
    assert "not a Softwares-tab product" in HOME
    assert "/v1/mesh" in HOME
    assert 'product: "azchat"' in HOME
    assert 'id="node-gate"' not in HOME
    assert 'href="/node-gate"' not in HOME
    assert "auto-heal this node" not in HOME


def test_docs_advertise_mesh_proxy() -> None:
    assert "/v1/mesh" in README
    assert "/v1/mesh" in SKILL
    assert "QNS-CD-1.0" in README
    assert "QNS-CD-1.0" in SKILL
    assert "https://github.com/AzielEliab/qnm-node" in README
    assert "https://github.com/AzielEliab/aziel-runtime" in README
    assert "https://github.com/AzielEliab/qnm-node" in SKILL
    assert "Not a Softwares-tab product" in README
    assert "No public qnsd proxy" in README
    assert "QNM-BUILD-1.0" in WORKER_README
    assert "QNS-CD-1.0" in WORKER_README
    assert "AZIEL_RUNTIME" in WORKER_README
    assert "Live Nodes" in WORKER_README
    assert "Aziel Eliab" in MESH
    assert "default OFF" in WORKER_README or "Default OFF" in WORKER_README
    assert "SPLIT THE WIRES" in README
    assert "COLD-COPY SURVIVAL" in README
    assert "SPLIT THE WIRES" in SKILL
    assert "COLD-COPY SURVIVAL" in SKILL
    assert "SPLIT THE WIRES" in WORKER_README
    assert "COLD-COPY SURVIVAL" in WORKER_README


def test_split_the_wires_locked_law() -> None:
    assert 'STW_SPEC = "STW-1.0"' in MESH
    assert 'STW_NAME = "SPLIT THE WIRES"' in MESH
    assert "STW_TIP_TICK_MS_MIN = 500" in MESH
    assert "STW_TIP_TICK_MS_MAX = 1000" in MESH
    assert "STW_DWELL_S = 777" in MESH
    assert "STW_DWELL_MS = 777000" in MESH
    assert "STW_TIP_ONLY = true" in MESH
    assert "STW_PULL_ONLY = true" in MESH
    assert "STW_UPDATE_IS_PROOF = true" in MESH
    assert "STW_UPDATE_IS_TIMER = false" in MESH
    assert "STW_EQUIVOCATION_ENDS_PEER = true" in MESH
    assert "STW_EMIT_LAST_LOCAL = true" in MESH
    assert "STW_PHOENIX_LOCAL_ONLY = true" in MESH
    assert "STW_AUTO_SPLICE = false" in MESH
    assert "STW_HEARTBEAT_LOSS_IS_POISON = false" in MESH
    assert "STW_SOCKETS_EQUAL = false" in MESH
    assert "STW_HOP_DEFAULT_OFF = true" in MESH
    assert "tip-only 0.5–1s tick" in MESH
    assert "pull-only payload" in MESH
    assert "update=proof not timer" in MESH
    assert "777s dwell after valid cite" in MESH
    assert "equivocation ends peer" in MESH
    assert "emit last locally" in MESH
    assert "Phoenix local only" in MESH
    assert "partition no auto-splice" in MESH
    assert "heartbeat loss≠poison" in MESH
    assert "1s≠777s sockets" in MESH
    assert "export function evaluateSplitTheWires" in MESH
    assert "export function attachSplitTheWires" in MESH
    assert "split_the_wires: STW" in MESH
    assert "stw_spec: STW_SPEC" in MESH
    assert "X-Aziel-Stw" in RUNTIME
    assert "SPLIT THE WIRES" in HOME
    assert "hop default off" in MESH.lower()


def test_cold_copy_survival_locked_law() -> None:
    assert 'CCS_SPEC = "CCS-1.0"' in MESH
    assert 'CCS_NAME = "COLD-COPY SURVIVAL"' in MESH
    assert "CCS_MULTIPLY_COLD_COPIES = true" in MESH
    assert "CCS_MIN_COLD_COPIES = 2" in MESH
    assert "CCS_LIVE_BODY_SYNC = false" in MESH
    assert "CCS_TIP_EXPENSIVE_TO_ERASE = true" in MESH
    assert "CCS_SERVER_PULL_WIPES_COLD = false" in MESH
    assert "CCS_HASH_ABSOLUTE_POISON_REFUSE = true" in MESH
    assert "CCS_DATA_OUTLIVES_CREATORS = true" in MESH
    assert "CCS_HOP_DEFAULT_OFF = true" in MESH
    assert "multiply cold copies" in MESH
    assert "refuse live body sync" in MESH
    assert "tip expensive to erase" in MESH
    assert "server pull cannot wipe cold replicas" in MESH
    assert "hash-absolute poison refuse" in MESH
    assert "data outlives creators" in MESH
    assert "keeps_split_wires: true" in MESH
    assert "export function evaluateColdCopySurvival" in MESH
    assert "export function attachColdCopySurvival" in MESH
    assert "export function attachMeshCites" in MESH
    assert "cold_copy_survival: CCS" in MESH
    assert "ccs_spec: CCS_SPEC" in MESH
    assert "X-Aziel-Ccs" in RUNTIME
    assert "attachMeshCites" in RUNTIME
    assert "COLD-COPY SURVIVAL" in HOME
    assert "Keeps SPLIT THE WIRES" in MESH


def test_split_wires_and_cold_copy_evaluators() -> None:
    mesh = ROOT / "workers/download-tracker/src/mesh.js"
    script = f"""
import {{
  stwTipTickOk, stwPayloadOk, stwUpdateOk, stwDwellOpen,
  stwEquivocationEndsPeer, stwSocketsSplit, stwHopDefaultOff,
  stwPartitionSpliceOk, stwHeartbeatLossIsPoison, stwPhoenixOk,
  evaluateSplitTheWires, evaluateColdCopySurvival,
  ccsColdCopiesOk, ccsLiveBodySyncOk, ccsServerPullWipesCold,
  ccsDataOutlivesCreators, ccsHashAbsolutePoisonRefuse, ccsTipEraseOk,
  STW, CCS, MESH_DEFAULT_OFF, attachMeshCites,
}} from {mesh.resolve().as_uri()!r};

const cases = [];
function check(name, ok) {{ cases.push({{name, ok: !!ok}}); }}

check("hop_off", stwHopDefaultOff() === true && MESH_DEFAULT_OFF === true);
check("tick_500", stwTipTickOk(500));
check("tick_1000", stwTipTickOk(1000));
check("tick_499", !stwTipTickOk(499));
check("tick_1001", !stwTipTickOk(1001));
check("pull", stwPayloadOk("pull"));
check("push", !stwPayloadOk("push"));
check("proof", stwUpdateOk("proof"));
check("timer", !stwUpdateOk("timer"));
check("sockets", stwSocketsSplit("tip", "dwell"));
check("sockets_same", !stwSocketsSplit("tip", "tip"));
check("equiv", stwEquivocationEndsPeer("aaa", "bbb"));
check("equiv_same", !stwEquivocationEndsPeer("aaa", "aaa"));
check("splice", stwPartitionSpliceOk() === false);
check("hb", stwHeartbeatLossIsPoison() === false);
check("phoenix_local", stwPhoenixOk("local"));
check("phoenix_remote", !stwPhoenixOk("remote"));
check("dwell", stwDwellOpen(new Date(0).toISOString(), new Date(776000).toISOString()));
check("dwell_done", !stwDwellOpen(new Date(0).toISOString(), new Date(777000).toISOString()));
check("ccs_min", ccsColdCopiesOk(["a", "b"]));
check("ccs_one", !ccsColdCopiesOk(["a"]));
check("ccs_sync", ccsLiveBodySyncOk() === false);
check("ccs_pull_wipe", ccsServerPullWipesCold() === false);
check("ccs_outlive", ccsDataOutlivesCreators() === true);
check("ccs_poison", ccsHashAbsolutePoisonRefuse("abc", ["abc"]));
check("ccs_erase_cheap", !ccsTipEraseOk("cheap"));
check("ccs_erase_op", ccsTipEraseOk("local_operator"));
const hop = evaluateSplitTheWires({{ kind: "hop" }});
check("eval_hop", hop.ok === false && hop.code === "STW-HOP-DEFAULT-OFF");
const splice = evaluateSplitTheWires({{ kind: "splice" }});
check("eval_splice", splice.ok === false);
const sync = evaluateColdCopySurvival({{ kind: "live_body_sync" }});
check("eval_sync", sync.ok === false);
const wipe = evaluateColdCopySurvival({{ kind: "server_pull", wipe: true }});
check("eval_wipe", wipe.ok === false);
const cite = attachMeshCites({{}});
check("attach_stw", cite.split_the_wires && cite.split_the_wires.spec === "STW-1.0");
check("attach_ccs", cite.cold_copy_survival && cite.cold_copy_survival.spec === "CCS-1.0");
check("stw_name", STW.name === "SPLIT THE WIRES");
check("ccs_name", CCS.name === "COLD-COPY SURVIVAL");
check("ccs_keeps_stw", CCS.keeps_split_wires === true);
console.log(JSON.stringify(cases));
"""
    proc = subprocess.run(
        ["node", "--input-type=module", "-e", script],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    cases = json.loads(proc.stdout.strip().splitlines()[-1])
    failed = [c["name"] for c in cases if not c["ok"]]
    assert not failed, "evaluator cases failed: " + ", ".join(failed)
