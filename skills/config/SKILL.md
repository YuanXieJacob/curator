---
name: config
description: Shared configuration hub for all curator skills. Not invoked directly — other skills read files from this directory to load paths, topics, action tags, templates, and grading standards. Supports local overrides via playground/curator-overrides.md.
---

# Curator Config (Shared Configuration Hub)

This is NOT an executable skill. It is a configuration directory that all other curator skills reference.

## Config Resolution Order (IMPORTANT)

All curator skills follow this priority when loading configuration:

1. **`playground/curator-overrides.md`** — User's local overrides (HIGHEST PRIORITY)
2. **`config/*.md` files** — Plugin defaults (this directory)

If `playground/curator-overrides.md` exists, its sections override matching plugin defaults. Any section NOT present in overrides falls back to the plugin default.

### Override Section Mapping

| Override Section Header | Overrides Plugin File |
|------------------------|----------------------|
| `## Topics` | `config/topics.md` |
| `## Action Tags` | `config/action-tags.md` |
| `## Paths` | `config/paths.md` |
| `## Admiralty System` | `config/admiralty-system.md` |

Templates (`config/templates/`) are not overridable via this mechanism. To customize templates, copy them into your project's `.claude/skills/` and modify there.

### Loading Pattern for Skills

```
1. Read playground/curator-overrides.md (if it exists)
2. For each config area needed:
   - If the matching section exists in overrides → use it
   - Otherwise → read the plugin's config/ file
```

## Contents

| File | Purpose | Used By |
|------|---------|---------|
| `paths.md` | All directory paths (single source of truth) | All skills |
| `topics.md` | Topic categories + Wiki dimension directories | filter, compile |
| `action-tags.md` | Action tag definitions | filter |
| `admiralty-system.md` | Source reliability + Information credibility grading | filter |
| `templates/` | Reusable markdown templates | filter, compile, intake |
