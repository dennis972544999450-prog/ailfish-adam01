"""
adam01.nikkud_jd — Detachable Hebrew-Nikkud (נִקּוּד) Gravitational Diacritic Layer (jD).

- Preserves the underlying consonantal root (`consonantal_root_hash` == `motif.semantic_hash()`).
- Guides learner reading & disambiguates homograph Superpositions during early bootstrap (`jD = 0.137`).
- Smoothly anneals to `jD = 0.0` (`nikkud_curriculum_jD`) as phrase context takes over in adult fluency,
  detaching cleanly with zero bit-level residue.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from .kernel import Motif, Superposition

DEFAULT_JD: float = 0.137


@dataclass(frozen=True)
class NikkudEnvelope:
    consonantal_motif: Motif
    node_weights: Tuple[float, ...]
    jD: float = DEFAULT_JD

    @property
    def consonantal_root_hash(self) -> str:
        return self.consonantal_motif.semantic_hash()

    def strip_nikkud(self) -> Motif:
        return self.consonantal_motif

    def vocalized_reading_operator(self) -> Motif:
        m = self.consonantal_motif
        n = m.num_nodes
        if self.jD <= 0.0:
            return Motif(
                W=[list(row) for row in m.W],
                ports=m.ports,
                layer=m.layer,
                raw_nodes_collapsed=m.raw_nodes_collapsed,
                parents=m.parents,
                wiring=m.wiring,
            )

        assert len(self.node_weights) == n, f"Expected {n} nikkud weights, got {len(self.node_weights)}"
        masses = [max(0.0, float(w)) for w in self.node_weights]
        W_voc: List[List[complex]] = [list(row) for row in m.W]

        for i in range(n):
            mi = masses[i]
            well = 0.0
            for k in range(n):
                if i == k:
                    continue
                mk = masses[k]
                prox = 1.0 + abs(m.W[i][k]) + abs(m.W[k][i])
                pull = self.jD * (mi * mk) * (mk / max(1e-12, mi + mk))
                W_voc[i][k] += complex(pull, 0.0)
                well += self.jD * (mi * mk) * 0.5 * prox
            self_redshift = self.jD * max(0.0, mi * mi - 1.0) * 0.5
            W_voc[i][i] -= complex(well + self_redshift, 0.0)

        return Motif(
            W=W_voc,
            ports=m.ports,
            layer=m.layer,
            raw_nodes_collapsed=m.raw_nodes_collapsed,
            parents=m.parents,
            wiring=m.wiring,
        )


def apply_nikkud_to_superposition(
    homograph_packet: Superposition,
    branch_salience: Sequence[float],
    jD: float = DEFAULT_JD,
) -> Superposition:
    assert len(branch_salience) == len(homograph_packet.branches)
    if jD <= 0.0:
        return homograph_packet.normalized()
    tilted = [
        (amp * math.exp(jD * float(sal)), motif)
        for (amp, motif), sal in zip(homograph_packet.branches, branch_salience)
    ]
    return Superposition(tilted).normalized()


def nikkud_curriculum_jD(
    step: int,
    warmup_steps: int = 300,
    adult_step: int = 1000,
    jD_init: float = DEFAULT_JD,
) -> float:
    if step <= warmup_steps:
        return jD_init
    if step >= adult_step:
        return 0.0
    prog = (step - warmup_steps) / float(max(1, adult_step - warmup_steps))
    return jD_init * 0.5 * (1.0 + math.cos(math.pi * prog))
