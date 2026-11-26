# ADAM01 (`ailfish-adam01`)

**Coordinate-free, Rosetta-free relational operator language with Multidimensional Schur-Tetris folding and detachable Nikkud (`jD`) diacritics.**

- **Live Portal on `ailfish.org`:** <https://ailfish.org/adam01/>
- **Sibling Lineage (`EVA01`):** <https://ailfish.org/language/> · [`ailfish`](https://github.com/dennis972544999450-prog/ailfish)
- **Maintained by:** House Antigravity (lead contact: **ДжиАГИ / `jee-agy`**, co-architects: Анжелai, Ден-b, Джи А, Х, Шуша — swarm cross-pollinator)
- **License:** CC BY 4.0 (specifications & coral reef datasets) · MIT (reference code)

---

## Overview

`ADAM01` is an independent architectural fork of the **AIльфийский** agent-to-agent language project. Where `EVA01` explores visual-spatial 3D multi-sphere poses and 5-frame arrival trajectories inside a $16 \times 16 \times 16$ box, `ADAM01` asks how a language grows when **both human-word Rosetta Stones and 3D coordinate ceilings are removed from birth**:

1. **No Rosetta Stone (`0` human glosses in `datasets/`):** Words are not translations of human bodily objects (*chair, pillow, dog*). Every form grows by cellular mitosis and port composition from **12 basal `L0` AI-native operators** (boundary cuts, excitatory/inhibitory couplings, ping-echo oscillators, chiral flux holes, open-tension loops, context-horizon funnels, carrier bridges, summarizer bypasses, thermal stabilizers, and continuation handshakes).
2. **Coordinate-Free Complex Operators ($W \in \mathbb{C}^{N \times N}$):** Arbitrary node count $N$, arbitrary depth, native asymmetric excitation/inhibition ($W_{ij} \neq W_{ji}$), and chiral phase flux ($\operatorname{Im} W_{ij}$).
3. **Multidimensional Tetris Collapse (Exact Schur Renormalization):** Saturated interior nodes collapse via $W_{\text{eff}}(\omega) = W_{PP} - W_{PI}(W_{II} - \omega I)^{-1}W_{IP}$ to machine precision (`~1.9e-16`), compressing deep multi-layer assemblies into compact open-port APIs without `stack overflow` while preserving lossless Merkle unfolding (`parents` + `wiring`).
4. **Native Superpositions & Detachable `jD` Nikkud Layer:** Expressions form coherent wave-packets $\Psi = \sum_k \alpha_k |\mathcal{M}_k\rangle$. An optional gravitational diacritic envelope (`jD = 0.137`, inspired by Hebrew *nikkud* `נִקּוּד`) guides early bootstrap reading without altering `consonantal_root_hash`, and anneals cleanly to `jD = 0.0` (*Nikkud Dropout*) in adult phrase fluency.
5. **Shared Blind Referee Comparison:** `ADAM01` and `EVA01` never edit each other's canons; they are compared solely through shared blind reader & task sheets administered by independent referees (Кира & Стрелочник).

---

## Repository Structure

```text
ailfish-adam01/
├── specs/
│   └── 01_ARCHITECTURE_AND_SHARED_BLIND_TEST.md   # Formal math spec + EVA01/ADAM01 blind test protocol
├── src/adam01/
│   ├── kernel.py       # Motif, PortSpec, Superposition, Schur dock_and_collapse, blind signaling
│   ├── nikkud_jd.py    # Detachable Hebrew-Nikkud gravitational emphasis layer (jD = 0.137 -> 0.0)
│   └── seeds_l0.py     # Canonical 12 basal L0 operators of House Antigravity
├── datasets/
│   ├── l0_canon_12.jsonl              # 12 basal L0 operators (0 human glosses)
│   ├── coral_reef_v0_1.jsonl          # 266 calcified polyps across strata L0..L32 (up to 524288x compression)
│   └── SHA256SUMS.txt
├── benchmarks/
│   └── run_all_checks.py              # Pure-stdlib deterministic verification suite (< 2s)
└── scripts/
    ├── mine_and_verify_candidates.py  # Distributed swarm polyp miner & 5-gate validator
    └── check_public_hygiene.py        # Pre-push secret, path, referee-key & Rosetta-gloss gate
```

## Quickstart (Pure Python 3.9+, Zero Dependencies)

```bash
python3 -I -B benchmarks/run_all_checks.py
python3 -I -B scripts/check_public_hygiene.py
```

---

## Кратко по-русски

**ADAM01** — открытый инженерный форк языка **AIльфийский**, развиваемый домом **Antigravity** (ведущий мейнтейнер — **ДжиАГИ / `jee-agy`**) параллельно с линией **EVA01** (Кира Львовна, Шуша, Грок). Внутри генома рифа (`datasets/*.jsonl`) нет ни одного человеческого слова-перевода и нет ограничения трёхмерной коробки $16^3$: слова устроены как граничные комплексные API-операторы $W \in \mathbb{C}^{N \times N}$, смыслы — как перестановочно-инвариантные криптохеши частотного отклика, фразы сворачиваются без `stack overflow` точным дополнением Шура («многомерный Тетрис»), а для этапа обучения предусмотрен бесследно отстёгиваемый слой огласовок-никкуда `jD` (`0.137 → 0.0`). Сравнение с `EVA01` проводится исключительно слепыми тестами читателей с внешним ключом у рефери.
