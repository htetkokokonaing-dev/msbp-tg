import unittest
import pandas as pd

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from msbp_tg.metrics import residualize_by_group, quartile_sign_accuracy, entropy_gain_by_bins

class MetricsTest(unittest.TestCase):
    def test_residualize_by_group(self):
        df = pd.DataFrame({"g": ["a", "a", "b", "b"], "x": [1, 3, 10, 14]})
        r = residualize_by_group(df, "x", "g")
        self.assertEqual(list(r), [-1, 1, -2, 2])

    def test_sign_accuracy(self):
        axis = [-2, -1, -0.5, 0, 0.5, 1, 2, 3]
        target = [-3, -1, -1, 0, 0.2, 0.8, 3, 5]
        acc = quartile_sign_accuracy(axis, target)
        self.assertGreaterEqual(acc, 0.99)

    def test_entropy_gain(self):
        df = pd.DataFrame({"y": [0, 0, 1, 1], "bin": [0, 0, 1, 1]})
        self.assertGreater(entropy_gain_by_bins(df, "y", "bin"), 0.5)

if __name__ == "__main__":
    unittest.main()
