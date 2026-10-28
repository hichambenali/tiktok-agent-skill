#!/usr/bin/env python3
"""Lint a TikTok caption. Usage: python3 caption.py caption.txt"""
import re
import sys

HASH = re.compile(r"#[\w\u0600-\u06FF]+")
GENERIC = ["follow for more", "like and share", "tag a friend", "تابع للمزيد", "لايك وشير", "شير"]
CTA = re.compile(r"\b(comment|follow|share|save|link|تعليق|علّق|علق|تابع|شارك|احفظ)\b|[?؟]", re.IGNORECASE)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    text = open(sys.argv[1], encoding="utf-8").read().strip()
    tags = HASH.findall(text)
    body = HASH.sub("", text).strip()
    first_line = body.split("\n")[0].strip()
    ctas = CTA.findall(body)
    generic = [g for g in GENERIC if g in body.lower()]

    checks = [
        ("LENGTH", len(text) <= 2200, f"{len(text)} / 2200 characters"),
        ("FIRST LINE", 0 < len(first_line) <= 80,
         f"{len(first_line)} chars: {first_line[:60]!r}. Keep it under 80 so it reads alone in the preview."),
        ("HASHTAGS", 3 <= len(tags) <= 5, f"{len(tags)} found. Aim for 3 to 5 relevant ones."),
        ("CALL TO ACTION", len(ctas) <= 2, f"{len(ctas)} asks found. Keep it to one or two."),
        ("GENERIC PHRASES", not generic, "none" if not generic else f"found: {', '.join(generic)}"),
    ]
    print("CAPTION CHECK")
    print("=" * 72)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'WARN'}  {name:<16} {detail}")


if __name__ == "__main__":
    main()
