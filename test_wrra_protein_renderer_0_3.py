#!/usr/bin/env python3
import json
import subprocess
import sys
import unittest
from pathlib import Path

import wrra_protein_renderer_0_3 as renderer


ROOT = Path(__file__).resolve().parent


class RendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(ROOT / "wrra_protein_renderer_0_3.py")], check=True)
        cls.result = json.loads((ROOT / "WRRA_Motor_0.3_Renderer_Result.json").read_text())
        _, cls.h1 = renderer.read_single_fasta(ROOT / "WRRA_Motor_Calibration_H1.fasta")
        _, cls.h2 = renderer.read_single_fasta(ROOT / "WRRA_Motor_H2_candidates.fasta")
        _, cls.dna = renderer.read_single_fasta(ROOT / "WRRA_Motor_H2_top_DNA.fasta")
        cls.topology = json.loads((ROOT / "WRRA_Motor_H2_topology.json").read_text())

    def test_calibration_boundaries(self) -> None:
        self.assertEqual(len(self.h1), 382)
        self.assertEqual(len(self.h1[:353]), 353)
        self.assertEqual(len(self.h1[353:]), 29)

    def test_top_hybrid_ownership(self) -> None:
        self.assertEqual(len(self.h2), 385)
        self.assertEqual(self.h2[:353], self.h1[:353])
        self.assertNotEqual(self.h2[353:], self.h1[353:])
        self.assertIn("IFAYGQTSSGKT", self.h2[:353])

    def test_DNA_round_trip(self) -> None:
        self.assertEqual(len(self.dna), 1158)
        self.assertEqual(renderer.translate(self.dna), self.h2 + "*")

    def test_DNA_filters(self) -> None:
        config = renderer.yaml.safe_load(renderer.CONFIG_PATH.read_text())
        for site in config["DNA_renderer"]["forbidden_sites"]:
            self.assertNotIn(site, self.dna)
        gc = (self.dna.count("G") + self.dna.count("C")) / len(self.dna)
        self.assertGreaterEqual(gc, 0.55)
        self.assertLessEqual(gc, 0.61)
        self.assertLessEqual(renderer.longest_homopolymer(self.dna), 4)

    def test_fully_de_novo_fail_closed(self) -> None:
        self.assertEqual(
            self.result["N1_fully_de_novo"]["status"],
            "FAIL_CLOSED_NO_SEQUENCE_EMITTED",
        )

    def test_deterministic_top_candidate(self) -> None:
        self.assertEqual(self.result["search_summary"]["top_candidate"], "H2-b2f820d18e")

    def test_topology_keeps_atomic_boundary_open(self) -> None:
        self.assertEqual(self.topology["candidate_id"], "H2-b2f820d18e")
        self.assertEqual(len(self.topology["chains"]), 2)
        self.assertEqual(self.topology["atomic_coordinates"], "OPEN_NOT_PREDICTED")


if __name__ == "__main__":
    unittest.main()
