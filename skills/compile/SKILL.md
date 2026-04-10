---
name: compile
description: Wiki Knowledge Compiler. Handles three modes: ingest (process raw/ files + maintain wiki), query (answer questions + optionally promote to topic pages), and fix (clean up WIKI_MAINTENANCE.md issues). Triggered manually.
---

# Curator Compile (Wiki Knowledge Compiler)

## Three Modes

Select via slash argument:
- `/curator:compile ingest` — Process new files in raw/ (**does NOT handle maintenance**)
- `/curator:compile query` — Answer questions against the Wiki, optionally promote to topic pages
- `/curator:compile fix` — Clean up issues from WIKI_MAINTENANCE.md

---

# MODE: fix

## Purpose
Process backlogged maintenance issues from WIKI_MAINTENANCE.md and clean up resolved entries.

## Prerequisites
1. `playground/wiki/WIKI_SCHEMA.md` — Wiki constraints and conventions
2. `playground/wiki/WIKI_MAINTENANCE.md` — Issue queue to fix

## Execution Mode (subagent)
Run up to **3 subagents** at a time, each handling **1 maintenance issue**.

## Methodology (mandatory)

Every maintenance issue follows a **Research -> Fix** two-phase approach:

1. **Research Phase**
   - Deep-dive into related page context
   - Understand the issue's position and connections across the wiki
   - Confirm the fix approach (merge/expand/correct/fill)
   - **FORBIDDEN to modify files before research is complete**

2. **Fix Phase**
   - Execute the fix based on research conclusions
   - Verify the issue is resolved

## Common Issue Types & Fixes

| Issue Type | Fix |
|-----------|-----|
| Contradiction | Add `> [!WARNING] Contradiction` block in related pages |
| Orphan page | Add wikilink to it from the most related existing page |
| Missing page | Create stub page or extract content from source file |
| Thin page | Merge into most related existing page, delete original |
| Empty Pointer | Extract content from source file to fill |
| Pointer format violation | Fix naming/directory/extension |
| Missing backlink | Add wikilink in source file's `## Related Wiki Pages` |

## Post-Fix Cleanup

After processing a batch, **MUST update WIKI_MAINTENANCE.md**:
1. Move fixed issues from the pending section to a "Fixed" section
2. Note the fix date and method
3. If all issues are fixed, clear the "Fixed" section (or keep the most recent record)

**FORBIDDEN**: Ending without cleaning up WIKI_MAINTENANCE.md — otherwise the next fix run will re-process already-fixed issues.

## Output
```
Wiki fix complete:
- Issues processed: X
- Fixed: Y (list issue types)
- Remaining: Z
- WIKI_MAINTENANCE.md updated
```

---

# MODE: ingest

## Purpose
Compile high-value source files into the Wiki by extracting entities, concepts, and data points.

**Note**: Maintenance issues (contradictions, orphans, missing pages, thin pages, empty pointers, format violations, missing backlinks) are ALL handled by `/curator:compile fix`. Ingest does NOT handle maintenance.

## Prerequisites (MUST read before every run)

Locate the `config/` sibling skill directory (same parent as this skill).

0. **Load config with overrides**: If `playground/curator-overrides.md` exists, its `## Topics` section overrides `config/topics.md`.
1. `playground/wiki/WIKI_SCHEMA.md` — Wiki constraints and conventions
2. `playground/wiki/log.md` — Check which files have already been processed
3. `playground/wiki/index.md` — Understand current wiki structure
4. `config/topics.md` — Wiki dimension directories
5. `config/templates/pointer-note.md` — Pointer note template

## Inputs
Scan `playground/wiki/raw/` for `.md` files **not appearing in log.md**.
- If no new files -> reply "Wiki raw/ has no new files" and end.
- If new files exist -> process per steps below.

## Execution Mode: Per-file processing (max 3 per run)

Process at most 3 new source files per invocation. If more than 3 new files, process the first 3 then stop and report the remainder.

FORBIDDEN:
- Processing more than 3 per run
- Creating Python/Shell scripts for batch processing
- Skipping reading and just extracting title keywords

---

## Processing Steps (for each new source file)

> **Key Principle**: Move the file first to determine its actual path, THEN create Wiki pages. Wiki `sources` always point to files in their classified directory (Obsidian wikilink), never to `raw/`.

### Step 1: Full Reading
Read the source file in full. Understand its core content.

### Step 2: Extract Wiki Elements
Identify from the article:
- **Entities**: Tool names (e.g., OpenClaw, Scrapling), people (e.g., Pieter Levels), companies
- **Concepts**: Methodologies (e.g., Build in Public), strategies (e.g., Reddit persona seeding), patterns
- **Data Points**: Specific numbers, comparisons, quotable lines

### Step 3: Determine Classification
Determine the file's primary and secondary classifications using the dimension directories from `config/topics.md`.
- Primary: Based on the file's core content, choose the most relevant dimension
- Secondary: If up to 2 strongly related dimensions exist, handle in Step 5

### Step 4: Move File to Primary Directory
`mv` the file from `raw/` to its primary dimension directory.

**This step MUST complete before Step 6** because Wiki `sources` need to point to the file's actual final path.

### Step 5: Create Pointer Notes (if secondary classifications exist)
If there are secondary classifications, create pointer notes in those directories.

Follow the template in `config/templates/pointer-note.md`.

### Step 6: Create Wiki Pages (pre-check required)

**Important rule**: For every source file, you MUST identify its entities/concepts/topics AND check whether corresponding Wiki pages already exist.

**Creating concept pages is MANDATORY**, not optional.

**Priority**: Entities -> Concepts -> Topics

For each identified entity/concept/topic:

**If page already exists:**
1. Read existing page content
2. Append new data under "Key Findings":
   ```
   - [YYYY-MM-DD] New finding (source: [[06_Productivity/filename]])
   ```
3. Check for contradictions with existing content. If found:
   ```
   > [!WARNING] Contradiction
   > Previously recorded X (source: [[old-category/file]]), but new source claims Y (source: [[new-category/file]])
   ```
4. Update frontmatter: `source_count` +1, append to `sources`, update `last_updated`
5. Update "Related Pages": add [[wikilinks]] to other relevant pages

**If page does not exist:**
1. Create new page with template:
   ```markdown
   ---
   source_count: 1
   sources:
     - "[[06_Productivity/filename]]"
   created: YYYY-MM-DD
   last_updated: YYYY-MM-DD
   tags: [tag1, tag2]
   ---

   # Page Title

   ## Core Definition
   One paragraph overview of this entity/concept/topic.

   ## Key Findings
   - [YYYY-MM-DD] Finding from article (source: [[06_Productivity/filename]])

   ## Related Pages
   - [[related-entity-or-concept]]
   ```
2. Page naming: lowercase, hyphen-separated, English (e.g., `build-in-public.md`)
3. Place in correct subdirectory:
   - Tools -> `entities/tools/`
   - People -> `entities/people/`
   - Companies/communities -> `entities/companies/`
   - Methodologies/strategies/patterns -> `concepts/`
   - Survey/overview -> `topics/`

### Step 7: Add Reverse Wikilinks (source file -> Wiki pages)
Append backlinks at the end of the classified source file:

```markdown
---

## Related Wiki Pages

- [[concepts/game-theory-daily-life]] — Game theory core concepts
- [[entities/people/reed-hastings]] — Reed Hastings page
- [[08_Self/source_name_pointer]] — *(dimension entry from 08_Self)*
```

**Atom Rules**:
- MUST append wikilinks pointing to Pointer files (dimension entries)
- When the same source is referenced by multiple Pointers, each link appears only once (deduplicate)
- This step forms **bidirectional connections**: Wiki page `sources` -> source file <- source file wikilink -> Wiki page

### Step 8: Update index.md
- Add new page entries under the appropriate category:
  ```
  - [[page-name]] — one-line summary
  ```
- Update footer stats: `Total pages: N | Last updated: YYYY-MM-DD`

---

## Extra Signals

If during ingest you notice an entity/concept page already has 3+ sources, append to log.md:
```
Suggestion: topics/ could benefit from a [[topic-name]] survey page
```

---

## Append to log.md

```markdown
## [YYYY-MM-DD] ingest | Source File Title
- Moved to: 06_Productivity/filename.md (from: raw/filename.md)
- Secondary: 03_Relations/ (pointer note)
- Pages created: N (list new page names)
- Pages updated: M (list updated page names)
```

---

## Output

```
Wiki ingest complete:
- Source files processed: N
- Pages created: X
- Pages updated: Y
```

---

# MODE: query

## Purpose
Answer natural language questions against the Wiki by synthesizing multiple pages. Valuable answers can be promoted to topic survey pages.

## Prerequisites (MUST read before every run)
1. `playground/wiki/WIKI_SCHEMA.md`
2. `playground/wiki/index.md`

## Flow

### Step 1: Understand the Question
Parse the user's natural language question. Determine which Wiki pages to search.

### Step 2: Search & Synthesize
Search relevant Wiki pages and synthesize an answer.

**Do NOT fabricate Wiki content.** Answers must come only from existing Wiki pages.

### Step 3: Promotion Decision
If the answer synthesized **3+ different Wiki pages** -> ask the user:
```
This answer draws from N Wiki pages. Promote it to a [[topic-name]] survey page?
- [Yes] -> proceed to Step 4
- [No] -> output the answer, done
```

If fewer than 3 sources -> output the answer directly, done.

### Step 4: Create Topic Page
Create a new page in `topics/` reusing the ingest page template:

```markdown
---
source_count: N
sources:
  - "[[06_Productivity/source-file]]"
  - "[[03_Relations/source-file]]"
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: [topic]
---

# Topic Name

## Overview
(LLM-synthesized answer)

## Perspectives
- [[page-a]]: ...
- [[page-b]]: ...

## Related Pages
- [[entity-page]]
- [[concept-page]]
```

### Step 5: Update index.md and log.md
- Add new page under Topics in index.md
- Append to log.md:
```markdown
## [YYYY-MM-DD] query | Question summary | Promoted to [[topic-name]]
```

---

## File Operation Rules

- All paths wrapped in double quotes
- `raw/` files are read-only before ingest starts; during ingest they are moved out via Step 4 (not edited in place in `raw/`)
- Wiki pages use write/edit tools, never rm+create
- FORBIDDEN: Creating Python/Shell scripts
