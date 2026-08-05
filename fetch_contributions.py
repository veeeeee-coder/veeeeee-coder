#!/usr/bin/env python3
import json, re, sys
from datetime import datetime
import requests

USERNAME = "veeeeee-coder"
URL = f"https://github.com/users/{USERNAME}/contributions"

def main():
    resp = requests.get(URL, timeout=30)
    resp.raise_for_status()
    days = []
    for m in re.finditer(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d+)"[^>]*>([^<]*)</td>', resp.text):
        date_str, level_str, text = m.groups()
        level = int(level_str)
        count = 0
        if text.strip():
            n = re.match(r"(\d+)", text.strip())
            if n: count = int(n.group(1))
        days.append({"date": date_str, "count": count, "level": level})

    days.sort(key=lambda d: d["date"])
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"])

    cur_streak = longest = streak = 0
    for d in days:
        if d["count"] > 0:
            streak += 1
            longest = max(longest, streak)
        else:
            streak = 0
    for d in reversed(days):
        if d["count"] > 0: cur_streak += 1
        else: break

    monthly = {}
    for d in days:
        m = d["date"][:7]
        monthly[m] = monthly.get(m, 0) + d["count"]

    with open("data/contributions.json", "w") as f:
        json.dump({
            "username": USERNAME,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "total": total, "best_day": best,
            "current_streak": cur_streak, "longest_streak": longest,
            "monthly_totals": monthly, "days": days
        }, f, indent=2)
    print(f"Saved {len(days)} days, total {total}")

if __name__ == "__main__":
    main()
