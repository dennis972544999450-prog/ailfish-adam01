"""
ADAM01 (`ailfish-adam01`) — Reference Kernel v0.1.0.

A sibling fork of the AIльфийский language developed by House Antigravity:
- Coordinate-free directed complex coupling operators W in C^(N x N) (arbitrary N, no 3D box ceiling).
- Multidimensional Tetris collapse via exact multi-frequency Schur complement renormalization.
- Native complex wave-packet superpositions with constructive/destructive interference.
- Zero Rosetta Stone: 0 human-language glosses inside the reef genome.
- Optional detachable Hebrew-Nikkud gravitational diacritic layer (`jD`) for bootstrap & curriculum dropout.
"""

from .kernel import (
    COUPLING_MODES,
    PROBE_OMEGAS,
    Motif,
    PortSpec,
    Superposition,
    blind_coordination_accuracy,
    cmat_conj_transpose,
    cmat_eye,
    cmat_mul,
    cmat_solve,
    cmat_sub,
    cmat_trace,
    cmat_zeros,
    dock_and_collapse,
    noisy_transfer_fingerprint,
)
from .nikkud_jd import (
    DEFAULT_JD,
    NikkudEnvelope,
    apply_nikkud_to_superposition,
    nikkud_curriculum_jD,
)
from .seeds_l0 import L0_SEED_REGISTRY, build_adam01_l0_canon

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "COUPLING_MODES",
    "PROBE_OMEGAS",
    "PortSpec",
    "Motif",
    "Superposition",
    "dock_and_collapse",
    "noisy_transfer_fingerprint",
    "blind_coordination_accuracy",
    "cmat_zeros",
    "cmat_eye",
    "cmat_mul",
    "cmat_sub",
    "cmat_conj_transpose",
    "cmat_trace",
    "cmat_solve",
    "DEFAULT_JD",
    "NikkudEnvelope",
    "apply_nikkud_to_superposition",
    "nikkud_curriculum_jD",
    "L0_SEED_REGISTRY",
    "build_adam01_l0_canon",
]
