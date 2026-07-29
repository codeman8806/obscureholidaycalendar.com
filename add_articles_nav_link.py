"""
One-off, idempotent script: inserts an "Articles" link into every page's
site-wide nav and footer, right after the existing "Holidays" link.

Scoped to the specific <nav class="nav-links"> and <div class="footer-links">
containers so it doesn't get confused by unrelated "Holidays" links elsewhere
on the page (e.g. breadcrumbs on individual holiday pages).

Safe to re-run — skips any file that already has an /articles/ link.
"""
import re
from pathlib import Path

ROOT = Path(".")
HOLIDAYS_LINK = '<a href="/holiday/">Holidays</a>'
ARTICLES_LINK = '<a href="/articles/">Articles</a>'

NAV_BLOCK_RE = re.compile(r'<nav class="nav-links">.*?</nav>', re.S)
FOOTER_BLOCK_RE = re.compile(r'<div class="footer-links">.*?</div>', re.S)


def insert_articles_link(block_text, indent):
    if HOLIDAYS_LINK not in block_text:
        return block_text, False
    new_block = block_text.replace(
        HOLIDAYS_LINK, HOLIDAYS_LINK + f"\n{indent}{ARTICLES_LINK}", 1
    )
    return new_block, True


changed = []
skipped_already_present = []
skipped_no_match = []

for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts:
        continue
    text = path.read_text(encoding="utf-8")
    if HOLIDAYS_LINK not in text:
        continue
    if 'href="/articles/"' in text:
        skipped_already_present.append(str(path))
        continue

    any_changed = False

    nav_match = NAV_BLOCK_RE.search(text)
    if nav_match:
        new_block, did_change = insert_articles_link(nav_match.group(0), "      ")
        if did_change:
            text = text[: nav_match.start()] + new_block + text[nav_match.end() :]
            any_changed = True

    footer_match = FOOTER_BLOCK_RE.search(text)
    if footer_match:
        new_block, did_change = insert_articles_link(footer_match.group(0), "      ")
        if did_change:
            text = text[: footer_match.start()] + new_block + text[footer_match.end() :]
            any_changed = True

    if any_changed:
        path.write_text(text, encoding="utf-8")
        changed.append(str(path))
    else:
        skipped_no_match.append(str(path))

print(f"Changed: {len(changed)} files")
print(f"Already had /articles/ link (skipped): {len(skipped_already_present)} files")
print(f"No nav-links/footer-links match found (skipped): {len(skipped_no_match)} files")
if skipped_no_match:
    print("Files with no match:")
    for p in skipped_no_match:
        print(" ", p)
