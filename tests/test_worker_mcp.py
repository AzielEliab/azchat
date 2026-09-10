"""Worker /mcp is a dual-surface JSON-RPC double of safe AZChat ops."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = (ROOT / "workers/download-tracker/src/runtime.js").read_text(encoding="utf-8")
INDEX = (ROOT / "workers/download-tracker/src/index.js").read_text(encoding="utf-8")
WRANGLER = (ROOT / "workers/download-tracker/wrangler.toml").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")

THIN_TOOLS = (
    "azchat_health",
    "azchat_skill",
    "azchat_doctor",
    "azchat_handle_new",
    "azchat_room_open",
    "azchat_verify_receipt",
)


def test_wrangler_runs_worker_first_for_mcp() -> None:
    assert '"/mcp"' in WRANGLER or '"/mcp",' in WRANGLER
    assert "/mcp/" in WRANGLER
    assert "run_worker_first" in WRANGLER


def test_runtime_handles_mcp_and_mcp_slash() -> None:
    assert 'stripped === "/mcp"' in RUNTIME
    assert "handleMcp" in RUNTIME
    assert "handleMcpJson" in RUNTIME
    assert "replace(/\\/+$/, " in RUNTIME or "replace(/\\/+$/" in RUNTIME


def test_jsonrpc_methods_and_thin_doubles() -> None:
    for method in ("initialize", "tools/list", "tools/call", "ping"):
        assert method in RUNTIME
    for tool in THIN_TOOLS:
        assert tool in RUNTIME
    assert "protocolVersion" in RUNTIME
    assert "jsonrpc" in RUNTIME


def test_mcp_points_at_fraggate_slug_azchat() -> None:
    assert 'slug: "azchat"' in RUNTIME or "slug=azchat" in RUNTIME
    assert "aziel-runtime.vibelock.workers.dev" in RUNTIME
    assert "/v1/fraggate/call" in RUNTIME
    assert "/v1/fraggate/list" in RUNTIME
    assert "/v1/fraggate/describe" in RUNTIME
    assert 'door: "fraggate"' in RUNTIME or "door: 'fraggate'" in RUNTIME
    assert "AZIEL_RUNTIME" in RUNTIME or "env.AZIEL_RUNTIME" in RUNTIME


def test_mcp_and_openapi_point_at_suite_mesh() -> None:
    assert "meshPointer" in RUNTIME
    assert "meshOpenApiPaths" in RUNTIME
    assert "/v1/mesh" in RUNTIME
    assert "QNM-BUILD-1.0" in RUNTIME
    assert "No Node Gate" in RUNTIME
    assert "mesh_*" in RUNTIME or "mesh_\\*" in RUNTIME


def test_mcp_refuses_stubs() -> None:
    for name in ("smtp", "bridge_azmail", "mesh_enable"):
        assert name in RUNTIME
    assert "AZC-CHAT-REFUSE" in RUNTIME


def test_mcp_does_not_increment_downloads() -> None:
    assert "kv_increment: false" in RUNTIME
    assert "Does not increment" in RUNTIME or "does not increment" in RUNTIME.lower()


def test_docs_advertise_worker_mcp() -> None:
    assert "azchat-download-tracker.vibelock.workers.dev/mcp" in README
    assert "azchat-download-tracker.vibelock.workers.dev/mcp" in SKILL
    assert "aziel-runtime.vibelock.workers.dev/mcp" in README
    assert "Aziel Eliab" in README
