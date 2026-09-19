import os
import json
import tempfile
import unittest
from pathlib import Path

from repoScan.scanner.metrics import generate_metrics
from repoScan.utility.helpers import (
    total_files,
    total_lines,
    total_bytes,
    average_lines_per_file,
    average_file_size,
    largest_file_by_lines,
    get_max_file,
    get_total_bytes,
)
from repoScan.reports.jsonReports import write_json_report


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.sample_files = ["app/main.py", "app/utils.py", "README.md"]
        self.sample_size_report = {
            "total_files": 3,
            "total_bytes": 1024,
            "average_file_size": 341,
            "total_lines": 120,
            "average_lines": 40,
            "largest_files": [("app/main.py", 600), ("app/utils.py", 300), ("README.md", 124)],
            "size_by_extension": {".py": 900, ".md": 124},
        }
        self.sample_dep_report = {
            "app/main.py": ["os", "sys"],
            "app/utils.py": ["math"],
            "README.md": [],
        }

    def test_generate_metrics_contains_new_fields(self):
        metrics = generate_metrics(self.sample_files, self.sample_size_report, self.sample_dep_report)

        self.assertIn("file_metrics", metrics)
        file_metrics = metrics["file_metrics"]

        # Check existing metrics
        self.assertEqual(file_metrics["total"], 3)
        self.assertEqual(file_metrics["total_lines"], 120)
        self.assertEqual(file_metrics["average_lines"], 40)
        self.assertEqual(file_metrics["largest_file"], ("app/main.py", 600))

        # Check newly added metrics
        self.assertIn("total_bytes", file_metrics)
        self.assertEqual(file_metrics["total_bytes"], 1024)

        self.assertIn("average_file_size", file_metrics)
        self.assertEqual(file_metrics["average_file_size"], 341)

        self.assertIn("max_file", file_metrics)
        self.assertEqual(file_metrics["max_file"], ("app/main.py", 600))

    def test_helpers_total_bytes_and_average_size(self):
        self.assertEqual(total_bytes(self.sample_size_report), 1024)
        self.assertEqual(total_bytes({}), 0)
        self.assertEqual(total_bytes(None), 0)

        self.assertEqual(average_file_size(self.sample_size_report), 341)
        self.assertEqual(average_file_size({}), 0)
        self.assertEqual(average_file_size(None), 0)

    def test_helpers_get_max_file_with_size_report(self):
        max_file = get_max_file(self.sample_size_report)
        self.assertEqual(max_file, ("app/main.py", 600))

        empty_max = get_max_file({"largest_files": []})
        self.assertEqual(empty_max, (None, -1))

    def test_helpers_get_total_bytes_with_size_report(self):
        self.assertEqual(get_total_bytes(self.sample_size_report), 1024)

    def test_json_report_export(self):
        metrics = generate_metrics(self.sample_files, self.sample_size_report, self.sample_dep_report)
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_path = write_json_report(metrics, output_dir=tmp_dir)
            self.assertTrue(os.path.exists(json_path))

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertIn("metrics", data)
            file_metrics = data["metrics"]["file_metrics"]
            self.assertEqual(file_metrics["total_bytes"], 1024)
            self.assertEqual(file_metrics["average_file_size"], 341)
            self.assertEqual(file_metrics["max_file"], ["app/main.py", 600])


if __name__ == "__main__":
    unittest.main()
