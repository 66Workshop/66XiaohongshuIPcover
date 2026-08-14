import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_creative_governance import validate_creative_governance


ROOT = Path(__file__).resolve().parents[1]


class CreativeGovernanceTests(unittest.TestCase):
    def _sandbox(self) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="creative-governance-"))
        self.addCleanup(lambda: shutil.rmtree(tmp, ignore_errors=True))
        shutil.copytree(ROOT / "governance", tmp / "governance")
        shutil.copytree(ROOT / "assets" / "manifests", tmp / "assets" / "manifests")
        return tmp

    @staticmethod
    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _write(path: Path, data: dict) -> None:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_current_repository_passes_creative_governance(self):
        result = validate_creative_governance(ROOT)
        self.assertTrue(result["ok"], result["errors"])
        self.assertEqual(result["profile"], "creative_content")

    def test_rejects_pinned_core_ref_drift(self):
        root = self._sandbox()
        path = root / "governance" / "core-lock.json"
        data = self._load(path)
        data["pinned_core_ref"] = "0" * 40
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_task_fixture_byte_drift(self):
        root = self._sandbox()
        path = root / "governance" / "core-fixtures" / "task-contract-v0.1.json"
        path.write_bytes(path.read_bytes() + b"\n")
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_approval_fixture_byte_drift(self):
        root = self._sandbox()
        path = root / "governance" / "core-fixtures" / "approval-contract-v0.2.json"
        path.write_bytes(path.read_bytes() + b"\n")
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_wrong_profile(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["profile"] = "engineering_simulation"
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_original_identity_sources_in_public_repo(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["public_repo_original_identity_source_allowed"] = True
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_non_derivative_repo_identity_assets(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["repo_identity_assets"] = "original_sources_allowed"
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_missing_human_identity_qa(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["human_identity_qa_required"] = False
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_route_c_as_trusted_output(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["generated_identity_reference_output"] = "trusted_output"
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_typography_binary_redistribution(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["typography_binary_redistribution_allowed"] = True
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_third_party_generation_api(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["third_party_generation_api_enabled"] = True
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_self_hosted_execution(self):
        root = self._sandbox()
        path = root / "governance" / "creative-boundary.json"
        data = self._load(path)
        data["self_hosted_enabled"] = True
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_person_role_drift(self):
        root = self._sandbox()
        path = root / "assets" / "manifests" / "person_assets.json"
        data = self._load(path)
        data["assets"][0]["role"] = "identity_source_original"
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_missing_identity_constraints(self):
        root = self._sandbox()
        path = root / "assets" / "manifests" / "person_assets.json"
        data = self._load(path)
        data["assets"][0]["constraints"] = ["identity_lock"]
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_typography_role_drift(self):
        root = self._sandbox()
        path = root / "assets" / "manifests" / "visual_assets.json"
        data = self._load(path)
        data["typography"][0]["role"] = "font_binary"
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_missing_typography_redistribution_guard(self):
        root = self._sandbox()
        path = root / "assets" / "manifests" / "visual_assets.json"
        data = self._load(path)
        data["typography"][0]["rules"] = ["black_for_fact_or_object"]
        self._write(path, data)
        self.assertFalse(validate_creative_governance(root)["ok"])

    def test_rejects_forbidden_secret_like_governance_keys(self):
        for key in ("private_key", "pat", "token", "secret"):
            with self.subTest(key=key):
                root = self._sandbox()
                path = root / "governance" / "creative-boundary.json"
                data = self._load(path)
                data[key] = "forbidden"
                self._write(path, data)
                self.assertFalse(validate_creative_governance(root)["ok"])


if __name__ == "__main__":
    unittest.main()
