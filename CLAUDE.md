# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Curator is a **Claude Code plugin** (not a standalone app) that implements an LLM-powered content curation pipeline. It works as a set of skills that process web content through: intake -> filter -> compile -> lint, with a human-in-the-loop feedback system.

The plugin is distributed via the `.claude-plugin/` directory and installed into Claude Code with `/plugin marketplace add`.

## Architecture

### Skill-Based Design

Each pipeline stage is a self-contained skill defined in `skills/curator-<name>/SKILL.md`. Skills are markdown-based instructions (no traditional code), except for `curator-feedback-loop` which includes a Python script.

**Pipeline order:**
1. `curator-init` — One-time workspace setup (`playground/` directory tree)
2. `curator-intake` — Downloads URLs from `inbox.txt` to `00_INBOX/` as markdown. **Only skill with external dependencies** (see below)
3. `curator-filter` — Grades articles using Admiralty system (A1-F6), routes to `01_PROJECTS/`, `02_DEFER/`, or `03_NOISE/`, generates daily digest in `05_OUTBOX/`
4. `curator-feedback-loop` — Detects user file movements (implicit feedback) and reads explicit feedback table, updates `SOURCE_REPUTATION.md` and `05_SYSTEM_LEARNINGS.md`
5. `curator-compile` — Three modes: `ingest` (raw files -> wiki pages), `query` (search wiki), `fix` (resolve maintenance issues)
6. `curator-lint` — Read-only wiki health scan, writes issues to `WIKI_MAINTENANCE.md`

### Config Override System

Skills resolve config by checking user overrides first, then falling back to plugin defaults:
- Config: `playground/curator-config/<file>.md` overrides `skills/curator-config/<file>.md`
- Templates: `playground/curator-templates/<file>.md` overrides `skills/curator-config/templates/<file>.md`

All skills must implement this resolution pattern. User overrides survive plugin updates; plugin defaults do not.

### Key Config Files (in `skills/curator-config/`)

- `paths.md` — Canonical path variables for all directories. All skills reference this; never hardcode paths
- `topics.md` — Filter topic categories AND wiki dimension directories (dual purpose)
- `admiralty-system.md` — Two-axis grading system (Source Reliability A-F x Information Credibility 1-6) with routing matrix
- `action-tags.md` — Actionable labels for high-value articles
- `templates/` — Markdown templates for assessment blocks, digests, inbox files, pointer notes

### User Data (in `playground/`)

- `CURRENT_FOCUS.md` — Drives filtering decisions; filter skill requires this to exist
- `SOURCE_REPUTATION.md` — Domain strikes and blacklist; intake checks blacklist, filter adds strikes
- `05_SYSTEM_LEARNINGS.md` — Human-corrected rules that override default Admiralty grading
- `04_SUPERVISOR_FEEDBACK.md` — Explicit feedback table processed by feedback-loop

### External Dependencies (intake only)

All skills except `intake` are fully self-contained. Intake requires:

- **[web-content-fetcher](https://github.com/shirenchuang/web-content-fetcher)** — Primary URL downloader (Claude Code skill). Requires Python packages: `scrapling`, `html2text`
- **[agent-browser](https://github.com/vercel-labs/agent-browser)** — Optional fallback for JS-heavy/anti-scraping sites (standalone CLI tool, `npm install -g agent-browser`). Only needed when web-content-fetcher fails

### The Only Python Code

`skills/curator-feedback-loop/track_feedback.py` — Detects file movements by comparing assessment block destinations against actual file locations. Run from project root. Max 5 anomalies per run. This script should not be modified by skill consumers.

## Development Notes

- This is a plugin repo, not an application. There is no build system, test suite, or package manager
- Skills are pure markdown instructions executed by Claude Code at runtime
- To test changes to a skill, use the corresponding `/curator:<skill>` command in a project that has been initialized with `/curator:init`
- The filter skill processes max 5 articles per batch; compile ingest processes max 3 per run. These are deliberate constraints to manage token usage
- Filter explicitly forbids: Python/shell scripts for batch processing, subagents for parallelization, processing more than 5 per batch
- All file operations must use `mv` for moves (never rm+create), and all paths must be double-quoted (filenames may contain Chinese characters and spaces)
