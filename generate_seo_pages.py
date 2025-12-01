import json
import os
import re
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------

JSON_FILE = "holidays.json"
ADSENSE_CLIENT = "ca-pub-7162731177966348"
AD_SLOT = "7747026448"
DOMAIN = "https://www.obscureholidaycalendar.com"

IOS_URL = "https://apps.apple.com/us/app/obscure-holiday-calendar/id6755315850"
ANDROID_URL = "https://play.google.com/store/apps/details?id=com.codeman8806.obscureholidaycalendar"

BRAND_ICON_HTML = """
<img src="/assets/app-icon.png" alt="Obscure Holiday Calendar App Icon" class="brand-icon">
"""

BRAND_ICON_CSS = """
<!-- BRAND-ICON-CSS-START -->
<style>
.brand-icon {
    display: block;
    margin: 20px auto 10px auto;
    width: 140px;
}
.store-buttons-top {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin: 10px 0 20px 0;
}
.store-badge {
    height: 50px;
}
</style>
<!-- BRAND-ICON-CSS-END -->
"""

ADSENSE_LOADER = f"""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}"
     crossorigin="anonymous"></script>
""".strip()

STORE_BUTTONS_TOP = f"""
<div class="store-buttons-top">
  <a href="{IOS_URL}" target="_blank" rel="noopener">
    <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg"
         alt="Download on the App Store" class="store-badge" />
  </a>
  <a href="{ANDROID_URL}" target="_blank" rel="noopener">
    <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png"
         alt="Get it on Google Play" class="store-badge" />
  </a>
</div>
""".strip()

AD_BANNER = f"""
<!-- START-SEO-BLOCK -->
<!-- AdSense banner -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="{ADSENSE_CLIENT}"
     data-ad-slot="{AD_SLOT}"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({{}});
</script>
"""

WHY_OBSCURE = """
<h2>Why Obscure Holiday Calendar?</h2>
<p>Obscure Holiday Calendar celebrates the fun, weird, and wonderfully obscure national days that make every single day worth sharing...</p>
""".strip()

APP_FAQ = """
<h2>Obscure Holiday Calendar App FAQ</h2>
<p><strong>Is Obscure Holiday Calendar free?</strong><br>Yes — the core daily holiday experience is completely free.</p>
""".strip()

# -----------------------------
# HELPERS
# -----------------------------

def slugify(name: str) -> str:
    s = name.lower()
    s = s.replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


def pretty_date(mm_dd: str) -> str:
    mm, dd = mm_dd.split("-")
    month = MONTH_NAMES.get(mm, mm)
    return f"{month} {int(dd)}"


def load_holiday_data(json_file: str):
    with open(json_file, "r") as f:
        data = json.load(f)

    slug_map = {}
    holidays = data.get("holidays", {})

    for date_key, holiday_list in holidays.items():
        for entry in holiday_list:
            name = entry.get("name")
            if not name:
                continue
            slug = slugify(name)
            slug_map[slug] = {
                "name": name,
                "description": entry.get("description", ""),
                "emoji": entry.get("emoji", ""),
                "funFacts": entry.get("funFacts", []),
                "pretty_date": pretty_date(date_key),
            }

    print(f"Loaded {len(slug_map)} holidays.")
    return slug_map


def build_schema_block(hdata, slug):
    import json as _json

    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": hdata["name"],
        "description": hdata["description"],
        "mainEntityOfPage": f"{DOMAIN}/holiday/{slug}/",
        "author": {"@type": "Organization", "name": "Obscure Holiday Calendar"},
        "publisher": {
            "@type": "Organization",
            "name": "Obscure Holiday Calendar",
            "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/app-icon.png"}
        }
    }

    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"When is {hdata['name']}?",
                "acceptedAnswer": {"@type": "Answer", "text": f"It is observed on {hdata['pretty_date']}."}
            },
            {
                "@type": "Question",
                "name": f"Is {hdata['name']} an official holiday?",
                "acceptedAnswer": {"@type": "Answer", "text": "No — it is an unofficial observance."}
            }
        ]
    }

    return f"""
<!-- ARTICLE-SCHEMA-START -->
<script type="application/ld+json">
{_json.dumps(article, indent=2)}
</script>
<!-- ARTICLE-SCHEMA-END -->

<!-- FAQ-SCHEMA-START -->
<script type="application/ld+json">
{_json.dumps(faq, indent=2)}
</script>
<!-- FAQ-SCHEMA-END -->
""".strip()


def ensure_head_assets(html, hdata, slug):
    head_close = html.lower().find("</head>")
    if head_close == -1:
        return html

    head = html[:head_close]
    rest = html[head_close:]

    if ADSENSE_CLIENT not in head:
        head += "\n" + ADSENSE_LOADER + "\n"

    if "BRAND-ICON-CSS-START" not in head:
        head += "\n" + BRAND_ICON_CSS + "\n"

    head = re.sub(r"<!-- ARTICLE-SCHEMA-START -->.*?<!-- FAQ-SCHEMA-END -->",
                  "", head, flags=re.DOTALL)

    head += "\n" + build_schema_block(hdata, slug) + "\n"

    return head + rest


def inject_brand_icon_and_store_buttons(html):
    # Insert brand icon before <h1> if missing
    if "brand-icon" not in html:
        h1 = re.search(r"<h1[^>]*>", html)
        if h1:
            html = html[:h1.start()] + BRAND_ICON_HTML + "\n" + html[h1.start():]

    # Insert store buttons after <h1> if missing
    if "store-buttons-top" not in html:
        h1_block = re.search(r"<h1[^>]*>.*?</h1>", html, flags=re.DOTALL)
        if h1_block:
            html = html[:h1_block.end()] + "\n\n" + STORE_BUTTONS_TOP + "\n\n" + html[h1_block.end():]

    # Remove old store-buttons div
    html = re.sub(r'<div\s+class="store-buttons".*?</div>', "", html, flags=re.DOTALL)

    return html


def build_seo_block(hdata):
    name = hdata["name"]
    desc = hdata["description"]
    pretty = hdata["pretty_date"]
    fun = hdata["funFacts"][0] if hdata["funFacts"] else f"A fun tradition tied to {name}."

    return f"""
{AD_BANNER}

<h2>What is {name}?</h2>
<p>{desc}</p>

<h2>History of {name}</h2>
<p>{name} has grown in popularity thanks to social sharing and themed online observances...</p>

<h2>How to Celebrate {name}</h2>
<ul>
    <li>Share a themed post</li>
    <li>Do a related activity</li>
    <li>Teach kids or coworkers about the holiday</li>
</ul>

<h2>Fun Fact</h2>
<p>{fun}</p>

<h2>{name} FAQ</h2>
<p><strong>When is it?</strong> {pretty}</p>

{WHY_OBSCURE}

{APP_FAQ}

<!-- END-SEO-BLOCK -->
""".strip()


def inject_seo_block(html, hdata):
    html = re.sub(r"<!-- START-SEO-BLOCK -->.*?<!-- END-SEO-BLOCK -->",
                  "", html, flags=re.DOTALL)

    date_block = re.search(r'<div\s+class="date"[^>]*>.*?</div>',
                           html, flags=re.IGNORECASE | re.DOTALL)
    if not date_block:
        return html

    pos = date_block.end()
    block = build_seo_block(hdata)

    return html[:pos] + "\n\n" + block + "\n\n" + html[pos:]


# -----------------------------
# MAIN
# -----------------------------

def main():
    slug_map = load_holiday_data(JSON_FILE)

    root = Path("holiday")
    updated = 0
    skipped = 0

    for dirpath, dirnames, filenames in os.walk(root):
        if "index.html" not in filenames:
            continue

        path = Path(dirpath) / "index.html"
        slug = Path(dirpath).name

        if slug not in slug_map:
            print(f"Skipping {slug} — no JSON match")
            skipped += 1
            continue

        hdata = slug_map[slug]
        html = path.read_text()

        html = inject_brand_icon_and_store_buttons(html)
        html = ensure_head_assets(html, hdata, slug)
        html = inject_seo_block(html, hdata)

        path.write_text(html)
        updated += 1

        print(f"Updated: {slug}")

    print(f"\nDone. Updated {updated}, skipped {skipped}.")


if __name__ == "__main__":
    main()

