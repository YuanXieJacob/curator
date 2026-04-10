# Curator — LLM Content Curation Pipeline

A Claude Code plugin that turns your LLM into a professional content curator. Inspired by [Karpathy's LLM Wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), Curator goes further — it handles the entire pipeline from raw URL intake to graded routing to Obsidian wiki compilation, with a human-in-the-loop feedback system that learns from your corrections.

## The Pipeline

```
URLs / inbox.txt
    |
/curator:intake          Fetch & materialize URLs as local Markdown
    |
00_INBOX/                Raw downloaded articles
    |
/curator:filter          Grade (Admiralty A1-F6) + route + daily digest
    |
01_PROJECTS/[topic]/     High-value (A1-B3, with action briefs)
02_DEFER/[topic]/        Hold (C1-C3, F1-F2)
03_NOISE/                Discard (D-F noise)
05_OUTBOX/digest.md      Daily briefing report
    |
User reads digest        Drag-and-drop to correct AI mistakes
    |
/curator:feedback-loop   Learn from corrections (strikes, rules)
    |
/curator:compile ingest  Weave into Obsidian wiki (entities, concepts, topics)
    |
/curator:lint            Periodic wiki health scan
    |
/curator:compile fix     Fix issues found by lint
```

## Skills Included

| Skill | Command | Purpose |
|-------|---------|---------|
| **init** | `/curator:init` | One-time workspace setup |
| **config** | *(not invoked directly)* | Shared configuration hub |
| **intake** | `/curator:intake` | Download URLs to local Markdown |
| **filter** | `/curator:filter` | Grade, classify, route articles |
| **compile** | `/curator:compile [ingest\|query\|fix]` | Wiki knowledge compilation |
| **lint** | `/curator:lint` | Wiki health inspection |
| **feedback-loop** | `/curator:feedback-loop` | Learn from human corrections |

## Installation

```
/plugin marketplace add YuanXieJacob/curator-plugin
/plugin install curator@YuanXieJacob-curator-plugin
```

Then initialize your workspace:
```
/curator:init
```

## Configuration

All configuration lives in `skills/config/`:

| File | What to Customize |
|------|-------------------|
| `topics.md` | Topic categories for filtering + Wiki dimension directories |
| `action-tags.md` | Action labels assigned to high-value articles |
| `admiralty-system.md` | Grading criteria (rarely needs changing) |
| `paths.md` | Directory structure (only if you rename folders) |
| `templates/` | Assessment blocks, digest format, pointer notes |

Your personal settings live in `playground/`:

| File | Purpose |
|------|---------|
| `CURRENT_FOCUS.md` | Your active projects & watch signals (drives filtering) |
| `SOURCE_REPUTATION.md` | Auto-maintained domain reputation ledger |
| `05_SYSTEM_LEARNINGS.md` | Rules learned from your corrections |
| `04_SUPERVISOR_FEEDBACK.md` | Quick correction table |

## Key Features

### Admiralty Grading System
Two-axis evaluation: Source Reliability (A-F) x Information Credibility (1-6). Articles are routed to 01/02/03 folders based on their composite grade.

### Human-in-the-Loop Learning
The system learns from your corrections in two ways:
- **Explicit**: Fill in the feedback table
- **Implicit**: Just drag files between folders. Moved from noise to projects? The AI learns it was wrong.

### Obsidian Wiki Compilation
High-value articles are compiled into a structured wiki with entities, concepts, topics, and bidirectional wikilinks. Pointer notes enable cross-dimensional access.

### Wiki Health Maintenance
Periodic lint scans detect contradictions, orphan pages, missing pages, thin pages, and broken pointers. Compile fix mode resolves them.

## Dependencies

These skills are used by `curator:intake` but not bundled:
- **web-content-fetcher** — Primary URL downloading (Scrapling-based)
- **agent-browser** — Fallback for JS-heavy / anti-scraping sites

Install them separately if you want full intake functionality.

## License

MIT
