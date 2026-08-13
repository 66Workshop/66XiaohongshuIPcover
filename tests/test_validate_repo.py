import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
ROOT = Path(__file__).resolve().parents[1]


class ValidateRepoTests(unittest.TestCase):
    def test_repo_validator_checks_assets_and_structure(self):
        from validate_repo import validate_repo
        result = validate_repo(ROOT)
        self.assertEqual(result["asset_count"], 8)
        self.assertEqual(result["job_count"], 1)
        self.assertEqual(result["status"], "VALID")


if __name__ == "__main__":
    unittest.main()
