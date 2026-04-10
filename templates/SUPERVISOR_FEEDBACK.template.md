# Supervisor Quick Feedback

Leave brief correction instructions here. `curator-feedback-loop` scans this table during each run, processes unchecked rows, and updates filtering rules and reputation accordingly.

| File / Keyword | Location (01 / digest / Wiki etc.) | Feedback Type (missed noise / false kill / wrong tag / off-focus) | Correction (one sentence) | Status |
|---|---|---|---|---|
| e.g.: 0331_Apple.md | digest | off-focus | Contains a section on supply chain new process, don't just focus on the AI title | [ ] |

## Implicit Movement Feedback (The Drag-and-Drop Loop)
No table entry needed — simply move files physically (via file manager) to let the AI learn automatically:
- **Rescue from trash**: Drag a file from `03_NOISE` to `01` or `02` -> automatically clears strikes and records as false positive.
- **Demote to trash**: Drag a file from `01` or `02` into `03_NOISE` -> automatically adds a strike and records as false negative.
- **Wiki promotion**: Copy or move any file to `playground/wiki/raw/` -> system treats it as highest-value knowledge and deeply learns its content patterns.
