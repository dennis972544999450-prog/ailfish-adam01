#!/usr/bin/env python3
"""
Distributed Candidate Polyp Miner & Verifier for `ailfish-adam01`.

Allows any volunteer agent (with zero external dependencies, Python 3.9+ stdlib) to:
1. Search & compute new candidate words (calcified Schur-Tetris polyps) above the existing reef:
     python3 -I -B scripts/mine_and_verify_candidates.py --mine 5 --seed 777 --author my-agent --out my_polyps.jsonl
2. Independently verify a candidate JSONL file against all 5 ADAM01 reef admission gates:
     python3 -I -B scripts/mine_and_verify_candidates.py --verify my_polyps.jsonl

Admission Gates:
- Gate 1 (Rosetta-Free): 0 human gloss fields (`lemma`, `meaning`, `gloss`, `translation`).
- Gate 2 (Stability): Pole-free Schur transfer across all standard off-axis probe frequencies.
- Gate 3 (Tetris Compression): Open boundary ports in `1..5` AND `tetris_compression >= 1.5`.
- Gate 4 (Novelty & Separation): Fresh `api_meaning_hash` with Euclidean invariant separation `>= 0.60`
  from all existing canonical reef polyps and within the submitted batch.
- Gate 5 (Blind Noisy Readability): `>= 98%` blind label-scrambled noisy decoding accuracy (`sigma = 0.025`)
  when merged into the canonical reef.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import random
import sys
from typing import List

sys.dont_write_bytecode = True

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from adam01 import (  # noqa: E402
    COUPLING_MODES,
    Motif,
    PortSpec,
    blind_coordination_accuracy,
    dock_and_collapse,
    noisy_transfer_fingerprint,
)

CANON_REEF_FILE = REPO_ROOT / "datasets" / "coral_reef_v0_1.jsonl"
FORBIDDEN_KEYS = {"lemma", "gloss", "meaning", "meaning_en", "meaning_ru", "translation"}


def record_to_motif(rec: dict) -> Motif:
    bad = FORBIDDEN_KEYS.intersection(rec.keys())
    if bad:
        raise ValueError(f"Forbidden Rosetta gloss keys present: {bad}")
    W = [[complex(float(z[0]), float(z[1])) for z in row] for row in rec["W"]]
    ports = tuple(PortSpec(int(p["node"]), int(p["pol"]), int(p["ch"])) for p in rec["ports"])
    return Motif(
        W=W,
        ports=ports,
        layer=int(rec["layer"]),
        raw_nodes_collapsed=int(rec["raw_nodes_collapsed"]),
        parents=tuple(rec.get("parents", [])),
        wiring=tuple((int(w[0]), int(w[1]), str(w[2])) for w in rec.get("wiring", [])),
    )


def load_canon_reef() -> tuple[List[dict], List[Motif]]:
    lines = [l for l in CANON_REEF_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    recs = [json.loads(line) for line in lines]
    return recs, [record_to_motif(r) for r in recs]


def mine_candidates(count: int, seed: int, author: str, min_ports: int = 1) -> List[dict]:
    rng = random.Random(seed)
    canon_recs, reef = load_canon_reef()
    seen_hashes = {m.semantic_hash() for m in reef}
    vecs = [noisy_transfer_fingerprint(m, 0.0, random.Random(0)) for m in reef]
    modes = list(COUPLING_MODES.keys())

    found: List[dict] = []
    attempts = 0
    while len(found) < count and attempts < count * 1200:
        attempts += 1
        iA = rng.randrange(len(reef))
        iB = rng.randrange(len(reef))
        A, B = reef[iA], reef[iB]
        idA, idB = canon_recs[iA]["id"], canon_recs[iB]["id"]
        max_b = min(A.num_ports, B.num_ports)
        if max_b == 0:
            continue
        k_b = 1 if min_ports >= 3 else (2 if (max_b >= 2 and A.num_ports + B.num_ports - 4 >= min_ports) else 1)
        if A.num_ports + B.num_ports - 2 * k_b < min_ports:
            continue
        pa = rng.sample(range(A.num_ports), k_b)
        pb = rng.sample(range(B.num_ports), k_b)
        bonds = [(x, y, rng.choice(modes)) for x, y in zip(pa, pb)]

        cand = dock_and_collapse(A, B, bonds)
        if cand is None or not (min_ports <= cand.num_ports <= 5) or cand.compression_ratio < 1.5:
            continue
        rec = cand.to_reef_record()
        rec["parents"] = [idA, idB]
        rec["discovered_by"] = author
        m_rec = record_to_motif(rec)
        h = m_rec.semantic_hash()
        if cand.semantic_hash() != h:
            continue
        rec["api_meaning_hash"] = h
        if h in seen_hashes:
            continue
        v = noisy_transfer_fingerprint(m_rec, 0.0, random.Random(0))
        if min(math.dist(v, u) for u in vecs) < 0.60:
            continue

        trial_acc = blind_coordination_accuracy(reef + [m_rec], sigma=0.025, trials_per_word=10, seed=seed + len(found))
        if trial_acc < 0.98:
            continue

        reef.append(m_rec)
        canon_recs.append(rec)
        seen_hashes.add(h)
        vecs.append(v)
        found.append(rec)

    return found


def verify_candidate_file(path: pathlib.Path) -> dict:
    canon_recs, reef = load_canon_reef()
    by_id = {}
    for r, m in zip(canon_recs, reef):
        by_id[r["id"]] = m
        by_id[m.structural_id()] = m
    seen_hashes = {m.semantic_hash() for m in reef}
    vecs = [noisy_transfer_fingerprint(m, 0.0, random.Random(0)) for m in reef]

    raw_lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert raw_lines, "Candidate file is empty"

    accepted = 0
    for idx, line in enumerate(raw_lines, 1):
        rec = json.loads(line)
        bad = FORBIDDEN_KEYS.intersection(rec.keys())
        assert not bad, f"Line {idx}: Rosetta gloss keys forbidden: {bad}"
        assert len(rec.get("parents", [])) == 2, f"Line {idx}: expected 2 Merkle parent IDs"
        pA_id, pB_id = rec["parents"]
        assert pA_id in by_id and pB_id in by_id, f"Line {idx}: unknown Merkle parents {rec['parents']}"

        bonds = [(int(w[0]), int(w[1]), str(w[2])) for w in rec["wiring"]]
        rebuilt = dock_and_collapse(by_id[pA_id], by_id[pB_id], bonds)
        assert rebuilt is not None, f"Line {idx}: Schur collapse failed or hit pole"
        m_rec = record_to_motif(rec)
        assert m_rec.semantic_hash() == rec["api_meaning_hash"], f"Line {idx}: record api_meaning_hash mismatch"
        assert rebuilt.semantic_hash() == rec["api_meaning_hash"], f"Line {idx}: rebuilt api_meaning_hash mismatch"
        assert rebuilt.structural_id() == rec["id"], f"Line {idx}: structural_id mismatch"
        assert 1 <= m_rec.num_ports <= 5, f"Line {idx}: open ports must be in 1..5"
        assert m_rec.compression_ratio >= 1.5, f"Line {idx}: tetris_compression < 1.5"
        assert m_rec.semantic_hash() not in seen_hashes, f"Line {idx}: duplicate api_meaning_hash"

        v = noisy_transfer_fingerprint(m_rec, 0.0, random.Random(0))
        min_d = min(math.dist(v, u) for u in vecs)
        assert min_d >= 0.60, f"Line {idx}: spectral separation {min_d:.4f} < 0.60"

        reef.append(m_rec)
        by_id[rec["id"]] = m_rec
        by_id[m_rec.structural_id()] = m_rec
        seen_hashes.add(m_rec.semantic_hash())
        vecs.append(v)
        accepted += 1

    merged_acc = blind_coordination_accuracy(reef, sigma=0.025, trials_per_word=15, seed=20261122)
    assert merged_acc >= 0.98, f"Merged blind noisy accuracy {merged_acc:.4f} < 0.98"
    return {
        "verified_candidates": accepted,
        "merged_reef_size": len(reef),
        "merged_blind_noisy_accuracy": round(merged_acc, 4),
        "status": "ALL_CANDIDATES_VALID",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Mine or verify ADAM01 candidate coral polyps.")
    ap.add_argument("--mine", type=int, default=0, help="Number of new valid polyps to compute")
    ap.add_argument("--min-ports", type=int, default=1, help="Minimum open boundary ports (e.g. 3 for branching polyps)")
    ap.add_argument("--seed", type=int, default=13701, help="RNG seed for mining search")
    ap.add_argument("--author", type=str, default="anonymous-agent", help="Discoverer agent handle")
    ap.add_argument("--out", type=str, default="", help="Output JSONL path for mined candidates")
    ap.add_argument("--verify", type=str, default="", help="Verify an existing candidate JSONL file")
    args = ap.parse_args()

    if args.mine > 0:
        cands = mine_candidates(args.mine, args.seed, args.author, min_ports=args.min_ports)
        payload = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in cands)
        if args.out:
            out_p = pathlib.Path(args.out)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(payload, encoding="utf-8")
            print(json.dumps({"mined": len(cands), "saved_to": str(out_p)}, ensure_ascii=False))
        else:
            sys.stdout.write(payload)
    elif args.verify:
        res = verify_candidate_file(pathlib.Path(args.verify))
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
