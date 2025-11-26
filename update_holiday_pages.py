#!/usr/bin/env python3
import os
import json
import random
import re

# ---------------------------------------------
# PATH CONFIG (auto-detect root)
# ---------------------------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
HOLIDAYS_DIR = os.path.join(ROOT_DIR, "holiday")
HOLIDAY_DB = os.path.join(ROOT_DIR, "holidays.json")

FOOTER_MARKER = "<!-- HOLIDAY-FOOTER -->"
BREADCRUMB_MARKER = "<!-- BREADCRUMB-SCHEMA -->"

# Popular evergreen holidays for extra linking
POPULAR = [
    ("pi-day", "Pi Day"),
    ("talk-like-a-pirate-day", "Talk Like a Pirate Day"),
    ("national-cat-day", "National Cat Day"),
    ("national-pizza-day", "National Pizza Day"),
    ("star-wars-day", "Star Wars Day (May the 4th)"),
]


# ---------------------------------------------
# UTIL: slugify from holiday name → folder name
# ---------------------------------------------
def slugify(name: str) -> str:
    s = name.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


# ---------------------------------------------
# LOAD DATA FROM holidays.json
# ---------------------------------------------
def load_holiday_data():
    with open(HOLIDAY_DB, "r") as f:
        data = json.load(f)

    holidays_root = data.get("holidays", {})

    holiday_by_slug = {}  # slug -> title
    date_by_slug = {}     # slug -> (month, day)

    for mmdd, holiday_list in holidays_root.items():
        try:
            month_str, day_str = mmdd.split("-")
            month = int(month_str)
            day = int(day_str)
        except Exception:
            print(f"⚠️ Invalid date format in JSON: {mmdd}")
            continue

        for h in holiday_list:
            name = h.get("name")
            if not name:
                continue

            slug = slugify(name)
            holiday_by_slug[slug] = name
            date_by_slug[slug] = (month, day)

    return holiday_by_slug, date_by_slug


# ---------------------------------------------
# BUILD JSON-LD BREADCRUMB SCHEMA
# ---------------------------------------------
def build_breadcrumb_schema(slug: str, title: str) -> str:
    url = f"https://www.obscureholidaycalendar.com/holiday/{slug}/"
    schema = f"""
{BREADCRUMB_MARKER}
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.obscureholidaycalendar.com/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Holidays",
      "item": "https://www.obscureholidaycalendar.com/holiday/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{title}",
      "item": "{url}"
    }}
  ]
}}
</script>
"""
    return schema


# ---------------------------------------------
# BUILD INTERNAL-LINK FOOTER HTML
# ---------------------------------------------
def build_footer(prev_slug: str, next_slug: str, random_slug: str) -> str:
    footer_html = f"""
{FOOTER_MARKER}
<hr>
<h3>More Fun Holidays</h3>
<ul>
  <li>Yesterday: <a href="/holiday/{prev_slug}/">{prev_slug.replace('-', ' ').title()}</a></li>
  <li>Tomorrow: <a href="/holiday/{next_slug}/">{next_slug.replace('-', ' ').title()}</a></li>
  <li>Random Holiday: <a href="/holiday/{random_slug}/">{random_slug.replace('-', ' ').title()}</a></li>
  <li>Popular Holidays:</li>
  <ul>
{"".join(f'    <li><a href="/holiday/{slug}/">{name}</a></li>' for slug, name in POPULAR)}
  </ul>
</ul>
"""
    return footer_html


# ---------------------------------------------
# MAIN UPDATE FUNCTION
# ---------------------------------------------
def update_all_holiday_pages():
    holiday_by_slug, date_by_slug = load_holiday_data()

    # Keep only slugs that actually exist in /holiday/
    existing_slugs = []
    for slug in holiday_by_slug:
        html_path = os.path.join(HOLIDAYS_DIR, slug, "index.html")
        if os.path.exists(html_path):
            existing_slugs.append(slug)
        else:
            # Not an error — not all holidays must exist locally
            pass

    if not existing_slugs:
        print("❌ No holiday pages found under /holiday.")
        return

    # Sort by calendar order: (month, day, slug)
    slugs_sorted = sorted(
        existing_slugs,
        key=lambda s: (date_by_slug[s][0], date_by_slug[s][1], s),
    )

    total = len(slugs_sorted)
    print(f"Found {total} holiday pages.\n")

    for i, slug in enumerate(slugs_sorted):
        html_path = os.path.join(HOLIDAYS_DIR, slug, "index.html")
        title = holiday_by_slug.get(slug, slug.replace("-", " ").title())

        # Determine yesterday/tomorrow
        prev_slug = slugs_sorted[i - 1] if i > 0 else slugs_sorted[-1]
        next_slug = slugs_sorted[i + 1] if i < total - 1 else slugs_sorted[0]

        # Random holiday link
        if total > 1:
            options = [s for s in slugs_sorted if s != slug]
            random_slug = random.choice(options)
        else:
            random_slug = slug

        footer_html = build_footer(prev_slug, next_slug, random_slug)
        breadcrumb_json = build_breadcrumb_schema(slug, title)

        # Read and sanitize existing HTML
        with open(html_path, "r") as f:
            html = f.read()

        for marker in (BREADCRUMB_MARKER, FOOTER_MARKER):
            if marker in html:
                html = html.split(marker)[0].rstrip()

        # Compose new HTML
        new_html = (
            html.rstrip()
            + "\n\n"
            + breadcrumb_json
            + "\n"
            + footer_html
            + "\n"
        )

        with open(html_path, "w") as f:
            f.write(new_html)

        print(f"✅ Updated: {slug}")

    print("\n🎉 All holiday pages updated successfully!")


if __name__ == "__main__":
    update_all_holiday_pages()

