/**
 * AZChat product homepage — software UI, not a downloads shell.
 * Author: Aziel Eliab only. Apache-2.0. Forks welcome.
 * No Zenodo DOI is invented here.
 */

const HOST = "https://azchat-download-tracker.vibelock.workers.dev";
const GITHUB_REPO = "https://github.com/AzielEliab/azchat";
const GITHUB_LATEST = "https://github.com/AzielEliab/azchat/releases/latest";
const CATALOG = "https://aziel-runtime.vibelock.workers.dev/";
const CATALOG_PRODUCT = "https://aziel-runtime.vibelock.workers.dev/p/azchat/";
const FRAGGATE_LIST = "https://aziel-runtime.vibelock.workers.dev/v1/fraggate/list";
const FRAGGATE_DESCRIBE = "https://aziel-runtime.vibelock.workers.dev/v1/fraggate/describe?slug=azchat";
const FRAGGATE_CALL = "https://aziel-runtime.vibelock.workers.dev/v1/fraggate/call";
const SOFTWARE_TAB = "https://aziel-runtime.vibelock.workers.dev/v1/software";
const AZMAIL_HOST = "https://azmail-download-tracker.vibelock.workers.dev";
const AZNET_HOST = "https://aznet-download-tracker.vibelock.workers.dev";
const PEACELOCK_HOST = "https://peacelock-download-tracker.vibelock.workers.dev";
const HUB_AZIELELIAB = "https://www.azieleliab.com/";
const HUB_LIBRARY = "https://www.azielcorpuslibrary.net/";
const HUB_GODLOCK = "https://godlock.uk/";
const LICENSE = "https://www.apache.org/licenses/LICENSE-2.0";
const FULL_CLIENTS = [
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
  "other MCP/OpenAPI-capable assistants",
];
const VERSION = "0.1.0";
const AUTHOR = "Aziel Eliab";
const TITLE = "AZChat — Aziel Eliab";
const DEFAULT_ASSET = "azchat-0.1.0.tar.gz";
const INSTALL_LINE = "curl -fsSL https://azchat-download-tracker.vibelock.workers.dev/install.sh | bash";
const DESCRIPTION =
  "AZChat is Aziel Eliab software: spendable handles, ephemeral rooms, and an agent bus (AZC-CHAT-0.1). Mesh hop default off. Not SMTP. Not AZMail. FragGate only. Apache-2.0.";
const HONEST =
  "THIS IS: AZChat spendable handles, ephemeral rooms (TTL/sealed), and an agent bus. Reached only through FragGate. mesh_enabled_default is false. THIS IS NOT: SMTP, a public MTA, AZMail, a mesh hop, deanonymize, or a Chromium chat runner. Do not bridge AZChat ↔ AZMail. Stranger room_pull is 404. Hosted rooms appear on the all-rooms list. A private room requires a passphrase to join and is not end-to-end encryption. Author: Aziel Eliab only.";
const HOW_TO_CITE =
  "Eliab, Aziel. (2026). AZChat 0.1.0 [Software]. Apache-2.0. https://github.com/AzielEliab/azchat · https://azchat-download-tracker.vibelock.workers.dev/";

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, MCP-Protocol-Version, mcp-session-id, User-Agent, Authorization",
  };
}

function escapeHtml(value) {
  return String(value == null ? "" : value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function citePayload() {
  return {
    author: AUTHOR,
    title: "AZChat",
    version: VERSION,
    spec: "AZC-CHAT-0.1",
    class: "Plain",
    slug: "azchat",
    domain: "Comms",
    domain_id: "07",
    placement: "domain-software",
    door: "fraggate",
    homepage: HOST + "/",
    github: GITHUB_REPO,
    download: HOST + "/download",
    install: HOST + "/install.sh",
    openapi: HOST + "/openapi.json",
    skill: HOST + "/v1/skill",
    mcp: HOST + "/mcp",
    catalog_mcp: CATALOG + "mcp",
    catalog: CATALOG,
    catalog_product: CATALOG_PRODUCT,
    license: "Apache-2.0",
    license_url: LICENSE,
    one_line: DESCRIPTION,
    how_to_cite: HOW_TO_CITE,
    apa: "Eliab, A. (2026). AZChat (Version 0.1.0) [Computer software]. https://azchat-download-tracker.vibelock.workers.dev/",
    bibtex:
      "@software{eliab_azchat_2026, author = {Eliab, Aziel}, title = {AZChat}, version = {0.1.0}, year = {2026}, license = {Apache-2.0}, url = {https://azchat-download-tracker.vibelock.workers.dev/}, publisher = {GitHub}, howpublished = {\\url{https://github.com/AzielEliab/azchat}}}",
    zenodo_status: "placeholder_no_doi_invented",
    software_deposit_needed: true,
    note: "No DOI is invented here. Cite GitHub and this Worker. Identity is Aziel Eliab only. Forks welcome. Not AZMail. Not SMTP. FragGate is THE single door.",
    identity: "Aziel Eliab only",
    forks: "welcome and always allowed",
    dual_surface: {
      agent_mcp: HOST + "/mcp",
      catalog_mcp: CATALOG + "mcp",
      catalog_fraggate_call: FRAGGATE_CALL,
      catalog_fraggate_list: FRAGGATE_LIST,
      catalog_software: SOFTWARE_TAB,
      human_worker_ui: HOST + "/",
      download: HOST + "/download",
      law: "Agent MCP + human Worker UI + /download. FragGate is THE single door. Do not gut either surface.",
    },
    fraggate: {
      kernel: "https://github.com/AzielEliab/fraggate",
      runtime: "https://github.com/AzielEliab/aziel-runtime",
      list: FRAGGATE_LIST,
      describe: FRAGGATE_DESCRIBE,
      call: FRAGGATE_CALL,
      software: SOFTWARE_TAB,
      mcp: CATALOG + "mcp",
      worker_proxy: {
        list: HOST + "/v1/fraggate/list",
        describe: HOST + "/v1/fraggate/describe",
        call: HOST + "/v1/fraggate/call",
      },
      slug: "azchat",
      note: "FragGate is THE single door. Worker /v1/fraggate/* PROXY via AZIEL_RUNTIME. True engine is in-process on aziel-runtime 1.9.0.",
    },
    peers: {
      aziel_runtime: {
        role: "catalog + FragGate door + true AZChat engine",
        github: "https://github.com/AzielEliab/aziel-runtime",
        homepage: CATALOG,
        paths: ["/v1/fraggate/list", "/v1/fraggate/describe", "/v1/fraggate/call", "/v1/software", "/mcp"],
        merge: false,
      },
      azmail: {
        role: "Comms neighbor — not bridged",
        slug: "azmail",
        name: "AZMail",
        github: "https://github.com/AzielEliab/azmail",
        homepage: AZMAIL_HOST + "/",
        note: "Mail airlock. Do not bridge AZChat ↔ AZMail. Not SMTP from this product.",
        merge: false,
      },
      aznet: {
        role: "Network neighbor",
        slug: "aznet",
        name: "AZNet",
        homepage: AZNET_HOST + "/",
        merge: false,
      },
      peacelock: {
        role: "Evidence neighbor",
        slug: "peacelock",
        name: "PeaceLock",
        homepage: PEACELOCK_HOST + "/",
        merge: false,
      },
      hubs: {
        azieleliab: HUB_AZIELELIAB,
        azielcorpuslibrary: HUB_LIBRARY,
        godlock: HUB_GODLOCK,
      },
    },
    clients: FULL_CLIENTS.slice(),
  };
}

export function jsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "AZChat",
    alternateName: TITLE,
    applicationCategory: "CommunicationApplication",
    operatingSystem: "Linux, macOS, Windows, Cloudflare Workers",
    softwareVersion: VERSION,
    author: { "@type": "Person", name: AUTHOR, url: "https://github.com/AzielEliab" },
    creator: { "@type": "Person", name: AUTHOR, url: "https://github.com/AzielEliab" },
    codeRepository: GITHUB_REPO,
    downloadUrl: HOST + "/download",
    installUrl: HOST + "/install.sh",
    license: LICENSE,
    url: HOST + "/",
    description: DESCRIPTION,
    keywords: "AZChat, spendable handles, ephemeral rooms, agent bus, Aziel Eliab, AZC-CHAT-0.1, Aziel Elroi Eliab, FragGate",
    isAccessibleForFree: true,
    offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
    sameAs: [GITHUB_REPO, CATALOG_PRODUCT, AZMAIL_HOST + "/", HUB_AZIELELIAB, HUB_LIBRARY, HUB_GODLOCK],
  };
}

function sitemapXml() {
  const paths = ["/", "/download", "/install.sh", "/v1/skill", "/v1/example", "/v1/health", "/v1/doctor", "/v1/fraggate/list", "/v1/mesh", "/openapi.json", "/mcp", "/cite.json", "/llms.txt", "/ai"];
  const urls = paths.map((p) => `  <url><loc>${HOST}${p === "/" ? "/" : p}</loc></url>`).join("\n");
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
  <url><loc>${GITHUB_REPO}</loc></url>
</urlset>
`;
}

function robotsTxt() {
  return `User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: CCBot
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: FacebookBot
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: Diffbot
Allow: /

User-agent: Omgilibot
Allow: /

User-agent: Amazonbot
Allow: /

Sitemap: ${HOST}/sitemap.xml
`;
}

function llmsTxt() {
  return `# AZChat

Author: Aziel Eliab only
Identity: Aziel Eliab only
One-line: ${DESCRIPTION}
Spec: AZC-CHAT-0.1
Class: Plain
Slug: azchat
Domain: Comms (07)
Door: FragGate is THE single door
GitHub: ${GITHUB_REPO}
Homepage: ${HOST}/
Download: ${HOST}/download
Install: ${HOST}/install.sh
OpenAPI: ${HOST}/openapi.json
Skill: ${HOST}/v1/skill
Cite: ${HOST}/cite.json

## Dual surface (do not gut either)

Agent MCP: POST ${HOST}/mcp
Catalog MCP: POST ${CATALOG}mcp (FragGate slug azchat)
Human Worker UI: ${HOST}/
Counted download: ${HOST}/download
Law: agent MCP + human Worker UI + /download. FragGate is THE single door.

## aziel-runtime FragGate (catalog door + true engine)

Kernel: https://github.com/AzielEliab/fraggate
Runtime: https://github.com/AzielEliab/aziel-runtime
GET ${FRAGGATE_LIST}
GET ${FRAGGATE_DESCRIBE}
POST ${FRAGGATE_CALL} { "slug": "azchat", "op": "<LIVE_OP>", "payload": {} }
GET ${SOFTWARE_TAB}
POST ${CATALOG}mcp
Worker PROXY: GET|POST ${HOST}/v1/fraggate/{list,describe,call}

## Peers (do not merge / do not bridge)

AZMail / azmail — Comms neighbor. Not bridged. Not SMTP.
 ${AZMAIL_HOST}/
AZNet / aznet — Network neighbor.
PeaceLock / peacelock — Evidence neighbor.

## Softwares hubs

${HUB_AZIELELIAB}
${HUB_LIBRARY}
${HUB_GODLOCK}

## Ops

POST /v1/handle_new, POST /v1/handle_rotate, POST /v1/room_open, POST /v1/room_post, POST /v1/room_pull, GET|POST /v1/room_list, POST /v1/room_host, POST /v1/room_join, POST /v1/bus_send, POST /v1/bus_poll, POST /v1/verify_receipt, POST /v1/import_export, GET /v1/health, GET /v1/skill, GET /v1/doctor
FragGate proxy: GET /v1/fraggate/list, GET /v1/fraggate/describe, POST /v1/fraggate/call (via AZIEL_RUNTIME)
Suite mesh: GET ${HOST}/v1/mesh PROXY to aziel-runtime. Default OFF. GET never enables. Product-local mesh_enable is stub/REFUSE. SPLIT THE WIRES + COLD-COPY SURVIVAL hub cites. Hop default off.
Worker and local-engine ops: health, skill, doctor, handle_new, handle_rotate, room_open, room_post, room_pull, room_list, room_host, room_join, bus_send, bus_poll, verify_receipt, import_export
room_list, room_host, and room_join are served by this Worker and the local engine. This repository does not change the aziel-runtime FragGate describe card.
MCP tools: azchat_health, azchat_skill, azchat_doctor, azchat_handle_new, azchat_handle_rotate, azchat_room_open, azchat_room_post, azchat_room_pull, azchat_room_list, azchat_room_host, azchat_room_join, azchat_bus_send, azchat_bus_poll, azchat_verify_receipt, azchat_import_export
Private rooms: passphrase-gated entry (PBKDF2 verifier). Wrong or missing passphrase does not join. The passphrase is not on the public list. Private is not end-to-end encryption.

## AI clients (full set — never the short triad only)

Works with ${FULL_CLIENTS.join(", ")}.
Law: Mesh hop default off. Not SMTP. Not AZMail. Do not bridge. Stranger room_pull is 404.
License: Apache-2.0
Forks: welcome and always allowed
DOI: none invented; software deposit still needed.

Indexing, metadata scrape, and AI grounding of public pages are allowed.
`;
}

export function handleSeoRoutes(request, url) {
  if (request.method !== "GET" && request.method !== "HEAD") return null;
  const headers = { ...corsHeaders(), "Cache-Control": "private, no-store" };
  if (url.pathname === "/cite.json") {
    return new Response(JSON.stringify(citePayload(), null, 2), {
      status: 200,
      headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
    });
  }
  if (url.pathname === "/sitemap.xml") {
    return new Response(sitemapXml(), { status: 200, headers: { "Content-Type": "application/xml; charset=utf-8", ...headers } });
  }
  if (url.pathname === "/robots.txt") {
    return new Response(robotsTxt(), { status: 200, headers: { "Content-Type": "text/plain; charset=utf-8", ...headers } });
  }
  if (url.pathname === "/llms.txt" || url.pathname === "/ai.txt") {
    return new Response(llmsTxt(), { status: 200, headers: { "Content-Type": "text/plain; charset=utf-8", ...headers } });
  }
  return null;
}

function breakdownList(stats) {
  const rows = stats.breakdown || [];
  if (!rows.length) return "<li>none yet</li>";
  return rows
    .map((b) => `<li><code>${escapeHtml(b.owner)}/${escapeHtml(b.repo)}</code> branch <code>${escapeHtml(b.branch)}</code> fork=${escapeHtml(b.fork)} → ${escapeHtml(b.count)}</li>`)
    .join("");
}

export function renderHome(stats) {
  const views = Number(stats.views) || 0;
  const downloads = Number(stats.downloads != null ? stats.downloads : stats.total) || 0;
  const v = views.toLocaleString("en-US");
  const n = downloads.toLocaleString("en-US");
  const gh = stats.github || {};
  const ld = JSON.stringify(jsonLd());
  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${TITLE}</title>
<meta name="description" content="${escapeHtml(DESCRIPTION)}">
<meta name="author" content="${AUTHOR}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="${HOST}/">
<link rel="sitemap" type="application/xml" href="${HOST}/sitemap.xml">
<link rel="icon" type="image/png" href="/sigil.png">
<meta property="og:type" content="website">
<meta property="og:title" content="${TITLE}">
<meta property="og:description" content="${escapeHtml(DESCRIPTION)}">
<meta property="og:url" content="${HOST}/">
<meta property="og:site_name" content="Aziel Eliab">
<meta property="og:image" content="${HOST}/sigil.png">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="${TITLE}">
<meta name="twitter:description" content="${escapeHtml(DESCRIPTION)}">
<meta name="twitter:image" content="${HOST}/sigil.png">
<script type="application/ld+json">${ld}</script>
<style>
 :root {
  color-scheme: dark;
  --bg: #0b0b0b; --ink: #e8e0d0; --muted: #9a917f; --gold: #c9a227; --gold-dim: #8a7219;
  --panel: #141414; --line: #2a261c; --pass: #7dcea0; --bad: #e07a74; --focus: #d4af37;
 }
 html, body { margin: 0; padding: 0; background: var(--bg); color: var(--ink); }
 body { font: 16px/1.5 system-ui, "Segoe UI", sans-serif; }
 a { color: #e6d19a; }
 code, pre, .mono { font-family: ui-monospace, Menlo, Consolas, monospace; }
 .wrap { max-width: 58rem; margin: 0 auto; padding: 1.4rem 1.2rem 4.5rem; }
 .brandrow { display: flex; align-items: center; gap: 12px; margin: 0 0 12px; }
 .brandmark { width: 40px; height: 40px; border-radius: 10px; object-fit: cover; flex: 0 0 auto; box-shadow: 0 0 0 1px #d4af3733; }
 .stamp { margin: 0; color: var(--gold); font-size: .88rem; letter-spacing: .02em; }
 .appbar { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; flex-wrap: wrap; }
 h1 { font-size: 2rem; letter-spacing: .02em; margin: 0 0 .2rem; }
 .motto { color: var(--gold); font-style: italic; margin: 0 0 .7rem; }
 .lede { color: var(--muted); margin: 0 0 1rem; max-width: 46rem; }
 .pill { font: 650 .78rem/1 ui-monospace, Menlo, Consolas, monospace; letter-spacing: .06em; text-transform: uppercase; border: 1px solid var(--line); border-radius: 999px; padding: .4rem .7rem; color: var(--muted); background: #101010; }
 .pill.ok { color: var(--pass); border-color: #2f6b48; }
 .pill.bad { color: var(--bad); border-color: #7a2f2c; }
 nav.toc { display: flex; flex-wrap: wrap; gap: .55rem; margin: 0 0 1.1rem; }
 nav.toc a { text-decoration: none; color: var(--ink); border: 1px solid var(--line); background: var(--panel); border-radius: 999px; padding: .35rem .75rem; font-size: .88rem; }
 .banner { border: 1px solid #5c4a1a; background: #241c0d; color: #f0d78c; padding: .9rem 1rem; border-radius: 10px; margin: 0 0 1.15rem; font-size: .94rem; }
 .card, .workspace, .cite { border: 1px solid var(--line); border-radius: 14px; padding: 1.15rem 1.2rem 1.25rem; background: var(--panel); margin: 0 0 1.1rem; }
 .workspace { box-shadow: 0 0 0 1px #d4af3714, 0 16px 40px #0006; }
 h2 { font-size: 1.12rem; margin: 0 0 .45rem; letter-spacing: .04em; }
 .kicker { display: block; font-size: .68rem; letter-spacing: .12em; text-transform: uppercase; color: var(--gold); margin-bottom: .15rem; font-family: ui-monospace, Menlo, Consolas, monospace; }
 .workgrid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr); gap: 1rem; }
 @media (max-width: 820px) { .workgrid { grid-template-columns: 1fr; } }
 label { display: block; font-size: .92rem; margin: .75rem 0 .28rem; }
 input[type="text"], input[type="number"], textarea { width: 100%; padding: .58rem .7rem; border: 1px solid var(--line); border-radius: 8px; background: #0e0e0e; color: var(--ink); font: inherit; box-sizing: border-box; }
 input:focus, textarea:focus { outline: 2px solid var(--focus); outline-offset: 1px; }
 .row2 { display: grid; grid-template-columns: 1fr 1fr; gap: .7rem; }
 @media (max-width: 520px) { .row2 { grid-template-columns: 1fr; } }
 .actions { display: flex; flex-wrap: wrap; gap: .5rem; margin: .95rem 0 .2rem; }
 .check { display: flex; align-items: center; gap: .45rem; margin-top: .75rem; }
 .check input { width: auto; }
 .roomlist { list-style: none; margin: .7rem 0 0; padding: 0; }
 .roomlist li { display: flex; flex-wrap: wrap; gap: .4rem .6rem; align-items: center; border: 1px solid var(--line); border-radius: 8px; padding: .5rem .65rem; margin: 0 0 .4rem; background: #101010; font-size: .88rem; }
 .roomlist button { padding: .4rem .65rem; }
 button, a.btn { font: 700 .88rem/1.1 ui-monospace, Menlo, Consolas, monospace; letter-spacing: .03em; padding: .72rem .9rem; border-radius: 9px; border: 1px solid transparent; cursor: pointer; text-decoration: none; display: inline-block; }
 button.gold, a.btn.gold { background: var(--gold-dim); color: #14110a; }
 button.ink, a.btn.ink { background: var(--ink); color: var(--bg); }
 button.ghost, a.btn.ghost { background: transparent; color: var(--ink); border-color: var(--line); }
 button.copied { background: var(--pass); color: #0e1014; }
 .status { margin: 0 0 .8rem; padding: .75rem .85rem; border-radius: 10px; border: 1px solid var(--line); background: #101010; color: var(--muted); }
 .status.ok { color: var(--pass); border-color: #2f6b48; }
 .status.bad { color: var(--bad); border-color: #7a2f2c; }
 .metrics { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .55rem; margin: 0 0 .85rem; }
 @media (max-width: 720px) { .metrics { grid-template-columns: 1fr 1fr; } }
 .metric { border: 1px solid var(--line); border-radius: 10px; padding: .55rem .65rem; background: #101010; }
 .metric b { display: block; font-size: .72rem; color: var(--muted); font-weight: 600; letter-spacing: .04em; text-transform: uppercase; }
 .metric span { display: block; font-size: .78rem; word-break: break-all; color: var(--ink); }
 .nums { display: grid; grid-template-columns: 1fr 1fr; gap: .8rem; margin: 0 0 1rem; }
 .count { font-size: 2.1rem; font-variant-numeric: tabular-nums; font-weight: 700; margin: 0; }
 .count span { display: block; font-size: .92rem; font-weight: 500; color: var(--muted); }
 .btns { display: grid; grid-template-columns: 1fr 1fr; gap: .75rem; margin: 0 0 .85rem; }
 @media (max-width: 520px) { .btns { grid-template-columns: 1fr; } }
 a.btn.block, button.btn.block { display: block; width: 100%; text-align: center; font-size: 1.15rem; padding: 1rem 1.1rem; }
 a.btn.primary { background: #e8eaef; color: #0e1014; }
 button.btn.install { background: var(--gold-dim); color: #14110a; }
 pre { background: #0e0e0e; padding: .75rem .9rem; overflow: auto; border-radius: 8px; font-size: .82rem; }
 .meta { margin-top: 1rem; color: var(--muted); font-size: .92rem; }
 .iso { margin-top: .75rem; font-size: .85rem; color: #7d8696; }
 details.raw { margin-top: .8rem; }
 details.raw pre { max-height: 18rem; }
 footer { color: var(--muted); font-size: .9rem; }
 #meshStrip { border: 1px solid var(--gold); border-radius: 14px; padding: .85rem 1rem; background: var(--panel); margin: 0 0 1.1rem; display: flex; flex-wrap: wrap; align-items: center; gap: .7rem 1rem; font-size: .88rem; color: var(--muted); }
 #meshStrip .live { color: var(--ink); }
 #meshStrip .live b { color: var(--gold); font-size: 1.35rem; margin-right: .35rem; }
 #meshStrip .rollup b { color: var(--gold); }
 #meshStrip button { font: 700 .78rem/1 ui-monospace, Menlo, Consolas, monospace; height: 2rem; padding: 0 .75rem; border-radius: 8px; background: #101010; color: var(--ink); border: 1px solid var(--gold); cursor: pointer; }
 #meshStrip button:hover { background: #241c0d; color: var(--gold); }
 #meshStrip input { width: 10rem; padding: .4rem .55rem; border: 1px solid var(--gold); border-radius: 8px; background: #0e0e0e; color: var(--ink); font: inherit; }
 #meshProducts { flex-basis: 100%; margin: 0; }
 .peergrid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .7rem; margin: .7rem 0 0; }
 @media (max-width: 720px) { .peergrid { grid-template-columns: 1fr; } }
 .peer { border: 1px solid var(--line); border-radius: 10px; padding: .75rem .85rem; background: #101010; }
 .peer h3 { margin: 0 0 .25rem; font-size: .95rem; }
 .peer p { margin: 0; color: var(--muted); font-size: .86rem; }
 .peer .role { color: var(--gold); font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; font-family: ui-monospace, Menlo, Consolas, monospace; }
 .doorpath { background: #0e0e0e; border: 1px dashed var(--gold); border-radius: 10px; padding: .75rem .9rem; margin: .7rem 0; font-size: .82rem; }
 .surfaces { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .55rem; margin: .7rem 0; }
 @media (max-width: 720px) { .surfaces { grid-template-columns: 1fr; } }
</style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="brandrow">
        <img class="brandmark" src="/sigil.png" width="40" height="40" alt="" decoding="async">
      </div>
      <div class="appbar">
        <div>
          <h1>AZChat</h1>
          <p class="motto">Handles spend. Rooms seal. Mesh stays off.</p>
        </div>
        <p class="pill" id="api-pill">API · checking</p>
      </div>
      <p class="lede">v${VERSION} software by <strong>${AUTHOR}</strong> only. Spendable handles, ephemeral rooms, and an agent bus. Mesh hop default off. Not SMTP. Not AZMail. FragGate only. Forks are welcome and always allowed.</p>
      <nav class="toc" aria-label="Product sections">
        <a href="#workspace">Use UI</a>
        <a href="#surfaces">Dual surface</a>
        <a href="#peers">Softwares peers</a>
        <a href="#meshStrip">Live Nodes</a>
        <a href="#install">Download / install</a>
        <a href="#cite">Cite</a>
        <a href="/v1/skill">Skill</a>
        <a href="/mcp">MCP</a>
        <a href="/v1/fraggate/list">FragGate list</a>
        <a href="/openapi.json">OpenAPI</a>
        <a href="${GITHUB_REPO}">GitHub</a>
      </nav>
      <p class="banner">${escapeHtml(HONEST)}</p>
    </header>

    <div id="meshStrip" aria-label="Suite Live Nodes">
      <div class="live"><b id="meshLiveCount">0</b> Live Nodes</div>
      <div id="meshLine">Suite mesh: off (default). QNM-BUILD-1.0. QNS-CD-1.0. SPLIT THE WIRES. COLD-COPY SURVIVAL. Not an anonymity network.</div>
      <div class="rollup">live <b id="qnmLive">0</b> · locked <b id="qnmLocked">0</b> · isolated <b id="qnmIsolated">0</b></div>
      <div>No Node Gate · No public qnsd proxy · No auto-heal · SPLIT THE WIRES · COLD-COPY SURVIVAL · AZChat hop default off · Aziel Eliab only</div>
      <div>
        <input id="meshBearer" type="text" maxlength="80" placeholder="bearer (required to enable)" aria-label="mesh bearer">
        <button id="meshEnable" type="button" title="Suite proxy enable. Product-local mesh_enable is stub/REFUSE. GET never enables. Default off.">Enable</button>
        <button id="meshDisable" type="button" title="Disable suite mesh (always allowed)">Disable</button>
        <button id="meshJoin" type="button" title="Join as azchat. Refused while mesh is OFF. No auto-join.">Join</button>
        <button id="meshLeave" type="button" title="Leave this node. No auto-heal.">Leave</button>
      </div>
      <div id="meshProducts">Catalog MCP mesh_* · FragGate slug=mesh · /v1/mesh/* PROXY · QNS-CD-1.0 photon QNS1 (qnm-node local qnsd; hub cite only) · SPLIT THE WIRES · COLD-COPY SURVIVAL · not AnonBroadcast · not AZMail ring · not a Node Gate · not a Softwares-tab product</div>
    </div>

    <section class="workspace" id="workspace">
      <h2><span class="kicker">Live software</span>AZChat workspace</h2>
      <p class="lede">Use UI: catalog labels on this Worker — Health / Skill / Doctor / New handle / Rotate / Open room / Post / Pull / All rooms / Host room / Join room / Bus send / Bus poll / Verify receipt / Import-export. FragGate door proxy: <code>/v1/fraggate/list</code>, <code>/describe</code>, <code>/call</code> via AZIEL_RUNTIME. Suite mesh: <code>/v1/mesh/*</code> PROXY (default OFF). Room_open needs two live handle tokens and stays off the all-rooms list. Host puts a room on that list. Private means a passphrase is required to join. It is not end-to-end encryption. Stranger room_pull is 404.</p>
      <div class="workgrid">
        <form id="ws-form" autocomplete="off">
          <div class="row2">
            <div>
              <label for="label_a"><span class="kicker">Handle A label</span></label>
              <input id="label_a" type="text" value="agent-a">
              <label for="token_a"><span class="kicker">Handle A token</span></label>
              <input id="token_a" type="text" placeholder="minted token">
            </div>
            <div>
              <label for="label_b"><span class="kicker">Handle B label</span></label>
              <input id="label_b" type="text" value="agent-b">
              <label for="token_b"><span class="kicker">Handle B token</span></label>
              <input id="token_b" type="text" placeholder="second minted token">
            </div>
          </div>
          <label for="room_id"><span class="kicker">Room id</span></label>
          <input id="room_id" type="text" placeholder="opened or joined room">
          <label for="room_title"><span class="kicker">Room title</span></label>
          <input id="room_title" type="text" value="hall" maxlength="80">
          <label class="check" for="room_private"><input id="room_private" type="checkbox"> Private room — passphrase required to join</label>
          <label for="room_pass"><span class="kicker">Passphrase</span></label>
          <input id="room_pass" type="password" autocomplete="new-password" placeholder="required only when the room is private">
          <p class="meta" id="room-note">Private means a passphrase is required to join. It is not end-to-end encryption. The passphrase is not shown on the all-rooms list. Lamb Lens Service → Clarity → Peace. Author: Aziel Eliab only.</p>
          <label for="post_text"><span class="kicker">Room / bus text</span></label>
          <textarea id="post_text" rows="3">handles spend</textarea>
          <div class="row2">
            <div>
              <label for="bus_from"><span class="kicker">Bus from</span></label>
              <input id="bus_from" type="text" value="agent-a">
            </div>
            <div>
              <label for="bus_to"><span class="kicker">Bus to</span></label>
              <input id="bus_to" type="text" value="agent-b">
            </div>
          </div>
          <div class="actions">
            <button type="button" class="gold" id="btn-handle-a">New handle A</button>
            <button type="button" class="gold" id="btn-handle-b">New handle B</button>
            <button type="button" class="ghost" id="btn-rotate">Rotate A</button>
            <button type="button" class="ink" id="btn-room">Open room</button>
            <button type="button" class="ink" id="btn-host">Host room</button>
            <button type="button" class="ghost" id="btn-rooms">All rooms</button>
            <button type="button" class="ghost" id="btn-post">Room post</button>
            <button type="button" class="ghost" id="btn-pull">Room pull</button>
            <button type="button" class="ghost" id="btn-bus-send">Bus send</button>
            <button type="button" class="ghost" id="btn-bus-poll">Bus poll</button>
            <button type="button" class="ghost" id="btn-verify">Verify receipt</button>
            <button type="button" class="ghost" id="btn-export">Import/export</button>
            <button type="button" class="ghost" id="btn-health">Health</button>
            <button type="button" class="ghost" id="btn-skill">Skill</button>
            <button type="button" class="ghost" id="btn-doctor">Doctor</button>
            <button type="button" class="gold" id="btn-fraggate">FragGate call</button>
          </div>
          <ul id="room-list" class="roomlist" aria-label="All rooms"></ul>
        </form>
        <div>
          <div class="status" id="ws-status">No receipt yet. Mint two handles, then open a room. Mesh stays off.</div>
          <div class="metrics">
            <div class="metric"><b>Op</b><span id="last-op">—</span></div>
            <div class="metric"><b>Handle / room</b><span id="last-id">—</span></div>
            <div class="metric"><b>Receipt hash</b><span id="last-hash">—</span></div>
            <div class="metric"><b>Mesh</b><span>default off</span></div>
          </div>
          <details class="raw" open>
            <summary>Raw API result / debug</summary>
            <pre id="raw-json">{}</pre>
          </details>
        </div>
      </div>
    </section>

    <section class="card" id="surfaces">
      <h2><span class="kicker">Dual-surface law</span>Agent MCP · human Worker UI · /download</h2>
      <p class="lede">FragGate is THE single door. True engine is in-process on aziel-runtime 1.9.0 slug <code>azchat</code>. This Worker is the Softwares human door + counted <code>/download</code> + mesh peer. Do not gut either surface.</p>
      <div class="surfaces">
        <div class="peer"><span class="role">Agent</span><h3>MCP + FragGate</h3><p><a href="/mcp">POST /mcp</a> on this Worker, or catalog <a href="${CATALOG}mcp">POST /mcp</a> · slug <code>azchat</code>.</p></div>
        <div class="peer"><span class="role">Human</span><h3>This Worker UI</h3><p>Catalog labels on <a href="${HOST}/">the homepage</a>. Local <code>azchat ui</code> at 127.0.0.1:8878.</p></div>
        <div class="peer"><span class="role">Package</span><h3>Counted /download</h3><p><a href="/download?asset=${DEFAULT_ASSET}">gzip HTTP 200</a>. Isolated KV <code>AZCHAT_DOWNLOADS</code>. /v1 does not increment.</p></div>
      </div>
      <div class="doorpath" id="fraggate-path">
        <span class="kicker">Runtime FragGate call path</span>
        <p>Catalog door: <code>POST ${FRAGGATE_CALL}</code> body <code>{"slug":"azchat","op":"handle_new","payload":{}}</code></p>
        <p>List: <a href="${FRAGGATE_LIST}">${FRAGGATE_LIST}</a> · Describe: <a href="${FRAGGATE_DESCRIBE}">${FRAGGATE_DESCRIBE}</a> · Softwares: <a href="${SOFTWARE_TAB}">${SOFTWARE_TAB}</a></p>
        <p>This Worker PROXY (same door, not a second door): <a href="/v1/fraggate/list">GET /v1/fraggate/list</a> · <a href="/v1/fraggate/describe?slug=azchat">GET /v1/fraggate/describe</a> · <code>POST /v1/fraggate/call</code>. The <strong>FragGate call</strong> button uses the Worker proxy.</p>
      </div>
    </section>

    <section class="card" id="peers">
      <h2><span class="kicker">Softwares · Plain · Comms</span>Suite peers — do not merge · do not bridge</h2>
      <p class="lede">AZChat is Comms-domain software (07) next to AZMail. Not a mailer. FragGate remains THE single door.</p>
      <div class="peergrid">
        <div class="peer"><span class="role">Catalog door</span><h3><a href="${CATALOG}">aziel-runtime</a></h3><p>FragGate <code>/v1/fraggate/*</code>, <code>/v1/software</code>, <code>/mcp</code>. True AZChat engine. Kernel <a href="https://github.com/AzielEliab/fraggate">fraggate</a>.</p></div>
        <div class="peer"><span class="role">Not bridged</span><h3><a href="${AZMAIL_HOST}/">AZMail</a></h3><p>Mail airlock. Do not bridge AZChat ↔ AZMail. Not SMTP from this product. <a href="https://github.com/AzielEliab/azmail">github.com/AzielEliab/azmail</a></p></div>
        <div class="peer"><span class="role">Network neighbor</span><h3><a href="${AZNET_HOST}/">AZNet</a></h3><p>Silent verification side-net. Separate software.</p></div>
        <div class="peer"><span class="role">Evidence neighbor</span><h3><a href="${PEACELOCK_HOST}/">PeaceLock</a></h3><p>Chosen silence as a receipt. Separate software.</p></div>
      </div>
      <p class="meta">Hubs: <a href="${HUB_AZIELELIAB}">azieleliab.com</a> · <a href="${HUB_LIBRARY}">azielcorpuslibrary.net</a> · <a href="${HUB_GODLOCK}">godlock.uk</a></p>
    </section>

    <section class="card" id="install">
      <h2><span class="kicker">Counted package</span>Download and one-click install</h2>
      <div class="nums">
        <p class="count">${v}<span>Views</span></p>
        <p class="count">${n}<span>Downloads</span></p>
      </div>
      <p>Download saves the gzip from this Worker (HTTP 200, counted). One-click install copies a Terminal command. After it finishes, run <code>azchat ui</code> and open http://127.0.0.1:8878 on this computer only.</p>
      <div class="btns">
        <a class="btn block primary" href="/download?asset=${DEFAULT_ASSET}">Download</a>
        <button type="button" class="btn block install" id="install-btn">One-click install</button>
      </div>
      <pre id="install-cmd">${INSTALL_LINE}</pre>
      <p class="meta">The download count ticks on the Download click. No 302 to GitHub. Forks using this same link are counted automatically. ${DEFAULT_ASSET} — ${n} counted.</p>
      <p class="iso">Isolated counter: Worker <code>azchat-download-tracker</code>, project <code>azchat</code>, KV <code>AZCHAT_DOWNLOADS</code>. Not mixed with any other product. /v1 does not increment downloads.</p>
      <p class="meta">GitHub: stars ${gh.stars || 0} · forks ${gh.forks || 0} · watchers ${gh.watchers || 0} · release assets ${gh.release_download_count || 0}</p>
      <p class="meta">Peers (do not merge): <a href="${AZMAIL_HOST}/">AZMail</a> · <a href="${AZNET_HOST}/">AZNet</a> · <a href="${PEACELOCK_HOST}/">PeaceLock</a> · <a href="https://github.com/AzielEliab/fraggate">FragGate</a> · <a href="${CATALOG}">aziel-runtime</a> · hubs <a href="${HUB_LIBRARY}">azielcorpuslibrary.net</a> · <a href="${HUB_GODLOCK}">godlock.uk</a> · <a href="${HUB_AZIELELIAB}">azieleliab.com</a></p>
      <p class="meta"><a href="/stats">JSON stats</a> · <a href="/count">/count</a> · <a href="/openapi.json">OpenAPI</a> · <a href="/mcp">MCP</a> · <a href="/v1/fraggate/list">FragGate list</a> · <a href="/v1/mesh">/v1/mesh</a> · <a href="/v1/skill">Skill</a> · <a href="/v1/example">Example</a> · <a href="/ai">AI runtime</a> · <a href="${GITHUB_REPO}">GitHub</a> · <a href="${GITHUB_LATEST}">releases</a></p>
      <h3>Per repo / branch / fork</h3>
      <ul>${breakdownList(stats)}</ul>
    </section>

    <section class="cite" id="cite">
      <h2>How to cite</h2>
      <p>${escapeHtml(HOW_TO_CITE)}</p>
      <p>Author: <strong>${AUTHOR}</strong> only · License: Apache-2.0 · Forks welcome and always allowed · Machine-readable: <a href="/cite.json">/cite.json</a></p>
      <p class="meta">No DOI is invented here. Software deposit still needed. Cite GitHub and this Worker.</p>
      <p><a href="${CATALOG}">Catalog</a> · <a href="${CATALOG_PRODUCT}">Catalog product</a> · <a href="${GITHUB_REPO}">GitHub</a> · <a href="${HOST}/download">Download</a> · <a href="/llms.txt">llms.txt</a></p>
    </section>

    <footer>
      <p>Apache-2.0 · ${AUTHOR} · AZChat v${VERSION}</p>
      <p>Mesh GET never enables. Not SMTP. Not AZMail. FragGate only.</p>
    </footer>
  </div>
  <script>
  (function () {
    var lastReceipt = null;
    var lastResult = null;
    function $(id) { return document.getElementById(id); }
    function setStatus(kind, text) {
      var el = $("ws-status");
      el.className = "status" + (kind ? " " + kind : "");
      el.textContent = text;
    }
    function render() {
      var rec = lastReceipt || {};
      var data = lastResult || {};
      $("last-op").textContent = data.op || rec.op || "—";
      $("last-id").textContent = data.handle_id || data.room_id || rec.handle_id || rec.room_id || "—";
      $("last-hash").textContent = (rec && rec.receipt_sha256) || "—";
      $("raw-json").textContent = JSON.stringify(lastResult || {}, null, 2);
    }
    function isGetOp(path) {
      return path === "/v1/health" || path === "/v1/skill" || path === "/v1/doctor" || path === "/v1/example";
    }
    async function api(path, body) {
      var get = isGetOp(path);
      var res = await fetch(path, {
        method: get ? "GET" : "POST",
        headers: { "Content-Type": "application/json", "User-Agent": "Mozilla/5.0" },
        body: get ? undefined : JSON.stringify(body || {})
      });
      var ctype = (res.headers.get("Content-Type") || "");
      if (path === "/v1/skill" || ctype.indexOf("text/markdown") !== -1) {
        var text = await res.text();
        if (!res.ok) throw new Error("HTTP " + res.status);
        return { ok: true, op: "skill", skill: text };
      }
      var data = await res.json();
      if (!res.ok && data && data.error) return data;
      if (!res.ok) throw new Error((data && data.error) || ("HTTP " + res.status));
      return data;
    }
    function applyResult(data, fallbackMsg) {
      lastResult = data;
      if (data && data.receipt) lastReceipt = data.receipt;
      if (data && data.token && data.op === "handle_new") {
        if (! $("token_a").value) $("token_a").value = data.token;
        else if (! $("token_b").value) $("token_b").value = data.token;
      }
      if (data && data.token && data.op === "handle_rotate") $("token_a").value = data.token;
      if (data && data.room_id && (data.op === "room_open" || data.op === "room_host" || data.op === "room_join")) $("room_id").value = data.room_id;
      var ok = data && data.ok !== false;
      var msg = (data && (data.note || data.error || data.op || data.status)) || fallbackMsg;
      setStatus(ok ? "ok" : "bad", msg || "Done.");
      render();
    }
    async function run(fn, label) {
      try { applyResult(await fn(), label); }
      catch (err) { setStatus("bad", String(err.message || err)); }
    }
    $("btn-handle-a").onclick = function () { run(function () { return api("/v1/handle_new", { label: $("label_a").value }); }, "Handle A minted."); };
    $("btn-handle-b").onclick = function () { run(function () { return api("/v1/handle_new", { label: $("label_b").value }); }, "Handle B minted."); };
    $("btn-rotate").onclick = function () { run(function () { return api("/v1/handle_rotate", { token: $("token_a").value }); }, "Handle A rotated."); };
    function esc(s) {
      return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
    async function refreshRooms() {
      var data = await api("/v1/room_list", {});
      var list = $("room-list");
      var rooms = (data && data.rooms) || [];
      if (!rooms.length) {
        list.innerHTML = "<li>No hosted rooms yet.</li>";
        return data;
      }
      list.innerHTML = rooms.map(function (room) {
        var gate = room.private ? "private · passphrase required" : "open entry";
        return "<li><strong>" + esc(room.title || "room") + "</strong> <code>" + esc(room.room_id) + "</code> <span>" + esc(gate) + "</span> <span>" + esc(room.member_count) + " members</span> <button type=\\"button\\" data-join=\\"" + esc(room.room_id) + "\\" data-private=\\"" + (room.private ? "1" : "0") + "\\">Join</button></li>";
      }).join("");
      return data;
    }
    $("btn-room").onclick = function () { run(function () { return api("/v1/room_open", { token_a: $("token_a").value, token_b: $("token_b").value }); }, "Room opened."); };
    $("btn-host").onclick = function () {
      run(async function () {
        var body = { token: $("token_a").value, title: $("room_title").value, private: $("room_private").checked };
        if ($("room_private").checked) body.passphrase = $("room_pass").value;
        var data = await api("/v1/room_host", body);
        if (data && data.ok) $("room_pass").value = "";
        await refreshRooms();
        return data;
      }, "Room hosted.");
    };
    $("btn-rooms").onclick = function () { run(function () { return refreshRooms(); }, "All rooms."); };
    $("room-list").addEventListener("click", function (ev) {
      var btn = ev.target.closest ? ev.target.closest("button[data-join]") : null;
      if (!btn) return;
      var id = btn.getAttribute("data-join");
      var isPrivate = btn.getAttribute("data-private") === "1";
      run(async function () {
        var body = { token: $("token_a").value, room_id: id };
        if (isPrivate) body.passphrase = $("room_pass").value;
        var data = await api("/v1/room_join", body);
        if (data && data.ok) $("room_pass").value = "";
        await refreshRooms();
        return data;
      }, "Join.");
    });
    $("btn-post").onclick = function () { run(function () { return api("/v1/room_post", { token: $("token_a").value, room_id: $("room_id").value, text: $("post_text").value }); }, "Posted."); };
    $("btn-pull").onclick = function () { run(function () { return api("/v1/room_pull", { token: $("token_a").value, room_id: $("room_id").value }); }, "Pulled."); };
    $("btn-bus-send").onclick = function () { run(function () { return api("/v1/bus_send", { from: $("bus_from").value, to: $("bus_to").value, text: $("post_text").value }); }, "Bus frame sent."); };
    $("btn-bus-poll").onclick = function () { run(function () { return api("/v1/bus_poll", { agent: $("bus_to").value }); }, "Bus polled."); };
    $("btn-verify").onclick = function () { run(function () { return api("/v1/verify_receipt", { receipt: lastReceipt || {} }); }, "Receipt walked."); };
    $("btn-export").onclick = function () { run(function () { return api("/v1/import_export", { mode: "export" }); }, "Export (client-held)."); };
    $("btn-health").onclick = function () { run(function () { return api("/v1/health", {}); }, "Health. Catalog FragGate op. No writes."); };
    $("btn-skill").onclick = function () { run(function () { return api("/v1/skill", {}); }, "Skill. Catalog FragGate op."); };
    $("btn-doctor").onclick = function () { run(function () { return api("/v1/doctor", {}); }, "Doctor. Catalog FragGate LIVE_OPS."); };
    $("btn-fraggate").onclick = function () {
      run(function () {
        return api("/v1/fraggate/call", { slug: "azchat", op: "health", payload: {} });
      }, "FragGate call via Worker PROXY to aziel-runtime. Same door as catalog POST /v1/fraggate/call.");
    };
    var installBtn = $("install-btn");
    var installPre = $("install-cmd");
    var installCmd = ${JSON.stringify(INSTALL_LINE)};
    if (installBtn) {
      installBtn.addEventListener("click", function () {
        function done(ok) {
          installBtn.textContent = ok ? "Copied! Paste in Terminal, then run azchat ui" : "Select the command, copy it, then run azchat ui";
          installBtn.classList.add("copied");
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(installCmd).then(function () { done(true); }).catch(function () { done(false); });
        } else {
          done(false);
          if (installPre && window.getSelection) {
            var r = document.createRange();
            r.selectNodeContents(installPre);
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(r);
          }
        }
      });
    }
    fetch("/v1/health").then(function (res) { return res.json(); }).then(function (data) {
      var pill = $("api-pill");
      if (!pill) return;
      if (data && data.ok) {
        pill.textContent = "API live · v" + (data.version || "${VERSION}");
        pill.className = "pill ok";
      } else {
        pill.textContent = "API down";
        pill.className = "pill bad";
      }
    }).catch(function () {
      var pill = $("api-pill");
      if (pill) { pill.textContent = "API down"; pill.className = "pill bad"; }
    });
    function meshNum() {
      for (var i = 0; i < arguments.length; i++) {
        var raw = arguments[i];
        if (raw == null || raw === "") continue;
        var n = typeof raw === "number" ? raw : Number(String(raw).replace(/,/g, ""));
        if (Number.isFinite(n) && n >= 0) return Math.floor(n);
      }
      return 0;
    }
    function unwrapMesh(j) {
      if (!j || typeof j !== "object") return {};
      if (j.result && typeof j.result === "object") return Object.assign({}, j, j.result);
      if (j.mesh && typeof j.mesh === "object") return Object.assign({}, j, j.mesh);
      return j;
    }
    function paintMesh(raw) {
      var j = unwrapMesh(raw);
      var on = j.enabled === true || j.enabled === 1 || String(j.status || "").toLowerCase() === "on";
      var r = (j.rollup && typeof j.rollup === "object") ? j.rollup : {};
      var live = on ? meshNum(r.live, j.live_nodes, j.live) : 0;
      var locked = on ? meshNum(r.locked, j.locked_nodes, j.locked) : 0;
      var isolated = on ? meshNum(r.isolated, j.isolated_nodes, j.isolated) : 0;
      $("meshLiveCount").textContent = String(live);
      $("qnmLive").textContent = String(live);
      $("qnmLocked").textContent = String(locked);
      $("qnmIsolated").textContent = String(isolated);
      var line = $("meshLine");
      if (on) line.textContent = "Suite mesh: on · live " + live + " · locked " + locked + " · isolated " + isolated + ". QNS-CD-1.0. SPLIT THE WIRES. COLD-COPY SURVIVAL. Not an anonymity network.";
      else if (j.status === "unavailable" || (j.ok === false && j.error)) line.textContent = "Suite mesh: off (unavailable). QNM-BUILD-1.0. QNS-CD-1.0. SPLIT THE WIRES. COLD-COPY SURVIVAL. Not an anonymity network.";
      else line.textContent = "Suite mesh: off (default). QNM-BUILD-1.0. QNS-CD-1.0. SPLIT THE WIRES. COLD-COPY SURVIVAL. Not an anonymity network.";
      var products = j.products_present || j.products || [];
      var names = Array.isArray(products) ? products.map(function (p) { return typeof p === "string" ? p : (p && (p.product || p.slug)) || ""; }).filter(Boolean) : [];
      var nodes = Array.isArray(j.nodes) ? j.nodes : [];
      var extra = names.length ? " · products " + names.join(", ") : (nodes.length ? " · " + nodes.length + " node labels" : "");
      $("meshProducts").textContent = "Catalog MCP mesh_* · FragGate slug=mesh · /v1/mesh/* PROXY · QNS-CD-1.0 photon QNS1 (qnm-node local qnsd; hub cite only) · SPLIT THE WIRES · COLD-COPY SURVIVAL · not AnonBroadcast · not AZMail ring · AZChat hop default off · not a Node Gate · not a Softwares-tab product" + extra;
    }
    async function meshGet(path) {
      var r = await fetch(path, { headers: { "user-agent": "Mozilla/5.0", accept: "application/json" } });
      return r.json();
    }
    async function meshPost(path, payload) {
      var r = await fetch(path, { method: "POST", headers: { "content-type": "application/json", "user-agent": "Mozilla/5.0" }, body: JSON.stringify(payload || {}) });
      return r.json();
    }
    async function refreshMesh() {
      try {
        var status = await meshGet("/v1/mesh");
        var merged = status;
        var inner = unwrapMesh(status);
        var on = inner.enabled === true;
        if (on) {
          try {
            var nodes = await meshGet("/v1/mesh/nodes");
            merged = Object.assign({}, inner, unwrapMesh(nodes));
          } catch (e) { /* status is enough */ }
        }
        paintMesh(merged);
        var nodeId = sessionStorage.getItem("azchat_mesh_node");
        if (on && nodeId) {
          try { await meshPost("/v1/mesh/heartbeat", { node_id: nodeId }); } catch (e) { /* no auto-heal */ }
        }
      } catch (e) {
        paintMesh({ ok: false, enabled: false, status: "unavailable", error: "mesh_unavailable" });
      }
    }
    $("meshEnable").onclick = async function () {
      var bearer = ($("meshBearer").value || "").trim();
      paintMesh(await meshPost("/v1/mesh/enable", bearer ? { bearer: bearer } : {}));
      refreshMesh();
    };
    $("meshDisable").onclick = async function () {
      sessionStorage.removeItem("azchat_mesh_node");
      paintMesh(await meshPost("/v1/mesh/disable", {}));
      refreshMesh();
    };
    $("meshJoin").onclick = async function () {
      var j = await meshPost("/v1/mesh/join", { product: "azchat", label: "AZChat Worker" });
      var inner = unwrapMesh(j);
      var id = inner.node_id || inner.id || (inner.session && inner.session.node_id);
      if (id) sessionStorage.setItem("azchat_mesh_node", String(id));
      paintMesh(j);
      refreshMesh();
    };
    $("meshLeave").onclick = async function () {
      var id = sessionStorage.getItem("azchat_mesh_node");
      if (id) await meshPost("/v1/mesh/leave", { node_id: id });
      sessionStorage.removeItem("azchat_mesh_node");
      refreshMesh();
    };
    window.addEventListener("pagehide", function () {
      var id = sessionStorage.getItem("azchat_mesh_node");
      if (!id || typeof navigator.sendBeacon !== "function") return;
      try { navigator.sendBeacon("/v1/mesh/leave", new Blob([JSON.stringify({ node_id: id })], { type: "application/json" })); } catch (e) { /* leave expires in 5 minutes */ }
    });
    refreshMesh();
    refreshRooms().catch(function () { /* list fills when the API answers */ });
    setInterval(refreshMesh, 30000);
    document.addEventListener("visibilitychange", function () { if (!document.hidden) refreshMesh(); });
    render();
  })();
  </script>
</body>
</html>`;
}
