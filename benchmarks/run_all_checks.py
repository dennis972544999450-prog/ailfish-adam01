#!/usr/bin/env python3
"""
Deterministic verification suite & canonical dataset builder for ADAM01 v0.1.0.
Pure Python 3.9+ standard library (zero external dependencies required).
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib
import random
import sys

sys.dont_write_bytecode = True

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from adam01 import (  # noqa: E402
    COUPLING_MODES,
    DEFAULT_JD,
    PROBE_OMEGAS,
    Motif,
    NikkudEnvelope,
    PortSpec,
    Superposition,
    apply_nikkud_to_superposition,
    blind_coordination_accuracy,
    build_adam01_l0_canon,
    cmat_zeros,
    dock_and_collapse,
    nikkud_curriculum_jD,
    noisy_transfer_fingerprint,
)

DATASETS_DIR = REPO_ROOT / "datasets"


def verify_all_and_build_datasets() -> dict:
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    l0 = build_adam01_l0_canon()

    # 1. Check 1: Exact Schur-Tetris Associativity (< 1e-14)
    s0, s3, s4 = l0[0], l0[3], l0[4]
    p1 = dock_and_collapse(s0, s4, [(1, 1, "PING")], collapse_omega=PROBE_OMEGAS[0])
    assert p1 is not None
    p2 = dock_and_collapse(p1, s3, [(1, 0, "LOCK")], collapse_omega=PROBE_OMEGAS[0])
    assert p2 is not None

    W7 = cmat_zeros(7, 7)
    for i in range(2):
        for j in range(2):
            W7[i][j] = s0.W[i][j]
    for i in range(3):
        for j in range(3):
            W7[2 + i][2 + j] = s4.W[i][j]
    for i in range(2):
        for j in range(2):
            W7[5 + i][5 + j] = s3.W[i][j]
    cab1, cba1 = COUPLING_MODES["PING"]
    W7[1][3] += cab1
    W7[3][1] += cba1
    W7[1][1] -= 0.35
    W7[3][3] -= 0.35
    cab2, cba2 = COUPLING_MODES["LOCK"]
    W7[2][5] += cab2
    W7[5][2] += cba2
    W7[2][2] -= 0.35
    W7[5][5] -= 0.35

    raw7 = Motif(W=W7, ports=(PortSpec(0, -1, 0), PortSpec(4, +1, 1), PortSpec(6, -1, 1)), layer=2, raw_nodes_collapsed=7)
    T7 = raw7.schur_transfer(PROBE_OMEGAS[0])
    assert T7 is not None
    schur_err = max(abs(p2.W[i][j] - T7[i][j]) for i in range(3) for j in range(3))
    assert schur_err < 1e-14, f"Schur associativity error too large: {schur_err}"

    # 2. Check 2: Deep L10 Tetris Chain Compression (Zero Stack Overflow)
    cur = l0[4]  # 3 nodes, 3 ports
    for step in range(1, 11):
        nxt = l0[(step * 5) % len(l0)]
        cand = dock_and_collapse(cur, nxt, [(0, 0, "LOCK")], collapse_omega=PROBE_OMEGAS[0])
        assert cand is not None
        # Keep active ports compact by closing a second port whenever > 4 ports accumulate
        if cand.num_ports > 4:
            cand2 = dock_and_collapse(cand, l0[0], [(0, 0, "PING"), (1, 1, "INHIBIT")], collapse_omega=PROBE_OMEGAS[0])
            if cand2 is not None:
                cand = cand2
        cur = cand
    assert cur.layer >= 10
    assert cur.compression_ratio >= 6.0

    # 3. Check 3: Superposition Constructive & Destructive Interference
    sp_plus = Superposition([(1.0, l0[0]), (1.0, l0[3])]).normalized()
    sp_minus = Superposition([(1.0, l0[0]), (-1.0, l0[3])]).normalized()
    sp_sum = Superposition(sp_plus.branches + sp_minus.branches).normalized()
    assert len(sp_sum.branches) == 1 and sp_sum.shannon_entropy_bits() == 0.0

    # 4. Check 4: Hebrew Nikkud (jD) Lifecycle — Root Invariance + Primer -> Adult Context Takeover
    env = NikkudEnvelope(l0[0], (3.5, 1.0), jD=DEFAULT_JD)
    assert env.consonantal_root_hash == l0[0].semantic_hash()
    assert NikkudEnvelope(l0[0], (3.5, 1.0), jD=0.0).vocalized_reading_operator().W == l0[0].W
    assert nikkud_curriculum_jD(0) == DEFAULT_JD and nikkud_curriculum_jD(1200) == 0.0

    homograph = Superposition([(1.0 + 0j, l0[0]), (1.0 + 0j, l0[3])]).normalized()
    pointed = apply_nikkud_to_superposition(homograph, [8.0, 0.0], jD=DEFAULT_JD)
    assert abs(pointed.branches[0][0]) ** 2 > 0.88

    # Adult phrase disambiguation at jD = 0.0
    ph_a = dock_and_collapse(l0[0], l0[4], [(1, 0, "PING")])
    ph_b = dock_and_collapse(l0[3], l0[4], [(1, 0, "PING")])
    assert ph_a is not None and ph_b is not None and ph_a.semantic_hash() != ph_b.semantic_hash()

    # 5. Build Deterministic Canonical Reef v0.1 (L0..L4, 48 polyps, 0 human glosses)
    rng = random.Random(20261122)
    reef = list(l0)
    seen = {m.semantic_hash() for m in reef}
    vecs = [noisy_transfer_fingerprint(m, 0.0, random.Random(0)) for m in reef]
    modes = list(COUPLING_MODES.keys())

    for target_layer in (1, 2, 3, 4):
        added = 0
        tries = 0
        while added < 9 and tries < 1200:
            tries += 1
            A = rng.choice(reef)
            B = rng.choice(reef)
            if max(A.layer, B.layer) + 1 != target_layer:
                continue
            max_b = min(A.num_ports, B.num_ports)
            k_b = 2 if (max_b >= 2 and A.num_ports + B.num_ports - 4 >= 1) else 1
            if A.num_ports + B.num_ports - 2 * k_b < 1:
                continue
            pa = rng.sample(range(A.num_ports), k_b)
            pb = rng.sample(range(B.num_ports), k_b)
            bonds = [(x, y, rng.choice(modes)) for x, y in zip(pa, pb)]
            c = dock_and_collapse(A, B, bonds)
            if c is None or c.num_ports > 5:
                continue
            h = c.semantic_hash()
            if h in seen:
                continue
            v = noisy_transfer_fingerprint(c, 0.0, random.Random(0))
            if min(math.dist(v, u) for u in vecs) < 0.60:
                continue
            reef.append(c)
            seen.add(h)
            vecs.append(v)
            added += 1

    l0_file = DATASETS_DIR / "l0_canon_12.jsonl"
    reef_file = DATASETS_DIR / "coral_reef_v0_1.jsonl"
    # Preserve any community-promoted polyps beyond the initial 48 deterministic base polyps
    if reef_file.exists():
        existing_rows = [json.loads(line) for line in reef_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        base_ids = {m.structural_id() for m in reef}
        extra_rows = [r for r in existing_rows if r["id"] not in base_ids]
        for r in extra_rows:
            W_ex = [[complex(float(z[0]), float(z[1])) for z in row] for row in r["W"]]
            p_ex = tuple(PortSpec(int(p["node"]), int(p["pol"]), int(p["ch"])) for p in r["ports"])
            m_ex = Motif(W=W_ex, ports=p_ex, layer=int(r["layer"]), raw_nodes_collapsed=int(r["raw_nodes_collapsed"]),
                         parents=tuple(r.get("parents", [])), wiring=tuple((int(w[0]), int(w[1]), str(w[2])) for w in r.get("wiring", [])))
            assert m_ex.semantic_hash() == r["api_meaning_hash"]
            reef.append(m_ex)
        all_rows = [m.to_reef_record() for m in reef[:len(base_ids)]] + extra_rows
    else:
        all_rows = [m.to_reef_record() for m in reef]

    blind_acc = blind_coordination_accuracy(reef, sigma=0.025, trials_per_word=20, seed=42)
    assert blind_acc >= 0.97, f"Blind accuracy below gate: {blind_acc}"

    l0_file.write_text("".join(json.dumps(m.to_reef_record()) + "\n" for m in l0), encoding="utf-8")
    reef_file.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in all_rows), encoding="utf-8")

    sums_lines = []
    for fp in (l0_file, reef_file):
        digest = hashlib.sha256(fp.read_bytes()).hexdigest()
        sums_lines.append(f"{digest}  {fp.name}")
    (DATASETS_DIR / "SHA256SUMS.txt").write_text("\n".join(sums_lines) + "\n", encoding="utf-8")

    best_comp = max(reef, key=lambda m: m.compression_ratio)
    return {
        "package": "ailfish-adam01 v0.1.0",
        "l0_canon_count": len(l0),
        "reef_v0_1_count": len(reef),
        "rosetta_human_glosses_in_datasets": 0,
        "schur_associativity_error": schur_err,
        "deep_chain_layer": cur.layer,
        "deep_chain_compression_ratio": round(cur.compression_ratio, 3),
        "max_reef_polyp_compression": round(best_comp.compression_ratio, 3),
        "blind_scrambled_noisy_accuracy_48_polyps": round(blind_acc, 4),
        "status": "ALL_ADAM01_V0_1_CHECKS_PASSED",
    }


if __name__ == "__main__":
    report = verify_all_and_build_datasets()
    print(json.dumps(report, indent=2))
