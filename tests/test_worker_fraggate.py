"""Worker /v1/fraggate/* is a PROXY to aziel-runtime via AZIEL_RUNTIME."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOOR = (ROOT / "workers/download-tracker/src/door.js").read_text(encoding="utf-8")
RUNTIME = (ROOT / "workers/download-tracker/src/runtime.js").read_text(encoding="utf-8")
INDEX = (ROOT / "workers/download-tracker/src/index.js").read_text(encoding="utf-8")
WRANGLER = (ROOT / "workers/download-tracker/wrangler.toml").read_text(encoding="utf-8")
HOME = (ROOT / "workers/download-tracker/src/home.js").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")

LIVE_OPS = (
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
)


def test_wrangler_binds_aziel_runtime() -> None:
    assert 'binding = "AZIEL_RUNTIME"' in WRANGLER
    assert 'service = "aziel-runtime"' in WRANGLER
    assert "AZIEL_RUNTIME_ORIGIN" in WRANGLER
    assert "/v1/*" in WRANGLER
    assert 'name = "azchat-download-tracker"' in WRANGLER
    assert 'account_id = "ac575a9b822bea2bed97d0ab73aed238"' in WRANGLER
    assert "01a3bbf8ad5e449eb0eb7648d75f8ae0" in WRANGLER
    assert "00000000000000000000000000000000" not in WRANGLER
    assert "AZCHAT_DOWNLOADS" in WRANGLER
    assert "workers_dev = true" in WRANGLER


def test_door_classifies_list_describe_call() -> None:
    for path in ("/v1/fraggate/list", "/v1/fraggate/describe", "/v1/fraggate/call"):
        assert path in DOOR
    assert 'kind: "door"' in DOOR
    assert "DOOR_ALIASES" in DOOR
    assert '"/v1/runtime/list": "/v1/fraggate/list"' in DOOR
    assert '"/v1/runtime/describe": "/v1/fraggate/describe"' in DOOR
    assert '"/v1/runtime/call": "/v1/fraggate/call"' in DOOR
    assert "localOpFromPath" in DOOR
    assert "doorTargetUrl" in DOOR


def test_runtime_proxies_via_aziel_runtime_binding() -> None:
    assert 'from "./door.js"' in RUNTIME
    assert "classifyV1Path" in RUNTIME
    assert "proxyDoor" in RUNTIME
    assert "runtimeFetcher" in RUNTIME
    assert "env.AZIEL_RUNTIME" in RUNTIME
    assert "X-Aziel-Door" in RUNTIME
    assert "fraggate_proxy_failed" in RUNTIME
    assert "handleRuntimeApi(request, url, env)" in RUNTIME
    assert "handleRuntimeApi(request, url, env)" in INDEX


def test_openapi_and_mcp_advertise_proxy_and_live_ops() -> None:
    assert "/v1/fraggate/list" in RUNTIME
    assert "/v1/fraggate/describe" in RUNTIME
    assert "/v1/fraggate/call" in RUNTIME
    assert "FRAGGATE_LIVE_OPS" in RUNTIME
    for op in LIVE_OPS:
        assert op in RUNTIME


def test_doctor_is_fraggate_live() -> None:
    assert "fraggate_live: true" in RUNTIME or "engineDoctor" in RUNTIME
    assert "FragGate LIVE_OPS" in SKILL
    assert "doctor" in README.lower()


def test_ui_labels_match_catalog() -> None:
    for token in ("btn-handle-a", "btn-room", "btn-bus-send", "btn-verify", "btn-health", "btn-skill", "btn-doctor"):
        assert token in HOME
    assert ">Health<" in HOME
    assert ">Skill<" in HOME
    assert ">Doctor<" in HOME
    assert "/v1/health" in HOME
    assert "/v1/skill" in HOME
    assert "/v1/fraggate/list" in HOME


def test_docs_advertise_fraggate_proxy() -> None:
    assert "/v1/fraggate/list" in README
    assert "AZIEL_RUNTIME" in README
    assert "/v1/fraggate/list" in SKILL
    assert "/v1/fraggate/describe" in SKILL
    assert "/v1/fraggate/call" in SKILL
    assert "Aziel Eliab" in README


def test_door_classifies_mesh_as_door() -> None:
    assert '"mesh"' in DOOR
    assert "/v1/mesh" in DOOR
    assert 'path === "/v1/mesh"' in DOOR or 'path.startsWith("/v1/mesh/")' in DOOR


def test_ui_has_live_nodes_strip() -> None:
    assert 'id="meshStrip"' in HOME
    assert "Live Nodes" in HOME
    assert "QNM-BUILD-1.0" in HOME
    assert "No Node Gate" in HOME
    assert "No auto-heal" in HOME
    assert "/v1/mesh" in HOME
    assert 'id="node-gate"' not in HOME
