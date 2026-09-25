"""CLI smoke. Human text is the default. --json keeps machine fields."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from azchat.cli import main
from azchat.engine import health, reset_azchat_store

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _isolated_session(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("AZCHAT_STATE", str(tmp_path / "state.json"))
    reset_azchat_store()


def test_cli_bare_welcome(capsys) -> None:
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "short-lived rooms" in out
    assert "azchat ui" in out
    assert "azchat doctor" in out
    assert "Aziel Eliab" in out
    assert not out.lstrip().startswith("{")
    assert "THIS IS NOT" not in out


def test_cli_help(capsys) -> None:
    assert main(["--help"]) == 0
    out = capsys.readouterr().out
    assert "usage: azchat" in out
    assert "examples:" in out
    assert "azchat ui" in out
    assert "advanced:" in out
    assert "--json" in out
    assert "the following arguments are required" not in out


def test_cli_unknown_command(capsys) -> None:
    assert main(["bogus"]) == 2
    err = capsys.readouterr().err
    assert 'Unknown command "bogus".' in err
    assert "azchat --help" in err


def test_cli_missing_token(capsys) -> None:
    assert main(["handle-rotate"]) == 2
    err = capsys.readouterr().err
    assert "handle token is required" in err
    assert "azchat handle-new" in err


def test_cli_health(capsys) -> None:
    assert main(["health"]) == 0
    out = capsys.readouterr().out
    assert "AZChat is up." in out
    assert "azchat" in out
    assert "AZC-CHAT-0.1" in out
    assert not out.lstrip().startswith("{")


def test_cli_health_json(capsys) -> None:
    assert main(["--json", "health"]) == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data == health()
    assert main(["health", "--json"]) == 0
    again = json.loads(capsys.readouterr().out)
    assert again["op"] == "health"
    assert again["spec"] == "AZC-CHAT-0.1"
    assert "limitation" in again


def test_cli_doctor_human(capsys) -> None:
    assert main(["doctor"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Doctor: pass")
    assert "azchat ui" in out


def test_cli_handle_new(capsys) -> None:
    rc = main(["handle-new", "--label", "agent-a"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "handle_new" in out
    assert "token:" in out


def test_cli_handle_new_json(capsys) -> None:
    assert main(["handle-new", "--json", "--label", "agent-a"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True
    assert data["op"] == "handle_new"
    assert data["label"] == "agent-a"
    assert data["token"]


def test_cli_stub_smtp(capsys) -> None:
    rc = main(["stub", "smtp"])
    assert rc == 1
    err_out = capsys.readouterr().out
    assert "AZC-CHAT-REFUSE" in err_out


def test_cli_stub_bridge_azmail(capsys) -> None:
    rc = main(["stub", "bridge_azmail"])
    assert rc == 1
    assert "AZC-CHAT-REFUSE" in capsys.readouterr().out


def test_cli_stub_json(capsys) -> None:
    assert main(["--json", "stub", "smtp"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is False
    assert data["code"] == "AZC-CHAT-REFUSE"
    assert data["stub"] is True
    assert data["op"] == "smtp"


def test_session_file_keeps_handles_for_the_next_command(capsys, monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("AZCHAT_STATE", str(tmp_path / "state.json"))
    assert main(["handle-new", "--json", "--label", "me"]) == 0
    first = json.loads(capsys.readouterr().out)
    assert main(["handle-new", "--json", "--label", "other"]) == 0
    second = json.loads(capsys.readouterr().out)
    reset_azchat_store()
    assert main(["room-open", "--json", "--token-a", first["token"], "--token-b", second["token"]]) == 0
    room = json.loads(capsys.readouterr().out)
    assert room["ok"] is True
    assert room["op"] == "room_open"
    assert room["room_id"]


def test_session_file_survives_a_new_process(tmp_path) -> None:
    env = os.environ.copy()
    env["AZCHAT_STATE"] = str(tmp_path / "state.json")
    env["PYTHONPATH"] = str(ROOT)
    first = subprocess.run(
        [sys.executable, "-m", "azchat", "handle-new", "--json", "--label", "me"],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
        check=False,
    )
    assert first.returncode == 0
    token = json.loads(first.stdout)["token"]
    second = subprocess.run(
        [sys.executable, "-m", "azchat", "handle-new", "--json", "--label", "other"],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
        check=False,
    )
    assert second.returncode == 0
    other = json.loads(second.stdout)["token"]
    opened = subprocess.run(
        [sys.executable, "-m", "azchat", "room-open", "--json", "--token-a", token, "--token-b", other],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
        check=False,
    )
    assert opened.returncode == 0
    room = json.loads(opened.stdout)
    assert room["ok"] is True
    assert room["room_id"]


def test_corrupt_session_file_is_a_plain_error(capsys, monkeypatch, tmp_path) -> None:
    path = tmp_path / "state.json"
    path.write_text("{", encoding="utf-8")
    monkeypatch.setenv("AZCHAT_STATE", str(path))
    assert main(["handle-new", "--label", "me"]) == 1
    err = capsys.readouterr().err
    assert "Could not read the session file" in err
    assert "Move it aside" in err
    assert path.read_text(encoding="utf-8") == "{"


def test_cli_missing_receipt(capsys) -> None:
    assert main(["verify", "--receipt", "no-such-receipt.json"]) == 1
    err = capsys.readouterr().err
    assert "Could not read that receipt file." in err
    assert "azchat verify" in err
