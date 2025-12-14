import os
import re
import datetime
import json
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

DOMAIN = "https://www.obscureholidaycalendar.com"
HOLIDAY_DIR = "holiday"
OUTPUT_DIR = "sitemaps"
HOLIDAYS_JSON = Path("holidays.json")
STATIC_PAGES = [
    f"{DOMAIN}/",
    f"{DOMAIN}/holiday/",
    f"{DOMAIN}/about/",
    f"{DOMAIN}/contact/",
    f"{DOMAIN}/privacy/",
    f"{DOMAIN}/discord-bot/",
    f"{DOMAIN}/discord-bot/success.html",
    f"{DOMAIN}/discord-bot/canceled.html",
]

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_slug_dates():
    """
    Return mapping of slug -> MM-DD string from holidays.json
    """
    if not HOLIDAYS_JSON.exists():
        return {}
    data = json.loads(HOLIDAYS_JSON.read_text(encoding="utf-8"))
    holidays = data.get("holidays", {})
    mapping = {}
    for date_key, items in holidays.items():
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            if not name:
                continue
            slug = item.get("slug") or slugify(name)
            mapping[slug] = item.get("date", date_key)
    return mapping


def create_sitemap(urls, output_file):
    urlset = Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for url, lastmod in urls:
        url_el = SubElement(urlset, "url")
        loc = SubElement(url_el, "loc")
        loc.text = url

        if lastmod:
            last = SubElement(url_el, "lastmod")
            last.text = lastmod

    tree = ElementTree(urlset)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def create_sitemap_index(files, output_file):
    sitemapindex = Element("sitemapindex")
    sitemapindex.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    for fname in files:
        sm = SubElement(sitemapindex, "sitemap")
        loc = SubElement(sm, "loc")
        loc.text = f"{DOMAIN}/sitemaps/{fname}"

    tree = ElementTree(sitemapindex)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def main():
    monthly = {f"{m:02d}": [] for m in range(1, 13)}
    sitemap_files = []
    today_str = datetime.date.today().isoformat()
    slug_dates = load_slug_dates()

    # Walk holiday directory
    for folder in Path(HOLIDAY_DIR).iterdir():
        index_file = folder / "index.html"
        if not index_file.exists():
            continue

        slug = folder.name
        url = f"{DOMAIN}/holiday/{slug}/"

        date_mmdd = slug_dates.get(slug)
        lastmod = None
        if date_mmdd and "-" in date_mmdd:
            try:
                mm, dd = date_mmdd.split("-")
                lastmod = f"2025-{int(mm):02d}-{int(dd):02d}"
            except Exception:
                pass

        try:
            html = index_file.read_text(encoding="utf-8")
            m = re.search(r'<meta name="last-modified" content="([\\d-]+)"', html, flags=re.IGNORECASE)
            if m:
                lastmod = m.group(1)
        except Exception:
            pass

        month_bucket = date_mmdd.split("-")[0] if date_mmdd and "-" in date_mmdd else "12"
        monthly[month_bucket].append((url, lastmod))

    # Generate monthly sitemaps
    for month, entries in monthly.items():
        if not entries:
            continue

        filename = f"sitemap-2025-{month}.xml"
        filepath = os.path.join(OUTPUT_DIR, filename)

        create_sitemap(entries, filepath)
        sitemap_files.append(filename)

    # Static pages sitemap
    static_entries = [(url, today_str) for url in STATIC_PAGES]
    static_filename = "sitemap-static.xml"
    create_sitemap(static_entries, os.path.join(OUTPUT_DIR, static_filename))
    sitemap_files.append(static_filename)

    # Generate index
    create_sitemap_index(sitemap_files, "sitemap-index.xml")

    print("Done! Generated sitemap-index.xml and monthly sitemaps.")


if __name__ == "__main__":
    main()
