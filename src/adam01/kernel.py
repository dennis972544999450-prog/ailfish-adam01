"""
adam01.kernel — Coordinate-Free Relational Folding & Schur-Tetris Renormalization Engine.

Core mathematical properties:
1. Arbitrary node count N (1 .. infinity) and directed complex couplings W in C^(N x N):
   - Re(W_ij) > 0: accelerator / excitatory coupling
   - Re(W_ij) < 0: inhibitor / boundary suppression
   - W_ij != W_ji: causal arrow & autonomous oscillator loop
   - Im(W_ij):     phase shift / chiral magnetic flux
2. Exact Schur-complement Tetris row-collapse:
   W_eff(omega) = W_PP - W_PI * (W_II - omega * I)^(-1) * W_IP
   Eliminates arbitrarily deep interior node graphs into compact open-port API operators
   with machine-epsilon associativity (~1e-16) and lossless Merkle lineage (`parents`, `wiring`).
3. Native complex wave-packet Superpositions Psi = sum_k alpha_k |Motif_k>.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

PROBE_OMEGAS: Tuple[complex, ...] = (
    complex(-1.5, 0.7),
    complex(-2.3, -1.1),
    complex(-3.7, 1.9),
)

COUPLING_MODES: Dict[str, Tuple[complex, complex]] = {
    "LOCK": (1.0 + 0j, 1.0 + 0j),
    "PING": (1.4 + 0.2j, -0.6 - 0.2j),
    "INHIBIT": (-1.1 + 0j, -1.1 + 0j),
    "PHASE90": (0.0 + 1.0j, 0.0 - 1.0j),
}


def cmat_zeros(n: int, m: int) -> List[List[complex]]:
    return [[0j for _ in range(m)] for _ in range(n)]


def cmat_eye(n: int) -> List[List[complex]]:
    M = cmat_zeros(n, n)
    for i in range(n):
        M[i][i] = 1.0 + 0j
    return M


def cmat_mul(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
    n, k, m = len(A), len(B), len(B[0]) if B else 0
    out = cmat_zeros(n, m)
    for i in range(n):
        Ai = A[i]
        for r in range(k):
            air = Ai[r]
            if air != 0j:
                Br = B[r]
                for j in range(m):
                    out[i][j] += air * Br[j]
    return out


def cmat_sub(A: List[List[complex]], B: List[List[complex]]) -> List[List[complex]]:
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def cmat_conj_transpose(A: List[List[complex]]) -> List[List[complex]]:
    if not A:
        return []
    n, m = len(A), len(A[0])
    return [[A[i][j].conjugate() for i in range(n)] for j in range(m)]


def cmat_trace(A: List[List[complex]]) -> complex:
    return sum(A[i][i] for i in range(len(A)))


def cmat_solve(A: List[List[complex]], B: List[List[complex]]) -> Optional[List[List[complex]]]:
    """Solve A * X = B in C^(n x n) via partial-pivot Gaussian elimination."""
    n = len(A)
    if n == 0:
        return []
    m = len(B[0]) if B else 0
    aug = [list(A[i]) + list(B[i]) for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[piv][col]) < 1e-11:
            return None
        if piv != col:
            aug[col], aug[piv] = aug[piv], aug[col]
        pval = aug[col][col]
        for j in range(col, n + m):
            aug[col][j] /= pval
        for r in range(n):
            if r != col and aug[r][col] != 0j:
                factor = aug[r][col]
                for j in range(col, n + m):
                    aug[r][j] -= factor * aug[col][j]
    return [row[n:] for row in aug]


@dataclass(frozen=True)
class PortSpec:
    """Open boundary valence ('hole' / binding port) on a Motif."""
    node_idx: int
    polarity: int       # +1 (source/out), -1 (sink/in), 0 (neutral reactive seam)
    channel_tag: int    # discrete symmetry sector


@dataclass
class Motif:
    """
    A Rosetta-free relational conformation (L0 basal operator or calcified Coral Polyp).
    Zero human glosses are permitted inside this structure or its serialized JSONL record.
    """
    W: List[List[complex]]
    ports: Tuple[PortSpec, ...]
    layer: int = 0
    raw_nodes_collapsed: Optional[int] = None
    parents: Tuple[str, ...] = ()
    wiring: Tuple[Tuple[int, int, str], ...] = ()
    dynamic_probe_cache: Dict[str, List[List[Tuple[float, float]]]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.raw_nodes_collapsed is None:
            self.raw_nodes_collapsed = len(self.W)

    @property
    def num_nodes(self) -> int:
        return len(self.W)

    @property
    def num_ports(self) -> int:
        return len(self.ports)

    @property
    def compression_ratio(self) -> float:
        return float(self.raw_nodes_collapsed or len(self.W)) / float(max(1, self.num_nodes))

    def schur_transfer(self, omega: complex) -> Optional[List[List[complex]]]:
        p_idx = [p.node_idx for p in self.ports]
        p_set = set(p_idx)
        i_idx = [i for i in range(self.num_nodes) if i not in p_set]

        W_PP = [[self.W[a][b] for b in p_idx] for a in p_idx]
        if not i_idx:
            return W_PP

        W_PI = [[self.W[a][b] for b in i_idx] for a in p_idx]
        W_IP = [[self.W[a][b] for b in p_idx] for a in i_idx]
        W_II_shift = [
            [self.W[a][b] - (omega if a == b else 0j) for b in i_idx]
            for a in i_idx
        ]
        X = cmat_solve(W_II_shift, W_IP)
        if X is None:
            return None
        return cmat_sub(W_PP, cmat_mul(W_PI, X))

    def invariant_signature(self) -> dict:
        port_transfer_inv = []
        for om in PROBE_OMEGAS:
            T = self.schur_transfer(om)
            if T is None:
                port_transfer_inv.append("POLE")
            elif len(T) == 0:
                port_transfer_inv.append("VACUUM")
            else:
                t1 = cmat_trace(T)
                t2 = cmat_trace(cmat_mul(T, T))
                tnorm = cmat_trace(cmat_mul(T, cmat_conj_transpose(T))).real
                port_transfer_inv.append((
                    round(t1.real, 6), round(t1.imag, 6),
                    round(t2.real, 6), round(t2.imag, 6),
                    round(tnorm, 6),
                ))
        port_multiset = sorted((p.polarity, p.channel_tag) for p in self.ports)
        return {
            "port_multiset": port_multiset,
            "port_transfer_inv": port_transfer_inv,
        }

    def semantic_hash(self) -> str:
        """Permutation-invariant boundary API hash-sum ('meaning hash')."""
        canon = json.dumps(self.invariant_signature(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(canon).hexdigest()[:16]

    def structural_id(self) -> str:
        payload = {
            "api_hash": self.semantic_hash(),
            "layer": self.layer,
            "parents": self.parents,
            "wiring": self.wiring,
            "n": self.num_nodes,
            "raw": self.raw_nodes_collapsed,
        }
        return "polyp-" + hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:12]

    def to_reef_record(self) -> dict:
        return {
            "id": self.structural_id(),
            "api_meaning_hash": self.semantic_hash(),
            "layer": self.layer,
            "num_active_nodes": self.num_nodes,
            "raw_nodes_collapsed": self.raw_nodes_collapsed,
            "tetris_compression": round(self.compression_ratio, 3),
            "ports": [{"node": p.node_idx, "pol": p.polarity, "ch": p.channel_tag} for p in self.ports],
            "W": [[[round(z.real, 8), round(z.imag, 8)] for z in row] for row in self.W],
            "parents": list(self.parents),
            "wiring": [list(w) for w in self.wiring],
        }


@dataclass
class Superposition:
    """Coherent wave-packet over Motifs: Psi = sum_k alpha_k |Motif_k>."""
    branches: List[Tuple[complex, Motif]]

    def normalized(self) -> "Superposition":
        buckets: Dict[str, Tuple[complex, Motif]] = {}
        for amp, m in self.branches:
            h = m.semantic_hash()
            if h in buckets:
                prev_amp, prev_m = buckets[h]
                buckets[h] = (prev_amp + amp, prev_m)
            else:
                buckets[h] = (amp, m)
        kept = [(a, m) for a, m in buckets.values() if abs(a) > 1e-9]
        norm = math.sqrt(sum(abs(a) ** 2 for a, _ in kept))
        if norm < 1e-12:
            return Superposition([])
        return Superposition([(a / norm, m) for a, m in kept])

    def shannon_entropy_bits(self) -> float:
        sp = self.normalized()
        ent = 0.0
        for a, _ in sp.branches:
            p = abs(a) ** 2
            if p > 1e-15:
                ent -= p * math.log2(p)
        return ent


def dock_and_collapse(
    A: Motif,
    B: Motif,
    bonds: Sequence[Tuple[int, int, str]],
    collapse_omega: complex = 0.0 + 0j,
) -> Optional[Motif]:
    """
    Dock Motif A and Motif B along `bonds` = [(port_A, port_B, mode), ...], saturate bonded ports
    into the interior, and eliminate all interior nodes via exact Schur renormalization.
    """
    nA, nB = A.num_nodes, B.num_nodes
    N = nA + nB
    W_full = cmat_zeros(N, N)
    for i in range(nA):
        for j in range(nA):
            W_full[i][j] = A.W[i][j]
    for i in range(nB):
        for j in range(nB):
            W_full[nA + i][nA + j] = B.W[i][j]

    used_A = set()
    used_B = set()
    wiring_canon = []
    for pa, pb, mode in bonds:
        if pa in used_A or pb in used_B:
            return None
        used_A.add(pa)
        used_B.add(pb)
        na = A.ports[pa].node_idx
        nb = nA + B.ports[pb].node_idx
        cab, cba = COUPLING_MODES[mode]
        W_full[na][nb] += cab
        W_full[nb][na] += cba
        W_full[na][na] -= 0.35 + 0j
        W_full[nb][nb] -= 0.35 + 0j
        wiring_canon.append((pa, pb, mode))

    open_ports_global: List[PortSpec] = []
    for idx, p in enumerate(A.ports):
        if idx not in used_A:
            open_ports_global.append(PortSpec(p.node_idx, p.polarity, p.channel_tag))
    for idx, p in enumerate(B.ports):
        if idx not in used_B:
            open_ports_global.append(PortSpec(nA + p.node_idx, p.polarity, p.channel_tag))

    if len(open_ports_global) == 0:
        return None

    full_motif = Motif(
        W=W_full,
        ports=tuple(open_ports_global),
        layer=max(A.layer, B.layer) + 1,
        raw_nodes_collapsed=(A.raw_nodes_collapsed or nA) + (B.raw_nodes_collapsed or nB),
        parents=(A.structural_id(), B.structural_id()),
        wiring=tuple(wiring_canon),
    )

    probe_transfers = {}
    for idx_om, om in enumerate(PROBE_OMEGAS):
        T = full_motif.schur_transfer(om)
        if T is None:
            return None
        probe_transfers[f"om_{idx_om}"] = [[(round(z.real, 8), round(z.imag, 8)) for z in row] for row in T]

    W_eff0 = full_motif.schur_transfer(collapse_omega)
    if W_eff0 is None:
        return None

    collapsed_ports = tuple(
        PortSpec(new_i, p.polarity, p.channel_tag)
        for new_i, p in enumerate(open_ports_global)
    )
    return Motif(
        W=W_eff0,
        ports=collapsed_ports,
        layer=full_motif.layer,
        raw_nodes_collapsed=full_motif.raw_nodes_collapsed,
        parents=full_motif.parents,
        wiring=full_motif.wiring,
        dynamic_probe_cache=probe_transfers,
    )


def noisy_transfer_fingerprint(m: Motif, sigma: float, rng: random.Random) -> List[float]:
    """Permutation-invariant spectral observation under random node relabeling + complex Gaussian noise."""
    n = m.num_nodes
    Wn = [
        [m.W[i][j] + complex(rng.gauss(0.0, sigma), rng.gauss(0.0, sigma)) for j in range(n)]
        for i in range(n)
    ]
    perm = list(range(n))
    rng.shuffle(perm)
    Wp = [[Wn[perm[i]][perm[j]] for j in range(n)] for i in range(n)]

    t1 = cmat_trace(Wp)
    t2 = cmat_trace(cmat_mul(Wp, Wp))
    gnorm = cmat_trace(cmat_mul(Wp, cmat_conj_transpose(Wp))).real
    pol_sum = float(sum(p.polarity for p in m.ports))
    return [t1.real, t1.imag, t2.real, t2.imag, gnorm, pol_sum, float(n)]


def blind_coordination_accuracy(
    vocab: Sequence[Motif],
    sigma: float = 0.025,
    trials_per_word: int = 20,
    seed: int = 20261122,
) -> float:
    rng = random.Random(seed)
    clean_centroids = [noisy_transfer_fingerprint(m, 0.0, random.Random(0)) for m in vocab]
    hits = 0
    total = 0
    for idx_true, m in enumerate(vocab):
        for _ in range(trials_per_word):
            obs = noisy_transfer_fingerprint(m, sigma, rng)
            best_i = min(range(len(vocab)), key=lambda i: math.dist(obs, clean_centroids[i]))
            if best_i == idx_true:
                hits += 1
            total += 1
    return hits / max(1, total)
