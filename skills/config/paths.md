# Paths Configuration

> All curator skills MUST use these paths. Never hardcode absolute paths in SKILL.md files.
> All paths are relative to the project root (the working directory when Claude Code runs).

## Core Directories

| Variable | Path | Purpose |
|----------|------|---------|
| `PLAYGROUND` | `playground/` | Root of the curation workspace |
| `INBOX` | `playground/00_INBOX/` | Raw downloaded articles awaiting filter |
| `PROJECTS` | `playground/01_PROJECTS_AND_RESOURCES/` | High-value articles (A1-B3) |
| `DEFER` | `playground/02_DEFER/` | Held articles (C1-C3, F1-F2) |
| `NOISE` | `playground/03_NOISE/` | Discarded articles (D-F noise) |
| `OUTBOX` | `playground/05_OUTBOX/` | Daily digest reports |

## Configuration Files

| Variable | Path | Purpose |
|----------|------|---------|
| `CURRENT_FOCUS` | `playground/CURRENT_FOCUS.md` | Active projects + signals + ignore list |
| `SOURCE_REPUTATION` | `playground/SOURCE_REPUTATION.md` | Domain reputation ledger (strikes + blacklist) |
| `SYSTEM_LEARNINGS` | `playground/05_SYSTEM_LEARNINGS.md` | Human-corrected filtering rules |
| `SUPERVISOR_FEEDBACK` | `playground/04_SUPERVISOR_FEEDBACK.md` | Explicit human feedback table |
| `INBOX_FILE` | `playground/inbox.txt` | URL list for intake |

## Wiki Directories

| Variable | Path | Purpose |
|----------|------|---------|
| `WIKI_ROOT` | `playground/wiki/` | Obsidian wiki vault root |
| `WIKI_RAW` | `playground/wiki/raw/` | New source files for compile ingest |
| `WIKI_SCHEMA` | `playground/wiki/WIKI_SCHEMA.md` | Wiki structure rules |
| `WIKI_MAINTENANCE` | `playground/wiki/WIKI_MAINTENANCE.md` | Lint issue queue |
| `WIKI_INDEX` | `playground/wiki/index.md` | Wiki page directory |
| `WIKI_LOG` | `playground/wiki/log.md` | Operation log (append-only) |

## Script Paths

| Variable | Path | Purpose |
|----------|------|---------|
| `FEEDBACK_SCRIPT` | `.claude/skills/curator-feedback-loop/track_feedback.py` | File movement detector |
| `FETCH_SCRIPT` | `.claude/skills/web-content-fetcher/scripts/fetch.py` | Web content fetcher |
