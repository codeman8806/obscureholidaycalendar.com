#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOLIDAY_DIR = ROOT / "holiday"

CSS_POLISH_BLOCK = """
    :root {
      --pro-space: clamp(18px, 2vw, 28px);
      --pro-border: #e6e8f3;
      --pro-ink: #172033;
      --pro-muted: #4d5b75;
      --pro-bg: #fbfbff;
    }
    .page-wrap {
      max-width: 1160px;
      padding-bottom: 64px;
    }
    .holiday-card {
      max-width: 980px;
      margin: 0 auto;
      padding: clamp(22px, 2.2vw, 36px);
      border: 1px solid var(--pro-border);
      box-shadow: 0 22px 56px rgba(20, 12, 70, 0.13);
      background: linear-gradient(180deg, #ffffff 0%, #fbfaff 100%);
    }
    .hero {
      gap: clamp(18px, 2vw, 30px);
    }
    .holiday-title {
      letter-spacing: -0.02em;
      text-wrap: balance;
    }
    .lead,
    .section p,
    .section li,
    .faq dd,
    .link-list .meta {
      color: var(--pro-ink);
      line-height: 1.72;
    }
    .section {
      padding: 14px 0;
      border-top: 1px solid rgba(44, 0, 95, 0.08);
    }
    .section:first-of-type {
      border-top: 0;
      padding-top: 0;
    }
    .section h2 {
      letter-spacing: -0.01em;
      margin: 0 0 10px;
      font-size: clamp(1.25rem, 1.2vw + 1rem, 1.6rem);
    }
    .note-bar {
      border-left: 4px solid rgba(44, 0, 95, 0.42);
      background: linear-gradient(90deg, rgba(44,0,95,0.11), rgba(28,150,243,0.11));
    }
    .ad-section {
      border-radius: 14px;
      border: 1px solid #e6e8f3;
      background: var(--pro-bg);
      padding: 12px;
      margin: 16px 0;
    }
    .link-list li,
    .recent-list li a,
    .faq-item {
      transition: transform 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
    }
    .link-list li:hover,
    .recent-list li a:hover,
    .faq-item:hover {
      transform: translateY(-1px);
      border-color: #d6d9ea;
      box-shadow: 0 10px 24px rgba(17, 24, 39, 0.08);
    }
    .footer-links a {
      font-weight: 600;
    }
    @media (max-width: 900px) {
      .holiday-card {
        border-radius: 18px;
      }
      .section {
        padding: 12px 0;
      }
    }
""".strip("\n")

ANALYTICS_BLOCK = """
      function initAdvancedEngagementTracking() {
        const once = new Set();

        function emit(name, payload) {
          if (!window.gtag) return;
          try {
            gtag('event', name, payload || {});
          } catch (_) {}
        }

        const milestones = [25, 50, 75, 100];
        function onScrollDepth() {
          const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
          if (maxScroll <= 0) return;
          const pct = Math.round((window.scrollY / maxScroll) * 100);
          milestones.forEach((m) => {
            const key = `scroll_${m}`;
            if (pct >= m && !once.has(key)) {
              once.add(key);
              emit('scroll_depth', {
                source_page: pageData.slug,
                percent: m,
                page_type: 'holiday'
              });
            }
          });
        }

        let engagedSeconds = 0;
        let active = true;
        let lastTick = Date.now();
        let idleTimer = null;
        const engagedMilestones = [30, 90, 180];

        function resetIdle() {
          active = true;
          if (idleTimer) clearTimeout(idleTimer);
          idleTimer = setTimeout(() => { active = false; }, 15000);
        }

        ['scroll', 'click', 'keydown', 'touchstart', 'mousemove'].forEach((evt) => {
          window.addEventListener(evt, resetIdle, { passive: true });
        });
        document.addEventListener('visibilitychange', () => {
          if (document.hidden) active = false;
          else resetIdle();
        });

        setInterval(() => {
          const now = Date.now();
          const delta = (now - lastTick) / 1000;
          lastTick = now;
          if (document.hidden || !active) return;
          engagedSeconds += delta;
          engagedMilestones.forEach((m) => {
            const key = `engaged_${m}`;
            if (engagedSeconds >= m && !once.has(key)) {
              once.add(key);
              emit('engaged_time', {
                source_page: pageData.slug,
                seconds: m,
                page_type: 'holiday'
              });
            }
          });
        }, 1000);

        window.addEventListener('scroll', onScrollDepth, { passive: true });
        onScrollDepth();
        resetIdle();

        const adSections = document.querySelectorAll('.ad-section');
        if ('IntersectionObserver' in window && adSections.length) {
          const adIo = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
              if (!entry.isIntersecting) return;
              const adKey = entry.target.getAttribute('data-ad-key') || `ad_${Array.from(adSections).indexOf(entry.target) + 1}`;
              if (once.has(adKey)) return;
              once.add(adKey);
              emit('ad_viewable', {
                source_page: pageData.slug,
                ad_slot: adKey,
                page_type: 'holiday'
              });
            });
          }, { threshold: 0.45 });
          adSections.forEach((el, idx) => {
            el.setAttribute('data-ad-key', `ad_slot_${idx + 1}`);
            adIo.observe(el);
          });
        }

        const shareBtnEl = document.getElementById('share-btn');
        const copyBtnEl = document.getElementById('copy-btn');
        if (shareBtnEl) {
          shareBtnEl.addEventListener('click', () => {
            emit('share_button_click', { source_page: pageData.slug, page_type: 'holiday' });
          });
        }
        if (copyBtnEl) {
          copyBtnEl.addEventListener('click', () => {
            emit('copy_link_click', { source_page: pageData.slug, page_type: 'holiday' });
          });
        }
      }

      initAdvancedEngagementTracking();
""".strip("\n")


def patch_file(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    out = src

    if "--pro-space" not in out:
        out = out.replace("  </style>", CSS_POLISH_BLOCK + "\n  </style>", 1)

    if "initAdvancedEngagementTracking" not in out:
        hook = "      addRecent();\n      renderRecents();"
        out = out.replace(hook, ANALYTICS_BLOCK + "\n\n" + hook, 1)

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
