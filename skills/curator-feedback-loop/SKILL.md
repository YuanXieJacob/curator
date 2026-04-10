---
name: curator-feedback-loop
description: The Human-in-the-Loop Coach. Reads quick notes from 04_SUPERVISOR_FEEDBACK.md and runs a python script to monitor physical file movements. Then updates SOURCE_REPUTATION.md and 05_SYSTEM_LEARNINGS.md so the filter can learn.
---

# Curator Feedback Loop (The Learning Engine)

## Purpose
Learn from human manual interventions. Uses both explicit feedback (table) and implicit feedback (drag-and-drop file movements, Wiki ascension).

## Prerequisites

Locate the `curator-config/` sibling skill directory (same parent as this skill), then read:
- `curator-config/paths.md` — resolve all directory paths

## Inputs & Execution Steps

Execute both steps in order:

### Step 1: Process Implicit Feedback (File Movement Detection)

Run the dedicated Python script to detect files moved by the user.

The script is located in the same directory as this SKILL.md. Run it from the **project root**:
```bash
python3 <THIS_SKILL_DIR>/track_feedback.py
```
*(Replace `<THIS_SKILL_DIR>` with the actual path to this skill's directory.)*

**NEVER modify this script's content.** Just call it.

The script outputs three types of anomalies:

1. **Rescued Article (False Positive)**
    - **Meaning**: The AI graded it as noise and routed to 03, but the user rescued it to 01 or 02.
    - **Action**: Go to `playground/SOURCE_REPUTATION.md` and clear that domain's Strikes to zero. Record the lesson in `playground/05_SYSTEM_LEARNINGS.md` (why wasn't this noise? Learn this edge case).

2. **Discarded Article (False Negative)**
    - **Meaning**: The AI thought it was valuable and put it in 01 or 02, but the user tossed it into 03.
    - **Action**: Go to `playground/SOURCE_REPUTATION.md` and add a Strike for that domain. Record the lesson in `playground/05_SYSTEM_LEARNINGS.md` (why was the AI fooled?).

3. **Wiki Ascension**
    - **Meaning**: The user moved a file into `playground/wiki/raw/`. This is the highest reward signal in the system.
    - **Action**: Record this prominently in `playground/05_SYSTEM_LEARNINGS.md`. Deeply analyze the article's patterns, style, and structural features. Instruct the filter to unconditionally prioritize and score highly any articles with similar characteristics in the future.

### Step 2: Process Explicit Table Feedback

Read: `playground/04_SUPERVISOR_FEEDBACK.md`

Find rows where the `Status` column is `[ ]`:
- Parse the "Location" and "Correction" fields.
- **Action**:
    - If the instruction is about whitelisting/blacklisting a specific domain, update `playground/SOURCE_REPUTATION.md`.
    - Summarize the pattern and append a "rule" to `playground/05_SYSTEM_LEARNINGS.md`, using clear imperative phrasing like: "In the future, when encountering X-type articles, MUST apply Y treatment."
- Mark the processed row's status as `[x]`.

---

## The Learning Loop Closure

All these modifications close the loop. The `curator:filter` ALWAYS reads `SOURCE_REPUTATION.md` and `05_SYSTEM_LEARNINGS.md` before grading.

What you write here directly becomes the Filter's instructions for the next run.
