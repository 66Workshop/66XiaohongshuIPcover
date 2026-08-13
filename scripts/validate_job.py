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
    "job_id", "topic", "main_hook", "person_asset_id",
    "layout_template_id", "font_style_id", "output",
}


def fail(message: str) -> None:
    raise ValueError(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid json: {path}: {exc}")


def approved_ids(repo_root: Path):
    people = load_json(repo_root / "assets/manifests/person_assets.json")
    visual = load_json(repo_root / "assets/manifests/visual_assets.json")
    person_ids = {a["id"] for a in people.get("assets", []) if a.get("status") == "approved"}
    font_ids = {a["id"] for a in visual.get("typography", []) if a.get("status") == "approved"}
    return person_ids, font_ids


def validate_job(path: Path, repo_root: Path | None = None):
    path = Path(path)
    repo_root = Path(repo_root) if repo_root else Path.cwd()
    data = load_json(path)

    missing = sorted(k for k in REQUIRED if k not in data)
    if missing:
        fail("missing required fields: " + ", ".join(missing))

    hook = str(data.get("main_hook", "")).strip()
    if not (4 <= len(hook) <= 24):
        fail("main_hook should be 4-24 characters")

    template = data.get("layout_template_id")
    if template not in ALLOWED_TEMPLATES:
        fail(f"unsupported layout_template_id: {template}")

    output = data.get("output") or {}
    if output.get("aspect_ratio") != "3:4":
        fail("output.aspect_ratio must be 3:4")
    count = output.get("candidate_count")
    if not isinstance(count, int) or not (1 <= count <= 4):
        fail("candidate_count must be integer 1-4")

    evidence = data.get("evidence_images", [])
    if not isinstance(evidence, list) or len(evidence) > 3:
        fail("evidence_images max is 3")

    status = data.get("status", "pending")
    if status not in {"pending", "approved", "archived"}:
        fail(f"unsupported status: {status}")

    person_ids, font_ids = approved_ids(repo_root)
    if data.get("person_asset_id") not in person_ids:
        fail(f"unknown person_asset_id: {data.get('person_asset_id')}")
    if data.get("font_style_id") not in font_ids:
        fail(f"unknown font_style_id: {data.get('font_style_id')}")

    return data


def main():
    if len(sys.argv) != 2:
        print("INVALID: usage: validate_job.py <job.json>")
        raise SystemExit(2)
    try:
        data = validate_job(Path(sys.argv[1]), Path.cwd())
    except Exception as exc:
        print(f"INVALID: {exc}")
        raise SystemExit(1)
    print("VALID")
    print(f"job_id={data['job_id']}")
    print(f"template={data['layout_template_id']}")
    print(f"candidate_count={data['output']['candidate_count']}")


if __name__ == "__main__":
    main()
