"""
Renders a monthly "Obscure Holiday Guide" hub page (e.g. articles/december/index.html)
from holidays.json data plus hand-written editorial blurbs supplied per month below.

Usage: python3 build_month_guide.py <month-slug>
       python3 build_month_guide.py december
"""
import json
import sys
from pathlib import Path

DOMAIN = "https://www.obscureholidaycalendar.com"
HOLIDAYS_JSON = Path("holidays.json")

# A handful of holidays.json entries have no explicit "slug" field, so their
# auto-generated slug (via slugify(name)) doesn't match the real /holiday/{slug}/
# folder the page actually lives at on disk (a pre-existing data/page mismatch,
# same class of bug as the known apostrophe/& slug issues). Map the data-lookup
# key to the real URL slug here rather than editing holidays.json.
SLUG_LINK_OVERRIDES = {
    "national-hug-high-5-day": "national-hug-and-high-5-day",
}

sys.path.insert(0, ".")
import generate_sitemaps as gs  # reuse slugify() + load_slug_dates() (fixed + resolved floating dates)

HEAD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canonical}">
  <link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png" />
  <link rel="icon" type="image/png" sizes="96x96" href="/favicon-96.png" />
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png" />
  <link rel="icon" href="/favicon.ico" type="image/x-icon" />
  <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <meta name="google-adsense-account" content="ca-pub-7162731177966348">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-JTLDP7FMGV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-JTLDP7FMGV');
  </script>
  <link rel="stylesheet" href="/styles.css">
{schema_scripts}  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7162731177966348" crossorigin="anonymous"></script>
  <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin />
  <link rel="preconnect" href="https://www.google-analytics.com" crossorigin />
  <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin />
  <link rel="preconnect" href="https://tpc.googlesyndication.com" crossorigin />

</head>
"""

HEADER_HTML = """<body class="modern page">
  <header class="site-header">
    <div class="bot-banner">
      <span>Now available for Slack and Discord</span>
      <a class="bot-banner-link" href="/slack-bot/">
        <img class="bot-banner-badge" src="https://platform.slack-edge.com/img/add_to_slack.png" alt="Add to Slack" />
      </a>
      <a class="bot-banner-link" href="/discord-bot/">
        <img class="bot-banner-badge" src="/assets/brands/chat-badge.svg" alt="Add to Discord" />
      </a>
    </div>
    <a class="brand" href="/">
      <img src="/assets/app-icon.png" alt="Obscure Holiday Calendar icon" class="brand-mark" />
      <div class="brand-text">
        <span class="brand-name">Obscure Holiday Calendar</span>
        <span class="brand-tagline">Daily fun, weird, and wonderful observances</span>
      </div>
    </a>
        <nav class="nav-links">
      <a href="/holiday/">Holidays</a>
      <a href="/articles/">Articles</a>
      <a href="/discord-bot/">Discord</a>
      <a href="/slack-bot/">Slack</a>
      <a class="ig-link" href="https://instagram.com/obscureholidaycalendar" target="_blank" rel="noopener">Instagram</a>
      <a class="shop-link" href="https://shop.obscureholidaycalendar.com/?utm_source=site&utm_medium=nav&utm_campaign=shop" target="_blank" rel="noopener">Shop</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
    </nav>
  </header>
"""

FOOTER_HTML = """  <footer class="site-footer">
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/holiday/">Holidays</a>
      <a href="/articles/">Articles</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
      <a href="/discord-bot/">Discord Bot</a>
    </div>
    <p>&copy; 2026 Obscure Holiday Calendar</p>
  </footer>
</body>
</html>
"""


def load_month_facts(month_num):
    """slug -> {name, emoji, description, funFacts, date} for every holiday resolved to this month."""
    data = json.loads(HOLIDAYS_JSON.read_text(encoding="utf-8"))
    holidays = data.get("holidays", {})
    floating = data.get("floatingHolidays", {})
    mapping = gs.load_slug_dates()  # slug -> resolved MM-DD, includes floating

    fixed_by_slug = {}
    for date_key, items in holidays.items():
        for item in items:
            slug = item.get("slug") or gs.slugify(item["name"])
            fixed_by_slug[slug] = item

    month_str = f"{month_num:02d}"
    out = {}
    for slug, date in mapping.items():
        if not date.startswith(month_str + "-"):
            continue
        if slug in fixed_by_slug:
            rec = fixed_by_slug[slug]
            out[slug] = {"date": date, "name": rec["name"], "emoji": rec["emoji"]}
        elif slug in floating:
            rec = floating[slug]
            out[slug] = {"date": date, "name": rec.get("name", slug.replace("-", " ").title()), "emoji": rec.get("emoji", "")}
    return out


def render_month_page(month_config):
    """
    month_config keys:
      month_num, month_name, url_slug, title, description, intro_html,
      why_html, how_to_use_html, faq (list of (q, a)), about_html,
      entries: list of (slug, blurb_html) in display order
    """
    facts = load_month_facts(month_config["month_num"])
    canonical = f"{DOMAIN}/articles/{month_config['url_slug']}/"

    missing = [slug for slug, _ in month_config["entries"] if slug not in facts]
    if missing:
        raise SystemExit(f"ERROR: no holidays.json data found for slugs: {missing}")

    faq_items_schema = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in month_config["faq"]
    ]

    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": month_config["h1"],
        "description": month_config["description"],
        "author": {"@type": "Organization", "name": "Obscure Holiday Calendar"},
        "publisher": {
            "@type": "Organization",
            "name": "Obscure Holiday Calendar",
            "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/app-icon.png"},
        },
        "datePublished": month_config["date_published"],
        "dateModified": month_config["date_modified"],
        "mainEntityOfPage": canonical,
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items_schema,
    }

    schema_scripts = (
        f'  <script type="application/ld+json">\n{json.dumps(article_schema, indent=2)}\n  </script>\n'
        f'  <script type="application/ld+json">\n{json.dumps(faq_schema, indent=2)}\n  </script>\n'
    )

    head = HEAD_TEMPLATE.format(
        title=month_config["title"],
        description=month_config["description"],
        canonical=canonical,
        schema_scripts=schema_scripts,
    )

    # group entries by date, preserving the order given in month_config["entries"]
    day_order = []
    by_day = {}
    for slug, blurb_html in month_config["entries"]:
        date = facts[slug]["date"]
        if date not in by_day:
            by_day[date] = []
            day_order.append(date)
        by_day[date].append((slug, blurb_html))

    day_sections = []
    for date in day_order:
        day_num = int(date.split("-")[1])
        day_sections.append(f'    <h2>{month_config["month_name"]} {day_num}</h2>')
        for slug, blurb_html in by_day[date]:
            f = facts[slug]
            link_slug = SLUG_LINK_OVERRIDES.get(slug, slug)
            day_sections.append(
                f'    <h3>{f["emoji"]} <a href="/holiday/{link_slug}/">{f["name"]}</a></h3>\n'
                f'    <p>{blurb_html}</p>'
            )
    days_html = "\n".join(day_sections)

    faq_html_parts = ["    <h2>Frequently asked questions</h2>"]
    for q, a in month_config["faq"]:
        faq_html_parts.append(f"    <h3>{q}</h3>\n    <p>{a}</p>")
    faq_html = "\n".join(faq_html_parts)

    main_html = f"""  <main class="content-page">
    <h1>{month_config["h1"]}</h1>

{month_config["intro_html"]}

    <h2>Why does {month_config["month_name"]} have so many obscure holidays?</h2>
{month_config["why_html"]}

    <h2>How to use this guide</h2>
{month_config["how_to_use_html"]}

    <hr>

{days_html}

    <hr>

{faq_html}

    <h2>About this guide</h2>
{month_config["about_html"]}
  </main>
"""

    script_tail = """  <script>
    (function() {
      const shopLink = document.querySelector(".shop-link");
      if (shopLink && window.gtag) {
        shopLink.addEventListener("click", () => {
          gtag("event", "shop_click", {
            link_url: shopLink.href,
            link_text: "Shop",
            source_page: "articles-month-guide"
          });
        });
      }
    })();
  </script>
"""

    return head + HEADER_HTML + main_html + FOOTER_HTML.replace("</body>\n</html>\n", script_tail + "</body>\n</html>\n")


def main():
    if len(sys.argv) != 2:
        raise SystemExit(f"Usage: python3 {sys.argv[0]} <month-slug>")
    month_slug = sys.argv[1]

    import month_guides

    config = getattr(month_guides, month_slug.upper(), None)
    if config is None:
        raise SystemExit(f"No config named {month_slug.upper()} found in month_guides.py")

    html = render_month_page(config)
    out_dir = Path("articles") / config["url_slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} ({len(html)} bytes, {len(config['entries'])} holidays)")


if __name__ == "__main__":
    main()
