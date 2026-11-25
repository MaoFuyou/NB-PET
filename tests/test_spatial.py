from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from nbpet_demo import legacy_threshold_demo, score_top_positive


class SpatialScoreTests(unittest.TestCase):
    def test_zero_threshold_can_mark_entire_grid(self):
        scores = [1.0] * 5 + [0.0] * 995
        ref = [900 <= index < 950 for index in range(1000)]
        threshold, legacy = legacy_threshold_demo(scores, ref)
        current = score_top_positive(scores, ref)
        self.assertEqual(threshold, 0.0)
        self.assertEqual((legacy.n_selected, legacy.hit, legacy.region_recall), (1000, 1, 1.0))
        self.assertEqual((current.budget, current.n_selected), (20, 5))
        self.assertEqual((current.hit, current.region_recall), (0, 0.0))

    def test_equal_scores_are_resolved_by_flat_index(self):
        scores = [1.0] * 100
        ref = [index in (0, 2) for index in range(100)]
        result = score_top_positive(scores, ref)
        self.assertEqual((result.budget, result.n_selected, result.n_overlap), (2, 2, 1))
        self.assertEqual((result.hit, result.region_recall), (1, 0.5))

    def test_nonfinite_and_nonpositive_scores_are_not_selected(self):
        scores = [float("nan"), float("inf"), float("-inf"), -1.0, 0.0, 0.5]
        ref = [True] * len(scores)
        result = score_top_positive(scores, ref, top_fraction=1.0)
        self.assertEqual(result.n_selected, 1)
        self.assertEqual(result.region_recall, 1 / 6)

    def test_empty_reference_excludes_hit_and_recall(self):
        result = score_top_positive([1.0] * 100, [False] * 100)
        self.assertIsNone(result.hit)
        self.assertIsNone(result.region_recall)
        self.assertEqual(result.n_selected, 2)

    def test_floor_budget_does_not_force_a_pick(self):
        result = score_top_positive([1.0] * 49, [True] * 49)
        self.assertEqual((result.budget, result.n_selected, result.hit), (0, 0, 0))
        result = score_top_positive([1.0] * 100, [True] * 100, top_fraction=0.58)
        self.assertEqual(result.n_selected, 58)

    def test_bad_input_rejected(self):
        with self.assertRaises(ValueError):
            score_top_positive([0.0], [])
        with self.assertRaises(ValueError):
            score_top_positive([], [])
        for ratio in (0, 1.1, float("nan"), "invalid"):
            with self.subTest(ratio=ratio):
                with self.assertRaises(ValueError):
                    score_top_positive([0.0], [False], top_fraction=ratio)


if __name__ == "__main__":
    unittest.main()
