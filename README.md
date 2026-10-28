# TikTok agent skill

A Claude skill for writing, timing, and analyzing TikTok videos. Works in Arabic (including dialects) and English.

## Install (Claude Code)
    cp -r tiktok-agent-skill ~/.claude/skills/

Then fill in `templates/voice.md`.

## What it does
- Writes a full video: hook, beats, payoff, and loop
- Scores hooks and times scripts locally, with no network calls
- Lints captions for the preview and hashtags
- Ranks your own videos from a TikTok Studio CSV export

## What it does not do
- It does not post, comment, follow, or DM for you.
- It does not scrape TikTok or other accounts.
- Hook scoring is heuristic. It catches weak hooks but does not predict which good hook will win.
