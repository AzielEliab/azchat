"""Local UI contract: one primary action, system theme, machine JSON on request."""

from __future__ import annotations

import json
import threading
import urllib.request

import pytest

from azchat.engine import reset_azchat_store
from azchat.ui import Handler, ThreadingHTTPServer, open_line, render_page, serve, wants_json


@pytest.fixture(autouse=True)
def _isolated_session(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("AZCHAT_STATE", str(tmp_path / "state.json"))
    reset_azchat_store()


def test_page_is_a_calm_first_screen() -> None:
    page = render_page()
    assert 'name="viewport"' in page
    assert "prefers-color-scheme" in page
    assert ":focus-visible" in page
    assert "#c9a227" in page
    assert 'id="btn-primary"' in page
    assert ">New handle<" in page
    assert 'id="advanced"' in page
    assert 'id="advanced" open' not in page
    assert "short-lived room" in page
    assert "Aziel Eliab" in page
    assert "Aziel Elroi" not in page
    hero, _, rest = page.partition('id="about"')
    assert "THIS IS NOT" not in hero
    assert "THIS IS NOT" in rest


def test_wants_json_respects_accept() -> None:
    assert wants_json("application/json") is True
    assert wants_json("text/html,application/xhtml+xml") is False
    assert wants_json("application/json, text/html") is True
    assert wants_json(None) is False


def test_open_line() -> None:
    assert open_line("127.0.0.1", 8878) == "Open http://127.0.0.1:8878/"


def test_serve_refuses_public_bind() -> None:
    with pytest.raises(ValueError, match="127.0.0.1"):
        serve(host="0.0.0.0", port=9)


def test_local_http_human_and_json() -> None:
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    try:
        page = urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5).read().decode("utf-8")
        assert "<h1>Open a room</h1>" in page
        req = urllib.request.Request(
            f"http://127.0.0.1:{port}/",
            headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        body = json.loads(urllib.request.urlopen(req, timeout=5).read().decode("utf-8"))
        assert body["op"] == "health"
        assert body["product"] == "azchat"
        assert body["spec"] == "AZC-CHAT-0.1"
        minted = urllib.request.Request(
            f"http://127.0.0.1:{port}/v1/handle_new",
            data=json.dumps({"label": "me"}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        )
        handle = json.loads(urllib.request.urlopen(minted, timeout=5).read().decode("utf-8"))
        assert handle["ok"] is True
        assert handle["op"] == "handle_new"
        assert handle["label"] == "me"
    finally:
        httpd.shutdown()
