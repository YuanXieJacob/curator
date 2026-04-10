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
/plugin marketplace add YuanXieJacob/curator
/plugin install curator@YuanXieJacob-curator
```

Then initialize your workspace:
```
/curator:init
```

## Configuration

The plugin works **out of the box** with sensible defaults. All customization is optional.

### Plugin Defaults (in `skills/config/`)

| File | What It Controls |
|------|-----------------|
| `topics.md` | Topic categories for filtering + Wiki dimension directories |
| `action-tags.md` | Action labels assigned to high-value articles |
| `admiralty-system.md` | Grading criteria (rarely needs changing) |
| `paths.md` | Directory structure (only if you rename folders) |
| `templates/` | Assessment blocks, digest format, pointer notes |

### User Overrides (optional, survive plugin updates)

To customize any config, copy it to your project and edit:

```bash
# Override topics
cp <plugin>/skills/config/topics.md playground/curator-config/topics.md

# Override a template
cp <plugin>/skills/config/templates/daily-digest.md playground/curator-templates/daily-digest.md
```

| Override Location | Overrides |
|------------------|-----------|
| `playground/curator-config/<file>.md` | `skills/config/<file>.md` |
| `playground/curator-templates/<file>.md` | `skills/config/templates/<file>.md` |

Rule: **file exists → use it. Missing → use plugin default.**

### User Data (accumulated, never touched by plugin updates)

| File | Purpose |
|------|---------|
| `playground/CURRENT_FOCUS.md` | Your active projects & watch signals (drives filtering) |
| `playground/SOURCE_REPUTATION.md` | Auto-maintained domain reputation ledger |
| `playground/05_SYSTEM_LEARNINGS.md` | Rules learned from your corrections |
| `playground/04_SUPERVISOR_FEEDBACK.md` | Quick correction table |
| `playground/wiki/` | Your Obsidian knowledge base |

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

> **Only `curator:intake` needs these.** All other skills (filter, compile, lint, feedback-loop) work without any external dependencies.

### 1. web-content-fetcher (primary URL downloader)

```bash
# Install the skill
npx skills add https://github.com/shirenchuang/web-content-fetcher --skill web-content-fetcher

# Install its Python dependencies
pip install scrapling html2text
```

### 2. agent-browser (fallback for JS-heavy / anti-scraping sites)

```bash
# Install the CLI tool
npm install -g agent-browser

# Download a browser for automation (auto-detects existing Chrome/Brave)
agent-browser install
```

`agent-browser` is optional — `web-content-fetcher` handles most sites. Only needed when a site blocks the primary fetcher (heavy JS rendering, CAPTCHAs, etc.).

## License

MIT
