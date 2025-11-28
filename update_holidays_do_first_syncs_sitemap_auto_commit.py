#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple, Set

import requests

# ==== CONFIG ====
REPO_ROOT = Path(__file__).resolve().parent
HOLIDAYS_JSON_PATH = REPO_ROOT / "holidays.json"
HOLIDAYS_DIR = REPO_ROOT / "holiday"
SITEMAP_PATH = REPO_ROOT / "sitemap.xml"

# Firebase Realtime Database root JSON
FIREBASE_URL = "https://gen-lang-client-0034763265-default-rtdb.firebaseio.com/.json"

SITE_BASE = "https://www.obscureholidaycalendar.com"


# ==== UTILITIES ====

MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


def slugify(name: str) -> str:
    """Convert a holiday name into a lowercase-hyphen slug."""
    import re

    name = name.lower()
    # replace any non-letter/digit with hyphen
    name = re.sub(r"[^a-z0-9]+", "-", name)
    # collapse multiple hyphens
    name = re.sub(r"-+", "-", name)
    # trim hyphens
    name = name.strip("-")
    return name


def ensure_repo_root() -> None:
    """Sanity check that we are in the expected repo."""
    expected_files = {"index.html", "robots.txt", "app-ads.txt"}
    present = {p.name for p in REPO_ROOT.iterdir() if p.is_file()}
    missing = expected_files - present
    if missing:
        raise RuntimeError(
            f"Repo sanity check failed. Missing files in {REPO_ROOT}: {missing}"
        )


def run(cmd, cwd=None) -> Tuple[int, str, str]:
    """Run a shell command and return (code, stdout, stderr)."""
    print(f"$ {' '.join(cmd)}")
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate()
    if out:
        print(out)
    if err:
        print(err)
    return proc.returncode, out, err


# ==== HOLIDAY DATA LOADING ====

def load_old_holidays() -> Dict[str, Any]:
    """Load the existing holidays.json (if present)."""
    if not HOLIDAYS_JSON_PATH.exists():
        print("No existing holidays.json, treating as empty.")
        return {"holidays": {}}

    with HOLIDAYS_JSON_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "holidays" not in data or not isinstance(data["holidays"], dict):
        raise RuntimeError("Existing holidays.json has unexpected structure.")
    return data


def download_new_holidays() -> Dict[str, Any]:
    """Download latest holidays JSON from Firebase and return parsed dict."""
    print(f"Downloading holidays from {FIREBASE_URL} ...")
    resp = requests.get(FIREBASE_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # The structure we saw is {"holidays": { "MM-DD": [ { ... }, ... ], ... }}
    if "holidays" not in data or not isinstance(data["holidays"], dict):
        raise RuntimeError("Remote JSON does not contain expected 'holidays' key.")

    # Optional: save raw snapshot for debugging
    snapshot_name = f"holidays_snapshot_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
    snapshot_path = REPO_ROOT / snapshot_name
    with snapshot_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved raw snapshot to {snapshot_path}")

    return data


def build_slug_index(holidays_root: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Build an index of slug -> holiday_record (with date).
    Handles both:
      - objects that already have 'slug'
      - objects where we need to slugify 'name'
    """
    idx: Dict[str, Dict[str, Any]] = {}

    holidays = holidays_root.get("holidays", {})
    for date_str, items in holidays.items():
        for item in items:
            if not isinstance(item, dict):
                continue
            slug = item.get("slug")
            if not slug:
                name = item.get("name")
                if not name:
                    continue
                slug = slugify(name)

            entry = dict(item)
            entry["date"] = entry.get("date", date_str)
            entry["slug"] = slug
            idx[slug] = entry

    return idx


def compute_slug_sets(old_root: Dict[str, Any], new_root: Dict[str, Any]) -> Tuple[Set[str], Set[str], Set[str]]:
    """Return (old_slugs, new_slugs, unchanged_slugs)."""
    old_idx = build_slug_index(old_root)
    new_idx = build_slug_index(new_root)

    old_slugs = set(old_idx.keys())
    new_slugs = set(new_idx.keys())
    unchanged = old_slugs & new_slugs

    return old_slugs, new_slugs, unchanged


# ==== HTML GENERATION ====

def date_to_pretty(date_str: str) -> str:
    """
    Convert 'MM-DD' to 'Month D'.
    Fallbacks to the raw string if something is off.
    """
    try:
        mm, dd = date_str.split("-")
        month_name = MONTH_NAMES.get(mm, mm)
        return f"{month_name} {int(dd)}"
    except Exception:
        return date_str


def render_holiday_html(holiday: Dict[str, Any]) -> str:
    """Render the full index.html content for a holiday page."""
    name = holiday.get("name", "Holiday")
    slug = holiday.get("slug", slugify(name))
    date_str = holiday.get("date", "")
    pretty_date = date_to_pretty(date_str)

    # Meta description: short and app-focused
    meta_desc = (
        f"{name} is one of the fun, weird holidays featured in the Obscure Holiday Calendar app. "
        f"Celebrate {pretty_date} and discover more obscure holidays in the app."
    )

    page_title = f"{name} — Obscure Holiday Calendar"
    canonical_url = f"{SITE_BASE}/holiday/{slug}"

    # We don’t dump the whole description (keeps pages light),
    # but we could use it later if you want.
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{page_title}</title>

  <link rel="canonical" href="{canonical_url}" />

  <!-- Basic SEO -->
  <meta name="description" content="{meta_desc}" />

  <!-- Open Graph -->
  <meta property="og:title" content="{page_title}" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:image" content="{SITE_BASE}/assets/app-icon.png" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{page_title}" />
  <meta name="twitter:description" content="{meta_desc}" />
  <meta name="twitter:image" content="{SITE_BASE}/assets/app-icon.png" />

  <link rel="icon" type="image/png" href="{SITE_BASE}/assets/app-icon.png" />

  <style>
    :root {{
      --bg: #faf7ff;
      --card-bg: #ffffff;
      --primary: #2c005f;
      --accent: #f25d94;
      --text-main: #222222;
      --text-sub: #555555;
      --shadow-soft: 0 4px 18px rgba(0,0,0,0.08);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      padding: 0;
      background: var(--bg);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      color: var(--text-main);
    }}

    .page-wrap {{
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px 16px;
    }}

    .container {{
      max-width: 720px;
      width: 100%;
      margin: 0 auto;
      background: var(--card-bg);
      border-radius: 24px;
      box-shadow: var(--shadow-soft);
      padding: 32px 20px 28px;
      text-align: center;
    }}

    .app-icon {{
      width: 120px;
      height: 120px;
      border-radius: 26px;
      box-shadow: 0 8px 18px rgba(0,0,0,0.18);
      margin-bottom: 10px;
    }}

    h1 {{
      font-size: 30px;
      margin: 10px 0 8px;
      font-weight: 800;
      color: var(--primary);
      letter-spacing: 0.02em;
    }}

    .date {{
      font-size: 16px;
      color: var(--text-sub);
      margin-bottom: 16px;
    }}

    .tagline {{
      font-size: 16px;
      color: var(--text-sub);
      margin-bottom: 24px;
    }}

    .store-buttons {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 18px;
      margin-bottom: 10px;
    }}

    @media (min-width: 520px) {{
      .store-buttons {{
        flex-direction: row;
        justify-content: center;
      }}
    }}

    .store-btn {{
      flex: 1;
      min-width: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 14px 18px;
      border-radius: 999px;
      font-size: 15px;
      font-weight: 600;
      text-decoration: none;
      border: 2px solid transparent;
      transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.16s ease, border-color 0.16s ease;
      white-space: nowrap;
    }}

    .store-btn span {{
      display: block;
      text-align: left;
      line-height: 1.2;
    }}

    .store-btn small {{
      display: block;
      font-size: 11px;
      font-weight: 500;
      opacity: 0.8;
    }}

    .store-btn strong {{
      display: block;
      font-size: 14px;
      font-weight: 700;
    }}

    .store-btn.ios {{
      background: #000;
      color: #fff;
      box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }}

    .store-btn.android {{
      background: #ffffff;
      color: #000;
      border-color: #000;
    }}

    .store-btn:hover {{
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    }}

    footer {{
      margin-top: 20px;
      font-size: 13px;
      color: #777777;
    }}

    footer a {{
      color: #555555;
      margin: 0 8px;
      text-decoration: none;
      font-weight: 500;
    }}

    footer a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="page-wrap">
    <main class="container">
      <img src="{SITE_BASE}/assets/app-icon.png" alt="Obscure Holiday Calendar App Icon" class="app-icon" />

      <h1>{name}</h1>
      <div class="date">{pretty_date}</div>

      <p class="tagline">
        This holiday is featured in the <strong>Obscure Holiday Calendar</strong> app.
        Open the app to see artwork, fun facts, and the full description.
      </p>

      <div class="store-buttons">
        <a class="store-btn ios" href="https://apps.apple.com/us/app/obscure-holiday-calendar/id6755315850" target="_blank" rel="noopener noreferrer">
          <span>
            <small>Download on the</small>
            <strong>App Store</strong>
          </span>
        </a>

        <a class="store-btn android" href="https://play.google.com/store/apps/details?id=com.codeman8806.obscureholidaycalendar" target="_blank" rel="noopener noreferrer">
          <span>
            <small>Get it on</small>
            <strong>Google Play</strong>
          </span>
        </a>
      </div>

      <footer>
        <a href="https://github.com/codeman8806/Privacy-Policy/wiki/Privacy-Policy-for-Obscure-Holiday-Calendar" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
        ·
        <a href="https://github.com/codeman8806/Privacy-Policy/wiki/Support-for-Obscure-Holiday-Calendar" target="_blank" rel="noopener noreferrer">Support</a>
      </footer>
    </main>
  </div>
</body>
</html>
"""
    return html


# ==== FILE UPDATES ====

def remove_old_pages(slugs_to_remove: Set[str]) -> None:
    if not slugs_to_remove:
        print("No pages to remove.")
        return

    print(f"Removing {len(slugs_to_remove)} old holiday page(s)...")
    for slug in sorted(slugs_to_remove):
        dir_path = HOLIDAYS_DIR / slug
        if dir_path.is_dir():
            print(f"  - Deleting directory {dir_path}")
            shutil.rmtree(dir_path)
        else:
            print(f"  - Skipping {dir_path} (not found)")


def create_new_pages(new_root: Dict[str, Any], slugs_to_add: Set[str]) -> None:
    if not slugs_to_add:
        print("No new holiday pages to create.")
        return

    idx = build_slug_index(new_root)
    print(f"Creating {len(slugs_to_add)} new holiday page(s)...")

    for slug in sorted(slugs_to_add):
        holiday = idx.get(slug)
        if not holiday:
            print(f"  ! No holiday data found for slug {slug}, skipping.")
            continue

        html = render_holiday_html(holiday)
        dir_path = HOLIDAYS_DIR / slug
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = dir_path / "index.html"
        print(f"  + Writing {file_path}")
        with file_path.open("w", encoding="utf-8") as f:
            f.write(html)


def rebuild_sitemap(final_slugs: Set[str]) -> None:
    """
    Rebuild sitemap.xml from scratch:
      - root homepage
      - all /holiday/<slug>/ URLs
    """
    print(f"Rebuilding sitemap.xml with {len(final_slugs)} holiday URLs...")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "  <url>",
        f"    <loc>{SITE_BASE}/</loc>",
        "    <changefreq>monthly</changefreq>",
        "    <priority>1.00</priority>",
        "  </url>",
    ]

    for slug in sorted(final_slugs):
        loc = f"{SITE_BASE}/holiday/{slug}/"
        lines.extend([
            "  <url>",
            f"    <loc>{loc}</loc>",
            "    <changefreq>yearly</changefreq>",
            "    <priority>0.80</priority>",
            "  </url>",
        ])

    lines.append("</urlset>")

    with SITEMAP_PATH.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote sitemap.xml to {SITEMAP_PATH}")


# ==== GIT INTEGRATION ====

def git_commit_and_push() -> None:
    # See if anything changed
    code, out, _ = run(["git", "status", "--porcelain"], cwd=REPO_ROOT)
    if code != 0:
        print("git status failed, not committing.")
        return

    if not out.strip():
        print("No git changes to commit.")
        return

    # Add all changes
    run(["git", "add", "."], cwd=REPO_ROOT)

    msg = f"Update holidays from Firebase {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ')}"
    run(["git", "commit", "-m", msg], cwd=REPO_ROOT)

    # Push to origin main (matches your remote setup)
    run(["git", "push", "origin", "main"], cwd=REPO_ROOT)


# ==== MAIN ====

def main() -> None:
    ensure_repo_root()

    # 1) Load old holidays.json
    old_root = load_old_holidays()

    # 2) Download latest DB snapshot
    new_root = download_new_holidays()

    # 3) Compute slug sets
    old_slugs, new_slugs, unchanged_slugs = compute_slug_sets(old_root, new_root)
    slugs_to_add = new_slugs - old_slugs
    slugs_to_remove = old_slugs - new_slugs

    print(f"Old slugs: {len(old_slugs)}")
    print(f"New slugs: {len(new_slugs)}")
    print(f"Unchanged: {len(unchanged_slugs)}")
    print(f"To add:    {len(slugs_to_add)}")
    print(f"To remove: {len(slugs_to_remove)}")

    # 4) Remove pages for holidays that no longer exist
    remove_old_pages(slugs_to_remove)

    # 5) Create pages only for newly added slugs
    create_new_pages(new_root, slugs_to_add)

    # 6) Write the new holidays.json (overwriting the old one)
    with HOLIDAYS_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(new_root, f, ensure_ascii=False, indent=2)
    print(f"Wrote updated holidays.json to {HOLIDAYS_JSON_PATH}")

    # 7) Rebuild sitemap based on the *final* slug set (new DB)
    final_slugs = new_slugs
    rebuild_sitemap(final_slugs)

    # 8) Commit and push via git
    git_commit_and_push()


if __name__ == "__main__":
    main()

