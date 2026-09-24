#!/usr/bin/env bash
# AZChat one-click install. Counted download via this project's Worker.
# Usage: curl -fsSL https://azchat-download-tracker.vibelock.workers.dev/install.sh | bash
set -euo pipefail

HOST="${AZCHAT_HOME_HOST:-https://azchat-download-tracker.vibelock.workers.dev}"
ASSET="${AZCHAT_HOME_ASSET:-azchat-0.1.0.tar.gz}"
WORKDIR="${AZCHAT_HOME:-$HOME/azchat}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "Downloading counted tarball from ${HOST}/download (User-Agent Mozilla/5.0)…"
curl -fsSL -A 'Mozilla/5.0' "${HOST}/download?asset=${ASSET}" -o "${ASSET}"

tar -xzf "${ASSET}"
DIR="$(find . -maxdepth 1 -type d -name 'azchat-*' | head -n 1)"
if [ -n "${DIR}" ]; then
  cd "${DIR}"
fi

python3 -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .

echo
echo "Installed AZChat."
echo "Next: azchat ui"
echo "Open http://127.0.0.1:8878/"
echo "Author: Aziel Eliab."
