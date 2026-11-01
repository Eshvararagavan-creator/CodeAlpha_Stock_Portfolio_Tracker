import tempfile
import unittest
from pathlib import Path

from portfolio_tracker import calculate_portfolio, save_csv


class PortfolioTests(unittest.TestCase):
    def test_calculates_total(self):
        values, total = calculate_portfolio({"AAPL": 2, "TSLA": 1})
        self.assertEqual(values, {"AAPL": 360.0, "TSLA": 250.0})
        self.assertEqual(total, 610.0)

    def test_rejects_unknown_symbol(self):
        with self.assertRaises(ValueError):
            calculate_portfolio({"NOPE": 1})

    def test_writes_csv_report(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.csv"
            self.assertEqual(save_csv({"MSFT": 1}, path), 420.0)
            self.assertIn("MSFT", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
