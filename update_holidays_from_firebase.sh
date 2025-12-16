#!/usr/bin/env bash
# Refresh holidays from Firebase, snapshot them, and sync into the bot copy.
# Usage:
#   FIREBASE_URL="https://gen-lang-client-0034763265-default-rtdb.firebaseio.com/.json" ./update_holidays_from_firebase.sh
# If FIREBASE_URL is not set, the default above is used.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
URL="${FIREBASE_URL:-https://gen-lang-client-0034763265-default-rtdb.firebaseio.com/.json}"

ROOT="$ROOT" URL="$URL" python3 - <<'PY'
import datetime
import json
import os
import pathlib
import sys
import urllib.request

root = pathlib.Path(os.environ["ROOT"])
url = os.environ["URL"]

try:
    with urllib.request.urlopen(url) as resp:
        raw = resp.read()
except Exception as exc:  # pragma: no cover
    sys.exit(f"Failed to download holidays from {url}: {exc}")

try:
    data = json.loads(raw)
except Exception as exc:  # pragma: no cover
    sys.exit(f"Downloaded data is not valid JSON: {exc}")

holidays = data.get("holidays", data)
if not isinstance(holidays, list):  # pragma: no cover
    sys.exit("Expected a list of holidays under 'holidays' or at root.")

timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
snap_path = root / f"holidays_snapshot_{timestamp}.json"
out_path = root / "holidays.json"
bot_path = root / "bot" / "holidays.json"

# Write a pretty snapshot for diffing and archival.
snap_path.write_text(json.dumps({"holidays": holidays}, ensure_ascii=False, indent=2))

# Write the canonical file used by the site generator.
out_path.write_text(json.dumps({"holidays": holidays}, ensure_ascii=False, indent=2))

# Keep the bot copy in sync.
bot_path.write_text(out_path.read_text())

print(f"Fetched {len(holidays)} holidays")
print(f"Snapshot saved to {snap_path.name}")
print("Updated holidays.json and bot/holidays.json")
PY
