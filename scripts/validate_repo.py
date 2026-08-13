#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from validate_job import validate_job

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_PATHS = [
    "SKILL.md",
    "assets/manifests/person_assets.json",
    "assets/manifests/visual_assets.json",
    "assets/manifests/assets_manifest.json",
    "schemas/job.schema.json",
    "scripts/validate_job.py",
    "scripts/validate_repo.py",
    ".github/workflows/validate.yml",
    "jobs/pending",
    "jobs/approved",
    "jobs/archived",
    "records",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str):
    raise ValueError(message)


def validate_asset(root: Path, asset: dict, seen_ids: set[str]):
    aid = asset.get("id")
    if not aid:
        fail("asset missing id")
    if aid in seen_ids:
        fail(f"duplicate asset id: {aid}")
    seen_ids.add(aid)

    path_text = asset.get("path")
    if not path_text:
        fail(f"asset missing path: {aid}")
    path = root / path_text
    if not path.is_file():
        fail(f"missing asset path: {path_text}")

    expected = asset.get("sha256")
    if not expected or not SHA256_RE.fullmatch(expected):
        fail(f"invalid sha256 field: {aid}")
    actual = sha256_file(path)
    if actual != expected:
        fail(f"sha256 mismatch: {aid}: expected={expected} actual={actual}")

    source_hash = asset.get("source_sha256")
    if not source_hash or not SHA256_RE.fullmatch(source_hash):
        fail(f"invalid source_sha256 field: {aid}")
    if asset.get("status") != "approved":
        fail(f"asset not approved: {aid}")


def validate_repo(root: Path = Path(".")):
    root = Path(root).resolve()
    missing = [p for p in REQUIRED_PATHS if not (root / p).exists()]
    if missing:
        fail("missing required repo paths: " + ", ".join(missing))

    people = load_json(root / "assets/manifests/person_assets.json")
    visual = load_json(root / "assets/manifests/visual_assets.json")
    flat = load_json(root / "assets/manifests/assets_manifest.json")

    seen_ids = set()
    for asset in people.get("assets", []):
        validate_asset(root, asset, seen_ids)
        required = {"face_no_redraw", "identity_lock", "no_beautify"}
        if not required.issubset(set(asset.get("constraints", []))):
            fail(f"identity constraints incomplete: {asset.get('id')}")
        if asset.get("role") != "identity_reference_derivative":
            fail(f"unexpected person role: {asset.get('id')}")

    for asset in visual.get("typography", []):
        validate_asset(root, asset, seen_ids)
        if asset.get("role") != "style_reference_only":
            fail(f"typography must be style_reference_only: {asset.get('id')}")
        if "do_not_treat_as_redistributable_font_file" not in set(asset.get("rules", [])):
            fail("typography redistribution guard missing")

    successful_cases = visual.get("successful_cases", [])
    if len(successful_cases) < 4:
        fail("successful_cases must contain at least 4 references")
    for asset in successful_cases:
        validate_asset(root, asset, seen_ids)
        if asset.get("role") != "successful_case_reference_derivative":
            fail(f"unexpected successful case role: {asset.get('id')}")

    flat_assets = flat.get("assets", [])
    if flat.get("asset_count") != len(flat_assets):
        fail("assets_manifest asset_count mismatch")
    if {a.get("id") for a in flat_assets} != seen_ids:
        fail("assets_manifest IDs do not match source manifests")

    jobs = sorted(root.glob("jobs/**/*.json"))
    for job_path in jobs:
        validate_job(job_path, root)

    return {"status": "VALID", "asset_count": len(seen_ids), "job_count": len(jobs)}


def main():
    try:
        result = validate_repo(Path.cwd())
    except Exception as exc:
        print(f"INVALID: {exc}")
        raise SystemExit(1)
    print("VALID")
    print(f"asset_count={result['asset_count']}")
    print(f"job_count={result['job_count']}")


if __name__ == "__main__":
    main()
