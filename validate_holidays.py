#!/usr/bin/env python3
"""
Validator for holidays.json.

Offline checks:
- holidays.json structure: {"holidays": {"MM-DD": [ {name, description, funFacts, ...}, ... ]}}
- Date keys are valid calendar days (allows Feb 29).
- Each holiday has a non-empty name/description and some fun facts.
- Slug/name duplicates across dates.
- Heuristic confidence for data completeness and date plausibility.

Optional OpenAI checks (requires OPENAI_API_KEY and --openai):
- For each holiday, ask the model to rate legitimacy, date match, and fact plausibility.
- Adds issues if confidence is low.

Usage:
  python3 validate_holidays.py
  python3 validate_holidays.py --json-out report.json
  python3 validate_holidays.py --file path/to/holidays.json
  python3 validate_holidays.py --openai --json-out report.json
"""

import argparse
import json
import os
import re
import time
from collections import defaultdict, Counter
from pathlib import Path
from typing import Dict, List, Any

import requests


MONTH_DAYS = {
    1: 31, 2: 29, 3: 31, 4: 30,
    5: 31, 6: 30, 7: 31, 8: 31,
    9: 30, 10: 31, 11: 30, 12: 31,
}

MONTH_NAMES = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def slugify(name: str) -> str:
    s = name.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def parse_date_key(key: str):
    if not re.fullmatch(r"\d{2}-\d{2}", key):
        return None
    mm, dd = int(key[:2]), int(key[3:])
    return mm, dd


def month_in_text(text: str) -> List[int]:
    text_low = text.lower()
    found = []
    for name, num in MONTH_NAMES.items():
        if name in text_low:
            found.append(num)
    return found


def load_holidays(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "holidays" in data:
        return data
    raise ValueError("Expected top-level {'holidays': {...}} structure")


def openai_score(entry: Dict[str, Any], model: str, base_url: str, timeout: float) -> Dict[str, Any]:
    name = entry.get("name", "")
    date_key = entry.get("date", "")
    desc = entry.get("description", "")
    facts = entry.get("funFacts") if isinstance(entry.get("funFacts"), list) else []
    facts_joined = "; ".join(facts[:5])
    prompt = (
        "You are verifying an obscure holiday entry. "
        "Rate on 0-1 scale: legitimacy of the holiday, whether the date matches the known observance, "
        "and whether the description/facts seem plausible. If unsure, lower the score. "
        "Return JSON with keys: legitimacy, date_match, fact_confidence (all 0-1), and notes (short list).\n\n"
        f"Name: {name}\n"
        f"Date: {date_key}\n"
        f"Description: {desc}\n"
        f"Fun facts: {facts_joined or 'N/A'}\n"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a careful fact-checker for holiday data. Respond ONLY with JSON."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 120,
    }
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "Content-Type": "application/json",
    }
    resp = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except Exception:
        return {}


def score_confidence(entry: Dict[str, Any]) -> Dict[str, float]:
    """Heuristic completeness scores, not ground-truth fact checking."""
    score = 1.0
    desc = (entry.get("description") or "").strip()
    facts = entry.get("funFacts") if isinstance(entry.get("funFacts"), list) else []
    emoji = (entry.get("emoji") or "").strip()
    source = (entry.get("sourceUrl") or "").strip()

    if not desc:
        score -= 0.4
    elif len(desc) < 80:
        score -= 0.2

    if not facts:
        score -= 0.3
    elif len(facts) < 2:
        score -= 0.15

    if not emoji:
        score -= 0.05
    if not source:
        score -= 0.1

    score = max(0.0, min(1.0, score))
    return {"data_confidence": round(score, 2)}


def date_plausibility(mm: int, dd: int, entry: Dict[str, Any]) -> float:
    if mm not in MONTH_DAYS or dd < 1 or dd > MONTH_DAYS[mm]:
        return 0.0
    score = 0.6
    text = f"{entry.get('name','')} {entry.get('description','')}"
    months = month_in_text(text)
    if months:
        if mm in months:
            score += 0.2
        else:
            score -= 0.2
    return max(0.0, min(1.0, score))


def validate(path: Path):
    data = load_holidays(path)
    holidays = data.get("holidays", {})

    issues = []
    dup_name_dates = defaultdict(list)
    slug_dates = defaultdict(list)

    for date_key, items in holidays.items():
        parsed = parse_date_key(date_key)
        if not parsed:
            issues.append({"severity": "error", "type": "bad_date_key", "date": date_key, "msg": "Date key not MM-DD"})
            continue
        mm, dd = parsed
        if mm not in MONTH_DAYS or dd < 1 or dd > MONTH_DAYS[mm]:
            issues.append({"severity": "error", "type": "invalid_calendar_day", "date": date_key, "msg": "Day not valid for month"})

        if not isinstance(items, list):
            issues.append({"severity": "error", "type": "bad_entry_list", "date": date_key, "msg": "Expected list of holidays"})
            continue

        for idx, entry in enumerate(items):
            if not isinstance(entry, dict):
                issues.append({"severity": "error", "type": "bad_entry", "date": date_key, "index": idx, "msg": "Entry is not an object"})
                continue
            name = (entry.get("name") or "").strip()
            if not name:
                issues.append({"severity": "error", "type": "missing_name", "date": date_key, "index": idx, "msg": "Missing name"})
            else:
                dup_name_dates[name].append(date_key)

            desc = (entry.get("description") or "").strip()
            if not desc:
                issues.append({"severity": "warn", "type": "missing_description", "date": date_key, "index": idx, "msg": "Missing description"})
            elif len(desc) < 60:
                issues.append({"severity": "info", "type": "short_description", "date": date_key, "index": idx, "msg": "Description is short (<60 chars)"})

            facts = entry.get("funFacts")
            if not facts:
                issues.append({"severity": "warn", "type": "missing_fun_facts", "date": date_key, "index": idx, "msg": "No funFacts provided"})
            elif not isinstance(facts, list):
                issues.append({"severity": "warn", "type": "bad_fun_facts_type", "date": date_key, "index": idx, "msg": "funFacts is not a list"})
            elif len([f for f in facts if str(f).strip()]) < 2:
                issues.append({"severity": "info", "type": "few_fun_facts", "date": date_key, "index": idx, "msg": "Less than 2 fun facts"})

            slug = entry.get("slug") or slugify(name) if name else None
            if slug:
                slug_dates[slug].append(date_key)

            # Confidence heuristics
            conf = score_confidence(entry)
            date_conf = date_plausibility(mm, dd, entry)
            if conf["data_confidence"] < 0.5:
                issues.append({"severity": "info", "type": "low_confidence", "date": date_key, "index": idx, "msg": f"Data confidence {conf['data_confidence']}"})
            if date_conf < 0.4:
                issues.append({"severity": "info", "type": "low_date_confidence", "date": date_key, "index": idx, "msg": f"Date plausibility {date_conf}"})

    for name, dates in dup_name_dates.items():
        if len(set(dates)) > 1:
            issues.append({"severity": "warn", "type": "duplicate_name", "name": name, "dates": sorted(set(dates)), "msg": "Name appears on multiple dates"})

    for slug, dates in slug_dates.items():
        if len(set(dates)) > 1:
            issues.append({"severity": "warn", "type": "duplicate_slug", "slug": slug, "dates": sorted(set(dates)), "msg": "Slug appears on multiple dates"})

    return issues


def run_openai_checks(issues: List[Dict[str, Any]], holidays: Dict[str, Any], model: str, base_url: str, timeout: float, throttle: float):
    for date_key, items in holidays.items():
        if not isinstance(items, list):
            continue
        for idx, entry in enumerate(items):
            if not isinstance(entry, dict):
                continue
            entry = dict(entry)
            entry.setdefault("date", date_key)
            try:
                result = openai_score(entry, model, base_url, timeout)
            except Exception as exc:
                issues.append({"severity": "warn", "type": "openai_error", "date": date_key, "index": idx, "msg": str(exc)})
                continue
            legit = result.get("legitimacy", 0)
            date_match = result.get("date_match", 0)
            fact_conf = result.get("fact_confidence", 0)
            notes = result.get("notes") or []
            if legit < 0.6:
                issues.append({"severity": "warn", "type": "low_legitimacy_openai", "date": date_key, "index": idx, "score": legit, "notes": notes})
            if date_match < 0.6:
                issues.append({"severity": "warn", "type": "low_date_match_openai", "date": date_key, "index": idx, "score": date_match, "notes": notes})
            if fact_conf < 0.6:
                issues.append({"severity": "info", "type": "low_fact_conf_openai", "date": date_key, "index": idx, "score": fact_conf, "notes": notes})
            if throttle:
                time.sleep(throttle)


def main():
    parser = argparse.ArgumentParser(description="Validate holidays.json for structure and completeness.")
    parser.add_argument("--file", default="holidays.json", help="Path to holidays.json (default: holidays.json)")
    parser.add_argument("--json-out", help="Write full issue list to a JSON file")
    parser.add_argument("--openai", action="store_true", help="Run OpenAI fact/date checks (requires OPENAI_API_KEY)")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI model name (default: gpt-4o-mini)")
    parser.add_argument("--openai-base-url", default="https://api.openai.com/v1", help="OpenAI API base URL")
    parser.add_argument("--openai-timeout", type=float, default=30.0, help="OpenAI request timeout seconds")
    parser.add_argument("--openai-throttle", type=float, default=0.0, help="Sleep seconds between OpenAI calls")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or "holidays" not in raw:
        raise SystemExit("File does not contain top-level 'holidays' key")
    holidays = raw["holidays"]

    issues = validate(path)

    if args.openai:
        if "OPENAI_API_KEY" not in os.environ:
            raise SystemExit("OPENAI_API_KEY is required for --openai")
        print("Running OpenAI checks…")
        run_openai_checks(issues, holidays, args.model, args.openai_base_url, args.openai_timeout, args.openai_throttle)

    counts = Counter(issue["severity"] for issue in issues)

    print(f"Issues found: {len(issues)} (errors: {counts.get('error',0)}, warnings: {counts.get('warn',0)}, info: {counts.get('info',0)})")
    for issue in issues[:20]:
        loc = issue.get("date", "")
        idx = issue.get("index")
        suffix = f" idx={idx}" if idx is not None else ""
        print(f"- [{issue['severity']}] {issue['type']} @ {loc}{suffix}: {issue.get('msg','')}")
    if len(issues) > 20:
        print(f"...and {len(issues)-20} more")

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.write_text(json.dumps(issues, indent=2), encoding="utf-8")
        print(f"Wrote full issue list to {out_path}")


if __name__ == "__main__":
    main()
