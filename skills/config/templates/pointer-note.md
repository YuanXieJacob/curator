# Pointer Note Template

## Naming Convention

Format: `{dimension_dir}/{source_file_name}_pointer.md`

Source file name rules:
- If source filename contains `_reading_notes` (or equivalent suffix), remove it
- Otherwise, use the original name as-is

Examples:
- Source: `03_Relations/controlling_parents_reading_notes.md` -> Pointer: `08_Self/controlling_parents_pointer.md`
- Source: `08_Self/stanford_happiness.md` -> Pointer: `08_Self/stanford_happiness_pointer.md`

## Template

```yaml
---
source_count: 1
sources:
  - "[[03_Relations/source_filename.md]]"
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: [tag1, tag2]
---

# Source Title

> This note primarily belongs to [[03_Relations/source_filename.md]]. This is a quick-access entry from the [[08_Self]] dimension.

## One-Line Summary
<Actual summary extracted from the source file — NEVER leave as placeholder>

## Key Takeaways
- **Point 1**: Actual content from source
- **Point 2**: Actual content from source
- **Point 3**: Actual content from source

## Related Wiki Pages
- [[concepts/concept-name]] — description
- [[entities/entity-name]] — description
```

## Atom Rules

- **NEVER leave template placeholders** — `## One-Line Summary` and `## Key Takeaways` must contain real content extracted from the source file
- Pointer file body MUST NOT be empty
- Frontmatter uses `source_count: 1` + `sources:` array format; `sources` use Obsidian wikilink format `[[dir/filename.md]]` (with `.md` extension)
- If multiple dimensions reference the same source, create separate pointers in each dimension directory
