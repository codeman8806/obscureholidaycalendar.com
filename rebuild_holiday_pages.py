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


# Category heuristics to tailor type, great-for, and celebrations
CATEGORY_RULES = [
    ("Food / Dessert", ["chocolate", "cookie", "cake", "pie", "pizza", "ice cream", "bake", "candy", "dessert", "sandwich", "taco", "burger", "bread", "soup", "coffee", "tea", "wine", "beer", "cocktail", "cheese"]),
    ("Pets / Animals", ["cat", "dog", "pet", "kitten", "puppy"]),
    ("Learning / Reading", ["book", "read", "poetry", "dictionary", "grammar", "library", "literacy"]),
    ("Games & Fun", ["game", "chess", "puzzle", "crossword", "scrabble", "trivia"]),
    ("Nature / Outdoors", ["tree", "garden", "flower", "earth", "nature", "hike", "outdoors"]),
    ("Health / Wellness", ["fitness", "health", "run", "walk", "yoga", "meditation"]),
    ("Kindness / Community", ["kindness", "friend", "hug", "thank", "compliment", "help", "appreciation"]),
    ("Geek / Tech", ["tech", "computer", "internet", "coding", "science", "math", "pi", "engineer", "robot"]),
]


def classify_holiday(name: str, description: str) -> dict:
    text = f"{name} {description}".lower()
    for label, keywords in CATEGORY_RULES:
        if any(k in text for k in keywords):
            return {
                "type_label": label,
                "great_for": {
                    "Food / Dessert": ["Foodies", "Chocolate lovers", "Home bakers"],
                    "Pets / Animals": ["Pet parents", "Shelters", "Veterinarians"],
                    "Learning / Reading": ["Book clubs", "Teachers", "Students"],
                    "Games & Fun": ["Game nights", "Families", "Puzzle fans"],
                    "Nature / Outdoors": ["Gardeners", "Hikers", "Eco clubs"],
                    "Health / Wellness": ["Wellness groups", "Gyms", "Health classes"],
                    "Kindness / Community": ["Community groups", "Friends", "Coworkers"],
                    "Geek / Tech": ["Tech teams", "STEM clubs", "Developers"],
                }.get(label, ["Friends", "Families", "Teams"]),
            }
    return {"type_label": "Cultural / community observance", "great_for": ["Friends", "Families", "Classrooms", "Teams"]}


def category_celebrations(label: str, name: str, pretty: str) -> List[str]:
    if "Food" in label:
        return [
            f"Try a playful twist: cover non-traditional foods in chocolate or sauces inspired by {name}.",
            "Host a tasting plate with sweet and savory pairings.",
            "Share a recipe photo, tag friends, and swap your favorite topping ideas.",
        ]
    if "Pets" in label:
        return [
            "Share photos of your pets enjoying a themed treat or outfit.",
            "Donate supplies to a local shelter or foster program.",
            "Schedule a short playdate or walk with a rescue in mind.",
        ]
    if "Learning" in label:
        return [
            "Set aside 15 minutes to read or learn something tied to the day’s theme.",
            "Share a favorite quote or fact with a friend or class.",
            "Start a tiny challenge: one page, one fact, one takeaway.",
        ]
    if "Games" in label:
        return [
            "Host a quick game round—board game, puzzle, or trivia tied to the theme.",
            "Share a digital puzzle link with friends and compare times.",
            "Teach someone a new game mechanic or strategy today.",
        ]
    if "Nature" in label:
        return [
            "Step outside for a themed photo or short walk, noting what fits the day.",
            "Plant something small—herbs, seeds, or a window box.",
            "Share a conservation tip or nature fact with friends.",
        ]
    if "Health" in label:
        return [
            "Do a 10-minute movement session inspired by the day’s theme.",
            "Prep a simple, nutritious snack to match the day.",
            "Share one healthy habit you’re keeping this week.",
        ]
    if "Kindness" in label:
        return [
            "Send a kind note or shout-out to someone who fits the theme.",
            "Do one small favor quietly for a friend or coworker.",
            "Share a feel-good story tied to the observance.",
        ]
    if "Geek" in label:
        return [
            "Share a favorite fact, meme, or tool related to the theme.",
            "Host a mini show-and-tell: a gadget, code snippet, or STEM story.",
            "Try a short experiment or demo that fits the day.",
        ]
    return celebration_ideas(name, pretty, [])


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

    web_page = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "url": canonical,
        "description": description,
        "breadcrumb": breadcrumb_schema,
        "isPartOf": {"@type": "WebSite", "name": "Obscure Holiday Calendar", "url": SITE_BASE},
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
            "<script type=\"application/ld+json\">",
            json_ld(web_page),
            "</script>",
        ]
    )


def badge_colors(slug: str) -> Tuple[str, str]:
    digest = hashlib.md5(slug.encode("utf-8")).hexdigest()
    c1 = "#" + digest[:6]
    c2 = "#" + digest[6:12]
    return c1, c2


def _wrap_badge_text(name: str) -> List[str]:
    """
    Wrap badge text into 1-2 lines so longer names still fit nicely.
    """
    clean = name.strip()
    if len(clean) <= 18:
        return [clean]
    words = clean.split()
    lines: List[str] = []
    current: List[str] = []
    for w in words:
        candidate = " ".join(current + [w])
        if len(candidate) <= 18:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    if len(lines) > 2:
        # collapse to two lines with ellipsis
        merged = " ".join(lines[:2])
        if len(merged) > 28:
            merged = merged[:27] + "…"
        return [merged, "Obscure Holiday"]
    return lines[:2]


def build_badge_svg(name: str, slug: str) -> str:
    c1, c2 = badge_colors(slug)
    lines = _wrap_badge_text(name)
    font_size = 20 if len(lines) == 1 else 16
    y_start = 56 if len(lines) == 1 else 48
    line_gap = 22
    tspans = []
    for i, line in enumerate(lines):
        y = y_start + i * line_gap
        tspans.append(
            f'<tspan x="50%" y="{y}" fill="#ffffff" font-family="Inter, Manrope, system-ui, sans-serif" '
            f'font-size="{font_size}" font-weight="700" text-anchor="middle">{html.escape(line)}</tspan>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="240" height="120" viewBox="0 0 240 120" role="img" aria-label="{html.escape(name)}">
  <defs>
    <linearGradient id="grad-{slug}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
  </defs>
  <rect rx="16" ry="16" width="240" height="120" fill="url(#grad-{slug})"/>
  <text>
    {''.join(tspans)}
  </text>
  <text x="50%" y="90%" fill="#f1f5f9" font-family="Inter, Manrope, system-ui, sans-serif" font-size="11" font-weight="600" text-anchor="middle">Obscure Holiday Calendar</text>
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
    data_lookup: Dict[str, Dict],
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

    # Category-tailored labels
    cat_info = classify_holiday(name, description)
    type_label = cat_info["type_label"]
    great_for = cat_info["great_for"]

    # Category-driven celebrations and FAQ tweak
    celebrations = category_celebrations(type_label, name, pretty)
    celebrate_line = celebrations[0] if celebrations else "Share the story, plan a small themed activity, and spread a little joy."
    faq = [
        (f"When is {name}?", f"It is observed on {pretty} each year."),
        (f"What is {name}?", description),
        (f"How do people celebrate {name}?", celebrate_line),
    ]

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

    # Concise "why it matters" with a higher limit to avoid awkward cutoffs for long names
    why_line = shorten_for_meta(description, f"Discover why {name} is celebrated on {pretty}.", 320)

    related_cards = []
    for r_slug in related_slugs[:3]:
        r_rec = data_lookup.get(r_slug, {})
        r_name = title_lookup.get(r_slug) or r_slug.replace("-", " ").title()
        r_date = pretty_date(r_rec.get("date", ""))
        r_desc = shorten_for_meta(r_rec.get("description", "") or f"Discover {r_name}.", f"Learn about {r_name}.", 110)
        related_cards.append(
            f"""
          <article class="related-card">
            <div class="related-pill">{html.escape(r_date)}</div>
            <h3><a href="/holiday/{r_slug}/">{html.escape(r_name)}</a></h3>
            <p>{html.escape(r_desc)}</p>
            <a class="related-link" href="/holiday/{r_slug}/" aria-label="Read about {html.escape(r_name)}">Read more →</a>
          </article>
        """
        )

    badge_path = f"/assets/badges/{slug}.svg"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(name)} — Obscure Holiday Calendar</title>
  <meta name="description" content="{html.escape(meta_desc)}" />
  <meta name="last-modified" content="{last_updated}" />
  <meta name="theme-color" content="#2c005f" />
  <meta name="google-adsense-account" content="ca-pub-7162731177966348" />
  <link rel="canonical" href="{canonical}" />
  <link rel="preload" href="/styles.css" as="style" crossorigin="anonymous" integrity="sha256-6thkjdloi9ZO0jXPomwwy5axQ9KPxbWvOcyD4umyijo=" onload="this.onload=null;this.rel='stylesheet'" />
  <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin />
  <link rel="preconnect" href="https://www.google-analytics.com" crossorigin />
  <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin />
  <link rel="preconnect" href="https://tpc.googlesyndication.com" crossorigin />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <!-- Critical above-the-fold CSS -->
  <style>
    body {{
      margin: 0;
      font-family: "Inter", "Manrope", system-ui, -apple-system, sans-serif;
      background: radial-gradient(circle at 20% 20%, #1a0c3f 0%, #0f0a2a 40%, #0b0b24 70%);
      color: #0f172a;
    }}
    .page-wrap {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 18px 16px 42px;
    }}
    .site-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 14px 16px;
      margin: 8px auto;
      max-width: 1120px;
    }}
    .brand {{
      display: inline-flex;
      gap: 10px;
      align-items: center;
      text-decoration: none;
    }}
    .brand-mark {{
      width: 44px;
      height: 44px;
      border-radius: 12px;
    }}
    .holiday-card {{
      background: linear-gradient(180deg, #ffffff 0%, #f8f5ff 100%);
      border-radius: 22px;
      padding: 18px;
      box-shadow: 0 24px 64px rgba(20, 12, 70, 0.16);
    }}
    .hero-badge {{
      max-width: 260px;
      width: min(90%, 260px);
      margin: 6px 0 4px;
      filter: drop-shadow(0 16px 40px rgba(44,0,95,0.18));
    }}
    .holiday-title {{
      margin: 8px 0 6px;
      font-size: 2rem;
    }}
  </style>
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
  <noscript><link rel="stylesheet" href="/styles.css" crossorigin="anonymous" integrity="sha256-6thkjdloi9ZO0jXPomwwy5axQ9KPxbWvOcyD4umyijo="></noscript>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADS_CLIENT}" crossorigin="anonymous"></script>
  <style>
    :root {{
      --brand-purple: #2c005f;
      --brand-pink: #f25d94;
      --brand-blue: #1c96f3;
      --bg: radial-gradient(circle at 20% 20%, #1a0c3f 0%, #0f0a2a 40%, #0b0b24 70%);
      --card: #ffffff;
      --muted: #5b6174;
      --border: #e4e7f2;
      --shadow: 0 24px 64px rgba(20, 12, 70, 0.16);
      --pill: linear-gradient(135deg, rgba(44,0,95,0.12), rgba(242,93,148,0.12));
      --related-bg: linear-gradient(180deg, #f8f5ff 0%, #f3f9ff 100%);
    }}
    body {{
      background: var(--bg);
    }}
    .skip-link {{
      position: absolute;
      left: -999px;
      top: auto;
      width: 1px;
      height: 1px;
      overflow: hidden;
    }}
    .skip-link:focus {{
      position: static;
      width: auto;
      height: auto;
      padding: 10px 14px;
      margin: 8px 12px;
      background: #ffffff;
      color: #000;
      border-radius: 10px;
      z-index: 1000;
      box-shadow: 0 8px 18px rgba(0,0,0,0.12);
    }}
    .breadcrumb {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
      margin: 10px 0 16px;
      color: #e5e7ef;
      font-weight: 600;
      font-size: 0.96rem;
    }}
    .breadcrumb a {{
      color: #f5f3ff;
      text-decoration: none;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.08);
    }}
    .breadcrumb a:hover {{
      border-color: rgba(255,255,255,0.18);
    }}
    .breadcrumb span {{
      color: #ffffff;
      font-weight: 700;
    }}
    .holiday-card {{
      background: linear-gradient(180deg, #ffffff 0%, #f8f5ff 100%);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      border-radius: 22px;
    }}
    .holiday-title {{
      color: var(--brand-purple);
      font-size: clamp(2rem, 2.4vw + 1.2rem, 2.8rem);
      line-height: 1.1;
      word-break: break-word;
      hyphens: auto;
    }}
    .meta-line {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 10px 0 16px;
      align-items: center;
    }}
    .eyebrow {{
      color: var(--brand-pink);
      font-weight: 800;
      letter-spacing: 0.08em;
    }}
    .pill {{
      background: var(--pill);
      color: #1f2937;
      border: 1px solid #ece9ff;
    }}
    .pill-secondary {{
      background: linear-gradient(135deg, rgba(28,150,243,0.12), rgba(242,93,148,0.12));
      border: 1px solid #dbeafe;
    }}
    .lead {{
      color: #1f2533;
    }}
    h2.section-title, .section h2 {{
      color: var(--brand-purple);
    }}
    .list li::marker {{
      color: var(--brand-pink);
    }}
    .ad-slot {{
      border: 1px dashed #d6d9ff;
      background: linear-gradient(135deg, rgba(28,150,243,0.08), rgba(242,93,148,0.08));
    }}
    .store-buttons-top .store-badge {{
      filter: drop-shadow(0 10px 24px rgba(44,0,95,0.12));
    }}
    .nav-links a {{
      color: #f0f4ff;
    }}
    .nav-links a:hover {{
      color: #fff;
    }}
    .brand-name {{
      color: #fff;
    }}
    .brand-tagline {{
      color: #e2e8f0;
    }}
    .related-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
    }}
    .related-card {{
      background: var(--related-bg);
      border: 1px solid #e8e8fb;
      border-radius: 16px;
      padding: 14px 16px;
      box-shadow: 0 14px 32px rgba(44,0,95,0.08);
    }}
    .related-card h3 {{
      margin: 8px 0 6px;
      color: #1f2533;
      font-size: 1.05rem;
    }}
    .related-card p {{
      margin: 0 0 8px;
      color: #4b5563;
      font-size: 0.95rem;
    }}
    .related-pill {{
      display: inline-flex;
      align-items: center;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(44,0,95,0.08);
      color: #2c005f;
      font-weight: 700;
      font-size: 0.85rem;
      border: 1px solid rgba(44,0,95,0.12);
    }}
    .related-link {{
      color: var(--brand-blue);
      font-weight: 700;
      text-decoration: none;
    }}
    .related-link:hover {{
      text-decoration: underline;
    }}
    .share-tools {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin: 12px 0 4px;
    }}
    .btn-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      background: linear-gradient(120deg, #2c005f, #f25d94);
      color: #fff;
      border-radius: 999px;
      font-weight: 800;
      text-decoration: none;
      border: none;
      cursor: pointer;
      box-shadow: 0 12px 28px rgba(44,0,95,0.26);
      transition: transform 120ms ease, box-shadow 120ms ease;
    }}
    .btn-pill.secondary {{
      background: linear-gradient(120deg, #1c96f3, #5ad4ff);
      box-shadow: 0 12px 24px rgba(28,150,243,0.22);
    }}
    .btn-pill:hover {{
      transform: translateY(-1px);
      box-shadow: 0 14px 30px rgba(44,0,95,0.3);
    }}
    .btn-pill:focus-visible {{
      outline: 2px solid #fff;
      outline-offset: 2px;
    }}
    .share-feedback {{
      color: #0f172a;
      font-weight: 700;
      margin: 6px 0 0;
    }}
    .recent-list {{
      list-style: none;
      padding: 0;
      margin: 0;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 10px;
    }}
    .recent-list li a {{
      display: block;
      padding: 10px 12px;
      border-radius: 12px;
      background: rgba(255,255,255,0.82);
      border: 1px solid #e5e7eb;
      color: #1f2937;
      text-decoration: none;
      box-shadow: 0 10px 20px rgba(15,23,42,0.08);
    }}
    .recent-list li a:hover {{
      border-color: #cbd5e1;
    }}
    .quick-links {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 12px 0 18px;
    }}
    .quick-links a {{
      background: rgba(255,255,255,0.12);
      color: #f8fafc;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.18);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.95rem;
    }}
    .quick-links a:hover {{
      border-color: rgba(255,255,255,0.28);
    }}
    .note-bar {{
      background: linear-gradient(90deg, rgba(44,0,95,0.14), rgba(28,150,243,0.14));
      color: #0f172a;
      border: 1px solid rgba(44,0,95,0.16);
      padding: 12px 14px;
      border-radius: 14px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 14px;
    }}
    .note-bar strong {{
      color: var(--brand-purple);
    }}
    .nav-links {{
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }}
    .nav-links .ig-icon {{
      width: 18px;
      height: 18px;
      vertical-align: middle;
    }}
    .nav-links .ig-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}
  </style>
  {schema}
</head>
<body class="page">
  <a class="skip-link" href="#main">Skip to main content</a>
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
      <a class="ig-link" href="https://instagram.com/obscureholidaycalendar" target="_blank" rel="noopener" aria-label="Follow us on Instagram">
        <svg class="ig-icon" viewBox="0 0 24 24" aria-hidden="true">
          <defs>
            <linearGradient id="ig-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#f77737"/>
              <stop offset="50%" stop-color="#e1306c"/>
              <stop offset="100%" stop-color="#4c35d3"/>
            </linearGradient>
          </defs>
          <rect x="2" y="2" width="20" height="20" rx="6" fill="url(#ig-grad)"/>
          <circle cx="12" cy="12" r="4.2" fill="none" stroke="#fff" stroke-width="2"/>
          <circle cx="17.1" cy="6.9" r="1.3" fill="#fff"/>
        </svg>
        @obscureholidaycalendar
      </a>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
    </nav>
  </header>

  <main id="main" class="page-wrap">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span aria-hidden="true">›</span>
      <a href="/holiday/">Holidays</a>
      <span aria-hidden="true">›</span>
      <span>{html.escape(name)}</span>
    </nav>
    <div class="quick-links" aria-label="Page quick links">
      <a href="#overview">Overview</a>
      <a href="#celebrate">Celebrate</a>
      <a href="#fun-facts">Fun facts</a>
      <a href="#faq">FAQ</a>
      <a href="#related">Related</a>
    </div>
    <article class="holiday-card">
      <div class="eyebrow">Annual observance</div>
      <h1 class="holiday-title">{html.escape(name)} <span class="holiday-emoji" aria-hidden="true">{html.escape(emoji)}</span></h1>
      <img src="{badge_path}" alt="{html.escape(name)} badge" class="hero-badge" loading="lazy" decoding="async" />
      <div class="meta-line">
        <span class="pill">{html.escape(pretty)}</span>
        <span class="pill pill-secondary">{html.escape(type_label)}</span>
        <span class="pill pill-secondary">Updated {last_updated}</span>
      </div>
      <div class="share-tools">
        <button class="btn-pill" type="button" id="share-btn" aria-label="Share this holiday">
          <span aria-hidden="true">🔗</span> Share this holiday
        </button>
        <button class="btn-pill secondary" type="button" id="copy-btn" aria-label="Copy link to clipboard">
          <span aria-hidden="true">📋</span> Copy link
        </button>
      </div>
      <div class="share-feedback" id="share-feedback" aria-live="polite"></div>

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

      <section class="section" id="overview">
        <h2>Overview</h2>
        <p>{safe_text(description)}</p>
        <p>Observed each year on {html.escape(pretty)}, {html.escape(name)} invites people to pause, share the story, and bring a little themed joy to their day.</p>
      </section>

      <div class="note-bar" role="note">
        <strong>Why it matters:</strong> {html.escape(why_line)}
      </div>

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
          <li><span>Type</span><span>{html.escape(type_label)}</span></li>
          <li><span>Great for</span><span>{html.escape(', '.join(great_for))}</span></li>
        </ul>
      </section>

      <section class="section" id="celebrate">
        <h2>Ways to celebrate</h2>
        <ul class="list">
          {''.join(f'<li>{safe_text(item)}</li>' for item in celebrations)}
        </ul>
      </section>

      <section class="section" id="fun-facts">
        <h2>Fun facts</h2>
        <ul class="list">
          {''.join(f'<li>{safe_text(item)}</li>' for item in fun_facts)}
        </ul>
      </section>

      <section class="section">
        <h2>Sources and attribution</h2>
        <p>Primary note: {safe_text(fun_facts[0])}</p>
      </section>

      <section class="section" id="related">
        <h2>Related holidays</h2>
        <div class="related-grid">
          {''.join(related_cards)}
        </div>
      </section>

      <section class="section" id="faq">
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

      <section class="section" id="recently-viewed">
        <h2>Recently viewed holidays</h2>
        <ul class="recent-list" aria-live="polite"></ul>
      </section>
    </article>
  </main>

  <button class="btn-pill secondary" id="back-to-top" type="button" aria-label="Back to top" style="position:fixed;right:18px;bottom:18px;display:none;z-index:999;">
    ↑ Top
  </button>

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
  <script>
    (function() {{
      const shareBtn = document.getElementById('share-btn');
      const copyBtn = document.getElementById('copy-btn');
      const feedback = document.getElementById('share-feedback');
      const recentList = document.querySelector('.recent-list');
      const pageData = {{ slug: "{slug}", name: "{html.escape(name)}", url: "{canonical}" }};

      function setFeedback(msg) {{
        if (feedback) feedback.textContent = msg;
      }}

      async function share() {{
        if (navigator.share) {{
          try {{
            await navigator.share({{ title: pageData.name, text: `Check out ${{pageData.name}}`, url: pageData.url }});
            setFeedback('Thanks for sharing!');
          }} catch(e) {{
            setFeedback('Share canceled.');
          }}
        }} else {{
          copy();
        }}
      }}

      function copy() {{
        try {{
          navigator.clipboard.writeText(pageData.url);
          setFeedback('Link copied to clipboard.');
        }} catch(e) {{
          setFeedback('Copy not available in this browser.');
        }}
      }}

      function loadRecents() {{
        try {{
          const raw = localStorage.getItem('ohc_recent');
          return raw ? JSON.parse(raw) : [];
        }} catch (e) {{
          return [];
        }}
      }}

      function saveRecents(list) {{
        try {{ localStorage.setItem('ohc_recent', JSON.stringify(list)); }} catch(e) {{}}
      }}

      function addRecent() {{
        const recents = loadRecents().filter(item => item.slug !== pageData.slug);
        recents.unshift(pageData);
        if (recents.length > 6) recents.length = 6;
        saveRecents(recents);
      }}

      function renderRecents() {{
        const recents = loadRecents().filter(item => item.slug !== pageData.slug);
        if (!recentList) return;
        if (!recents.length) {{
          recentList.innerHTML = '<li><a href="/holiday/">Browse all holidays →</a></li>';
          return;
        }}
        recentList.innerHTML = recents.map(item => `<li><a href=\"${{item.url}}\">${{item.name}}</a></li>`).join('');
      }}

      if (shareBtn) shareBtn.addEventListener('click', share);
      if (copyBtn) copyBtn.addEventListener('click', copy);
      addRecent();
      renderRecents();

      // Back to top
      const backTop = document.getElementById('back-to-top');
      if (backTop) {{
        backTop.addEventListener('click', () => window.scrollTo({{ top: 0, behavior: 'smooth' }}));
        window.addEventListener('scroll', () => {{
          const show = window.scrollY > 400;
          backTop.style.display = show ? 'inline-flex' : 'none';
        }});
      }}
    }})();
  </script>
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

        html_output = render_page(slug, record, prev_slug, next_slug, random_slug, title_lookup, related_slugs, data, last_updated)
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
