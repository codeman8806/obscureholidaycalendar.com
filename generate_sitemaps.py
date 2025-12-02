import os
import re
import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

DOMAIN = "https://www.obscureholidaycalendar.com"
HOLIDAY_DIR = "holiday"
OUTPUT_DIR = "sitemaps"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Regex to detect YYYY-MM-DD in each holiday page
DATE_REGEX = re.compile(r'<div class="date">([A-Za-z]+)\s+(\d{1,2})</div>')

# Map month names to numbers
MONTH_MAP = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

def extract_date(html):
    """
    Extracts the pretty date (e.g., December 30) from the holiday page
    and converts it to YYYY-MM-DD format.
    """
    m = DATE_REGEX.search(html)
    if not m:
        return None

    month_name, day = m.group(1), m.group(2)
    month_num = MONTH_MAP.get(month_name)

    if not month_num:
        return None

    # Use year 2025 since holidays repeat annually
    return f"2025-{month_num}-{int(day):02d}"


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

    # Walk holiday directory
    for folder in Path(HOLIDAY_DIR).iterdir():
        index_file = folder / "index.html"
        if not index_file.exists():
            continue

        slug = folder.name
        url = f"{DOMAIN}/holiday/{slug}/"

        html = index_file.read_text(encoding="utf-8")
        date = extract_date(html)

        if date:
            month = date[5:7]
            monthly[month].append((url, date))
        else:
            # If date missing, put into December by default
            monthly["12"].append((url, None))

    # Generate monthly sitemaps
    for month, entries in monthly.items():
        if not entries:
            continue

        filename = f"sitemap-2025-{month}.xml"
        filepath = os.path.join(OUTPUT_DIR, filename)

        create_sitemap(entries, filepath)
        sitemap_files.append(filename)

    # Generate index
    create_sitemap_index(sitemap_files, "sitemap-index.xml")

    print("Done! Generated sitemap-index.xml and monthly sitemaps.")


if __name__ == "__main__":
    main()

