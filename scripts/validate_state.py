#!/usr/bin/env python3
"""Check that Colony's config and state files are well-formed and consistent."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(path, errors):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        errors.append(f"{path.relative_to(ROOT)}: {e}")
        return None


def main():
    errors = []

    north_star = load_json(ROOT / "config/north_star.json", errors)
    progress = load_json(ROOT / "state/progress.json", errors)
    tasks = load_json(ROOT / "state/tasks.json", errors)

    if north_star is not None and progress is not None:
        pillars = set(north_star.get("pillars", []))
        tracked = set(progress) - {"overall"}
        for p in sorted(pillars - tracked):
            errors.append(f"state/progress.json: missing pillar '{p}'")
        for p in sorted(tracked - pillars):
            errors.append(f"state/progress.json: unknown pillar '{p}'")

    if progress is not None:
        for key, value in progress.items():
            if not isinstance(value, (int, float)) or not 0 <= value <= 100:
                errors.append(f"state/progress.json: '{key}' must be a number from 0 to 100")

    if tasks is not None and not isinstance(tasks.get("tasks"), list):
        errors.append("state/tasks.json: 'tasks' must be a list")

    activity = ROOT / "state/activity.jsonl"
    for n, line in enumerate(activity.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"state/activity.jsonl:{n}: {e}")

    for e in errors:
        print(e, file=sys.stderr)
    if errors:
        return 1
    print("state OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
