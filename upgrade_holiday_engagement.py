#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOLIDAY_DIR = ROOT / "holiday"

RAIL_HTML = """
    <aside class=\"next-rail\" id=\"next-rail\" aria-label=\"Keep browsing holidays\">
      <div class=\"next-rail-head\">Keep the streak going</div>
      <ul class=\"next-rail-list\"></ul>
      <a class=\"next-rail-fallback\" href=\"/holiday/\">Browse all holidays</a>
    </aside>
""".strip("\n")

MID_RELATED_HTML = """
      <section class=\"section\" id=\"related-mid\">
        <h2>People also viewed</h2>
        <ul class=\"link-list\"></ul>
      </section>
""".strip("\n")

CSS_BLOCK = """
    .next-rail {
      display: none;
    }
    .continue-lead {
      margin: 0 0 12px;
      color: #42526b;
      font-weight: 600;
      line-height: 1.5;
    }
    #related-mid .link-list li {
      background: linear-gradient(90deg, rgba(28,150,243,0.08), rgba(255,255,255,0.8));
      border-color: rgba(28,150,243,0.2);
    }
    @media (min-width: 1280px) {
      .next-rail {
        display: block;
        position: fixed;
        right: max(16px, calc((100vw - 1280px) / 2));
        top: 120px;
        width: 248px;
        border-radius: 16px;
        border: 1px solid #ded7ff;
        background: linear-gradient(180deg, #ffffff, #f6f3ff);
        box-shadow: 0 16px 34px rgba(44,0,95,0.18);
        padding: 14px;
        z-index: 160;
      }
      .next-rail-head {
        font-weight: 800;
        color: #2c005f;
        margin: 0 0 10px;
        font-size: 0.95rem;
      }
      .next-rail-list {
        list-style: none;
        margin: 0;
        padding: 0;
        display: grid;
        gap: 8px;
      }
      .next-rail-list a {
        display: block;
        border-radius: 10px;
        border: 1px solid #e8e2ff;
        background: #fff;
        color: #2c005f;
        text-decoration: none;
        font-weight: 700;
        padding: 9px 10px;
        font-size: 0.92rem;
      }
      .next-rail-list a:hover {
        border-color: #d5caff;
        text-decoration: underline;
        text-underline-offset: 3px;
      }
      .next-rail-fallback {
        display: inline-block;
        margin-top: 10px;
        font-size: 0.86rem;
        font-weight: 700;
        color: #334155;
      }
    }
""".strip("\n")

SCRIPT_BLOCK = """
      const rail = document.getElementById('next-rail');

      function track(eventName, payload) {
        if (!window.gtag) return;
        try {
          gtag('event', eventName, payload || {});
        } catch (_) {}
      }

      function textLabel(el) {
        return ((el && el.textContent) || '').trim().slice(0, 80);
      }

      function buildRail() {
        if (!rail) return;
        const railList = rail.querySelector('.next-rail-list');
        if (!railList) return;
        const links = Array.from(document.querySelectorAll('#continue .link-list a')).slice(0, 4);
        if (!links.length) return;
        railList.innerHTML = links.map((a) => `<li><a href=\"${a.getAttribute('href') || '/holiday/'}\">${textLabel(a)}</a></li>`).join('');
      }

      function buildMidRelated() {
        const midList = document.querySelector('#related-mid .link-list');
        const related = Array.from(document.querySelectorAll('#related .link-list li')).slice(0, 4);
        if (!midList || !related.length) return;
        midList.innerHTML = related.map((li) => li.outerHTML).join('');
      }

      function attachEngagementTracking() {
        document.addEventListener('click', (event) => {
          const anchor = event.target.closest('a');
          if (!anchor) return;
          const href = anchor.getAttribute('href') || '';
          if (anchor.closest('#next-rail')) {
            track('rail_click', { source_page: pageData.slug, link_text: textLabel(anchor), link_url: href });
          } else if (anchor.closest('#continue')) {
            track('continue_click', { source_page: pageData.slug, link_text: textLabel(anchor), link_url: href });
          } else if (anchor.closest('#related') || anchor.closest('#related-mid')) {
            track('related_click', { source_page: pageData.slug, link_text: textLabel(anchor), link_url: href });
          } else if (anchor.closest('.quick-links')) {
            track('jump_link_click', { source_page: pageData.slug, link_text: textLabel(anchor), link_url: href });
          }
        }, { passive: true });
      }

      buildRail();
      buildMidRelated();
      attachEngagementTracking();
""".strip("\n")


def insert_once(content: str, marker: str, block: str, before: str) -> str:
    if marker in content:
        return content
    return content.replace(before, block + "\n" + before, 1)


def patch_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    out = src

    # CSS injection
    if ".next-rail" not in out:
      out = out.replace("  </style>", CSS_BLOCK + "\n  </style>", 1)

    # Sticky rail HTML
    if 'id="next-rail"' not in out:
        out = out.replace(
            '</div>\n    <article class="holiday-card">',
            '</div>\n' + RAIL_HTML + '\n    <article class="holiday-card">',
            1,
        )

    # Mid-related module
    if 'id="related-mid"' not in out:
        out = out.replace(
            '\n\n      <section class="section" id="celebrate">',
            '\n\n' + MID_RELATED_HTML + '\n\n      <section class="section" id="celebrate">',
            1,
        )

    # Stronger continuation CTA copy
    out = out.replace('<section class="section" id="continue">\n        <h2>Continue to</h2>',
                      '<section class="section" id="continue">\n        <h2>Continue your streak</h2>', 1)
    if 'class="continue-lead"' not in out:
        out = out.replace(
            '<section class="section" id="continue">\n        <h2>Continue your streak</h2>',
            '<section class="section" id="continue">\n        <h2>Continue your streak</h2>\n        <p class="continue-lead">Open one more holiday before you go to build daily momentum.</p>',
            1,
        )

    # Expand quick link label for related mid section
    out = out.replace('<a href="#related">Related</a>', '<a href="#related-mid">People also viewed</a>', 1)

    # JS hook injection
    if "attachEngagementTracking" not in out:
        hook = "      addRecent();\n      renderRecents();"
        out = out.replace(hook, SCRIPT_BLOCK + "\n\n" + hook, 1)

    if out != src:
        path.write_text(out, encoding="utf-8")
        return True
    return False


def main() -> None:
    files = sorted(HOLIDAY_DIR.glob("*/index.html"))
    updated = 0
    for path in files:
        if patch_file(path):
            updated += 1
    print(f"Updated {updated} of {len(files)} holiday pages.")


if __name__ == "__main__":
    main()
