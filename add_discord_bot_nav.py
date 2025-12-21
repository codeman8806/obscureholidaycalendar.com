#!/usr/bin/env python3
"""One-off script to insert the Discord Bot link into nav menus.

- Looks for a <nav class="nav-links"> block.
- Inserts after the Holidays link.
- Skips files that already include /discord-bot/.
- Idempotent.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
INSERT_AFTER = '<a href="/holiday/">Holidays</a>'
INSERT_LINK = '<a href="/discord-bot/">Discord Bot</a>'


def should_skip(text: str) -> bool:
    return "/discord-bot/" in text


def update_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if should_skip(text):
        return False
    if INSERT_AFTER not in text:
        return False
    updated = text.replace(INSERT_AFTER, f"{INSERT_AFTER}\n      {INSERT_LINK}", 1)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*.html"):
        # Skip generated sitemaps or other non-page HTML if any.
        if "sitemaps" in path.parts:
            continue
        if update_html(path):
            changed += 1
    print(f"Updated {changed} file(s).")


if __name__ == "__main__":
    main()
