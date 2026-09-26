#!/usr/bin/env python3
"""WRRA-Motor Protein Renderer 0.3.

Produces hybrid H2 candidates by preserving a validated motor/track core and
searching a transparent coiled-coil gate grammar.  It deliberately refuses to
emit a fully de novo autonomous N1 motor because no backbone generator,
multistate structure predictor, or mechanochemical validator is available.

Outputs are computational hypotheses, not synthesis-ready or experimentally
validated proteins.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "WRRA_Motor_0.3_Renderer.yaml"
CALIBRATION_FASTA = ROOT / "WRRA_Motor_Calibration_H1.fasta"
RESULT_JSON = ROOT / "WRRA_Motor_0.3_Renderer_Result.json"
PROTEIN_FASTA = ROOT / "WRRA_Motor_H2_candidates.fasta"
DNA_FASTA = ROOT / "WRRA_Motor_H2_top_DNA.fasta"
TOPOLOGY_JSON = ROOT / "WRRA_Motor_H2_topology.json"

HYDROPHOBIC = set("AILMFWVY")
POSITIVE = set("KR")
NEGATIVE = set("DE")

# Small, transparent codon menus. This is constraint-aware reverse translation,
# not a substitute for a host-specific commercial codon-optimization model.
CODONS = {
    "A": ("GCC", "GCT", "GCA"), "R": ("CGC", "CGG", "AGA"),
    "N": ("AAC", "AAT"), "D": ("GAC", "GAT"), "C": ("TGC", "TGT"),
    "Q": ("CAG", "CAA"), "E": ("GAG", "GAA"), "G": ("GGC", "GGT", "GGA"),
    "H": ("CAC", "CAT"), "I": ("ATC", "ATT", "ATA"), "L": ("CTG", "CTC", "TTG"),
    "K": ("AAG", "AAA"), "M": ("ATG",), "F": ("TTC", "TTT"),
    "P": ("CCC", "CCT", "CCG"), "S": ("AGC", "TCC", "TCT"),
    "T": ("ACC", "ACT", "ACA"), "W": ("TGG",), "Y": ("TAC", "TAT"),
    "V": ("GTG", "GTC", "GTT"),
}


def read_single_fasta(path: Path) -> tuple[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header = ""
    chunks: list[str] = []
    for line in lines:
        if line.startswith(">"):
            if header:
                break
            header = line[1:]
        elif header and line.strip():
            chunks.append(line.strip())
    if not header:
        raise ValueError(f"No FASTA record in {path}")
    sequence = "".join(chunks)
    return header, sequence


def entropy(sequence: str) -> float:
    counts = Counter(sequence)
    n = len(sequence)
    return -sum((v / n) * math.log(v / n, 2) for v in counts.values())


def maximum_hydrophobic_window(sequence: str, width: int = 9) -> float:
    if len(sequence) < width:
        return sum(x in HYDROPHOBIC for x in sequence) / len(sequence)
    return max(
        sum(x in HYDROPHOBIC for x in sequence[i:i + width]) / width
        for i in range(len(sequence) - width + 1)
    )


def make_heptad(rng: random.Random, index: int) -> str:
    # a,d: hydrophobic seam; e,g: complementary electrostatics.
    a = rng.choice("LIV")
    d = rng.choice("LIV")
    b = rng.choice("AQEK")
    c = rng.choice("AQEN")
    f = rng.choice("AQEK")
    if index % 2 == 0:
        e, g = "E", "K"
    else:
        e, g = "K", "E"
    return "".join((a, b, c, d, e, f, g))


def make_gate(rng: random.Random, heptads: int, hinge: str) -> str:
    blocks = [make_heptad(rng, i) for i in range(heptads)]
    midpoint = heptads // 2
    return "".join(blocks[:midpoint]) + hinge + "".join(blocks[midpoint:])


def gate_metrics(sequence: str, heptads: int, hinge: str) -> dict[str, float | bool]:
    hinge_start = 7 * (heptads // 2)
    has_hinge = sequence[hinge_start:hinge_start + len(hinge)] == hinge
    stripped = sequence[:hinge_start] + sequence[hinge_start + len(hinge):]
    blocks = [stripped[i:i + 7] for i in range(0, len(stripped), 7)]
    core_positions = [b[p] for b in blocks for p in (0, 3)]
    core_fraction = sum(x in HYDROPHOBIC for x in core_positions) / len(core_positions)
    salt_fraction = sum(
        ((b[4] in NEGATIVE and b[6] in POSITIVE) or
         (b[4] in POSITIVE and b[6] in NEGATIVE))
        for b in blocks
    ) / len(blocks)
    outside_hinge = stripped
    proline_free = "P" not in outside_hinge
    charge_density = sum(x in POSITIVE | NEGATIVE for x in sequence) / len(sequence)
    max_hydro = maximum_hydrophobic_window(sequence)
    diversity = entropy(sequence) / math.log(20, 2)
    # A transparent proxy only: stable heptads on both sides plus a localized
    # stutter/hinge. It is not a predicted conformational free-energy gap.
    switch_proxy = 0.5 * (core_fraction + salt_fraction) if has_hinge else 0.0
    score = (
        2.5 * core_fraction + 1.5 * salt_fraction + 0.8 * switch_proxy
        + 0.4 * diversity - 1.5 * max(0.0, max_hydro - 0.67)
        - 0.5 * max(0.0, charge_density - 0.35)
    )
    return {
        "core_fraction": core_fraction,
        "salt_fraction": salt_fraction,
        "proline_free": proline_free,
        "charge_density": charge_density,
        "maximum_hydrophobic_window": max_hydro,
        "normalized_entropy": diversity,
        "switch_proxy": switch_proxy,
        "heuristic_score": score,
        "has_declared_hinge": has_hinge,
    }


def passes_gate(metrics: dict[str, float | bool], max_charge: float) -> bool:
    return bool(
        metrics["core_fraction"] == 1.0
        and metrics["salt_fraction"] == 1.0
        and metrics["proline_free"]
        and metrics["has_declared_hinge"]
        and float(metrics["charge_density"]) <= max_charge
    )


def longest_homopolymer(sequence: str) -> int:
    longest = current = 1
    for left, right in zip(sequence, sequence[1:]):
        current = current + 1 if left == right else 1
        longest = max(longest, current)
    return longest


def reverse_translate(protein: str, target_gc: float, forbidden: list[str]) -> str:
    dna = ""
    for aa in protein:
        choices = CODONS[aa]
        scored: list[tuple[float, str]] = []
        for codon in choices:
            trial = dna + codon
            gc = (trial.count("G") + trial.count("C")) / len(trial)
            new_forbidden = sum(site in trial[-(len(site) + 3):] for site in forbidden)
            run_penalty = max(0, longest_homopolymer(trial[-12:]) - 4)
            score = abs(gc - target_gc) + 8.0 * new_forbidden + 2.0 * run_penalty
            scored.append((score, codon))
        dna += min(scored)[1]
    return dna


def translate(dna: str) -> str:
    inverse = {codon: aa for aa, codon_list in CODONS.items() for codon in codon_list}
    inverse.update({"TAA": "*", "TAG": "*", "TGA": "*"})
    return "".join(inverse[dna[i:i + 3]] for i in range(0, len(dna), 3))


def wrap(sequence: str, width: int = 80) -> str:
    return "\n".join(sequence[i:i + width] for i in range(0, len(sequence), width))


def main() -> None:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    _, calibration = read_single_fasta(CALIBRATION_FASTA)
    core = calibration[:353]
    gcn4 = calibration[353:]

    required_motif = config["hard_filters"]["require_p_loop_motif"]
    assert len(core) == 353 and len(gcn4) == 29
    assert required_motif in core

    search = config["search"]
    rng = random.Random(config["renderer"]["seed"])
    candidates = []
    seen = set()
    while len(candidates) < search["candidates"]:
        gate = make_gate(rng, search["heptads"], search["hinge"])
        if gate in seen:
            continue
        seen.add(gate)
        metrics = gate_metrics(gate, search["heptads"], search["hinge"])
        if not passes_gate(metrics, config["hard_filters"]["maximum_gate_charge_density"]):
            continue
        full = core + gate
        candidate_id = "H2-" + hashlib.sha256(full.encode()).hexdigest()[:10]
        candidates.append({
            "candidate_id": candidate_id,
            "gate_sequence": gate,
            "protein_sequence": full,
            "protein_length": len(full),
            "metrics": metrics,
            "ownership": {
                "residues_1_353": "INHERITED_KIF5B_P33176",
                f"residues_354_{len(full)}": "DESIGNED_HEPTAD_GATE",
            },
            "claim": "PREDICTED_SEQUENCE_ONLY",
        })

    candidates.sort(
        key=lambda x: (
            -float(x["metrics"]["heuristic_score"]),
            float(x["metrics"]["maximum_hydrophobic_window"]),
            x["candidate_id"],
        )
    )
    top = candidates[:search["keep_top"]]

    dna_cfg = config["DNA_renderer"]
    top_dna = reverse_translate(top[0]["protein_sequence"], dna_cfg["target_GC"], dna_cfg["forbidden_sites"])
    top_dna += dna_cfg["append_stop"]
    assert translate(top_dna) == top[0]["protein_sequence"] + "*"
    assert not any(site in top_dna for site in dna_cfg["forbidden_sites"])
    gc = (top_dna.count("G") + top_dna.count("C")) / len(top_dna)

    result = {
        "renderer": config["renderer"],
        "calibration": {
            "H1_length": len(calibration),
            "inherited_core_length": len(core),
            "GCN4_length": len(gcn4),
            "status": "CALIBRATION_NOT_NOVEL",
        },
        "search_summary": {
            "generated_and_passed": len(candidates),
            "reported": len(top),
            "top_candidate": top[0]["candidate_id"],
        },
        "top_candidates": [
            {k: v for k, v in item.items() if k != "protein_sequence"}
            for item in top
        ],
        "top_DNA": {
            "candidate_id": top[0]["candidate_id"],
            "coding_nt_including_stop": len(top_dna),
            "GC_fraction": gc,
            "longest_homopolymer": longest_homopolymer(top_dna),
            "forbidden_sites_present": [],
            "status": "PREDICTED_NOT_SYNTHESIS_READY",
        },
        "N1_fully_de_novo": {
            "status": "FAIL_CLOSED_NO_SEQUENCE_EMITTED",
            "missing_validators": [
                "de_novo ATPase and track-binding backbone generator",
                "multistate complex structure prediction",
                "ATP-state free-energy calculation",
                "microtubule-bound mechanochemical-cycle simulation",
                "experimental expression and single-molecule motility",
            ],
        },
    }

    RESULT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    protein_records = []
    for item in top:
        protein_records.append(
            f">{item['candidate_id']} H2_hybrid; 1-353=INHERITED_KIF5B; "
            f"354-{item['protein_length']}=DESIGNED_GATE; PREDICTED_ONLY\n"
            + wrap(item["protein_sequence"])
        )
    PROTEIN_FASTA.write_text("\n".join(protein_records) + "\n", encoding="utf-8")
    DNA_FASTA.write_text(
        f">{top[0]['candidate_id']}_CDS generic_human_reverse_translation; "
        "PREDICTED_NOT_SYNTHESIS_READY; includes_stop\n" + wrap(top_dna) + "\n",
        encoding="utf-8",
    )
    topology = {
        "candidate_id": top[0]["candidate_id"],
        "assembly_hypothesis": "parallel homodimer of two identical 385-aa chains",
        "chains": [
            {
                "chain": chain,
                "length_aa": 385,
                "regions": [
                    {"residues": "1-328", "role": "motor and polar-track-binding core", "ownership": "INHERITED"},
                    {"residues": "329-353", "role": "neck/coupling junction", "ownership": "INHERITED"},
                    {"residues": "354-385", "role": "designed dimeric gate", "ownership": "DESIGNED"},
                ],
            }
            for chain in ("A", "B")
        ],
        "state_cycle_hypothesis": [
            {"state": "S0", "contact_A": "bound-rear", "contact_B": "bound-front"},
            {"state": "S1", "contact_A": "mobile", "contact_B": "bound-anchor"},
            {"state": "S2", "contact_A": "bound-new-front", "contact_B": "bound-rear"},
        ],
        "atomic_coordinates": "OPEN_NOT_PREDICTED",
        "claim": "TOPOLOGY_HYPOTHESIS_ONLY",
    }
    TOPOLOGY_JSON.write_text(json.dumps(topology, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(result["search_summary"], indent=2))
    print(json.dumps(result["top_DNA"], indent=2))
    print(json.dumps(result["N1_fully_de_novo"], indent=2))


if __name__ == "__main__":
    main()
