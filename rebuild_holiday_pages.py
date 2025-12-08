#!/usr/bin/env python3
"""
Rebuild all holiday landing pages with richer on-page content, aligned SEO/ASO
markup, and AdSense-friendly placement. Uses the existing local holidays.json
data (no network calls) and rewrites every /holiday/<slug>/index.html that
already exists on disk.
"""
import html
import json
import random
import re
import hashlib
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parent
HOLIDAYS_DIR = ROOT / "holiday"
HOLIDAYS_JSON = ROOT / "holidays.json"
BADGE_DIR = ROOT / "assets" / "badges"

SITE_BASE = "https://www.obscureholidaycalendar.com"
ADS_CLIENT = "ca-pub-7162731177966348"
ADS_SLOT = "7747026448"

IOS_URL = "https://apps.apple.com/us/app/obscure-holiday-calendar/id6755315850"
ANDROID_URL = "https://play.google.com/store/apps/details?id=com.codeman8806.obscureholidaycalendar"
APP_URL = f"{SITE_BASE}/app/"

POPULAR = [
    ("pi-day", "Pi Day"),
    ("talk-like-a-pirate-day", "Talk Like a Pirate Day"),
    ("national-cat-day", "National Cat Day"),
    ("national-pizza-day", "National Pizza Day"),
    ("star-wars-day", "Star Wars Day (May the 4th)"),
]

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
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def load_holiday_data() -> Dict[str, Dict]:
    if not HOLIDAYS_JSON.exists():
        raise FileNotFoundError(f"Missing {HOLIDAYS_JSON}")

    data = json.loads(HOLIDAYS_JSON.read_text(encoding="utf-8"))
    holidays = data.get("holidays", {})

    by_slug: Dict[str, Dict] = {}
    for date_key, items in holidays.items():
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            if not name:
                continue
            slug = item.get("slug") or slugify(name)
            entry = dict(item)
            entry["slug"] = slug
            entry["date"] = item.get("date", date_key)
            by_slug[slug] = entry
    return by_slug


def pretty_date(date_str: str) -> str:
    try:
        mm, dd = date_str.split("-")
        month = MONTH_NAMES.get(mm, mm)
        return f"{month} {int(dd)}"
    except Exception:
        return date_str


def safe_text(value: str) -> str:
    return html.escape(value.strip()) if value else ""


def shorten_for_meta(text: str, fallback: str, limit: int = 155) -> str:
    base = text.strip() if text else fallback
    if len(base) <= limit:
        return base
    # Try to cut at a sentence boundary
    cut = base[: limit + 1]
    for sep in [". ", "! ", "? "]:
        pos = cut.rfind(sep)
        if pos != -1 and pos > 60:
            return cut[: pos + 1].strip()
    return cut[:limit].rstrip() + "..."


def celebration_ideas(name: str, pretty: str, fun_facts: List[str]) -> List[str]:
    keyword = name.replace("Day", "").strip()
    slugged = slugify(name).replace("-", "")
    ideas = [
        f"Plan something small on {pretty}: a quick nod to {name} with friends, family, or coworkers.",
        f"Share the story of {name} on social and tag it with #{slugged} so others can join in.",
        f"Bring the theme into your day—decorate a workspace, cook or bake something inspired by {keyword}, or play music that matches the mood.",
        f"Add {name} to your Obscure Holiday Calendar app widget so you get a reminder next year.",
    ]
    if fun_facts:
        ideas.insert(0, f"Tell someone this fast fact about {name}: {fun_facts[0]}")
    return ideas


def build_faq(name: str, pretty: str, desc: str) -> List[Tuple[str, str]]:
    return [
        (f"When is {name}?", f"It is observed on {pretty} each year."),
        (f"What is {name}?", desc),
        (f"How do people celebrate {name}?", "Common ideas include sharing the story, planning a small themed activity, and spreading a little joy or reflection around the theme."),
    ]


def json_ld(data: Dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_structured_data(name: str, pretty: str, canonical: str, description: str, faq: List[Tuple[str, str]], breadcrumb: List[Dict]) -> str:
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": name,
        "description": description,
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "author": {"@type": "Organization", "name": "Obscure Holiday Calendar"},
        "publisher": {
            "@type": "Organization",
            "name": "Obscure Holiday Calendar",
            "logo": {"@type": "ImageObject", "url": f"{SITE_BASE}/assets/app-icon.png"},
        },
    }

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faq
        ],
    }

    mobile_app = {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "Obscure Holiday Calendar",
        "operatingSystem": "Android, iOS",
        "applicationCategory": "LifestyleApplication",
        "url": APP_URL,
        "downloadUrl": [ANDROID_URL, IOS_URL],
        "offers": {"@type": "Offer", "price": 0, "priceCurrency": "USD"},
        "publisher": {
            "@type": "Organization",
            "name": "Obscure Holiday Calendar",
            "logo": {"@type": "ImageObject", "url": f"{SITE_BASE}/assets/app-icon.png"},
        },
    }

    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": crumb["name"], "item": crumb["url"]}
            for i, crumb in enumerate(breadcrumb)
        ],
    }

    return "\n".join(
        [
            "<script type=\"application/ld+json\">",
            json_ld(article),
            "</script>",
            "<script type=\"application/ld+json\">",
            json_ld(faq_schema),
            "</script>",
            "<script type=\"application/ld+json\">",
            json_ld(mobile_app),
            "</script>",
            "<script type=\"application/ld+json\">",
            json_ld(breadcrumb_schema),
            "</script>",
        ]
    )


def badge_colors(slug: str) -> Tuple[str, str]:
    digest = hashlib.md5(slug.encode("utf-8")).hexdigest()
    c1 = "#" + digest[:6]
    c2 = "#" + digest[6:12]
    return c1, c2


def build_badge_svg(name: str, slug: str) -> str:
    c1, c2 = badge_colors(slug)
    display = name if len(name) <= 24 else name[:22] + "..."
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="240" height="120" viewBox="0 0 240 120" role="img" aria-label="{html.escape(name)}">
  <defs>
    <linearGradient id="grad-{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect rx="16" ry="16" width="240" height="120" fill="url(#grad-{slug})"/>
  <text x="50%" y="54%" fill="#ffffff" font-family="Inter, Manrope, system-ui, sans-serif" font-size="20" font-weight="700" text-anchor="middle">{html.escape(display)}</text>
  <text x="50%" y="78%" fill="#f1f5f9" font-family="Inter, Manrope, system-ui, sans-serif" font-size="11" font-weight="600" text-anchor="middle">Obscure Holiday Calendar</text>
</svg>
"""


def render_page(
    slug: str,
    record: Dict,
    prev_slug: str,
    next_slug: str,
    random_slug: str,
    title_lookup: Dict[str, str],
    related_slugs: List[str],
    last_updated: str,
) -> str:
    name = record.get("name") or slug.replace("-", " ").title()
    date_raw = record.get("date", "")
    pretty = pretty_date(date_raw)
    emoji = record.get("emoji") or "✨"

    description = record.get("description") or f"Learn about {name}, an unofficial observance celebrated on {pretty}."
    meta_desc = shorten_for_meta(description, f"{name} is celebrated on {pretty}.")

    fun_facts: List[str] = []
    if isinstance(record.get("funFacts"), list):
        fun_facts = [fact for fact in record["funFacts"] if isinstance(fact, str) and fact.strip()]
    if not fun_facts:
        fun_facts = [
            f"{name} is an informal observance that repeats every year on {pretty}.",
            "Many people discover the day through social media or community calendars.",
            "Small gestures—a note, a treat, or a themed activity—keep the spirit of the holiday alive.",
        ]

    celebrations = celebration_ideas(name, pretty, fun_facts)
    faq = build_faq(name, pretty, description)

    canonical = f"{SITE_BASE}/holiday/{slug}/"
    schema = build_structured_data(
        name,
        pretty,
        canonical,
        meta_desc,
        faq,
        breadcrumb=[
            {"name": "Home", "url": f"{SITE_BASE}/"},
            {"name": "Holidays", "url": f"{SITE_BASE}/holiday/"},
            {"name": name, "url": canonical},
        ],
    )

    # Stable random for the "random" link so the site is deterministic on rebuild
    rnd = random.Random(slug)
    random_popular = rnd.choice(POPULAR)

    def holiday_link(slug_value: str, override_label: str = "") -> str:
        label = title_lookup.get(slug_value) or slug_value.replace("-", " ").title()
        if override_label:
            label = override_label
        return f'<a href="/holiday/{slug_value}/">{html.escape(label)}</a>'

    # Related links (limit 3)
    related_links = "".join(f"<li>{holiday_link(s)}</li>" for s in related_slugs[:3])

    badge_path = f"/assets/badges/{slug}.svg"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(name)} — Obscure Holiday Calendar</title>
  <meta name="description" content="{html.escape(meta_desc)}" />
  <meta name="last-modified" content="{last_updated}" />
  <meta name="google-adsense-account" content="ca-pub-7162731177966348" />
  <link rel="canonical" href="{canonical}" />
  <link rel="icon" href="{SITE_BASE}/favicon.ico" type="image/x-icon" />
  <link rel="shortcut icon" href="{SITE_BASE}/favicon.ico" type="image/x-icon" />
  <link rel="icon" type="image/png" href="{SITE_BASE}/assets/app-icon.png" />
  <link rel="apple-touch-icon" href="{SITE_BASE}/apple-touch-icon.png">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-JTLDP7FMGV"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-JTLDP7FMGV');
  </script>
  <meta name="apple-itunes-app" content="app-id=6755315850">
  <meta name="google-play-app" content="app-id=com.codeman8806.obscureholidaycalendar">
  <meta property="og:title" content="{html.escape(name)} — Obscure Holiday Calendar" />
  <meta property="og:description" content="{html.escape(meta_desc)}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE_BASE}/assets/app-icon.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(name)} — Obscure Holiday Calendar" />
  <meta name="twitter:description" content="{html.escape(meta_desc)}" />
  <meta name="twitter:image" content="{SITE_BASE}/assets/app-icon.png" />
  <link rel="stylesheet" href="/styles.css">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS_CLIENT}" crossorigin="anonymous"></script>
  {schema}
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
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
    </nav>
  </header>

  <main class="page-wrap">
    <article class="holiday-card">
      <div class="eyebrow">Annual observance</div>
      <h1 class="holiday-title">{html.escape(name)} <span class="holiday-emoji" aria-hidden="true">{html.escape(emoji)}</span></h1>
      <img src="{badge_path}" alt="{html.escape(name)} badge" class="hero-badge" loading="lazy" decoding="async" />
      <div class="meta-line">
        <span class="pill">{html.escape(pretty)}</span>
        <span class="pill pill-secondary">Cultural / community observance</span>
        <span class="pill pill-secondary">Updated {last_updated}</span>
      </div>

      <p class="lead">
        This holiday is featured in the Obscure Holiday Calendar app with emoji-style visuals, reminders, and daily fun facts.
      </p>

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

      <section class="section">
        <h2>Overview</h2>
        <p>{safe_text(description)}</p>
        <p>Observed each year on {html.escape(pretty)}, {html.escape(name)} invites people to pause, share the story, and bring a little themed joy to their day.</p>
      </section>

      <section class="section">
        <h2>Origin and story</h2>
        <p>{safe_text(fun_facts[0])}</p>
        {"<p>" + safe_text(fun_facts[1]) + "</p>" if len(fun_facts) > 1 else ""}
      </section>

      <div class="ad-slot">
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="{ADS_CLIENT}"
             data-ad-slot="{ADS_SLOT}"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <section class="section">
        <h2>Quick facts</h2>
        <ul class="fact-list">
          <li><span>Date</span><span>{html.escape(pretty)}</span></li>
          <li><span>Type</span><span>Unofficial / cultural observance</span></li>
          <li><span>Great for</span><span>Friends, families, classrooms, and teams</span></li>
        </ul>
      </section>

      <section class="section">
        <h2>Ways to celebrate</h2>
        <ul class="list">
          {''.join(f'<li>{safe_text(item)}</li>' for item in celebrations)}
        </ul>
      </section>

      <section class="section">
        <h2>Fun facts</h2>
        <ul class="list">
          {''.join(f'<li>{safe_text(item)}</li>' for item in fun_facts)}
        </ul>
      </section>

      <section class="section">
        <h2>Sources and attribution</h2>
        <p>Primary note: {safe_text(fun_facts[0])}</p>
      </section>

      <section class="section">
        <h2>Related holidays</h2>
        <ul class="list">
          {related_links}
        </ul>
      </section>

      <section class="section">
        <h2>FAQ</h2>
        <dl class="faq">
          {''.join(f'<div class="faq-item"><dt>{safe_text(q)}</dt><dd>{safe_text(a)}</dd></div>' for q, a in faq)}
        </dl>
      </section>

      <section class="section app-cta">
        <h2>Get the app</h2>
        <p>Thousands of obscure holidays, daily widgets, reminders, and fun facts—free on iOS and Android.</p>
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
      </section>

      <section class="section more-holidays">
        <h2>Explore more holidays</h2>
        <ul>
          <li>Yesterday: {holiday_link(prev_slug)}</li>
          <li>Tomorrow: {holiday_link(next_slug)}</li>
          <li>Random pick: {holiday_link(random_slug)}</li>
          <li>Popular: {holiday_link(random_popular[0], random_popular[1])}</li>
        </ul>
      </section>
    </article>
  </main>

  <footer class="site-footer">
    <div class="footer-links">
      <a href="/">Home</a>
      <a href="/holiday/">Holidays</a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
    </div>
    <p>&copy; {datetime.now().year} Obscure Holiday Calendar</p>
  </footer>
</body>
</html>
"""


def main():
    data = load_holiday_data()
    last_updated = date.today().isoformat()

    existing_slugs = [p.name for p in HOLIDAYS_DIR.iterdir() if p.is_dir()]
    title_lookup = {slug: rec.get("name", slug.replace("-", " ").title()) for slug, rec in data.items()}

    dated_slugs = []
    for slug in existing_slugs:
        rec = data.get(slug, {})
        date_raw = rec.get("date", "")
        try:
            mm, dd = date_raw.split("-")
            dated_slugs.append((int(mm), int(dd), slug))
        except Exception:
            dated_slugs.append((99, 99, slug))

    slugs_sorted = [slug for _, _, slug in sorted(dated_slugs)]

    # Build month -> slugs map for related links
    slugs_by_month: Dict[str, List[str]] = {}
    for slug in slugs_sorted:
        rec = data.get(slug, {})
        date_raw = rec.get("date", "")
        mm = date_raw.split("-")[0] if "-" in date_raw else "00"
        slugs_by_month.setdefault(mm, []).append(slug)

    BADGE_DIR.mkdir(parents=True, exist_ok=True)

    for idx, slug in enumerate(slugs_sorted):
        record = data.get(slug, {})
        prev_slug = slugs_sorted[idx - 1] if idx > 0 else slugs_sorted[-1]
        next_slug = slugs_sorted[idx + 1] if idx < len(slugs_sorted) - 1 else slugs_sorted[0]

        options = [s for s in slugs_sorted if s != slug]
        random_slug = random.choice(options) if options else slug

        # Related: prefer same-month items
        date_raw = record.get("date", "")
        mm = date_raw.split("-")[0] if "-" in date_raw else "00"
        related_pool = [s for s in slugs_by_month.get(mm, []) if s != slug]
        rng = random.Random(f"related-{slug}")
        rng.shuffle(related_pool)
        related_slugs = related_pool[:3]
        if len(related_slugs) < 3:
            extra = [s for s in slugs_sorted if s not in related_slugs and s != slug]
            rng.shuffle(extra)
            related_slugs.extend(extra[: 3 - len(related_slugs)])

        html_output = render_page(slug, record, prev_slug, next_slug, random_slug, title_lookup, related_slugs, last_updated)
        out_path = HOLIDAYS_DIR / slug / "index.html"
        out_path.write_text(html_output, encoding="utf-8")

        # Badge
        badge_svg = build_badge_svg(record.get("name", slug), slug)
        badge_path = BADGE_DIR / f"{slug}.svg"
        badge_path.write_text(badge_svg, encoding="utf-8")

        print(f"✅ wrote {out_path}")

    print(f"\nDone. Rebuilt {len(slugs_sorted)} holiday pages.")


if __name__ == "__main__":
    main()
