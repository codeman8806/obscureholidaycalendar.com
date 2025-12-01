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

ADSENSE_LOADER = f"""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}"
     crossorigin="anonymous"></script>
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
""".rstrip()  # we'll append SEO content after this and then close with END-SEO-BLOCK

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

<p><strong>Does it support widgets?</strong><br>Yes — widgets show today’s holiday at a glance on iOS & Android.</p>
""".strip()


# -----------------------------
# HELPERS
# -----------------------------

def slugify(name: str) -> str:
    """Convert holiday name to URL slug, roughly matching your folder names."""
    s = name.lower()
    # replace apostrophes with nothing
    s = s.replace("’", "").replace("'", "")
    # replace non-alphanumeric with hyphen
    s = re.sub(r"[^a-z0-9]+", "-", s)
    # collapse multiple hyphens
    s = re.sub(r"-+", "-", s)
    # trim hyphens
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
                print(f"⚠️ Duplicate slug '{slug}' found for '{name}' and '{slug_map[slug]['name']}'")
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


def ensure_adsense_loader_in_head(html: str) -> str:
    """Insert the AdSense loader script into <head> if not already present."""
    if ADSENSE_CLIENT in html:
        # already present
        return html

    head_close_idx = html.lower().find("</head>")
    if head_close_idx == -1:
        return html  # malformed, skip

    return html[:head_close_idx] + "\n" + ADSENSE_LOADER + "\n" + html[head_close_idx:]


def build_seo_block(hdata: dict) -> str:
    name = hdata["name"]
    pretty = hdata["pretty_date"]
    description = hdata["description"] or f"{name} is one of the many fun, weird, and obscure holidays featured in the Obscure Holiday Calendar app."
    funfacts = hdata["funFacts"] or []
    fun_fact = funfacts[0] if funfacts else f"{name} is part of the growing trend of fun social holidays people share online."

    history_section = f"""
<h2>History of {name}</h2>
<p>{name} doesn’t have a long formal history like major public holidays, but it has grown in popularity thanks to social media, blogs, and people who love celebrating the little things in life. As more creators, families, and teachers look for reasons to mark each day with something fun, {name} has become one of those niche observances that quietly spreads through word of mouth and online posts.</p>
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

<p><strong>Is {name} an official national holiday?</strong><br>No — like most obscure holidays, it’s an informal observance that people celebrate for fun.</p>

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
    # We'll look for the first occurrence of <div class="date">
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
    # 1. Load JSON and build slug map
    slug_map = load_holiday_data(JSON_FILE)

    # 2. Walk holiday subfolders and update index.html
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
        slug = dirpath.name  # folder name as slug, e.g., "falling-needles-family-fest-day"
        html_path = dirpath / "index.html"

        if slug not in slug_map:
            print(f"⚠️ No JSON match for slug '{slug}' ({html_path}), skipping.")
            skipped_files += 1
            continue

        print(f"✅ Updating {html_path} for holiday '{slug_map[slug]['name']}'")

        html = html_path.read_text(encoding="utf-8")

        # Ensure AdSense loader in <head>
        html = ensure_adsense_loader_in_head(html)

        # Inject SEO block after date
        html = inject_seo_block(html, slug_map[slug])

        html_path.write_text(html, encoding="utf-8")
        updated_files += 1

    print(f"\nDone. Updated {updated_files} files, skipped {skipped_files} (no matching slug or missing date div).")


if __name__ == "__main__":
    main()

