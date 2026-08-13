#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ALLOWED_TEMPLATES = {
    "P01_DATA_CONFLICT",
    "P02_BEFORE_AFTER",
    "P03_VEHICLE_DECISION",
    "P04_PRODUCT_VALUE",
}

REQUIRED = {
    "job_id",
    "topic",
    "main_hook",
    "person_asset_id",
    "layout_template_id",
    "font_style_id",
    "output",
}


def fail(message: str, code: int = 1) -> None:
    print(f"INVALID: {message}")
    raise SystemExit(code)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: validate_job.py <job.json>", 2)

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}", 3)

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid json: {exc}", 4)

    missing = sorted(k for k in REQUIRED if k not in data)
    if missing:
        fail("missing required fields: " + ", ".join(missing), 5)

    hook = str(data.get("main_hook", "")).strip()
    if not (4 <= len(hook) <= 24):
        fail("main_hook should be 4-24 characters", 6)

    template = data.get("layout_template_id")
    if template not in ALLOWED_TEMPLATES:
        fail(f"unsupported layout_template_id: {template}", 7)

    output = data.get("output") or {}
    if output.get("aspect_ratio") != "3:4":
        fail("output.aspect_ratio must be 3:4", 8)

    count = output.get("candidate_count")
    if not isinstance(count, int) or not (1 <= count <= 4):
        fail("candidate_count must be integer 1-4", 9)

    evidence = data.get("evidence_images", [])
    if len(evidence) > 3:
        fail("evidence_images max is 3", 10)

    print("VALID")
    print(f"template={template}")
    print(f"hook={hook}")
    print(f"candidate_count={count}")


if __name__ == "__main__":
    main()
