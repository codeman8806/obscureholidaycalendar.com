#!/usr/bin/env python3
"""
Rebuild the holiday library page (/holiday/index.html) with month-by-month
links to each holiday instead of pointing users to raw sitemaps.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOLIDAYS_JSON = ROOT / "holidays.json"
OUTPUT = ROOT / "holiday" / "index.html"

MONTH_NAMES = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
}


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_by_month():
    data = json.loads(HOLIDAYS_JSON.read_text(encoding="utf-8"))
    holidays = data.get("holidays", {})
    by_month = {m: [] for m in MONTH_NAMES}
    for mmdd, items in holidays.items():
        if "-" not in mmdd:
            continue
        mm, dd = mmdd.split("-")
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            if not name:
                continue
            slug = item.get("slug") or slugify(name)
            by_month.setdefault(mm, []).append(
                (int(dd), name, slug)
            )
    # sort each month by day then name
    for mm in by_month:
        by_month[mm].sort(key=lambda t: (t[0], t[1].lower()))
    return by_month


def render_month_section(mm: str, entries):
    month_name = MONTH_NAMES.get(mm, mm)
    if not entries:
        return ""
    items = "\n".join(
        f'        <li><span class="day">{day}</span> <a href="/holiday/{slug}/">{name}</a></li>'
        for day, name, slug in entries
    )
    return f"""    <section class="month-section">
      <h2>{month_name}</h2>
      <ul class="month-list">
{items}
      </ul>
    </section>
"""


def main():
    by_month = load_by_month()
    last_updated = date.today().isoformat()

    month_html = "".join(render_month_section(mm, entries) for mm, entries in sorted(by_month.items()))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Holiday Library — Obscure Holiday Calendar</title>
  <meta name="description" content="Browse every fun and obscure holiday by month. Quick links to each day’s page, plus app downloads for reminders and widgets.">
  <meta name="google-adsense-account" content="ca-pub-7162731177966348">
  <link rel="canonical" href="https://www.obscureholidaycalendar.com/holiday/">
  <link rel="icon" href="/favicon.ico" type="image/x-icon">
  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
  <link rel="icon" type="image/png" href="/assets/app-icon.png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="/styles.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-JTLDP7FMGV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-JTLDP7FMGV');
  </script>
</head>
<body class="page">
  <header class="site-header">
    <a class="brand" href="/">
      <img src="/assets/app-icon.png" alt="Obscure Holiday Calendar icon" class="brand-mark" />
      <div class="brand-text">
        <span class="brand-name">Obscure Holiday Calendar</span>
        <span class="brand-tagline">Daily fun, weird, and wonderful observances</span>
      </div>
    </a>
    <nav class="nav-links">
      <a href="/holiday/">Holidays</a>
      <a class="shop-link" href="https://shop.obscureholidaycalendar.com/?utm_source=site&utm_medium=nav&utm_campaign=shop" target="_blank" rel="noopener">Shop</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
    </nav>
  </header>

  <main class="content-page">
    <h1>Holiday library</h1>
    <p>Browse every holiday in the Obscure Holiday Calendar by month. Tap a day to jump straight to its page and grab the app for reminders and widgets.</p>
    <p class="muted">Last updated: {last_updated}</p>
{month_html}
  </main>

  <footer class="site-footer">
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/holiday/">Holidays</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
    </div>
    <p>&copy; {date.today().year} Obscure Holiday Calendar</p>
  </footer>
  <script>
    (function() {{
      const shopLink = document.querySelector(".shop-link");
      if (shopLink && window.gtag) {{
        shopLink.addEventListener("click", () => {{
          gtag("event", "shop_click", {{
            link_url: shopLink.href,
            link_text: "Shop",
            source_page: "holiday-library"
          }});
        }});
      }}
    }})();
  </script>
</body>
</html>
"""
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"✅ wrote {OUTPUT}")


if __name__ == "__main__":
    main()
