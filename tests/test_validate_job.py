import json
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_job import validate_job

ROOT = Path(__file__).resolve().parents[1]


class ValidateJobTests(unittest.TestCase):
    def write_job(self, mutate=None):
        data = json.loads((ROOT / "jobs/pending/job-001-wj-m8-ap9321.json").read_text(encoding="utf-8"))
        if mutate:
            mutate(data)
        td = tempfile.TemporaryDirectory()
        path = Path(td.name) / "job.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.addCleanup(td.cleanup)
        return path

    def test_valid_job_passes_manifest_ids(self):
        data = validate_job(self.write_job(), ROOT)
        self.assertEqual(data["person_asset_id"], "ip_sit_explain_v1")

    def test_unknown_person_asset_id_fails(self):
        path = self.write_job(lambda d: d.__setitem__("person_asset_id", "not-approved"))
        with self.assertRaisesRegex(ValueError, "unknown person_asset_id"):
            validate_job(path, ROOT)

    def test_unknown_font_style_id_fails(self):
        path = self.write_job(lambda d: d.__setitem__("font_style_id", "not-approved"))
        with self.assertRaisesRegex(ValueError, "unknown font_style_id"):
            validate_job(path, ROOT)

    def test_invalid_aspect_ratio_fails(self):
        path = self.write_job(lambda d: d["output"].__setitem__("aspect_ratio", "1:1"))
        with self.assertRaisesRegex(ValueError, "aspect_ratio"):
            validate_job(path, ROOT)


if __name__ == "__main__":
    unittest.main()
