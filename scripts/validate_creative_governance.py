#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

EXPECTED_CORE_REF = "ca393246b5bc05d4896945d5bda8896506d870d1"
EXPECTED_TASK_BLOB = "cecd362a88d4f494e7dc7d33fc2e93e5d05a660c"
EXPECTED_APPROVAL_BLOB = "809b76c1ff59efb6fbee922e28e5d4af5bfd36e5"
EXPECTED_PROFILE = "creative_content"

EXPECTED_CORE_LOCK = {
    "schema_version": "0.1",
    "core_repository": "66Workshop/66-ai-workflow-core",
    "pinned_core_ref": EXPECTED_CORE_REF,
    "profile": EXPECTED_PROFILE,
    "task_contract_version": "0.1",
    "approval_contract_version": "0.2",
    "task_fixture_blob": EXPECTED_TASK_BLOB,
    "approval_fixture_blob": EXPECTED_APPROVAL_BLOB,
    "self_hosted_enabled": False,
}

EXPECTED_BOUNDARY = {
    "schema_version": "0.1",
    "profile": EXPECTED_PROFILE,
    "identity_source_policy": "original_authorized_source_required_for_identity_critical_production",
    "repo_identity_assets": "derivative_preview_only",
    "generated_identity_reference_output": "candidate_only",
    "human_identity_qa_required": True,
    "vehicle_and_part_evidence_required": True,
    "typography_binary_redistribution_allowed": False,
    "third_party_generation_api_enabled": False,
    "public_repo_original_identity_source_allowed": False,
    "self_hosted_enabled": False,
}

REQUIRED_IDENTITY_CONSTRAINTS = {"face_no_redraw", "identity_lock", "no_beautify"}
TYPOGRAPHY_REDISTRIBUTION_GUARD = "do_not_treat_as_redistributable_font_file"
FORBIDDEN_KEYS = {"private_key", "privatekey", "pat", "token", "secret"}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def _load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.is_file():
        errors.append(f"missing required governance file: {path.as_posix()}")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid json: {path.as_posix()}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"expected object: {path.as_posix()}")
        return None
    return value


def _walk_forbidden_keys(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower().replace("-", "_")
            if normalized in FORBIDDEN_KEYS:
                errors.append(f"forbidden governance key at {path}.{key}")
            errors.extend(_walk_forbidden_keys(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_walk_forbidden_keys(child, f"{path}[{index}]"))
    return errors


def _require_exact_fields(actual: dict[str, Any] | None, expected: dict[str, Any], prefix: str, errors: list[str]) -> None:
    if actual is None:
        return
    for key, expected_value in expected.items():
        if actual.get(key) != expected_value:
            errors.append(f"{prefix}.{key} mismatch: expected={expected_value!r} actual={actual.get(key)!r}")


def validate_creative_governance(root_dir: str | Path = ".") -> dict:
    root = Path(root_dir).resolve()
    errors: list[str] = []

    lock_path = root / "governance" / "core-lock.json"
    boundary_path = root / "governance" / "creative-boundary.json"
    task_fixture = root / "governance" / "core-fixtures" / "task-contract-v0.1.json"
    approval_fixture = root / "governance" / "core-fixtures" / "approval-contract-v0.2.json"
    person_manifest = root / "assets" / "manifests" / "person_assets.json"
    visual_manifest = root / "assets" / "manifests" / "visual_assets.json"

    lock = _load_json(lock_path, errors)
    boundary = _load_json(boundary_path, errors)
    people = _load_json(person_manifest, errors)
    visual = _load_json(visual_manifest, errors)

    _require_exact_fields(lock, EXPECTED_CORE_LOCK, "core-lock", errors)
    _require_exact_fields(boundary, EXPECTED_BOUNDARY, "creative-boundary", errors)

    if task_fixture.is_file():
        actual = git_blob_sha(task_fixture)
        if actual != EXPECTED_TASK_BLOB:
            errors.append(f"task fixture blob mismatch: expected={EXPECTED_TASK_BLOB} actual={actual}")
    else:
        errors.append(f"missing required governance file: {task_fixture.as_posix()}")

    if approval_fixture.is_file():
        actual = git_blob_sha(approval_fixture)
        if actual != EXPECTED_APPROVAL_BLOB:
            errors.append(f"approval fixture blob mismatch: expected={EXPECTED_APPROVAL_BLOB} actual={actual}")
    else:
        errors.append(f"missing required governance file: {approval_fixture.as_posix()}")

    if lock is not None:
        errors.extend(_walk_forbidden_keys(lock, "$.core_lock"))
    if boundary is not None:
        errors.extend(_walk_forbidden_keys(boundary, "$.creative_boundary"))

    if people is not None:
        assets = people.get("assets")
        if not isinstance(assets, list) or not assets:
            errors.append("person manifest must contain at least one asset")
        else:
            for index, asset in enumerate(assets):
                prefix = f"person_assets[{index}]"
                if not isinstance(asset, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                if asset.get("role") != "identity_reference_derivative":
                    errors.append(f"{prefix}.role must remain identity_reference_derivative")
                constraints = set(asset.get("constraints") or [])
                if not REQUIRED_IDENTITY_CONSTRAINTS.issubset(constraints):
                    errors.append(f"{prefix}.constraints missing identity locks")
                if asset.get("status") != "approved":
                    errors.append(f"{prefix}.status must remain approved")

    if visual is not None:
        typography = visual.get("typography")
        if not isinstance(typography, list) or not typography:
            errors.append("visual manifest must contain at least one typography reference")
        else:
            for index, asset in enumerate(typography):
                prefix = f"typography[{index}]"
                if not isinstance(asset, dict):
                    errors.append(f"{prefix} must be an object")
                    continue
                if asset.get("role") != "style_reference_only":
                    errors.append(f"{prefix}.role must remain style_reference_only")
                rules = set(asset.get("rules") or [])
                if TYPOGRAPHY_REDISTRIBUTION_GUARD not in rules:
                    errors.append(f"{prefix}.rules missing typography redistribution guard")
                path_text = str(asset.get("path") or "").lower()
                if path_text.endswith((".ttf", ".otf", ".woff", ".woff2")):
                    errors.append(f"{prefix}.path must not reference a redistributable font binary")

    profile = boundary.get("profile") if isinstance(boundary, dict) else None
    return {"ok": not errors, "errors": errors, "profile": profile}


def main() -> int:
    result = validate_creative_governance(Path.cwd())
    if result["ok"]:
        print("CREATIVE_GOVERNANCE=PASS")
        print(f"PROFILE={result['profile']}")
        print(f"CORE_REF={EXPECTED_CORE_REF}")
        print("HUMAN_IDENTITY_QA_REQUIRED=true")
        print("PUBLIC_REPO_ORIGINAL_IDENTITY_SOURCE_ALLOWED=false")
        print("TYPOGRAPHY_BINARY_REDISTRIBUTION_ALLOWED=false")
        print("THIRD_PARTY_GENERATION_API_ENABLED=false")
        print("SELF_HOSTED_ENABLED=false")
        return 0
    for error in result["errors"]:
        print(f"CREATIVE_GOVERNANCE_ERROR={error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
