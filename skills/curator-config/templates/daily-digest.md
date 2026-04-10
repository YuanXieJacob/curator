# Daily Digest Template

## File Path

`playground/05_OUTBOX/YYYY-MM-DD_FILTER.md`

## Header (first batch of the day — create file)

```markdown
# Daily Intelligence Briefing (YYYY-MM-DD)

> Curator Filter | Based on CURRENT_FOCUS.md (YYYY-MM-DD)
```

## Batch Report (append for each batch)

```markdown

---

## Batch HH:MM (This batch: X | Cumulative: Y/Z)

### HIGH VALUE

#### [Action Tag] Article Title
- **Grade**: B2 | **Topic**: AI_Agents_Tech | **Mapped Project**: [project name]
- **Key Findings**:
  - Specific fact 1
  - Specific fact 2
  - Specific fact 3
- **Next Step**: One concrete action
- 01_PROJECTS_AND_RESOURCES/AI_Agents_Tech/filename.md

(repeat for each HIGH VALUE article)

### HOLD

- **[Action Tag]** Article Title | Grade | Topic | 02_DEFER/[topic]/filename.md

(repeat for each HOLD article, compact format)

### NOISE (Discarded)

- ~~Article Title~~ | Grade | 03_NOISE/filename.md
```

## Section Rules

**HIGH VALUE** — 01-grade files (A1-A3, B1-B3) mapped to active projects in CURRENT_FOCUS.md:
- Must have action tag + 3-bullet key findings + next step
- Key findings must be **specific facts**, not "article discusses XX"

**HOLD** — 02-grade files (C1-C3, F1-F2), compact format, one line per article

**NOISE** — 03-grade files, strikethrough title, exists only so the user can verify no false negatives

## Content Rules

1. **Key findings must be specific**: Extract actual facts, numbers, names, quotes. NOT "article discusses AI trends"
2. **Next step must be actionable**: "Test Scrapling to replace agent-browser" is good. "Recommended reading" is bad.
3. **Mapped project must reference CURRENT_FOCUS.md**: Use exact project names. If no match, downgrade to HOLD.
4. **File paths must be correct**: Point to actual post-mv location.
5. **No empty parentheses `()`**
