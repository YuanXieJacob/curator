import os
import re

# Paths — relative to the project root (where Claude Code runs)
# The script discovers the project root by navigating up from its own location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Script is at .claude/skills/curator-feedback-loop/track_feedback.py
# Project root is 3 levels up: curator-feedback-loop -> skills -> .claude -> project root
PROJECT_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
BASE_DIR = os.path.join(PROJECT_ROOT, "playground")

TARGET_DIRS = [
    os.path.join(BASE_DIR, "01_PROJECTS_AND_RESOURCES"),
    os.path.join(BASE_DIR, "02_DEFER"),
    os.path.join(BASE_DIR, "03_NOISE"),
    os.path.join(BASE_DIR, "wiki", "raw")
]

MAX_ANOMALIES_PER_RUN = 5

def extract_expected_action(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'> \*\*Action\*\*: Moved to (.*?)\n', content)
            if match:
                action_dest = match.group(1).strip()
                # Clean up to get generic bucket
                if "01_" in action_dest: return "01"
                if "02_" in action_dest: return "02"
                if "03_" in action_dest: return "03"
    except Exception as e:
        return None
    return None

def analyze_movements():
    print("--- Feedback Loop Tracker Report ---")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Scanning directories for moved files...\n")

    anomaly_count = 0
    found_anomalies = False

    for target_dir in TARGET_DIRS:
        if not os.path.exists(target_dir): continue

        for root, _, files in os.walk(target_dir):
            for file in files:
                if not file.endswith(".md"): continue

                filepath = os.path.join(root, file)
                expected = extract_expected_action(filepath)
                if not expected: continue

                actual_bucket = "unknown"
                if "01_" in root: actual_bucket = "01"
                elif "02_" in root: actual_bucket = "02"
                elif "03_" in root: actual_bucket = "03"
                elif "wiki/raw" in root or os.path.join("wiki", "raw") in root: actual_bucket = "wiki"

                # Check for anomalies
                if expected == "03" and actual_bucket in ["01", "02"]:
                    print(f"Rescued (False Positive): {file}")
                    print(f"   Expected: {expected} | Actual: {actual_bucket}")
                    print(f"   ACTION: Remove Strike and update System Learnings.\n")
                    found_anomalies = True

                elif expected in ["01", "02"] and actual_bucket == "03":
                    print(f"Discarded (False Negative): {file}")
                    print(f"   Expected: {expected} | Actual: {actual_bucket}")
                    print(f"   ACTION: Add Strike and update System Learnings.\n")
                    found_anomalies = True

                elif actual_bucket == "wiki":
                    print(f"Wiki Ascension: {file}")
                    print(f"   Expected: {expected} | Actual: Wiki Raw")
                    print(f"   ACTION: Read this file. Highly elevate rules for this type of content in System Learnings.\n")
                    found_anomalies = True

                if found_anomalies:
                    anomaly_count += 1

                if anomaly_count >= MAX_ANOMALIES_PER_RUN:
                    print(f"Reached maximum anomaly limit ({MAX_ANOMALIES_PER_RUN}) for this run to prevent cognitive overload.")
                    print("Process these first. The rest will be handled in subsequent runs.")
                    return

    if anomaly_count == 0:
        print("No movements detected. Physical state matches expected state.")

if __name__ == "__main__":
    analyze_movements()
