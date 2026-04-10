---
name: config
description: Shared configuration hub for all curator skills. Not invoked directly — other skills read files from this directory to load paths, topics, action tags, templates, and grading standards.
---

# Curator Config (Shared Configuration Hub)

This is NOT an executable skill. It is a configuration directory that all other curator skills reference.

## How Other Skills Use This

Each skill's "Prerequisites" section specifies which config files to read before execution. Config files are located in the same directory as this SKILL.md.

When a skill says "Read `config/paths.md`", it means: find the `config/` sibling skill directory and read `paths.md` from it.

## Contents

| File | Purpose | Used By |
|------|---------|---------|
| `paths.md` | All directory paths (single source of truth) | All skills |
| `topics.md` | Topic categories + Wiki dimension directories | filter, compile |
| `action-tags.md` | Action tag definitions | filter |
| `admiralty-system.md` | Source reliability + Information credibility grading | filter |
| `templates/` | Reusable markdown templates | filter, compile, intake |
