import os
import re
from pathlib import Path

DOMAIN = "https://www.obscureholidaycalendar.com"
ADSENSE_CLIENT = "ca-pub-7162731177966348"
AD_SLOT = "7747026448"

IOS_URL = "https://apps.apple.com/us/app/obscure-holiday-calendar/id6755315850"
ANDROID_URL = "https://play.google.com/store/apps/details?id=com.codeman8806.obscureholidaycalendar"
APP_URL = "https://www.obscureholidaycalendar.com/app/"

# Brand icon with inline spacing so it isn't jammed on the H1
BRAND_ICON_HTML = """
<img src="/assets/app-icon.png"
     alt="Obscure Holiday Calendar App Icon"
     class="brand-icon"
     style="margin-top:10px;margin-bottom:14px;width:120px;">
"""

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
"""

ASO_BOOST_PARAGRAPH = """
<p class="aso-note">
  The Obscure Holiday Calendar app includes daily widgets, reminders, fun facts,
  and thousands of obscure holidays—free on iOS & Android.
</p>
"""

APP_BACKLINKS = f"""
<div class="app-backlinks">
  <p>
    Get the Obscure Holiday Calendar app on
    <a href="{IOS_URL}">iOS</a> or
    <a href="{ANDROID_URL}">Android</a>.
  </p>
</div>
"""

# Safe JS banner block
BANNER_TEMPLATE = (
    "<!-- ASO/SEO Banner Block -->\n"
    "<ins class=\"adsbygoogle\" style=\"display:block\" "
    f"data-ad-client=\"{ADSENSE_CLIENT}\" "
    f"data-ad-slot=\"{AD_SLOT}\" "
    "data-ad-format=\"auto\" "
    "data-full-width-responsive=\"true\"></ins>\n"
    "<script>\n"
    "    (adsbygoogle = window.adsbygoogle || []).push({});\n"
    "</script>\n"
)

ADSENSE_LOADER = f"""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
"""

IOS_SMART_BANNER = """
<meta name="apple-itunes-app" content="app-id=6755315850">
"""

ANDROID_SMART_BANNER = """
<meta name="google-play-app" content="app-id=com.codeman8806.obscureholidaycalendar">
"""

# -------------- HTML PARSERS ----------------

def get_headline(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return "Obscure Holiday"
    full = m.group(1).strip()
    parts = re.split(r"[–—-]", full, maxsplit=1)
    headline = parts[0].strip()
    return headline or full


def get_canonical(html: str, folder_slug: str) -> str:
    m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return f"{DOMAIN}/holiday/{folder_slug}"


def get_meta_description(html: str) -> str:
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    return ""


def get_date_text(html: str) -> str:
    m = re.search(
        r'<div\s+class=["\']date["\']>(.*?)</div>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()

# -------------- SCHEMA BUILDERS ----------------

def build_article_schema(headline: str, canonical: str, description: str) -> str:
    if not description:
        description = f"Learn about {headline} and fun ways to celebrate this obscure holiday."
    return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{headline}",
  "description": "{description}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "{canonical}"
  }},
  "author": {{
    "@type": "Organization",
    "name": "Obscure Holiday Calendar"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Obscure Holiday Calendar",
    "logo": {{
      "@type": "ImageObject",
      "url": "{DOMAIN}/assets/app-icon.png"
    }}
  }}
}}
</script>
"""


def build_faq_schema(headline: str, date_text: str) -> str:
    when_answer = f"{headline} is observed each year."
    if date_text:
        when_answer = f"{headline} is observed each year on {date_text}."
    return f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{
      "@type": "Question",
      "name": "When is {headline}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{when_answer}"
      }}
    }},
    {{
      "@type": "Question",
      "name": "How can I celebrate {headline}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "You can celebrate {headline} by learning the story behind the holiday, sharing it with friends, and enjoying fun themed activities."
      }}
    }}
  ]
}}
</script>
"""

# -------------- INJECTION / CLEANUP HELPERS ----------------

def inject_into_head(html: str, block: str, marker: str) -> str:
    """Inject block into <head> if marker not present (marker is a small unique substring)."""
    if marker in html:
        return html
    head_close = html.lower().find("</head>")
    if head_close == -1:
        return html
    return html[:head_close] + "\n" + block + "\n" + html[head_close:]


def inject_after_h1(html: str, block: str, marker: str) -> str:
    if marker in html:
        return html
    m = re.search(r"<h1[^>]*>.*?</h1>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return html
    return html[:m.end()] + "\n" + block + "\n" + html[m.end():]


def inject_banner_after_date(html: str) -> str:
    if BANNER_TEMPLATE in html:
        return html
    return html.replace('<div class="date">', BANNER_TEMPLATE + "\n<div class=\"date\">")


def add_backlinks_to_bottom(html: str) -> str:
    if "app-backlinks" in html:
        return html
    return html.replace("</body>", APP_BACKLINKS + "\n</body>")


def remove_legacy_ads_block(html: str) -> str:
    """
    Remove old hand-inserted AdSense block like:
    <!-- START-SEO-BLOCK --> ... <!-- END-SEO-BLOCK -->
    or a generic adsbygoogle block with a comment marker.
    """
    # If you used explicit START/END comments, strip that region:
    pattern = r"<!-- START-SEO-BLOCK -->.*?<!-- END-SEO-BLOCK -->"
    new_html, n = re.subn(pattern, "", html, flags=re.DOTALL | re.IGNORECASE)
    if n > 0:
        return new_html

    # Fallback: try to remove a lone commented adsbygoogle block if it exists
    pattern2 = r"<!-- AdSense banner -->.*?</script>"
    new_html2, n2 = re.subn(pattern2, "", html, flags=re.DOTALL | re.IGNORECASE)
    if n2 > 0:
        return new_html2

    return html


def move_breadcrumb_schema_into_head(html: str) -> str:
    """
    If there's a <!-- BREADCRUMB-SCHEMA --> block outside </html>,
    move that whole block into <head>.
    """
    m = re.search(r"<!-- BREADCRUMB-SCHEMA -->.*?</script>", html, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        return html

    block = m.group(0)
    # Remove from current position
    html_no = html.replace(block, "")
    # Inject into head
    html_new = inject_into_head(html_no, block, "BREADCRUMB-SCHEMA")
    return html_new

# -------------- MAIN ----------------

def main():
    root = Path("holiday")
    if not root.exists():
        print("No 'holiday' directory found.")
        return

    updated = 0

    for dirpath, dirnames, filenames in os.walk(root):
        if "index.html" not in filenames:
            continue

        path = Path(dirpath) / "index.html"
        folder_slug = Path(dirpath).name

        html = path.read_text(encoding="utf-8")

        # Basic info from HTML
        headline = get_headline(html)
        canonical = get_canonical(html, folder_slug)
        description = get_meta_description(html)
        date_text = get_date_text(html)

        # CLEANUP FIRST
        html = remove_legacy_ads_block(html)
        html = move_breadcrumb_schema_into_head(html)

        # 1) Brand icon at top
        if "brand-icon" not in html:
            html = BRAND_ICON_HTML + html

        # 2) Store buttons + ASO line after H1
        html = inject_after_h1(html, STORE_BUTTONS_TOP, "store-buttons-top")
        html = inject_after_h1(html, ASO_BOOST_PARAGRAPH, "aso-note")

        # 3) Smart banners
        html = inject_into_head(html, IOS_SMART_BANNER, "apple-itunes-app")
        html = inject_into_head(html, ANDROID_SMART_BANNER, "google-play-app")

        # 4) AdSense loader
        html = inject_into_head(html, ADSENSE_LOADER, "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js")

        # 5) MobileApp schema (generic)
        if '"MobileApplication"' not in html:
            mobile_schema = f"""
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "Obscure Holiday Calendar",
  "operatingSystem": "Android, iOS",
  "applicationCategory": "LifestyleApplication",
  "url": "{APP_URL}",
  "downloadUrl": [
    "{ANDROID_URL}",
    "{IOS_URL}"
  ],
  "offers": {{
    "@type": "Offer",
    "price": 0,
    "priceCurrency": "USD"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Obscure Holiday Calendar",
    "logo": {{
      "@type": "ImageObject",
      "url": "{DOMAIN}/assets/app-icon.png"
    }}
  }}
}}
</script>
"""
            html = inject_into_head(html, mobile_schema, '"MobileApplication"')

        # 6) Article + FAQ schema
        if '"Article"' not in html:
            article_schema = build_article_schema(headline, canonical, description)
            html = inject_into_head(html, article_schema, '"Article"')
        if '"FAQPage"' not in html:
            faq_schema = build_faq_schema(headline, date_text)
            html = inject_into_head(html, faq_schema, '"FAQPage"')

        # 7) Banner after date (if date marker exists)
        if '<div class="date">' in html:
            html = inject_banner_after_date(html)

        # 8) App backlinks at bottom
        html = add_backlinks_to_bottom(html)

        path.write_text(html, encoding="utf-8")
        updated += 1

    print(f"Done! Cleaned & updated {updated} holiday pages.")


if __name__ == "__main__":
    main()

