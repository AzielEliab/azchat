"""CLI smoke."""

from __future__ import annotations

from azchat.cli import main
from azchat.engine import reset_azchat_store


def setup_function() -> None:
    reset_azchat_store()


def test_cli_health(capsys) -> None:
    assert main(["health"]) == 0
    out = capsys.readouterr().out
    assert "azchat" in out
    assert "AZC-CHAT-0.1" in out


def test_cli_handle_new(capsys) -> None:
    rc = main(["handle-new", "--label", "agent-a"])
    assert rc == 0
    assert "handle_new" in capsys.readouterr().out


def test_cli_stub_smtp(capsys) -> None:
    rc = main(["stub", "smtp"])
    assert rc == 1
    assert "AZC-CHAT-REFUSE" in capsys.readouterr().out


def test_cli_stub_bridge_azmail(capsys) -> None:
    rc = main(["stub", "bridge_azmail"])
    assert rc == 1
    assert "AZC-CHAT-REFUSE" in capsys.readouterr().out
