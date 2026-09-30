# WRRA-Motor H2

## From Minimal State Transitions to a Candidate Walking Protein and DNA

WRRA-Motor H2 is a reproducible research package that applies the frozen
**WRRA Core 1.0** framework to the problem of directional intracellular
walking. It derives a minimal two-contact state architecture under a declared
strict processivity contract, maps that architecture onto a hybrid kinesin
candidate, and emits auditable protein and DNA sequence candidates.

The top candidate, **H2-b2f820d18e**, is a 385-amino-acid hybrid composed of:

- residues 1-353: inherited human KIF5B motor segment;
- residues 354-385: designed 32-aa WRRA gate;
- candidate coding sequence: 1,158 nt including the stop codon.

> **Claim boundary:** H2 is `PREDICTED_SEQUENCE_ONLY`. Its atomic structure,
> folding, oligomeric state, ATPase activity, processive walking, and cellular
> cargo transport have not been experimentally demonstrated.

## Evaluation chain

The repository follows the fixed WRRA evaluation order:

| Stage | This repository |
| --- | --- |
| Verified input | Human KIF5B residues 1-353; microtubule polarity; ATP-driven motor context; declared WRRA Core 1.0 contract |
| WRRA-specific transformation | Strict always-attached walking contract -> two-contact Pareto minimum -> present-state coordination requirement -> constrained hybrid renderer |
| Output | H2-b2f820d18e protein sequence, 32-aa gate, 1,158-nt candidate CDS, topology hypothesis, ranked candidate ledger |
| Falsification conditions | Incorrect folding or oligomerization; loss of ATPase or microtubule binding; no processive motility; no distinction from generic or scrambled coiled-coil controls |

The research contribution is the WRRA-specific structural and computational
lineage connecting a minimum functional contract to topology, sequence, DNA,
and explicit tests. It does not depend on claiming that every inherited
biophysical fact or numerical value is newly discovered.

## Main result

| Item | Value | Claim grade |
| --- | ---: | --- |
| Candidate | H2-b2f820d18e | HYBRID / PREDICTED |
| Protein length | 385 aa | EXACT sequence output |
| Inherited KIF5B segment | 353 aa (91.69%) | INHERITED |
| Designed gate | `VQNIEQKIANLKEEGAAALQQVEQKIQNLKAE` | DESIGNED |
| Designed fraction | 32 aa (8.31%) | EXACT sequence accounting |
| CDS length | 1,158 nt including stop | PREDICTED |
| GC fraction | 0.5768566494 | Deterministic renderer output |
| Assembly | Parallel homodimer | TOPOLOGY_HYPOTHESIS_ONLY |
| Atomic coordinates | Not generated | OPEN_NOT_PREDICTED |
| Physical walking | Not measured | OPEN |

The renderer score `5.080564251100865` and `switch_proxy = 1.0` are transparent
sequence-ranking heuristics. They are not probabilities of folding or walking.

## Repository contents

```text
.
├── README.md
├── CITATION.cff
├── LICENSE
├── LICENSE-CODE
├── LICENSE-DOCUMENTATION.md
├── requirements.txt
├── wrra_motor_0_1.py
├── wrra_protein_renderer_0_3.py
├── test_wrra_protein_renderer_0_3.py
├── WRRA_Motor_0.1_Domain_Profile.yaml
├── WRRA_Motor_0.3_Renderer.yaml
├── WRRA_Motor_0.3_Renderer_Result.json
├── WRRA_Motor_Calibration_H1.fasta
├── WRRA_Motor_H2_candidates.fasta
├── WRRA_Motor_H2_top_DNA.fasta
├── WRRA_Motor_H2_topology.json
└── docs/
    ├── WRRA_Motor_H2_Integrated_Research_Report_Wonsik_Choi_v0.4_EN.pdf
    ├── WRRA_Motor_H2_Integrated_Research_Report_Wonsik_Choi_v0.4_EN.docx
    └── Korean development notes
```

## Reproduce the architecture calculation

Python 3.10 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python wrra_motor_0_1.py
```

The architecture script enumerates 64 combinations formed by one to four
contacts and four binary functional conditions. Under the declared strict
contract, the unique Pareto-minimal survivor is the coordinated two-contact
architecture.

## Reproduce the H2 sequence renderer

```bash
python wrra_protein_renderer_0_3.py
python -m unittest -v test_wrra_protein_renderer_0_3.py
```

The renderer uses the fixed random seed `260908`. A successful run must recover
`H2-b2f820d18e` as the top candidate and pass the protein-ownership, DNA
round-trip, forbidden-site, deterministic-output, topology-boundary, and
fail-closed tests.

Running the renderer rewrites these deterministic outputs:

- `WRRA_Motor_0.3_Renderer_Result.json`
- `WRRA_Motor_H2_candidates.fasta`
- `WRRA_Motor_H2_top_DNA.fasta`
- `WRRA_Motor_H2_topology.json`

## Validation roadmap

Computational validation should examine the monomer, parallel dimer,
nucleotide-dependent states, microtubule-bound complex, strain transfer, and
negative-design landscape. Experimental comparison should include:

- an active KIF5B positive control;
- KIF5B 1-353 without a gate;
- KIF5B 1-353 with an established GCN4-type dimerization segment;
- H2 with the designed WRRA gate;
- a length-matched generic coiled coil;
- a composition-preserving scrambled gate.

H2-specific support requires measurable recovery or differentiation in
expression, oligomer state, ATPase activity, microtubule landing, velocity,
run length, detachment, or load response.

## Safety and interpretation

The DNA file is a computational reverse-translation candidate, not a complete
expression cassette and not a synthesis-ready protocol. It excludes promoter,
Kozak sequence, UTRs, polyadenylation signal, vector backbone, tags, localization
signals, cargo-binding modules, and containment design.

This repository is intended for transparent computational research and critical
evaluation. Sequence output must not be presented as evidence of biological
function.

## WRRA reference

WRRA Core 1.0 is treated as frozen for this application.

- Zenodo DOI: <https://doi.org/10.5281/zenodo.22650956>

## Author

**Wonsik Choi**  
Independent researcher  
Email: janefather@gmail.com

## License

- Code: MIT License (`LICENSE-CODE`)
- Reports, notes, configuration, structured data, and sequence files:
  Creative Commons Attribution 4.0 International (`LICENSE-DOCUMENTATION.md`)

See `LICENSE` for the repository-wide dual-license notice.

---

## Central corpus index

This work is part of the open research and publishing corpus of **Wonsik Choi (최원식)**.

- [Central Research & Publications Index](https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-research-history/blob/main/PUBLICATIONS.md)
- [Public GitBook index](https://independent-research.gitbook.io/mcc-and-wrra-research-history/publications)
- [Machine-readable corpus index](https://github.com/Wonsik-Choi-janefather/minimal-computing-cosmology-research-history/blob/main/works.json)
- Identity: [janefather@gmail.com](mailto:janefather@gmail.com)

Rights remain those stated in this repository and its linked archival record.

**Copyright (C) 2026 Wonsik Choi**


**ORCID:** [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772)


**ORCID:** [0009-0001-4263-9772](https://orcid.org/0009-0001-4263-9772)
