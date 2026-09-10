"""Worker homepage is AZChat software, not a downloads shell."""

from __future__ import annotations

from pathlib import Path

HOME = Path("workers/download-tracker/src/home.js").read_text(encoding="utf-8")
INDEX = Path("workers/download-tracker/src/index.js").read_text(encoding="utf-8")


def test_title_is_product_not_downloads_shell() -> None:
    assert "AZChat — Aziel Eliab" in HOME
    assert "AZChat downloads" not in HOME


def test_seo_and_softwareapplication_json_ld() -> None:
    assert "application/ld+json" in HOME
    assert "SoftwareApplication" in HOME
    assert "Aziel Eliab" in HOME
    assert "cite.json" in HOME
    assert "sitemap.xml" in HOME
    assert "Everblooming sigil" in HOME
    assert "/sigil.png" in HOME


def test_workspace_shows_fraggate_door_and_peers() -> None:
    assert "btn-fraggate" in HOME
    assert "/v1/fraggate/call" in HOME
    assert "Dual-surface law" in HOME
    assert "AZMail" in HOME
    assert "aznet" in HOME.lower() or "AZNet" in HOME
    assert "PeaceLock" in HOME


def test_workspace_calls_real_ops() -> None:
    for path in (
        "/v1/handle_new",
        "/v1/handle_rotate",
        "/v1/room_open",
        "/v1/room_post",
        "/v1/room_pull",
        "/v1/bus_send",
        "/v1/bus_poll",
        "/v1/verify_receipt",
        "/v1/import_export",
        "/v1/health",
        "/v1/skill",
        "/v1/doctor",
    ):
        assert path in HOME
    assert "btn-handle-a" in HOME
    assert "btn-room" in HOME
    assert "btn-bus-send" in HOME
    assert "btn-verify" in HOME
    assert "btn-health" in HOME
    assert "btn-skill" in HOME
    assert "btn-doctor" in HOME
    assert "Use UI" in HOME or "AZChat workspace" in HOME


def test_download_install_and_identity_remain() -> None:
    assert "/download?asset=" in HOME
    assert "azchat-0.1.0.tar.gz" in HOME
    assert "One-click install" in HOME
    assert "Aziel Eliab only" in HOME
    assert "Apache-2.0" in HOME
    assert "Forks welcome" in HOME or "Forks are welcome" in HOME


def test_no_invented_or_live_zenodo_identifier() -> None:
    assert "identifier:" not in HOME.split("export function jsonLd")[1].split("export function handleSeoRoutes")[0]
    assert "No DOI is invented here" in HOME
    assert "DOI =" not in INDEX
    assert "ZENODO =" not in INDEX


def test_worker_serves_home_and_seo() -> None:
    assert "renderHome" in INDEX
    assert "handleSeoRoutes" in INDEX
    assert 'url.pathname === "/"' in INDEX
    assert "/download" in INDEX
    assert "function totalKey()" in INDEX
    assert "azchat-download-tracker" in INDEX
    assert "AZCHAT_DOWNLOADS" in INDEX or "azchat" in INDEX
