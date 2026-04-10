---
name: filter
description: The Unified Assessor & Router. Reads CURRENT_FOCUS.md, then processes raw Markdown files from 00_INBOX/ — grades them (Admiralty A1-F6), assigns action tags and project mappings for 01-grade articles, moves files into 01/02/03 by topic, and appends a batch report to the daily digest in 05_OUTBOX/.
---

# Curator Filter (Unified Assessor & Router)

## Purpose
Single-pass processing: Grade + Action Tag + Summary + Project Mapping + Routing + Digest — all in one read per article.

## Prerequisites (MUST read before every run)

Locate the `config/` sibling skill directory (same parent as this skill).

### Step 0a: Read CURRENT_FOCUS.md
Read `playground/CURRENT_FOCUS.md`.
- If file does not exist, STOP and ask the user to create it.
- Load active project list and watch signals into working memory.
- Note the "Not Currently Watching" list — matching articles auto-downgrade to `[ARCHIVE_ONLY]`.

### Step 0b: Determine today's digest file
Path: `playground/05_OUTBOX/YYYY-MM-DD_FILTER.md`
- If file already exists (previous batch ran today) -> append to it later.
- If file does not exist -> create it after processing this batch.

### Step 0c: Load System Learnings & Blacklist (CRITICAL)
Read these files to load cognitive bias corrections, and apply them during grading:
1. `playground/SOURCE_REPUTATION.md` — Remember blacklisted domains/authors. If the current article comes from one, immediately grade D/E and route to `03_NOISE`. No deep token consumption needed.
2. `playground/05_SYSTEM_LEARNINGS.md` — Remember human-corrected rules. These rules take **HIGHER PRIORITY** than default Admiralty grading criteria.

### Step 0d: Load grading & classification config
For each file below, check `playground/curator-config/` first; if not found, fall back to plugin `config/`:
1. `admiralty-system.md` — grading criteria + routing matrix + narrative override
2. `topics.md` — topic categories
3. `action-tags.md` — action tag definitions

## Inputs
Read `.md` files from `playground/00_INBOX/`.

You MUST actually read every `.md` file. Creating Python scripts for keyword filtering instead of reading is STRICTLY FORBIDDEN.

## Execution Mode: Paginated Processing (max 5 per batch)

1. `ls "playground/00_INBOX/" | head -5` to get the first 5 files
2. For each file, execute Steps 1-4 (below)
3. After processing the current 5, execute Step 5 (generate/append digest)
4. Report remaining count: "Processed 5/N articles, M remaining. Continue?"
5. If total INBOX files <= 5, process all then execute Step 5

FORBIDDEN:
- Processing more than 5 articles per batch
- Creating Python/Shell scripts for batch processing
- Using subagents to parallelize file processing

### Filename Handling
Filenames may contain Chinese, spaces, special characters. This is normal.

Rules:
- All file paths in bash commands MUST be wrapped in double quotes
- Use original filenames as-is, do not rename, escape, or script around them
- mv example: `mv "playground/00_INBOX/article title.md" "playground/01_PROJECTS_AND_RESOURCES/AI_Agents_Tech/"`

FORBIDDEN:
- Refusing to process files because of Chinese/special characters in filenames
- Creating Python scripts for file operations
- Using rm + recreate instead of mv

### Resumption
If interrupted (timeout, manual stop):
- Files already moved out of `00_INBOX/` are considered done
- Next run only processes remaining files in `00_INBOX/`
- No need to backtrack and check already-processed files

---

## Step 1: Deep Reading & Synthesis

**WARNING**: You are the Assessor, NOT the Summarizer. **NEVER** shrink, summarize, or truncate the original article content. The original Markdown text must remain **100% INTACT**.

Read the full article and understand its core arguments, data, and conclusions. **Do not grade it before understanding it.**

## Step 2: Evaluate & Classify

Based on your deep reading:
1. Determine the Admiralty A1-F6 grade (per `config/admiralty-system.md`)
2. Determine the destination folder (01/02/03) per the routing matrix
3. Determine the topic category (per `config/topics.md`)
4. **For 01/02-grade files only**: Determine action tag (per `config/action-tags.md`) and mapped project (from `CURRENT_FOCUS.md`)

## Step 3: Prepend Assessment Block

At the **very top** of the file (above YAML frontmatter), insert the assessment block.

- Follow the template `assessment-block.md` (check `playground/curator-templates/` first, fall back to `config/templates/`)
- For 01-grade files, also append `action-brief-01.md` (same override logic)
- For 02-grade files, also append `action-brief-02.md` (same override logic)

*(Use file editing tools to safely prepend. DO NOT delete existing content!)*

## Step 4: Move File

Ensure the target topic subfolder exists, then move:

```bash
mkdir -p "playground/01_PROJECTS_AND_RESOURCES/AI_Agents_Tech"
mv "playground/00_INBOX/filename.md" "playground/01_PROJECTS_AND_RESOURCES/AI_Agents_Tech/"
```

Do NOT use Python scripts, AI rewrite, or rm+create to move files. Always `mv`.

**D/E-grade files**: After moving to `03_NOISE`, record the domain strike in `playground/SOURCE_REPUTATION.md`.

## Step 5: Append Batch Report to Daily Digest

**CRITICAL REPORTING RULE**: Every physically moved file in this batch MUST appear in the report. The destination path in the report MUST exactly match the actual post-mv physical path and filename. If graded as D/E noise in the report, the file MUST physically be in `03_NOISE/`, never in the wrong folder.

Follow the template `daily-digest.md` (check `playground/curator-templates/` first, fall back to `config/templates/`).

---

## The Full Information Processing Loop

```
inbox.txt / URL
    |
/curator:intake (materialize)
    |
00_INBOX/ (raw)
    |
/curator:filter (read CURRENT_FOCUS.md -> single-pass:
    grade + action tag + summary + project mapping + routing + digest)
    |
01_PROJECTS_AND_RESOURCES/[topic]/  (A1-B3 high value, with ACTION BRIEF)
02_DEFER/[topic]/                   (C1-C3, F1-F2 hold)
03_NOISE/                           (D-F noise)
05_OUTBOX/YYYY-MM-DD_FILTER.md      (daily cumulative digest, append per batch)
    |
User reads digest -> decides actions
    | (optional) copy high-value files to wiki/raw/
    |
/curator:compile -> Obsidian Wiki knowledge weaving
```

## Common Mistakes to Avoid
- Missing reports: Moving a file (mv) but not recording it in the final report (most serious error).
- Path mismatch: Report file path doesn't match the actual physical path after mv.
- Action contradiction: Grading D/E and listing under NOISE, but physically mv-ing to `01_` high-value folder.
- Creating Python scripts for batch processing.
- Processing more than 5 per batch.
- Using rm + recreate instead of mv.
- Writing "article discusses XX" instead of specific facts in key findings.
- Writing "recommended reading" instead of concrete actions in next step.
- Using generic categories instead of exact project names from CURRENT_FOCUS.md.
- Empty parentheses `()` in the digest.
- Truncating or shrinking original article content.
