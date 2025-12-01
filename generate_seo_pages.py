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

STORE_BUTTONS_CSS = """
<!-- STORE-BUTTONS-CSS-START -->
<style>
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
<!-- STORE-BUTTONS-CSS-END -->
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
""".rstrip()

WHY_OBSCURE = """
<h2>Why Obscure Holiday Calendar?</h2>
<p>Obscure Holiday Calendar celebrates the fun, weird, and wonderfully obscure national days that make every single day worth sharing. Instead of only caring about the major holidays you already know, this app highlights the quirky celebrations you might otherwise miss. From food holidays like Bubble Tea Day and National Cheeseburger Day, to cultural favorites like Talk Like A Pirate Day and World Emoji Day, the app gives you something new to enjoy daily.</p>

<h3>Perfect for:</h3>
<ul>
    <li>Creators looking for easy daily content ideas</li>
    <li>Teachers & classrooms celebrating themed days</li>
    <li>Parents doing fun “daily themes” with kids</li>
    <li>Food businesses wanting to post on food holidays</li>
    <li>Social media managers needing consistent content</li>
</ul>

<p>Whether you call them obscure holidays, weird holidays, national days, special observances, or just fun excuses to celebrate, Obscure Holiday Calendar makes it simple and enjoyable to see what holiday is today.</p>
""".strip()

APP_FAQ = """
<h2>Obscure Holiday Calendar App FAQ</h2>
<p><strong>Is Obscure Holiday Calendar free?</strong><br>Yes — the core daily holiday experience is completely free on both iOS and Android.</p>

<p><strong>Does it include real national days?</strong><br>Yes: food holidays, internet holidays, culture days, pet days, and obscure “just for fun” days.</p>

<p><strong>Can I share a holiday?</strong><br>Yes — every holiday includes a deep link you can share with friends or followers.</p>

<p><strong>Does it support widgets?</strong><br>Yes — widgets show today's holiday at a glance on iOS & Android.</p>
""".strip()


# -----------------------------
# HELPERS
# -----------------------------

def slugify(name: str) -> str:
    s = name.lower()
    s = s.replace("’", "").replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s


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


def pretty_date(mm_dd: str) -> str:
    mm, dd = mm_dd.split("-")
    month = MONTH_NAMES.get(mm, mm)
    day = int(dd)
    return f"{month} {day}"


def load_holiday_data(json_file: str):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    holidays = data.get("holidays", {})
    slug_map = {}

    for date_key, holiday_list in holidays.items():
        if not isinstance(holiday_list, list):
            continue
        for entry in holiday_list:
            name = entry.get("name")
            if not name:
                continue
            slug = slugify(name)
            if slug in slug_map:
                print(f"⚠️ Duplicate slug '{slug}' for '{name}' and '{slug_map[slug]['name']}'")
            slug_map[slug] = {
                "name": name,
                "emoji": entry.get("emoji", ""),
                "description": entry.get("description", "").strip(),
                "funFacts": entry.get("funFacts", []),
                "date_key": date_key,
                "pretty_date": pretty_date(date_key),
            }

    print(f"Loaded {len(slug_map)} holiday entries from JSON.")
    return slug_map


def ensure_adsense_loader_and_css_and_schema(html: str, hdata: dict, slug: str) -> str:
    """
    Ensure:
    - AdSense loader in <head>
    - store-buttons CSS in <head>
    - Article + FAQ schema in <head>
    """

    # Ensure <head> exists
    head_close_idx = html.lower().find("</head>")
    if head_close_idx == -1:
        return html

    head_section = html[:head_close_idx]
    rest = html[head_close_idx:]

    # AdSense loader
    if ADSENSE_CLIENT not in head_section:
        head_section += "\n" + ADSENSE_LOADER + "\n"

    # Store buttons CSS (idempotent via markers)
    if "STORE-BUTTONS-CSS-START" not in head_section:
        head_section += "\n" + STORE_BUTTONS_CSS + "\n"

    # Article + FAQ schema (idempotent via markers)
    article_start = "<!-- ARTICLE-SCHEMA-START -->"
    article_end = "<!-- ARTICLE-SCHEMA-END -->"
    faq_start = "<!-- FAQ-SCHEMA-START -->"
    faq_end = "<!-- FAQ-SCHEMA-END -->"

    # Remove old blocks if present
    def strip_block(text, start_marker, end_marker):
        s = text.find(start_marker)
        e = text.find(end_marker)
        if s != -1 and e != -1 and e > s:
            e += len(end_marker)
            return text[:s] + text[e:]
        return text

    head_section = strip_block(head_section, article_start, article_end)
    head_section = strip_block(head_section, faq_start, faq_end)

    # Build new schema
    schema_block = build_schema_block(hdata, slug)

    head_section += "\n" + schema_block + "\n"

    return head_section + rest


def build_schema_block(hdata: dict, slug: str) -> str:
    import json as _json

    name = hdata["name"]
    description = hdata["description"] or f"{name} is one of many fun, weird, and obscure holidays featured in the Obscure Holiday Calendar app."
    pretty = hdata["pretty_date"]
    url = f"{DOMAIN}/holiday/{slug}/"

    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": name,
        "description": description,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        },
        "author": {
            "@type": "Organization",
            "name": "Obscure Holiday Calendar"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Obscure Holiday Calendar",
            "logo": {
                "@type": "ImageObject",
                "url": f"{DOMAIN}/assets/og-image.png"
            }
        }
    }

    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"When is {name}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"{name} is observed each year on {pretty}."
                }
            },
            {
                "@type": "Question",
                "name": f"Is {name} an official national holiday?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No — like most obscure holidays, it is an informal observance people celebrate for fun."
                }
            },
            {
                "@type": "Question",
                "name": f"How do people celebrate {name}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"People typically mark {name} by sharing themed posts, doing a small related activity, or using it as a lighthearted reason to connect."
                }
            }
        ]
    }

    article_json = _json.dumps(article, ensure_ascii=False, indent=2)
    faq_json = _json.dumps(faq, ensure_ascii=False, indent=2)

    return f"""{'<!-- ARTICLE-SCHEMA-START -->'}
<script type="application/ld+json">
{article_json}
</script>
{'<!-- ARTICLE-SCHEMA-END -->'}

{'<!-- FAQ-SCHEMA-START -->'}
<script type="application/ld+json">
{faq_json}
</script>
{'<!-- FAQ-SCHEMA-END -->'}"""


def remove_top_image(html: str) -> str:
    """
    Remove the first <img ...> after the start of the main container.
    Assumes there's only one hero image we don't want anymore.
    """
    # Find first <img ...> and remove it
    new_html, count = re.subn(r"<img[^>]*>", "", html, count=1, flags=re.IGNORECASE)
    return new_html if count > 0 else html


def ensure_store_buttons_top(html: str) -> str:
    """
    Insert official store buttons right after <h1>...</h1>, and remove old .store-buttons block.
    """
    if "store-buttons-top" in html:
        # already done
        return html

    # Insert after first <h1>...</h1>
    h1_match = re.search(r"<h1[^>]*>.*?</h1>", html, flags=re.IGNORECASE | re.DOTALL)
    if not h1_match:
        return html

    insert_pos = h1_match.end()
    html = html[:insert_pos] + "\n\n" + STORE_BUTTONS_TOP + "\n\n" + html[insert_pos:]

    # Remove old store-buttons block(s)
    html = re.sub(r'<div\s+class="store-buttons".*?</div>', "", html, flags=re.IGNORECASE | re.DOTALL)

    return html


def build_seo_block(hdata: dict) -> str:
    name = hdata["name"]
    pretty = hdata["pretty_date"]
    description = hdata["description"] or f"{name} is one of the many fun, weird, and obscure holidays featured in the Obscure Holiday Calendar app."
    funfacts = hdata["funFacts"] or []
    fun_fact = funfacts[0] if funfacts else f"{name} is part of the growing trend of fun social holidays that people share online."

    history_section = f"""
<h2>History of {name}</h2>
<p>{name} doesn&apos;t have a long formal history like major public holidays, but it has grown in popularity thanks to social media, blogs, and people who love celebrating the little things in life. As more creators, families, and teachers look for reasons to mark each day with something fun, {name} has become one of those niche observances that quietly spreads through word of mouth and online posts.</p>
<p>Like many modern “national days,” {name} is part of a larger movement of unofficial holidays that help people connect, share laughs, and create small traditions around specific dates on the calendar.</p>
""".strip()

    celebrate_section = f"""
<h2>How to Celebrate {name}</h2>
<ul>
    <li>Share a post about {name} on social media.</li>
    <li>Do a small themed activity related to the holiday.</li>
    <li>Talk about the holiday with friends, family, or coworkers.</li>
    <li>Use it as a fun icebreaker in class or at work.</li>
    <li>Look up other obscure holidays happening this week.</li>
</ul>
""".strip()

    faq_section = f"""
<h2>{name} FAQ</h2>
<p><strong>When is {name}?</strong><br>{name} is observed each year on {pretty}.</p>

<p><strong>Is {name} an official national holiday?</strong><br>No — like most obscure holidays, it&apos;s an informal observance that people celebrate for fun.</p>

<p><strong>How do people usually celebrate?</strong><br>Most people mark {name} by sharing themed posts, doing a small related activity, or simply using it as a lighthearted excuse to smile and connect.</p>

<p><strong>Where did {name} come from?</strong><br>The exact origin is a bit unclear, as is the case with many internet-era holidays, but it has spread through online calendars, blogs, and social media.</p>
""".strip()

    fun_fact_section = f"""
<h2>Fun Fact</h2>
<p>{fun_fact}</p>
<p><em>Want to see all the fun facts for this holiday (and today’s other obscure holidays)? Open the Obscure Holiday Calendar app.</em></p>
""".strip()

    seo_block = f"""
{AD_BANNER}

<h2>What is {name}?</h2>
<p>{description}</p>

{history_section}

{celebrate_section}

{fun_fact_section}

{faq_section}

{WHY_OBSCURE}

{APP_FAQ}

<!-- END-SEO-BLOCK -->
""".strip()

    return "\n\n" + seo_block + "\n\n"


def inject_seo_block(html: str, hdata: dict) -> str:
    """
    Insert (or replace) the SEO block immediately after the <div class="date">...</div>.
    """
    # Remove old SEO block if present
    start_idx = html.find("<!-- START-SEO-BLOCK -->")
    end_idx = html.find("<!-- END-SEO-BLOCK -->")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        end_idx += len("<!-- END-SEO-BLOCK -->")
        html = html[:start_idx] + html[end_idx:]

    # Find the date div
    date_match = re.search(r'<div\s+class="date"[^>]*>.*?</div>', html, flags=re.IGNORECASE | re.DOTALL)
    if not date_match:
        print("  ⚠️ Could not find <div class=\"date\"> block; skipping SEO injection for this file.")
        return html

    insert_pos = date_match.end()  # insert right after </div>
    seo_block = build_seo_block(hdata)
    new_html = html[:insert_pos] + seo_block + html[insert_pos:]
    return new_html


# -----------------------------
# MAIN
# -----------------------------

def main():
    slug_map = load_holiday_data(JSON_FILE)

    root = Path("holiday")
    if not root.exists():
        print("❌ 'holiday' directory not found. Run this from the repo root.")
        return

    updated_files = 0
    skipped_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        if "index.html" not in filenames:
            continue

        dirpath = Path(dirpath)
        slug = dirpath.name
        html_path = dirpath / "index.html"

        if slug not in slug_map:
            print(f"⚠️ No JSON match for slug '{slug}' ({html_path}), skipping.")
            skipped_files += 1
            continue

        hdata = slug_map[slug]
        print(f"✅ Updating {html_path} for holiday '{hdata['name']}'")

        html = html_path.read_text(encoding="utf-8")

        # Remove top image
        html = remove_top_image(html)

        # Store buttons at top (official badges)
        html = ensure_store_buttons_top(html)

        # Ensure head: AdSense loader, CSS, Article + FAQ schema
        html = ensure_adsense_loader_and_css_and_schema(html, hdata, slug)

        # Inject SEO block
        html = inject_seo_block(html, hdata)

        html_path.write_text(html, encoding="utf-8")
        updated_files += 1

    print(f"\nDone. Updated {updated_files} files, skipped {skipped_files} (no matching slug or missing date div).")


if __name__ == "__main__":
    main()

