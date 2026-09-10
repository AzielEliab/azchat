"""cite.json / llms.txt name suite peers. Dual surface + FragGate door stay explicit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CITE = json.loads((ROOT / "cite.json").read_text(encoding="utf-8"))
LLMS = (ROOT / "llms.txt").read_text(encoding="utf-8")
HOME = (ROOT / "workers/download-tracker/src/home.js").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
WRANGLER = (ROOT / "workers/download-tracker/wrangler.toml").read_text(encoding="utf-8")

PEERS = (
    "aziel-runtime",
    "/v1/fraggate/list",
    "/v1/fraggate/call",
    "/v1/software",
    "/mcp",
    "azmail",
    "AZMail",
    "aznet",
    "peacelock",
    "azieleliab.com",
    "azielcorpuslibrary.net",
    "godlock.uk",
)

CLIENTS = (
    "ChatGPT (GPT Actions / OpenAI)",
    "Grok (xAI)",
    "Venice",
    "Claude (Anthropic)",
    "Cursor (MCP)",
    "Glama (MCP)",
    "Perplexity",
    "Microsoft Copilot / Bing",
    "Google Gemini / Vertex",
    "Mistral",
    "Meta AI",
    "Apple Intelligence surfaces",
    "Amazon Q tooling",
    "DuckAssist",
    "You.com",
    "Cohere",
)


def test_live_kv_id_committed() -> None:
    assert "01a3bbf8ad5e449eb0eb7648d75f8ae0" in WRANGLER
    assert "00000000000000000000000000000000" not in WRANGLER
    assert "AZCHAT_DOWNLOADS" in WRANGLER


def test_cite_json_names_peers_and_door() -> None:
    assert CITE["identity"] == "Aziel Eliab only"
    assert CITE["slug"] == "azchat"
    assert CITE["placement"] == "domain-software"
    assert CITE["door"] == "fraggate"
    peers = CITE["peers"]
    assert peers["azmail"]["merge"] is False
    assert peers["aznet"]["slug"] == "aznet"
    assert peers["peacelock"]["slug"] == "peacelock"
    assert "/v1/fraggate/call" in peers["aziel_runtime"]["paths"]
    assert "/v1/software" in peers["aziel_runtime"]["paths"]
    assert peers["hubs"]["azieleliab"] == "https://www.azieleliab.com/"
    assert peers["hubs"]["azielcorpuslibrary"] == "https://www.azielcorpuslibrary.net/"
    assert peers["hubs"]["godlock"] == "https://godlock.uk/"
    assert CITE["fraggate"]["call"].endswith("/v1/fraggate/call")
    assert CITE["dual_surface"]["human_worker_ui"].endswith("/")
    assert "/download" in CITE["dual_surface"]["download"]
    assert "/mcp" in CITE["dual_surface"]["agent_mcp"]
    for name in CLIENTS:
        assert name in CITE["clients"]


def test_llms_txt_names_peers_and_full_clients() -> None:
    for token in PEERS:
        assert token in LLMS
    for name in CLIENTS:
        assert name in LLMS
    assert "never the short triad only" in LLMS
    assert "agent MCP + human Worker UI + /download" in LLMS
    assert "Aziel Eliab only" in LLMS


def test_worker_cite_and_llms_emit_same_peers() -> None:
    for token in PEERS:
        assert token in HOME
    assert "citePayload" in HOME
    assert "function llmsTxt" in HOME
    assert "btn-fraggate" in HOME
    assert "/v1/fraggate/call" in HOME
    assert "Dual-surface law" in HOME
    assert "Softwares peers" in HOME
    for name in CLIENTS:
        assert name in HOME


def test_readme_and_skill_cross_map() -> None:
    for text in (README, SKILL):
        for token in PEERS:
            assert token in text
        assert "Aziel Eliab only" in text
        assert "do not bridge" in text.lower() or "Do not bridge" in text
