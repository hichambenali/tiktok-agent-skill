#!/usr/bin/env python3
"""Rank YOUR OWN TikTok videos from a CSV exported from TikTok Studio.

Usage:
  python3 analyze.py videos.csv --name "Video title" --views "Views" \
      [--watch "Average watch time"] [--formula "Hook formula"]

Ranks by views as a multiple of YOUR median. If a formula column is given,
shows median multiple per formula. Column names must match the CSV headers.
"""
import argparse
import csv
import statistics as st


def num(x):
    try:
        return float(str(x).replace(",", "").replace("%", "").strip())
    except (ValueError, AttributeError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--name", required=True)
    ap.add_argument("--views", required=True)
    ap.add_argument("--watch")
    ap.add_argument("--formula")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.csv, encoding="utf-8-sig")))
    data = []
    for r in rows:
        v = num(r.get(a.views))
        if v is None:
            continue
        data.append({
            "name": (r.get(a.name) or "")[:60],
            "views": v,
            "watch": num(r.get(a.watch)) if a.watch else None,
            "formula": (r.get(a.formula) or "unlabeled").strip() if a.formula else None,
        })
    if not data:
        print("No rows parsed. Check the column names against the CSV headers.")
        return

    med = st.median(d["views"] for d in data)
    for d in data:
        d["mult"] = d["views"] / med if med else 0
    data.sort(key=lambda d: -d["mult"])

    print(f"VIDEOS: {len(data)} · your median views: {med:,.0f}")
    print("=" * 78)
    for d in data:
        w = f"{d['watch']:.0f}" if d["watch"] is not None else "-"
        print(f"{d['mult']:6.2f}x  {d['views']:>10,.0f}  watch {w:>5}  {d['name']}")

    if a.formula:
        groups = {}
        for d in data:
            groups.setdefault(d["formula"], []).append(d)
        print("\nBY FORMULA (median multiple)")
        ordered = sorted(groups.items(), key=lambda kv: -st.median(x["mult"] for x in kv[1]))
        for f, g in ordered:
            print(f"{st.median(x['mult'] for x in g):6.2f}x  n={len(g):<3} {f}")

    print("\nGroups with fewer than 5 videos are noise, not findings.")


if __name__ == "__main__":
    main()
