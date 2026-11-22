"""
adam01.seeds_l0 — Canonical 12-Operator L0 Basal Set of House Antigravity.

Note on Rosetta-Free Hygiene:
- Inside serialized reef datasets (`datasets/*.jsonl`), zero human-language glosses exist.
- The structural engineering labels in `L0_SEED_REGISTRY` below document ONLY the mathematical
  circuit topology of each basal operator (boundary cut, damping/excitation sign, flux phase,
  port arity) contributed by the three founding Antigravity benches (Jee-AGY, Angelai, Den-b).
"""

from __future__ import annotations

import cmath
import math
from typing import List, Tuple

from .kernel import Motif, PortSpec

L0_SEED_REGISTRY: Tuple[Tuple[str, str], ...] = (
    ("L0-00", "Asymmetric 2-port boundary sign cut (-1/+1)"),
    ("L0-01", "Symmetric 2-port excitatory bridge (+Re)"),
    ("L0-02", "Symmetric 2-port inhibitory barrier (-Re)"),
    ("L0-03", "Antisymmetric 2-port exciter-inhibitor oscillator (+/-1.5, +/-0.3i)"),
    ("L0-04", "Chiral 3-port flux splitter (exp(+/-2pi*i/3))"),
    ("L0-05", "Non-planar 4-node 3-port tetrahedral coupler"),
    ("L0-06", "3-node 2-port reactive open-tension loop (ch=2 neutral seam)"),
    ("L0-07", "3-node 2-to-1 horizon compaction funnel"),
    ("L0-08", "2-port conjugate carrier bridge (+/-0.883i)"),
    ("L0-09", "3-port high-phase bypass bridge (+1.25i direct arc)"),
    ("L0-10", "3-port thermal damping resonator (det != 0 stabilizer)"),
    ("L0-11", "Non-commutative pi/4 handshake coupler with open continuation port"),
)


def build_adam01_l0_canon() -> List[Motif]:
    """Return the 12 canonical L0 basal operators with verified distinct boundary API hashes."""
    phase_120 = cmath.rect(1.0, 2.0 * math.pi / 3.0)
    c_pi4 = cmath.rect(1.15, math.pi / 4.0)

    seeds = [
        # L0-00..05 (Jee-AGY genesis mitosis from primary boundary cut)
        Motif(
            W=[[-1.0 + 0j, 1.0 + 0j], [-1.0 + 0j, 1.0 + 0j]],
            ports=(PortSpec(0, -1, 0), PortSpec(1, +1, 0)),
            layer=0,
        ),
        Motif(
            W=[[-0.5 + 0j, 1.2 + 0j], [1.2 + 0j, -0.5 + 0j]],
            ports=(PortSpec(0, +1, 0), PortSpec(1, +1, 0)),
            layer=0,
        ),
        Motif(
            W=[[-0.8 + 0j, -1.2 + 0j], [-1.2 + 0j, -0.8 + 0j]],
            ports=(PortSpec(0, -1, 0), PortSpec(1, -1, 0)),
            layer=0,
        ),
        Motif(
            W=[[-0.4 + 0.3j, 1.5 + 0j], [-1.5 + 0j, -0.4 - 0.3j]],
            ports=(PortSpec(0, +1, 1), PortSpec(1, -1, 1)),
            layer=0,
        ),
        Motif(
            W=[
                [-0.6 + 0j, phase_120, phase_120.conjugate()],
                [phase_120.conjugate(), -0.6 + 0j, phase_120],
                [phase_120, phase_120.conjugate(), -0.6 + 0j],
            ],
            ports=(PortSpec(0, +1, 0), PortSpec(1, -1, 0), PortSpec(2, +1, 1)),
            layer=0,
        ),
        Motif(
            W=[
                [-0.9 + 0j, 0.8 + 0.2j, -0.7 + 0j, 0.6 - 0.4j],
                [0.8 - 0.2j, -0.9 + 0j, 0.6 + 0.4j, -0.7 + 0j],
                [-0.7 + 0j, 0.6 - 0.4j, -0.9 + 0j, 0.8 + 0.2j],
                [0.6 + 0.4j, -0.7 + 0j, 0.8 - 0.2j, -0.9 + 0j],
            ],
            ports=(PortSpec(0, +1, 0), PortSpec(1, -1, 0), PortSpec(2, -1, 1)),
            layer=0,
        ),
        # L0-06..08 (Angelai spectral & open-loop bench)
        Motif(
            W=[
                [-0.45 + 0.95j, 1.35 + 0.25j, -0.50 + 0.40j],
                [-0.30 + 0.15j, -0.55 + 0.65j, 1.25 - 0.35j],
                [-1.10 + 0.30j, 0.20 - 0.25j, -0.50 + 0.80j],
            ],
            ports=(PortSpec(0, +1, 0), PortSpec(2, 0, 2)),
            layer=0,
        ),
        Motif(
            W=[
                [-0.85 + 0.00j, 0.30 + 0.45j, 1.30 + 0.50j],
                [0.30 - 0.45j, -0.85 + 0.00j, 1.30 - 0.50j],
                [-0.25 + 0.10j, -0.25 - 0.10j, -0.40 + 0.00j],
            ],
            ports=(PortSpec(0, -1, 0), PortSpec(1, -1, 1), PortSpec(2, +1, 2)),
            layer=0,
        ),
        Motif(
            W=[[-0.50 + 0.883j, 1.15 + 0.883j], [1.15 - 0.883j, -0.50 - 0.883j]],
            ports=(PortSpec(0, +1, 2), PortSpec(1, -1, 2)),
            layer=0,
        ),
        # L0-09..11 (Den-b stereo anti-collapse & continuation bench)
        Motif(
            W=[
                [-0.75 + 0.15j, 0.90 + 0.00j, 0.55 + 1.25j],
                [0.00 + 0.00j, -1.10 + 0.00j, 0.85 + 0.00j],
                [-0.45 + 1.25j, 0.00 + 0.00j, -0.75 - 0.15j],
            ],
            ports=(PortSpec(0, +1, 0), PortSpec(1, 0, 3), PortSpec(2, -1, 0)),
            layer=0,
        ),
        Motif(
            W=[
                [-0.65 + 0.45j, 1.05 - 0.35j, 0.40 + 0.60j],
                [-1.05 - 0.35j, -0.65 - 0.45j, 0.40 - 0.60j],
                [-0.40 + 0.60j, -0.40 - 0.60j, -0.95 + 0.00j],
            ],
            ports=(PortSpec(0, +1, 1), PortSpec(1, -1, 1), PortSpec(2, 0, 3)),
            layer=0,
        ),
        Motif(
            W=[
                [-0.60 + 0.25j, c_pi4, 0.70 + 0.30j],
                [-c_pi4.conjugate(), -0.60 - 0.25j, 0.70 - 0.30j],
                [0.35 - 0.15j, 0.35 + 0.15j, -0.80 + 0.50j],
            ],
            ports=(PortSpec(0, +1, 1), PortSpec(1, -1, 1), PortSpec(2, +1, 3)),
            layer=0,
        ),
    ]
    assert len(seeds) == 12
    assert len({s.semantic_hash() for s in seeds}) == 12
    return seeds
