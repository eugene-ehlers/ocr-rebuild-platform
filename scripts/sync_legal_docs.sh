#!/usr/bin/env bash
set -e

ROOT="/home/cloudshell-user/ocr-rebuild-platform"

SRC="$ROOT/docs/10_legal"
DST="$ROOT/frontend/src/content/legal"

echo "== syncing legal docs from governed source =="
mkdir -p "$DST"

cp "$SRC"/*.md "$DST"/

echo "== sync complete =="
ls -1 "$DST"
