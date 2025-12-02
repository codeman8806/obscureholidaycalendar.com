import os
import re
from pathlib import Path

HOLIDAY_DIR = Path("holiday")

CSS_LINK = '<link rel="stylesheet" href="/styles.css">\n'

INSTAGRAM_BLOCK = """
<div class="social-follow">
    <p>Follow us on Instagram:</p>
    <a href="https://instagram.com/obscureholidaycalendar" target="_blank" class="ig-link">
        @obscureholidaycalendar
    </a>
</div>
"""


def remove_inline_css(html):
    return re.sub(r"<style[\s\S]*?</style>", "", html, flags=re.IGNORECASE)


def add_stylesheet_link(html):
    if 'href="/styles.css"' in html:
        return html
    head_close = html.lower().find("</head>")
    if head_close == -1:
        return html
    return html[:head_close] + CSS_LINK + html[head_close:]


def insert_instagram(html):
    if "@obscureholidaycalendar" in html:
        return html  # already exists

    # Find brand icon
    brand_pos = html.find('<img src="/assets/app-icon.png')
    if brand_pos == -1:
        return html

    close_tag = html.find(">", brand_pos)
    insertion_point = close_tag + 1

    return html[:insertion_point] + INSTAGRAM_BLOCK + html[insertion_point:]


def cleanup_page(path):
    html = path.read_text(encoding="utf-8")
    original = html

    html = remove_inline_css(html)
    html = add_stylesheet_link(html)
    html = insert_instagram(html)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    updated = 0

    for root, dirs, files in os.walk(HOLIDAY_DIR):
        if "index.html" not in files:
            continue
        if cleanup_page(Path(root) / "index.html"):
            updated += 1

    print(f"Visual upgrade applied to {updated} holiday pages.")


if __name__ == "__main__":
    main()

