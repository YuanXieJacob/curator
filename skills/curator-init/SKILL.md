---
name: curator-init
description: Initialize the Curator workspace. Creates the playground/ directory structure, configuration files, and wiki scaffold. Run this once when setting up a new project.
---

# Curator Init (Workspace Setup)

## Purpose
One-time setup to create the full Curator workspace in the current project directory.

## What It Creates

```
playground/
├── 00_INBOX/                          # Downloaded articles land here
├── 01_PROJECTS_AND_RESOURCES/         # High-value articles (A1-B3)
├── 02_DEFER/                          # Held articles (C1-C3, F1-F2)
├── 03_NOISE/                          # Discarded articles
├── 05_OUTBOX/                         # Daily digest reports
├── inbox.txt                          # URL list for intake
├── CURRENT_FOCUS.md                   # User's active projects & signals
├── SOURCE_REPUTATION.md               # Domain reputation ledger
├── 04_SUPERVISOR_FEEDBACK.md          # Human feedback table
├── 05_SYSTEM_LEARNINGS.md             # Learned filtering rules
└── wiki/
    ├── raw/                           # Drop source files here for compile
    ├── entities/tools/
    ├── entities/people/
    ├── entities/companies/
    ├── concepts/
    ├── topics/
    ├── index.md
    ├── log.md
    ├── WIKI_SCHEMA.md
    └── WIKI_MAINTENANCE.md
```

## Execution Steps

### Step 1: Check if already initialized
If `playground/` exists and contains `CURRENT_FOCUS.md`, warn the user:
```
Curator workspace already exists at playground/. Re-initializing will overwrite config files.
Continue? [y/N]
```

### Step 2: Create directories
```bash
mkdir -p playground/{00_INBOX,01_PROJECTS_AND_RESOURCES,02_DEFER,03_NOISE,05_OUTBOX}
mkdir -p playground/wiki/{raw,entities/tools,entities/people,entities/companies,concepts,topics}
mkdir -p playground/curator-config
mkdir -p playground/curator-templates
```

### Step 3: Create configuration files

Locate the `curator-config/` sibling skill directory, then read the templates directory at the plugin root (`../templates/` relative to the skills directory). Use those templates to create the config files.

If templates are not found, create the files with these defaults:

**playground/CURRENT_FOCUS.md:**
```markdown
# Current Focus
> Last updated: YYYY-MM-DD

## Active Projects

### Project Name
- Description of what you're working on

## Watch Signals
- Topics and patterns to prioritize in filtering

## Not Currently Watching
- Topics to auto-downgrade during filtering
```

**playground/SOURCE_REPUTATION.md:**
```markdown
# Source Reputation Ledger

This ledger is automatically maintained by `curator:feedback-loop`. When a website/author accumulates 3 D or E grade ratings during filtering, its identifier is added to the Blacklist.

## Strikes (Under Observation)
| Domain/Author | Strikes | Last Flagged Reason | Related Article |
|---|---|---|---|

## Blacklist (Permanently Blocked)
| Domain/Author | Blocked Date | Reason |
|---|---|---|
```

**playground/04_SUPERVISOR_FEEDBACK.md:**
```markdown
# Supervisor Quick Feedback

Leave brief correction instructions here. The feedback loop scans this table during each run.

| File / Keyword | Location | Feedback Type | Correction | Status |
|---|---|---|---|---|

## Implicit Movement Feedback
Move files physically to let the AI learn:
- Rescue from trash: Drag from 03_NOISE to 01 or 02
- Demote to trash: Drag from 01 or 02 into 03_NOISE
- Wiki promotion: Copy/move any file to playground/wiki/raw/
```

**playground/05_SYSTEM_LEARNINGS.md:**
```markdown
# System Learnings (Cognitive Calibration Rules)

> Automatically maintained by the feedback loop.
> The filter MUST read and obey these rules before grading. Higher priority than default Admiralty criteria.

## Rules

(no entries yet)
```

**playground/wiki/WIKI_SCHEMA.md:**
Read the template from the plugin's templates directory. If not found, create a minimal version with the core rules from `curator-config/topics.md`.

**playground/wiki/index.md:**
```markdown
# Wiki Index

## Entities
### Tools
### People
### Companies

## Concepts

## Topics

---
Total pages: 0 | Last updated: YYYY-MM-DD
```

**playground/wiki/log.md:**
```markdown
# Wiki Operation Log

## [YYYY-MM-DD] init | Workspace initialized
```

**playground/wiki/WIKI_MAINTENANCE.md:**
```markdown
# Wiki Maintenance Queue

> Issues discovered by `/curator:lint`, consumed by `/curator:compile fix`.

## Pending

(no issues)

## Fixed

(no history)
```

**playground/inbox.txt:**
```
# Paste URLs here, one per line. Run /curator:intake to download them.
```

### Step 4: Report
```
Curator workspace initialized at playground/

Next steps:
1. Edit playground/CURRENT_FOCUS.md with your active projects and watch signals
2. Paste URLs into playground/inbox.txt
3. Run /curator:intake to download articles
4. Run /curator:filter to grade and route them

Customization (optional):
- To override topics: copy curator-config/topics.md to playground/curator-config/topics.md and edit
- To override templates: copy any file from curator-config/templates/ to playground/curator-templates/ and edit
- Your overrides survive plugin updates. Plugin defaults are used for anything not overridden.

Dependencies (install separately):
- web-content-fetcher skill (for intake URL downloading)
- agent-browser skill (for JS-heavy sites, optional fallback)
```
