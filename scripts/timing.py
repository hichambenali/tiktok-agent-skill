#!/usr/bin/env python3
"""Estimate timing of a TikTok script. One spoken beat per line.

Usage: python3 timing.py script.txt [--target 30] [--wpm 150]
"""
import argparse
import re

STOP = set(
    "the a an and or of to in is it i you that this for on with be as at by "
    "و في من على إلى عن أن إن هذا هذه هو هي لا ما ان".split()
)


def sig_words(text):
    out = set()
    for w in text.split():
        w = re.sub(r"[^\w]", "", w).lower()
        if len(w) > 2 and w not in STOP:
            out.add(w)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--target", type=float, default=30)
    ap.add_argument("--wpm", type=float, default=150)
    a = ap.parse_args()

    beats = [l.strip() for l in open(a.file, encoding="utf-8") if l.strip()]
    if not beats:
        print("No beats found.")
        return

    t, rows = 0.0, []
    for b in beats:
        d = len(b.split()) / a.wpm * 60 + 0.3  # 0.3s pause between beats
        rows.append((t, d, b))
        t += d

    print(f"BEAT SHEET · {len(beats)} beats · ~{t:.1f}s at {a.wpm:.0f} wpm · target {a.target:.0f}s")
    print("=" * 74)
    for i, (start, d, b) in enumerate(rows):
        tag = "HOOK" if i == 0 else ""
        print(f"{start:6.1f}s  {d:4.1f}s  {tag:<5} {b[:70]}")
    print("-" * 74)

    issues = []
    if rows[0][1] > 3:
        issues.append(f"Hook takes {rows[0][1]:.1f}s. Cut it to about 3s or less.")
    for i, (s, d, b) in enumerate(rows[1:], 1):
        if d > 4:
            issues.append(f"Beat {i + 1} runs {d:.1f}s. Split it or change the visual inside it.")
    if len(beats) > 1 and not (sig_words(beats[0]) & sig_words(beats[-1])):
        issues.append("No loop: the last line does not echo the hook. A loop lifts rewatches.")
    diff = t - a.target
    if abs(diff) > 3:
        issues.append(f"{abs(diff):.1f}s {'over' if diff > 0 else 'under'} target.")

    if issues:
        for x in issues:
            print("  - " + x)
    else:
        print("  No timing issues found.")


if __name__ == "__main__":
    main()
