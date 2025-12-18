#!/usr/bin/env python3
"""
Rebuild all holiday landing pages with richer on-page content, aligned SEO/ASO
markup, and AdSense-friendly placement. Uses the existing local holidays.json
data and rewrites every /holiday/<slug>/index.html that already exists on disk.
Optionally uses OpenAI for richer copy (why it matters, origin, celebrate ideas,
sources, FAQ) if OPENAI_USE=1 and OPENAI_API_KEY is set.
"""
import html
import json
import os
import random
import re
import hashlib
import urllib.error
import urllib.request
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Tuple, Any


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

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_TIMEOUT = float(os.environ.get("OPENAI_TIMEOUT", "30"))
OPENAI_DEBUG = os.environ.get("OPENAI_DEBUG", "").lower() in ("1", "true", "yes")
OPENAI_ENABLED = bool(OPENAI_API_KEY) and os.environ.get("OPENAI_USE", "").lower() in ("1", "true", "yes")

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

def first_sentence(text: str) -> str:
    if not text:
        return ""
    for sep in [". ", "! ", "? "]:
        pos = text.find(sep)
        if pos != -1 and pos > 30:
            return text[: pos + 1].strip()
    return text.strip()

def log_openai(message: str) -> None:
    if OPENAI_DEBUG:
        print(message)

def openai_why_it_matters(name: str, pretty: str, description: str, type_label: str, great_for: List[str], fun_facts: List[str]) -> str:
    if not OPENAI_ENABLED:
        return ""

    audience = ", ".join(great_for[:3]) if great_for else "friends and families"
    fact_snip = first_sentence(fun_facts[0]) if fun_facts else ""
    prompt = (
        "Write 1-2 sentences explaining why this holiday matters. "
        "Mention the date. Be specific to the holiday's meaning. "
        "No calls to action, no hashtags, no quotes, no emojis."
        "\n\n"
        f"Holiday: {name}\n"
        f"Date: {pretty}\n"
        f"Category: {type_label}\n"
        f"Audience: {audience}\n"
        f"Description: {description}\n"
        f"Fun fact: {fact_snip}\n"
    )

    payload = json.dumps({
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You write concise, specific 'why it matters' copy for holiday pages."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 120,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{OPENAI_BASE_URL}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        log_openai(f"OpenAI HTTP error: {exc}")
        return ""
    except Exception as exc:  # pragma: no cover
        log_openai(f"OpenAI request failed: {exc}")
        return ""

    try:
        data = json.loads(raw)
        content = data["choices"][0]["message"]["content"]
    except Exception as exc:  # pragma: no cover
        log_openai(f"OpenAI response parse failed: {exc}")
        return ""

    line = content.strip().strip('"').strip()
    line = re.sub(r"^Why it matters:\\s*", "", line, flags=re.IGNORECASE)
    return line


def openai_enrich_holiday(name: str, pretty: str, description: str, fun_facts: List[str]) -> Dict[str, Any]:
    """
    Single OpenAI call to fetch richer content:
      - why_it_matters (1-2 sentences)
      - origin_story (1 paragraph)
      - celebrations (3-5 concise bullets)
      - sources: [{title, url}]
      - faq: [{q,a}]
    """
    if not OPENAI_ENABLED:
        return {}

    facts_joined = "; ".join(fun_facts[:5])
    prompt = (
        "You are curating a short holiday page. Respond ONLY with JSON.\n"
        "Fields: why_it_matters (1-2 sentences), origin_story (<=2 sentences), "
        "celebrations (3-5 concise bullets), sources (1-3 items with title+url), "
        "faq (2-3 Q&A pairs, concise). Keep it factual, verifiable, and on-topic. "
        "No emojis, no fluff.\n\n"
        f"Holiday: {name}\n"
        f"Date: {pretty}\n"
        f"Description: {description}\n"
        f"Fun facts: {facts_joined or 'N/A'}\n"
    )

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You write concise, factual holiday page copy. Respond ONLY with JSON."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.35,
        "max_tokens": 260,
    }

    req = urllib.request.Request(
        f"{OPENAI_BASE_URL}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as exc:  # pragma: no cover
        log_openai(f"OpenAI enrich failed: {exc}")
        return {}


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

def compile_keyword_pattern(keyword: str) -> re.Pattern:
    parts = keyword.lower().split()
    last = parts[-1]
    suffix = "" if last.endswith("s") else "s?"
    sep = r"(?:\s+|-)"
    if len(parts) == 1:
        pattern = rf"\b{re.escape(last)}{suffix}\b"
    else:
        tokens = [re.escape(p) for p in parts[:-1]] + [re.escape(last) + suffix]
        pattern = r"\b" + sep.join(tokens) + r"\b"
    return re.compile(pattern)


CATEGORY_PATTERNS = [
    (label, [compile_keyword_pattern(k) for k in keywords])
    for label, keywords in CATEGORY_RULES
]


def classify_holiday(name: str, description: str) -> dict:
    text = f"{name} {description}".lower()
    for label, patterns in CATEGORY_PATTERNS:
        if any(p.search(text) for p in patterns):
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

def generate_celebrations(name: str, pretty: str, type_label: str, great_for: List[str], fun_facts: List[str], description: str, slug: str) -> List[str]:
    rng = random.Random(f"celebrate-{slug}")
    audience = ", ".join(great_for[:2]) if great_for else "friends and family"
    hashtag = slugify(name)
    fact_snip = first_sentence(fun_facts[0]) if fun_facts else ""
    desc_snip = first_sentence(description)
    type_lower = type_label.lower()

    templates = [
        "{name} lands on {pretty} — host a quick nod with {audience} and snap a photo.",
        "Share one fast fact about {name}: {fact}",
        "Post a story with #{hashtag} and invite others to try a tiny activity.",
        "Plan a 10-minute activity that fits the {type} vibe and make it a mini tradition.",
        "Bring {name} to work or school with a short shout-out in a meeting or group chat.",
        "Pair music, snacks, or décor that match the theme and enjoy a small break.",
        "Write a note or journal entry on why {name} matters, then set a reminder for next year.",
    ]

    base = [tmpl.format(
        name=name,
        pretty=pretty,
        audience=audience,
        fact=fact_snip or desc_snip or f"it celebrates the spirit of {name}",
        hashtag=hashtag,
        type=type_lower,
    ) for tmpl in templates]

    # Mix in category-flavored lines
    base.extend(category_celebrations(type_label, name, pretty))

    # Shuffle deterministically and pick top 5 unique
    rng.shuffle(base)
    seen = set()
    unique = []
    for line in base:
        if line in seen:
            continue
        seen.add(line)
        unique.append(line)
        if len(unique) == 5:
            break
    return unique

def build_why_it_matters(name: str, pretty: str, description: str, type_label: str, great_for: List[str], fun_facts: List[str], slug: str) -> str:
    rng = random.Random(f"why-{slug}")
    audience = ", ".join(great_for[:3]) if great_for else "friends and families"
    type_theme = type_label.lower()
    desc_snip = first_sentence(description)
    fact_snip = first_sentence(fun_facts[0]) if fun_facts else ""
    tie_ins = []
    if fact_snip:
        tie_ins.append(f"For example: {fact_snip}")
    if desc_snip:
        tie_ins.append(desc_snip)
    tie_in = rng.choice(tie_ins) if tie_ins else f"People mark the day with small activities that match the spirit of {name}."

    openai_line = openai_why_it_matters(name, pretty, description, type_label, great_for, fun_facts)
    if openai_line:
        return shorten_for_meta(
            openai_line,
            f"Discover why {name} is celebrated on {pretty}.",
            360,
        )

    templates = [
        "{name} sits on {pretty} and gives {audience} a reason to spotlight {type_theme} moments. {tie_in}",
        "On {pretty}, {name} nudges {audience} to honor the {type_theme} side of life. {tie_in}",
        "{name} matters because it keeps {type_theme} stories alive for {audience}, not just in theory but in simple actions. {tie_in}",
        "Marked on {pretty}, {name} is a reminder to {audience} that small gestures keep {type_theme} traditions meaningful. {tie_in}",
    ]
    choice = rng.choice(templates)
    return shorten_for_meta(
        choice.format(
            audience=audience,
            type_theme=type_theme,
            tie_in=tie_in,
            name=name,
            pretty=pretty,
        ),
        f"Discover why {name} is celebrated on {pretty}.",
        360,
    )


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
    celebrations = generate_celebrations(name, pretty, type_label, great_for, fun_facts, description, slug)
    celebrate_line = celebrations[0] if celebrations else "Share the story, plan a small themed activity, and spread a little joy."
    faq = [
        (f"When is {name}?", f"It is observed on {pretty} each year."),
        (f"What is {name}?", description),
        (f"How do people celebrate {name}?", celebrate_line),
    ]

    # Optional OpenAI enrichment
    ai_data = openai_enrich_holiday(name, pretty, description, fun_facts)
    ai_why = ai_data.get("why_it_matters") if isinstance(ai_data, dict) else ""
    ai_origin = ai_data.get("origin_story") if isinstance(ai_data, dict) else ""
    ai_celebrations = ai_data.get("celebrations") if isinstance(ai_data, dict) and isinstance(ai_data.get("celebrations"), list) else None
    ai_sources = ai_data.get("sources") if isinstance(ai_data, dict) and isinstance(ai_data.get("sources"), list) else None
    ai_faq = ai_data.get("faq") if isinstance(ai_data, dict) and isinstance(ai_data.get("faq"), list) else None

    if ai_celebrations:
        celebrations = [str(c).strip() for c in ai_celebrations if str(c).strip()]
    if ai_faq:
        faq = []
        for item in ai_faq:
            if isinstance(item, dict):
                q = item.get("q") or item.get("question")
                a = item.get("a") or item.get("answer")
                if q and a:
                    faq.append((q, a))
    origin_story = ai_origin or (fun_facts[0] if fun_facts else description)
    sources_list = []
    if ai_sources:
        for src in ai_sources:
            if not isinstance(src, dict):
                continue
            title = str(src.get("title") or "").strip()
            url = str(src.get("url") or "").strip()
            if title or url:
                sources_list.append({"title": title or "Source", "url": url})
    if not sources_list and record.get("sourceUrl"):
        sources_list.append({"title": name, "url": str(record.get("sourceUrl"))})

    canonical = f"{SITE_BASE}/holiday/{slug}/"
    share_url = f"{canonical}?utm_source=share&utm_medium=copy&utm_campaign=holiday_page&utm_content={slug}"
    ios_utm = f"{IOS_URL}?utm_source=site&utm_medium=store_badge&utm_campaign=holiday_page&utm_content={slug}"
    android_utm = f"{ANDROID_URL}?utm_source=site&utm_medium=store_badge&utm_campaign=holiday_page&utm_content={slug}"
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

    # Distinct "why it matters" using tailored summary + audience + celebrate hook
    why_line = ai_why or build_why_it_matters(name, pretty, description, type_label, great_for, fun_facts, slug)

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

    def build_sources_html() -> str:
        if not sources_list:
            return "<p>Source not provided.</p>"
        parts = []
        for src in sources_list:
            if not isinstance(src, dict):
                continue
            title = safe_text(src.get("title", "Source"))
            url = html.escape(src.get("url", ""))
            if url:
                parts.append(f'<p><a href="{url}" target="_blank" rel="noopener">{title}</a></p>')
            else:
                parts.append(f"<p>{title}</p>")
        return "".join(parts) if parts else "<p>Source not provided.</p>"

    sources_html = build_sources_html()

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
  <link rel="preload" href="/styles.css" as="style" crossorigin="anonymous" onload="this.onload=null;this.rel='stylesheet'" />
  <link rel="preconnect" href="https://www.googletagmanager.com" crossorigin />
  <link rel="preconnect" href="https://www.google-analytics.com" crossorigin />
  <link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin />
  <link rel="preconnect" href="https://tpc.googlesyndication.com" crossorigin />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <!-- Critical above-the-fold CSS -->
  <style>
    body {{
      margin: 0;
      font-family: "Manrope", "Inter", system-ui, -apple-system, sans-serif;
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
      padding: 32px;
      box-shadow: 0 24px 64px rgba(20, 12, 70, 0.16);
    }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 240px;
      gap: 28px;
      align-items: start;
    }}
    .hero-aside {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }}
    .badge-frame {{
      padding: 12px;
      border-radius: 18px;
      background: #f9f6ff;
      border: 1px solid #ece9ff;
      box-shadow: 0 16px 34px rgba(44, 0, 95, 0.12);
    }}
    .hero-badge {{
      max-width: 220px;
      width: min(90%, 220px);
      margin: 0;
      filter: drop-shadow(0 12px 30px rgba(44,0,95,0.18));
    }}
    .holiday-title {{
      margin: 8px 0 6px;
      font-size: 2.3rem;
      line-height: 1.08;
    }}
    @media (max-width: 900px) {{
      .hero {{
        grid-template-columns: 1fr;
      }}
      .hero-aside {{
        order: -1;
      }}
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
    (function() {{
      const params = new URLSearchParams(window.location.search || '');
      const ref = document.referrer || '';
      const refHost = (() => {{
        try {{ return ref ? new URL(ref).hostname : ''; }} catch (_) {{ return ''; }}
      }})();
      const makePayload = () => ({{
        ts: Date.now(),
        source: params.get('utm_source') || (refHost || 'direct'),
        medium: params.get('utm_medium') || (ref ? 'referral' : 'unknown'),
        campaign: params.get('utm_campaign') || '',
        content: params.get('utm_content') || '',
        term: params.get('utm_term') || '',
        referrer: refHost,
        landing_path: window.location.pathname || '',
      }});
      let first = null;
      try {{
        const stored = localStorage.getItem('ohc_first_touch');
        if (stored) {{
          first = JSON.parse(stored);
        }} else {{
          first = makePayload();
          localStorage.setItem('ohc_first_touch', JSON.stringify(first));
        }}
      }} catch (_) {{
        first = first || makePayload();
      }}
      if (window.gtag && first) {{
        try {{
          gtag('set', 'user_properties', {{
            first_source: first.source || '',
            first_medium: first.medium || '',
            first_campaign: first.campaign || '',
            first_content: first.content || '',
            first_term: first.term || '',
            first_referrer: first.referrer || '',
            first_landing_path: first.landing_path || ''
          }});
        }} catch (_) {{}}
      }}
    }})();
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
  <noscript><link rel="stylesheet" href="/styles.css" crossorigin="anonymous"></noscript>
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
      <a class="shop-link" href="https://shop.obscureholidaycalendar.com/?utm_source=site&utm_medium=nav&utm_campaign=shop" target="_blank" rel="noopener">Shop</a>
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
      <header class="hero">
        <div class="hero-content">
          <div class="eyebrow">Annual observance</div>
          <h1 class="holiday-title">{html.escape(name)} <span class="holiday-emoji" aria-hidden="true">{html.escape(emoji)}</span></h1>
          <div class="meta-line">
            <span class="pill">{html.escape(pretty)}</span>
            <span class="pill pill-secondary">{html.escape(type_label)}</span>
            <span class="pill pill-secondary">Updated {last_updated}</span>
          </div>
          <p class="lead">
            This holiday is featured in the Obscure Holiday Calendar app with emoji-style visuals, reminders, and daily fun facts.
          </p>
          <div class="share-tools">
            <button class="btn-pill" type="button" id="share-btn" aria-label="Share this holiday">
              <span aria-hidden="true">🔗</span> Share this holiday
            </button>
            <button class="btn-pill secondary" type="button" id="copy-btn" aria-label="Copy link to clipboard">
              <span aria-hidden="true">📋</span> Copy link
            </button>
          </div>
          <div class="share-feedback" id="share-feedback" aria-live="polite"></div>
          <div class="store-buttons-top">
            <a href="{ios_utm}" target="_blank" rel="noopener">
              <img src="https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg"
                   alt="Download on the App Store" class="store-badge" />
            </a>
            <a href="{android_utm}" target="_blank" rel="noopener">
              <img src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png"
                   alt="Get it on Google Play" class="store-badge" />
            </a>
          </div>
        </div>
        <aside class="hero-aside">
          <div class="badge-frame">
            <img src="{badge_path}" alt="{html.escape(name)} badge" class="hero-badge" loading="lazy" decoding="async" />
          </div>
          <p class="badge-caption">Shareable holiday card preview</p>
        </aside>
      </header>

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
        <p>{safe_text(origin_story)}</p>
        {"<p>" + safe_text(fun_facts[1]) + "</p>" if len(fun_facts) > 1 and not ai_origin else ""}
      </section>

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
        {sources_html}
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
      const pageData = {{ slug: "{slug}", name: "{html.escape(name)}", url: "{share_url}" }};
      const shopLink = document.querySelector('.shop-link');

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
      if (shopLink && window.gtag) {{
        shopLink.addEventListener('click', () => {{
          gtag('event', 'shop_click', {{
            link_url: shopLink.href,
            link_text: 'Shop',
            source_page: "{slug}"
          }});
        }});
      }}
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

    # Map slug -> date and date -> list of slugs (order preserved)
    date_by_slug: Dict[str, str] = {}
    date_to_slugs: Dict[str, List[str]] = {}
    date_order: List[str] = []
    for mm, dd, slug in sorted(dated_slugs):
        rec = data.get(slug, {})
        date_raw = rec.get("date", "")
        date_by_slug[slug] = date_raw
        date_to_slugs.setdefault(date_raw, []).append(slug)
        if date_raw not in date_order:
            date_order.append(date_raw)

    # Build month -> slugs map for related links
    slugs_by_month: Dict[str, List[str]] = {}
    for slug in slugs_sorted:
        rec = data.get(slug, {})
        date_raw = rec.get("date", "")
        mm = date_raw.split("-")[0] if "-" in date_raw else "00"
        slugs_by_month.setdefault(mm, []).append(slug)

    target_months = {
        m.strip().zfill(2)
        for m in os.environ.get("REBUILD_MONTHS", "").split(",")
        if m.strip()
    }
    if target_months:
        print(f"Filtering rebuild to months: {', '.join(sorted(target_months))}")

    BADGE_DIR.mkdir(parents=True, exist_ok=True)

    for idx, slug in enumerate(slugs_sorted):
        record = data.get(slug, {})
        date_raw = record.get("date", "")
        try:
            date_idx = date_order.index(date_raw)
            prev_date = date_order[date_idx - 1] if date_idx > 0 else date_order[-1]
            next_date = date_order[date_idx + 1] if date_idx < len(date_order) - 1 else date_order[0]
        except ValueError:
            prev_date = date_raw
            next_date = date_raw
        prev_slug = date_to_slugs.get(prev_date, [slug])[0]
        next_slug = date_to_slugs.get(next_date, [slug])[0]

        date_raw = record.get("date", "")
        mm = date_raw.split("-")[0] if "-" in date_raw else "00"
        if target_months and mm not in target_months:
            continue

        options = [s for s in slugs_sorted if s != slug]
        random_slug = random.choice(options) if options else slug

        # Related: prefer same-month items
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
