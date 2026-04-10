---
name: lint
description: Wiki Health Inspector. Manually triggered. Performs full wiki health scan (contradictions/orphans/missing pages/thin pages/stale pages) and writes problems to WIKI_MAINTENANCE.md for compile fix to consume.
---

# Curator Lint (Wiki Health Inspector)

## Purpose
Periodic full scan of Wiki health. Discovers issues and writes them to `WIKI_MAINTENANCE.md` for the next `/curator:compile fix` run to resolve.

**Lint does NOT fix anything.** Fixes are handled by compile fix mode.

## Prerequisites

Locate the `config/` sibling skill directory (same parent as this skill), then:
0. **Load config with overrides**: If `playground/curator-overrides.md` exists, its `## Topics` section overrides `config/topics.md`.
1. `playground/wiki/WIKI_SCHEMA.md`
2. `playground/wiki/index.md`
3. `config/topics.md` — for dimension directory list (unless overridden in step 0)

## Trigger
```
/curator:lint
```
(Manual, ad-hoc)

## Checks

### 1. Contradiction Detection
Scan all Wiki pages for contradictory statements about the same topic:
- Intra-page contradiction: Different paragraphs within the same page contradict each other
- Cross-page contradiction: Entity page says tool X is good, but concept page records the opposite experience

### 2. Orphan Page Detection
Find pages with 0 inbound [[wikilinks]].

### 3. Missing Page Detection
Scan **all Wiki pages** (including index.md) for [[wikilinks]] pointing to non-existent pages:
- **index.md link check**: Every [[wikilink]] in index.md must correspond to an actual Wiki page (.md file)
- **Common broken link pattern**: index.md links `[[concept_name]]` but only a `concept_name_reading_notes.md` source file exists, with no corresponding concept page

### 4. Thin Page Detection
Find pages with fewer than 3 lines of body content (excluding frontmatter and title).

### 5. Stale Page Detection
Find pages with `source_count: 1` and `created` date more than 90 days ago.

### 6. Empty Pointer Detection
Find pages with `source_count: 1` frontmatter and body < 3 lines, categorized as:
- **Misleading name**: Filename contains "reading_notes" but is actually a pointer to a source file
- **Missing content**: Filename contains `_pointer` but body < 3 lines
- **Broken**: `sources:` field points to a non-existent file

### 7. Pointer Empty Source Detection
Find pointer files with `source_count: 0` and `sources: []`, or where `source_count` doesn't match the length of the `sources` array.

### 8. Pointer Format Violation Detection
Find pointer files that don't follow naming conventions:
- **Convention**: `{dimension_dir}/{source_file_name}_pointer.md`
- **Source file name derivation**:
  - If source filename contains "reading_notes" suffix, remove it for the pointer name
  - If source filename has no such suffix, use it directly
- **Directory match**: Pointer file's directory should differ from the primary classification directory in its `sources` frontmatter

### 9. Pointer Unfilled Template Detection
Find pointer files whose body still contains template placeholders:
- Check if `## One-Line Summary` contains placeholder text like `*(extract from source...)*`
- Check if `## Key Takeaways` contains placeholder text like `*(3-5 points, extract from source)*`
- These files have frontmatter but empty/unfilled body — classified as **missing content empty Pointers**

### 10. Missing Backlink Detection
For Pointer files pointing to source files, check whether the source file's `## Related Wiki Pages` contains a wikilink back to the corresponding Pointer:
- Source files in dimension directories (00_Health through 08_Self) with reading notes
- Corresponding Pointer files in other dimension directories
- If source file's `## Related Wiki Pages` doesn't list the Pointer -> record as missing

## Output

### File 1: lint_report_YYYYMMDD.md

Create `playground/wiki/lint_report_YYYYMMDD.md`:

```markdown
# Wiki Lint Report (YYYY-MM-DD)

> Scanned N Wiki pages

## Summary
- Contradictions: X
- Orphan pages: Y
- Missing pages: Z
- Thin pages: W
- Stale pages: V
- Empty Pointers: P (misleading name: Q / missing content: R / broken: S)
- Pointer empty sources: U
- Pointer format violations: F
- Pointer unfilled templates: G
- Missing backlinks: T

## Details

### Contradictions
- [[page-a]] vs [[page-b]] — contradiction description
  - page-a source: raw/file1.md
  - page-b source: raw/file2.md

### Orphan Pages
- [[orphan-page]] — suggest linking from [[related-page]]

### Missing Pages
- [[missing-page]] — referenced by [[page-a]], [[page-b]]
- [[index-missing-page]] — linked in index.md but page does not exist

### Thin Pages
- [[thin-page]] — only N lines, suggest merging into [[related-page]]

### Stale Pages
- [[stale-page]] — created YYYY-MM-DD, only 1 source

### Empty Pointers
- [[empty-pointer]] (misleading name) — filename contains "reading_notes" but type=pointer, suggest renaming to *_pointer.md and filling content
- [[empty-pointer]] (missing content) — body < 3 lines, suggest extracting content from source
- [[broken-pointer]] (broken) — source points to non-existent file

### Pointer Empty Sources
- [[empty-source-pointer]] — source_count: 0 with sources: [], or source_count/sources length mismatch

### Pointer Format Violations
- [[malformed-pointer]] — doesn't follow `{dir}/{source_name}_pointer.md` format

### Pointer Unfilled Templates
- [[unfilled-template-pointer]] — body still contains `*(extract from source...)*` placeholder text

### Missing Backlinks
- [[source-file]] — missing wikilink to [[pointer-file]]

## Suggested Actions
(Findings have been written to WIKI_MAINTENANCE.md. Next compile fix run will process them automatically.)
```

### File 2: WIKI_MAINTENANCE.md

Read existing `playground/wiki/WIKI_MAINTENANCE.md` and append newly found issues.

Format: Append entries under the corresponding section, each noting its source `lint_report_YYYYMMDD.md`.

If an issue already exists in WIKI_MAINTENANCE.md and is not yet fixed, do NOT duplicate it.

### Append to log.md

```markdown
## [YYYY-MM-DD] lint | Contradictions:X | Orphans:Y | Missing:Z | Thin:W | Stale:V | Empty Pointers:P | Empty Sources:U | Format Violations:F | Unfilled Templates:G | Missing Backlinks:T
```

## Execution Mode

- No file moves — read-only scan + generate report + update WIKI_MAINTENANCE.md
- Full scan every time
- **FORBIDDEN: Auto-fixing** — report only, do not modify Wiki content
- FORBIDDEN: Creating Python/Shell scripts for scanning
