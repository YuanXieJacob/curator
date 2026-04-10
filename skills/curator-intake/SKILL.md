---
name: curator-intake
description: The Situation Monitor. Reads incoming URLs from inbox.txt or raw links, checks them against the SOURCE_REPUTATION blacklist, and downloads full text into 00_INBOX/ as Markdown files using web-content-fetcher or agent-browser.
---

# Curator Intake (The Loader)

## Purpose
Convert fragile, volatile web URLs into solid, permanent local Markdown files for offline processing. Act as the first line of defense against known garbage domains.

## Prerequisites

Locate the `curator-config/` sibling skill directory (same parent as this skill), then read:
1. `curator-config/paths.md` — resolve all directory paths
2. `playground/SOURCE_REPUTATION.md` — load the Blacklist

## Inputs
1. A text file with URLs (see `INBOX_FILE` in paths.md), or `experiment.md`, or raw URLs from the user.

## Processing Rules

1. **Blacklist Check**: For every URL, extract its root domain. If the domain is listed under the `Blacklist` section in `SOURCE_REPUTATION.md`, IMMEDIATELY SKIP it. Do not download.

2. **Download Execution**: Use the local `web-content-fetcher` skill to extract the full readable content. **CRITICAL**: If the fast script fails due to anti-scraping, you MUST follow its fallback chain and use `agent-browser` to render the page and extract the text before giving up.

3. **Save Format**: Save the clean markdown content to:
   `playground/00_INBOX/YYYYMMDD_<Title>.md`
   *(Replace YYYYMMDD with today's date, and `<Title>` with a short, sanitized English/pinyin version of the article title).*

4. **File Template**: Follow the template `inbox-file.md` (check `playground/curator-templates/` first, fall back to `curator-config/templates/`).

## Completion
Once all URLs are downloaded to `00_INBOX/`, delete the processed URLs from `inbox.txt` so they are not fetched twice.

## Error Handling
If a URL is blocked (e.g., 403 Forbidden, CAPTCHA, login wall), do not crash. Save an error placeholder in `00_INBOX/` with `status: BLOCKED` so it can be handled or manually reviewed later.
