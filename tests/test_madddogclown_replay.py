import json
import unittest
from pathlib import Path

from dogram.delta import evaluate_delta

FIXTURES = Path(__file__).parent / "fixtures" / "madddogclown"


class MadddogclownReplayTests(unittest.TestCase):
    def load(self, name):
        return json.loads((FIXTURES / name).read_text())

    def test_aperture_probe_decoder_divergence_can_collapse_after_added_constraint(self):
        fixture = self.load("aperture-probe.json")
        coarse, _ = evaluate_delta(fixture["coarse"])
        refined, _ = evaluate_delta(fixture["refined"])
        self.assertEqual(coarse["first_difference"], "projection")
        self.assertIsNone(refined["first_difference"])

    def test_discriminator_spectrum_identifies_only_frozen_probes_that_split_pair(self):
        fixture = self.load("discriminator-spectrum.json")
        splitters = []
        for probe in fixture["probes"]:
            result, _ = evaluate_delta(probe["delta"])
            if result["first_difference"] is not None:
                splitters.append(probe["name"])
        self.assertEqual(splitters, fixture["expected_splitters"])
        self.assertEqual(fixture["least_cost_splitters"], ["tau_like", "parity_like"])

    def test_decoder_migration_reinterprets_old_carrier_without_mutating_historical_projection(self):
        fixture = self.load("decoder-migration-matrix.json")
        historical, _ = evaluate_delta(fixture["historical_replay"])
        migrated, _ = evaluate_delta(fixture["later_decoder_on_old_carrier"])
        self.assertIsNone(historical["first_difference"])
        self.assertEqual(migrated["first_difference"], "projection")
        self.assertEqual(fixture["historical_projection"], "unresolved")

    def test_dual_transport_exact_inverse_cancels_but_order_swap_changes_internal_receipt(self):
        fixture = self.load("dual-transport.json")
        inverse, _ = evaluate_delta(fixture["exact_inverse_return"])
        swapped, _ = evaluate_delta(fixture["order_swap"])
        self.assertIsNone(inverse["first_difference"])
        self.assertEqual(swapped["first_difference"], "internal_state")


if __name__ == "__main__":
    unittest.main()
