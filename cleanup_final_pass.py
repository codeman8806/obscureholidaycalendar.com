import os
import re
from pathlib import Path


HOLIDAY_DIR = Path("holiday")

# Patterns to remove
LEGACY_BLOCKS = [
    r"<!-- STORE-BUTTONS-CSS-START -->.*?<!-- STORE-BUTTONS-CSS-END -->",
    r"<!-- BRAND-ICON-CSS-START -->.*?<!-- BRAND-ICON-CSS-END -->",
]

# Footer block pattern
FOOTER_PATTERN = r"<!-- HOLIDAY-FOOTER -->.*?$(.*)"
FOOTER_SINGLE = r"<!-- HOLIDAY-FOOTER -->"

def extract_footer(html):
    """
    Extract the holiday footer block if it exists anywhere outside </html>.
    """
    m = re.search(r"<!-- HOLIDAY-FOOTER -->.*", html, flags=re.DOTALL)
    if not m:
        return None
    return m.group(0)


def remove_footer(html, footer):
    """
    Removes the footer block from original location.
    """
    if footer:
        return html.replace(footer, "")
    return html


def place_footer_inside_body(html, footer):
    """
    Inserts footer just before </body>.
    """
    if not footer:
        return html
    if "</body>" not in html.lower():
        return html

    # Normalize body closing for search
    body_close_idx = html.lower().rfind("</body>")
    return html[:body_close_idx] + "\n" + footer + "\n</body>" + html[body_close_idx+7:]


def remove_legacy_css(html):
    """
    Removes old CSS blocks defined by LEGACY_BLOCKS.
    """
    for pattern in LEGACY_BLOCKS:
        html = re.sub(pattern, "", html, flags=re.DOTALL | re.IGNORECASE)
    return html


def trim_after_html(html):
    """
    Remove ANYTHING after </html> so pages are valid.
    """
    m = re.search(r"</html>", html, flags=re.IGNORECASE)
    if not m:
        return html

    end_pos = m.end()
    return html[:end_pos]


def main():
    if not HOLIDAY_DIR.exists():
        print("holiday/ directory not found.")
        return

    updated = 0

    for root, dirs, files in os.walk(HOLIDAY_DIR):
        if "index.html" not in files:
            continue

        path = Path(root) / "index.html"
        html = path.read_text(encoding="utf-8")

        original_html = html

        # 1) Extract footer
        footer_block = extract_footer(html)

        # 2) Remove legacy CSS
        html = remove_legacy_css(html)

        # 3) Remove footer from old position
        if footer_block:
            html = remove_footer(html, footer_block)

        # 4) Trim any HTML after </html> to clean garbage
        html = trim_after_html(html)

        # 5) Now reinsert footer INSIDE <body>
        if footer_block:
            html = place_footer_inside_body(html, footer_block)

        if html != original_html:
            path.write_text(html, encoding="utf-8")
            updated += 1

    print(f"Final cleanup complete! Updated {updated} holiday pages.")


if __name__ == "__main__":
    main()

