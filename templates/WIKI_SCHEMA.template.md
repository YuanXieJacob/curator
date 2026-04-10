# Wiki Schema (LLM Operating Rules)

> This file defines the Wiki's structural conventions and LLM operating rules.
> curator-compile and curator-lint MUST read this file before execution.

## 1. Directory Conventions

| Path | Content | Who Writes |
|------|---------|-----------|
| `raw/` | Source files placed by the user (new file entry point) | User (manual) |
| `00_Health/` etc. dimension dirs | Source files archived after ingest | LLM (compile ingest) |
| `entities/tools/` | Tool/product pages | LLM (compile) |
| `entities/people/` | People pages | LLM (compile) |
| `entities/companies/` | Company/community pages | LLM (compile) |
| `concepts/` | Methodology/strategy/pattern pages | LLM (compile) |
| `topics/` | Topic survey pages | LLM (compile) |
| `index.md` | Full page directory | LLM (compile, updated each run) |
| `log.md` | Operation log | LLM (compile/lint, append-only) |
| `WIKI_MAINTENANCE.md` | Issue queue written by lint, consumed by compile fix | LLM (lint/compile) |

## 2. Page Format

Every Wiki page must start with YAML frontmatter:

```yaml
---
source_count: N
sources:
  - "[[06_Productivity/filename]]"
  - "[[03_Relations/another-file]]"
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: [tag1, tag2]
---
```

`sources` uses Obsidian wikilinks pointing to files in their classified directory, **NOT** `raw/` paths.

## 3. Content Rules

- **Citations required**: Every key finding must note which classified source file it came from (Obsidian wikilink)
- **Contradictions must be flagged**: If new data contradicts existing content, use `> [!WARNING] Contradiction`
- **Cross-references use [[wikilinks]]**: `[[tool-name]]`, `[[concept-name]]`
- **Never delete old content**: New data is appended, old data is preserved (unless proven wrong)
- **Page naming**: lowercase, hyphen-separated, English (e.g., `build-in-public.md`)

## 4. Source File Conventions

- Files in `raw/` are read-only before ingest **starts**
- During ingest, files are moved out to their dimension directory via Step 4
- After ingest, the source file lives in its dimension directory; the original `raw/` path is only recorded in the log
- Classified source files should include a `## Related Wiki Pages` section at the end, with wikilinks back to Wiki pages (forming bidirectional connections)

## 5. Scope

The Wiki only collects **compounding knowledge** in these domains:
- AI / LLM / Agent systems — methodologies and tool evaluations
- Quantitative trading strategies and frameworks
- Solo business / indie developer business methodologies
- Personal IP / Build in Public tactical playbooks

**Excluded**: Time-sensitive news (product launches, funding gossip), beginner tutorials, marketing fluff.
