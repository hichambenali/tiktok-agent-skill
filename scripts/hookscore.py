#!/usr/bin/env python3
"""Score TikTok hook lines (first ~3 seconds). Local heuristics, no network.

Usage: python3 hookscore.py hooks.txt   (one hook per line)
"""
import re
import sys

GREETINGS = [
    "hey guys", "hey everyone", "hi guys", "welcome back", "what's up", "so today",
    "today i", "in this video", "in this tiktok",
    "السلام عليكم", "مرحبا", "مرحبًا", "أهلا", "اهلا", "يا جماعة", "في هذا الفيديو",
    "اليوم راح", "اليوم نتكلم", "خليني نقولك",
]
BEGGING = ["stop scrolling", "don't skip", "wait for it", "لا تسكرول", "ما تسكروش", "استنى"]
CURIOSITY = [
    "nobody", "secret", "mistake", "wrong", "lied", "never", "truth", "why", "how",
    "محد", "ما حد", "سر", "غلطة", "غلطه", "كذبة", "الحقيقة", "ليش", "كيف",
    "ما قالولك", "ما تعرفهاش",
]
ADDRESS_WORDS = ["you", "your", "انت", "أنت", "إنت", "انتي", "انتِ", "إنتي", "عندك", "تعرف"]


def _kw(words):
    # word-boundary match; \w includes Arabic letters in Python 3
    return re.compile(r"(?<!\w)(" + "|".join(map(re.escape, words)) + r")(?!\w)", re.IGNORECASE)


RX_BEG = _kw(BEGGING)
RX_CURIOUS = _kw(CURIOSITY)
RX_ADDRESS = _kw(ADDRESS_WORDS)
RX_CONCRETE = re.compile(r"\d|\$|%|€|دج|دينار|درهم|دولار|يورو|يوم|شهر|سنة|ساعة")
RX_QUESTION = re.compile(r"[?؟]")


def score(line):
    text = line.strip()
    low = text.lower()
    words = text.split()
    if not words:
        return 0, ["empty line"], "WEAK"
    notes, pts = [], 50

    if len(words) <= 12:
        pts += 15
        notes.append("short enough for 1-3 seconds")
    elif len(words) > 18:
        pts -= 15
        notes.append("too long for the first 3 seconds")

    if any(low[:40].startswith(g) for g in GREETINGS):
        pts -= 25
        notes.append("greeting or preamble: viewers scroll past these")
    if RX_BEG.search(text):
        pts -= 10
        notes.append("asks for attention instead of earning it")
    if RX_CONCRETE.search(text):
        pts += 15
        notes.append("concrete number or unit")
    if RX_CURIOUS.search(text):
        pts += 10
        notes.append("curiosity gap")
    if RX_ADDRESS.search(text):
        pts += 10
        notes.append("speaks to the viewer directly")
    if RX_QUESTION.search(text):
        pts += 5
        notes.append("question opens a loop")

    pts = max(0, min(100, pts))
    band = "STRONG" if pts >= 70 else "OK" if pts >= 50 else "WEAK"
    return pts, notes, band


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    lines = [l for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    rows = sorted((score(l) + (l.strip(),) for l in lines), key=lambda r: -r[0])
    print("HOOK RANKING")
    print("=" * 72)
    for pts, notes, band, text in rows:
        print(f"{pts:>4}  {band:<6}  {text[:90]}")
        for n in notes:
            print(f"        - {n}")


if __name__ == "__main__":
    main()
