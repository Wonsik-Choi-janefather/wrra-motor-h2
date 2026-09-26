#!/usr/bin/env python3
"""WRRA-Motor 0.1: architecture-level minimal walking model.

This model deliberately does not contain kinesin, dynein, or myosin sequence
information.  It enumerates generic walkers on a polar discrete track and
separates strict processive walking from relaxed flashing-ratchet motion.

The model establishes conditional architecture claims only; it does not
predict a fold, an amino-acid sequence, or experimental motility.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from math import ceil, exp, log


@dataclass(frozen=True)
class Architecture:
    contacts: int
    driven: bool
    polar_coupling: bool
    present_record: bool
    coordinated: bool

    @property
    def cost(self) -> tuple[int, int, int]:
        """Lexically neutral complexity vector: contacts, controls, drive."""
        controls = sum((self.polar_coupling, self.present_record, self.coordinated))
        return self.contacts, controls, int(self.driven)


def cycle_affinity(a: Architecture, chemical_affinity: float, load_work: float) -> float:
    """Dimensionless cycle affinity in units of kBT."""
    if not (a.driven and a.polar_coupling):
        return 0.0
    return chemical_affinity - load_work


def forward_probability(affinity: float) -> float:
    """Local-detailed-balance two-outcome probability."""
    return 1.0 / (1.0 + exp(-affinity))


def expected_step(affinity: float, lattice_spacing: float = 1.0) -> float:
    p_forward = forward_probability(affinity)
    return lattice_spacing * (2.0 * p_forward - 1.0)


def strict_processive(a: Architecture) -> bool:
    """At least one contact stays attached during every discrete-site exchange."""
    return (
        a.contacts >= 2
        and a.present_record
        and a.coordinated
        and a.driven
        and a.polar_coupling
    )


def directional(a: Architecture, chemical_affinity: float, load_work: float) -> bool:
    return expected_step(cycle_affinity(a, chemical_affinity, load_work)) > 0.0


def survival_probability(a: Architecture, steps: int, q: float) -> float:
    """Coarse exposure model.

    q is the probability that one exposed contact is lost in an exchange
    window.  Coordinated n-contact walkers fail only if all n protections are
    lost in that window; uncoordinated walkers receive no multiplicative
    protection.  This is a sensitivity model, not a fitted kinetic law.
    """
    exponent = a.contacts if a.coordinated and a.present_record else 1
    per_cycle_failure = q**exponent
    return (1.0 - per_cycle_failure) ** steps


def minimum_contacts_for_survival(steps: int, q: float, target: float) -> int:
    """Minimum n satisfying (1-q**n)**steps >= target."""
    if not (0.0 < q < 1.0 and 0.0 < target < 1.0 and steps > 0):
        raise ValueError("Require steps>0 and q,target strictly between 0 and 1")
    threshold = 1.0 - target ** (1.0 / steps)
    return max(1, ceil(log(threshold) / log(q)))


def enumerate_architectures() -> list[Architecture]:
    return [
        Architecture(n, driven, polar, record, coordinated)
        for n, driven, polar, record, coordinated in product(
            range(1, 5), (False, True), (False, True), (False, True), (False, True)
        )
    ]


def pareto_front(items: list[Architecture]) -> list[Architecture]:
    front: list[Architecture] = []
    for item in items:
        dominated = any(
            all(x <= y for x, y in zip(other.cost, item.cost))
            and any(x < y for x, y in zip(other.cost, item.cost))
            for other in items
        )
        if not dominated:
            front.append(item)
    return front


def main() -> None:
    chemical_affinity = 4.0
    load_work = 1.0
    candidates = [
        a
        for a in enumerate_architectures()
        if strict_processive(a) and directional(a, chemical_affinity, load_work)
    ]
    front = pareto_front(candidates)

    assert len(candidates) == 3
    assert len(front) == 1
    assert front[0] == Architecture(2, True, True, True, True)
    assert expected_step(0.0) == 0.0
    assert expected_step(-1.0) < 0.0
    assert not strict_processive(Architecture(1, True, True, True, True))

    print("WRRA-Motor 0.1 architecture enumeration")
    print(f"strict viable architectures: {len(candidates)}")
    print("Pareto-minimal strict architectures:")
    for a in front:
        print(asdict(a), "cost=", a.cost)

    print("\nSurvival sensitivity over 100 steps")
    print("contacts,q=0.01,q=0.05,q=0.10")
    for n in (1, 2, 3, 4):
        a = Architecture(n, True, True, True, True)
        values = [survival_probability(a, 100, q) for q in (0.01, 0.05, 0.10)]
        print(f"{n}," + ",".join(f"{v:.8f}" for v in values))

    affinity = cycle_affinity(front[0], chemical_affinity, load_work)
    print("\nDirectionality check")
    print(f"dimensionless affinity={affinity:.3f}")
    print(f"forward probability={forward_probability(affinity):.8f}")
    print(f"expected lattice steps/cycle={expected_step(affinity):.8f}")

    print("\nMinimum contacts for >=90% survival over 100 steps")
    for q in (0.01, 0.05, 0.10, 0.20):
        print(f"q={q:.2f},n_min={minimum_contacts_for_survival(100, q, 0.90)}")


if __name__ == "__main__":
    main()
