"""Worker engine mirror and homepage room options."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = (ROOT / "workers/download-tracker/src/home.js").read_text(encoding="utf-8")


def test_homepage_offers_list_host_and_private_join() -> None:
    assert 'id="btn-host"' in HOME
    assert 'id="btn-rooms"' in HOME
    assert 'id="room-list"' in HOME
    assert 'id="room_private"' in HOME
    assert 'type="password"' in HOME
    assert "/v1/room_list" in HOME
    assert "/v1/room_host" in HOME
    assert "/v1/room_join" in HOME
    assert "not end-to-end encryption" in HOME
    assert "Lamb Lens Service" in HOME


def test_worker_engine_room_gate() -> None:
    node = shutil.which("node")
    assert node, "node is required to check the Worker room gate"
    script = ROOT / "tests" / "worker_room_gate.mjs"
    proc = subprocess.run([node, str(script)], cwd=ROOT, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "worker room gate ok" in proc.stdout
    assert "correct-horse-battery-staple" not in proc.stdout
    assert "correct-horse-battery-staple" not in proc.stderr
