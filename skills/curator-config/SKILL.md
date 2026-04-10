---
name: curator-config
description: Shared configuration hub for all curator skills. Not invoked directly — other skills read files from this directory to load paths, topics, action tags, templates, and grading standards. Supports optional local overrides that survive plugin updates.
---

# Curator Config (Shared Configuration Hub)

This is NOT an executable skill. It is a configuration directory that all other curator skills reference.

The plugin works **out of the box** with the defaults in this directory. Users can optionally override any config file or template by placing a copy in their project — no overrides are required.

## Override System

Simple rule: **file exists in user's project → use it. Missing → use plugin default.**

### Config Overrides

| Plugin Default | User Override (optional) |
|---------------|------------------------|
| `curator-config/paths.md` | `playground/curator-config/paths.md` |
| `curator-config/topics.md` | `playground/curator-config/topics.md` |
| `curator-config/action-tags.md` | `playground/curator-config/action-tags.md` |
| `curator-config/admiralty-system.md` | `playground/curator-config/admiralty-system.md` |

### Template Overrides

| Plugin Default | User Override (optional) |
|---------------|------------------------|
| `curator-config/templates/assessment-block.md` | `playground/curator-templates/assessment-block.md` |
| `curator-config/templates/action-brief-01.md` | `playground/curator-templates/action-brief-01.md` |
| `curator-config/templates/action-brief-02.md` | `playground/curator-templates/action-brief-02.md` |
| `curator-config/templates/daily-digest.md` | `playground/curator-templates/daily-digest.md` |
| `curator-config/templates/inbox-file.md` | `playground/curator-templates/inbox-file.md` |
| `curator-config/templates/pointer-note.md` | `playground/curator-templates/pointer-note.md` |

### How to Customize

1. Copy the file you want to change from the plugin to your project:
   ```bash
   # Override topics
   mkdir -p playground/curator-config
   cp <plugin>/skills/curator-config/topics.md playground/curator-config/topics.md
   # Edit playground/curator-config/topics.md
   
   # Override a template
   mkdir -p playground/curator-templates
   cp <plugin>/skills/curator-config/templates/daily-digest.md playground/curator-templates/daily-digest.md
   # Edit playground/curator-templates/daily-digest.md
   ```
2. Done. Plugin updates will replace the defaults, but your copies are untouched.
3. To revert: just delete the override file.

### Loading Pattern (for all skills)

```
def resolve_config(filename):
    if exists("playground/curator-config/{filename}"):
        return read("playground/curator-config/{filename}")
    else:
        return read("curator-config/{filename}")  # plugin default

def resolve_template(filename):
    if exists("playground/curator-templates/{filename}"):
        return read("playground/curator-templates/{filename}")
    else:
        return read("curator-config/templates/{filename}")  # plugin default
```

### What Survives Plugin Updates

| Category | Location | Survives? |
|----------|----------|-----------|
| **User data (accumulated)** | | |
| Active projects & signals | `playground/CURRENT_FOCUS.md` | Yes |
| Domain reputation | `playground/SOURCE_REPUTATION.md` | Yes |
| Learned filter rules | `playground/05_SYSTEM_LEARNINGS.md` | Yes |
| Human feedback | `playground/04_SUPERVISOR_FEEDBACK.md` | Yes |
| All articles | `playground/00_INBOX/` through `05_OUTBOX/` | Yes |
| Obsidian wiki | `playground/wiki/` | Yes |
| **User overrides (optional)** | | |
| Config overrides | `playground/curator-config/` | Yes |
| Template overrides | `playground/curator-templates/` | Yes |
| **Plugin files** | | |
| Skill logic | `skills/*/SKILL.md` | No (updated) |
| Default config | `curator-config/*.md` | No (updated) |
| Default templates | `curator-config/templates/` | No (updated) |

## Contents

| File | Purpose | Used By |
|------|---------|---------|
| `paths.md` | All directory paths | All skills |
| `topics.md` | Topic categories + Wiki dimension directories | filter, compile, lint |
| `action-tags.md` | Action tag definitions | filter |
| `admiralty-system.md` | Grading criteria + routing matrix | filter |
| `templates/` | Reusable markdown templates | filter, compile, intake |
