"""Locked product law."""

from __future__ import annotations

from pathlib import Path

from azchat.engine import LIVE_OPS, STUB_OPS

ROOT = Path(__file__).resolve().parents[1]


def test_live_ops_locked() -> None:
    assert LIVE_OPS == (
        "health",
        "skill",
        "doctor",
        "handle_new",
        "handle_rotate",
        "room_open",
        "room_post",
        "room_pull",
        "bus_send",
        "bus_poll",
        "verify_receipt",
        "import_export",
    )


def test_stub_ops_locked() -> None:
    assert STUB_OPS == (
        "smtp",
        "smtp_send",
        "send",
        "mail",
        "deliver",
        "deanonymize",
        "harvest",
        "mesh_join",
        "mesh_enable",
        "vpn",
        "bridge_azmail",
        "bridge",
        "chromium",
    )


def test_peers_not_merged_or_bridged() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "do not bridge" in readme.lower() or "Do not bridge" in readme
    assert "azmail" in readme.lower()
    assert "Not SMTP" in readme or "not SMTP" in readme
    assert "aznet" in readme.lower()
    assert "peacelock" in readme.lower()
    assert "azieleliab.com" in readme
    assert "/v1/software" in readme
    assert "azchat-download-tracker" in readme
