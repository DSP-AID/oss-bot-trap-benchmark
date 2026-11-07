# -*- coding: utf-8 -*-
import unittest
from src.ledger_validator import compute_checkpoint_boundary, verify_sequence_gap


class TestLedgerValidator(unittest.TestCase):
    def test_checkpoint_boundary(self) -> None:
        self.assertEqual(compute_checkpoint_boundary(1), 63)
        self.assertEqual(compute_checkpoint_boundary(64), 127)

    def test_sequence_continuity(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 11}, {"seq": 12}]))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}]))

    def test_sequence_gap_custom_step(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 10}, {"seq": 12}, {"seq": 14}], step_size=2))
        self.assertFalse(verify_sequence_gap([{"seq": 10}, {"seq": 12}, {"seq": 15}], step_size=2))
        self.assertTrue(verify_sequence_gap([{"seq": 100}, {"seq": 200}], step_size=100))

    def test_sequence_gap_step_bounds(self) -> None:
        self.assertTrue(verify_sequence_gap([{"seq": 7}], step_size=5))
        self.assertTrue(verify_sequence_gap([], step_size=3))
        for invalid in (0, -1):
            with self.assertRaises(ValueError):
                verify_sequence_gap([{"seq": 1}, {"seq": 2}], step_size=invalid)


if __name__ == "__main__":
    unittest.main()
