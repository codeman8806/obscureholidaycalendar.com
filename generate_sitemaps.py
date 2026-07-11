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
CURRENT_YEAR = datetime.date.today().year
STATIC_PAGE_PATHS = [
    "/",
    "/holiday/",
    "/reports/",
    "/reports/2026-national-day-report/",
    "/about/",
    "/articles/",
    "/contact/",
    "/privacy/",
    "/subprocessors/",
    "/app/",
    "/discord-bot/",
    "/discord-bot/success.html",
    "/discord-bot/canceled.html",
    "/discord-bot/privacy.html",
    "/discord-bot/terms.html",
    "/slack-bot/",
    "/slack-bot/success.html",
    "/slack-bot/admin-installs.html",
    "/slack-bot/installed.html",
    "/slack-bot/terms.html",
]

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_slug_dates():
    """
    Return mapping of slug -> MM-DD string from holidays.json's fixed-date
    holidays, plus a resolved MM-DD for this year for any floatingHolidays
    entry whose dateRule can be resolved (see resolve_date_rule below).
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

    for slug, entry in data.get("floatingHolidays", {}).items():
        resolved = resolve_date_rule(entry.get("dateRule"), CURRENT_YEAR)
        if resolved:
            mapping[slug] = f"{resolved[0]:02d}-{resolved[1]:02d}"
    return mapping


# --- floatingHolidays dateRule resolver ---
# Mirrors assets/floating-dates.js exactly (same verified seasonal-marker
# table, sourced from astropixels.com/ephemeris/soleq2001.html and converted
# UTC->US-Eastern calendar date). Keep the two in sync if either changes.
_SEASONAL_MARKERS = {
    2024: [(3, 19), (6, 20), (9, 22), (12, 21)], 2025: [(3, 20), (6, 20), (9, 22), (12, 21)],
    2026: [(3, 20), (6, 21), (9, 22), (12, 21)], 2027: [(3, 20), (6, 21), (9, 23), (12, 21)],
    2028: [(3, 19), (6, 20), (9, 22), (12, 21)], 2029: [(3, 20), (6, 20), (9, 22), (12, 21)],
    2030: [(3, 20), (6, 21), (9, 22), (12, 21)], 2031: [(3, 20), (6, 21), (9, 23), (12, 21)],
    2032: [(3, 19), (6, 20), (9, 22), (12, 21)], 2033: [(3, 20), (6, 20), (9, 22), (12, 21)],
    2034: [(3, 20), (6, 21), (9, 22), (12, 21)], 2035: [(3, 20), (6, 21), (9, 23), (12, 21)],
    2036: [(3, 19), (6, 20), (9, 22), (12, 21)], 2037: [(3, 20), (6, 20), (9, 22), (12, 21)],
    2038: [(3, 20), (6, 21), (9, 22), (12, 21)], 2039: [(3, 20), (6, 21), (9, 22), (12, 21)],
    2040: [(3, 19), (6, 20), (9, 22), (12, 21)], 2041: [(3, 20), (6, 20), (9, 22), (12, 21)],
    2042: [(3, 20), (6, 21), (9, 22), (12, 21)], 2043: [(3, 20), (6, 21), (9, 22), (12, 21)],
    2044: [(3, 19), (6, 20), (9, 22), (12, 21)], 2045: [(3, 20), (6, 20), (9, 22), (12, 21)],
    2046: [(3, 20), (6, 21), (9, 22), (12, 21)], 2047: [(3, 20), (6, 21), (9, 22), (12, 21)],
    2048: [(3, 19), (6, 20), (9, 22), (12, 21)], 2049: [(3, 20), (6, 20), (9, 22), (12, 21)],
    2050: [(3, 20), (6, 20), (9, 22), (12, 21)],
}
_EVENT_INDEX = {"march-equinox": 0, "june-solstice": 1, "september-equinox": 2, "december-solstice": 3}
_SEASON_TO_EVENT = {
    "solstice": {"summer": "june-solstice", "winter": "december-solstice"},
    "equinox": {"spring": "march-equinox", "fall": "september-equinox"},
}


def _resolve_seasonal_marker(year, event_key):
    row = _SEASONAL_MARKERS.get(year)
    if not row or not event_key:
        return None
    idx = _EVENT_INDEX.get(event_key)
    if idx is None:
        return None
    return row[idx]


def _resolve_nth_weekday(year, month, weekday, ordinal):
    # weekday: 0=Sun..6=Sat (Python's date.weekday() is Mon=0..Sun=6, so convert)
    if ordinal == -1:
        next_month_first = datetime.date(year + (month // 12), (month % 12) + 1, 1)
        last = next_month_first - datetime.timedelta(days=1)
        last_wd = (last.weekday() + 1) % 7
        diff = (last_wd - weekday + 7) % 7
        day = last.day - diff
        return (month, day)
    first = datetime.date(year, month, 1)
    first_wd = (first.weekday() + 1) % 7
    offset = (weekday - first_wd + 7) % 7
    return (month, 1 + offset + (ordinal - 1) * 7)


def _resolve_relative_to_event(year, event, weekday, direction):
    anchor = _resolve_seasonal_marker(year, event)
    if not anchor:
        return None
    d = datetime.date(year, anchor[0], anchor[1])
    step = -1 if direction == "before" else 1
    while True:
        d += datetime.timedelta(days=step)
        if (d.weekday() + 1) % 7 == weekday:
            return (d.month, d.day)


def resolve_date_rule(date_rule, year):
    if not date_rule or not date_rule.get("type"):
        return None
    rule_type = date_rule["type"]
    if rule_type == "nth-weekday-of-month":
        return _resolve_nth_weekday(year, date_rule["month"], date_rule["weekday"], date_rule["ordinal"])
    if rule_type == "solstice":
        return _resolve_seasonal_marker(year, _SEASON_TO_EVENT["solstice"].get(date_rule.get("season")))
    if rule_type == "equinox":
        return _resolve_seasonal_marker(year, _SEASON_TO_EVENT["equinox"].get(date_rule.get("season")))
    if rule_type == "relative-to-event":
        return _resolve_relative_to_event(year, date_rule["event"], date_rule["weekday"], date_rule["direction"])
    return None


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

    for fname, lastmod in files:
        sm = SubElement(sitemapindex, "sitemap")
        loc = SubElement(sm, "loc")
        loc.text = f"{DOMAIN}/sitemaps/{fname}"
        if lastmod:
            last = SubElement(sm, "lastmod")
            last.text = lastmod

    tree = ElementTree(sitemapindex)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def static_page_lastmod(path: str, fallback: str) -> str:
    rel = path.lstrip("/")
    local_path = Path("index.html") if not rel else Path(rel)
    if path.endswith("/"):
        local_path = Path(rel) / "index.html" if rel else Path("index.html")
    try:
        if local_path.exists():
            return datetime.date.fromtimestamp(local_path.stat().st_mtime).isoformat()
    except Exception:
        pass
    return fallback


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
                lastmod = f"{CURRENT_YEAR}-{int(mm):02d}-{int(dd):02d}"
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

        filename = f"sitemap-{CURRENT_YEAR}-{month}.xml"
        filepath = os.path.join(OUTPUT_DIR, filename)

        create_sitemap(entries, filepath)
        lastmod = datetime.date.fromtimestamp(os.path.getmtime(filepath)).isoformat()
        sitemap_files.append((filename, lastmod))

    # Static pages sitemap
    static_entries = []
    for path in STATIC_PAGE_PATHS:
        static_entries.append((f"{DOMAIN}{path}", static_page_lastmod(path, today_str)))
    static_filename = "sitemap-static.xml"
    static_path = os.path.join(OUTPUT_DIR, static_filename)
    create_sitemap(static_entries, static_path)
    lastmod = datetime.date.fromtimestamp(os.path.getmtime(static_path)).isoformat()
    sitemap_files.append((static_filename, lastmod))

    # Generate index
    create_sitemap_index(sitemap_files, "sitemap-index.xml")

    print("Done! Generated sitemap-index.xml and monthly sitemaps.")


if __name__ == "__main__":
    main()
