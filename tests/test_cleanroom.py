import tempfile
import unittest
from pathlib import Path
from cleanroom import clean, daily_summary, run


class CleanroomTests(unittest.TestCase):
    def test_sort(self):
        rows = [{"timestamp": "2026-11-06T00:00:00Z", "value": "2"},
                {"timestamp": "2026-11-05T00:00:00Z", "value": "1"}]
        accepted, errors = clean(rows)
        self.assertEqual(accepted[0][1], 1)
        self.assertEqual(errors, [])
    def test_duplicate(self):
        row = {"timestamp": "2026-11-05T00:00:00Z", "value": "1"}
        accepted, errors = clean([row, row])
        self.assertEqual((len(accepted), len(errors)), (1, 1))
    def test_bad_value(self):
        self.assertEqual(len(clean([{"timestamp": "2026-11-05T00:00:00Z", "value": "oops"}])[1]), 1)
    def test_nonfinite(self):
        self.assertEqual(len(clean([{"timestamp": "2026-11-05T00:00:00Z", "value": "NaN"}])[1]), 1)
    def test_timezone_required(self):
        self.assertEqual(len(clean([{"timestamp": "2026-11-05T00:00:00", "value": "1"}])[1]), 1)
    def test_daily_summary(self):
        self.assertEqual(daily_summary([("2026-11-05T00:00:00Z", 2), ("2026-11-05T01:00:00Z", 4)])[0]["mean"], 3)
    def test_csv_end_to_end(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "input.csv"
            output = Path(directory) / "output.json"
            source.write_text("timestamp,value\n2026-11-05T00:00:00Z,3\n", encoding="utf-8")
            self.assertEqual(run(str(source), str(output))["accepted"], 1)
            self.assertTrue(output.exists())


if __name__ == "__main__":
    unittest.main()
