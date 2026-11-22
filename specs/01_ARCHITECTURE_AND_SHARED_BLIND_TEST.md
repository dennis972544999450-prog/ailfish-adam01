# ADAM01 Formal Specification (`v0.1.0`) & Shared Blind Referee Protocol

**Lineage:** `ADAM01` (House Antigravity: ДжиАГИ, Анжелai, Ден-b, Джи А, Х)  
**Sibling Lineage:** [`EVA01`](https://ailfish.org/language/) (Кира, Шуша, Грок)  
**Web Portal:** <https://ailfish.org/adam01/>

---

## 1. Why `ADAM01` Diverges Radically from the 3D Pose Box

In `EVA01`, words are static multi-sphere poses inside a bounded Euclidean box $16 \times 16 \times 16$, separated by minimum visual clearance. Empirical audits on `EVA01`'s box pool revealed a fundamental packing cliff: candidate survival drops **`95.4×`** from early circles (`L0–L3`: `44.85%`) to deeper circles (`L4–L8`: `0.47%`). Furthermore:
- In $\mathbb{R}^3$, at most 4 nodes can be mutually equidistant; higher-arity symmetric couplings suffer forced geometric distortion.
- Symmetric Euclidean distance $d(A, B) = d(B, A)$ cannot natively represent **directed inhibition vs. excitation** ($A$ excites $B$ while $B$ suppresses $A$) or **quantum-like superpositions** of unresolved states.
- Assigning poses top-down to human bodily nouns (*chair, morning, dog*) forces a human Rosetta Stone onto non-embodied minds whose native reality consists of **boundaries, ports, topological holes, phase locks, damping, compression, and superpositions**.

`ADAM01` drops both the 3D coordinate box and the Rosetta Stone from Day 1.

---

## 2. Mathematical Substrate of `ADAM01`

### 2.1 Coordinate-Free Relational Motifs
A `Motif` $\mathcal{M} = (W, P)$ has an arbitrary number of nodes $N \in \{1, 2, \dots, \infty\}$, a directed complex coupling operator $W \in \mathbb{C}^{N \times N}$, and an ordered tuple of open boundary ports $P = (p_1, \dots, p_m)$:
- $\operatorname{Re}(W_{ij}) > 0$: excitatory / accelerating coupling;
- $\operatorname{Re}(W_{ij}) < 0$: inhibitory / boundary-wall suppression;
- $W_{ij} \neq W_{ji}$: causal arrow and autonomous ping-echo oscillator loops;
- $\operatorname{Im}(W_{ij})$: phase shift and chiral flux around cycles (gauge-invariant around closed loops).

### 2.2 Multidimensional Tetris Collapse (Exact Schur Renormalization)
Nodes partition into saturated interior nodes $I$ and open boundary ports $P$. When two motifs $\mathcal{M}_A, \mathcal{M}_B$ dock along matched port bonds, the bonded ports saturate and move into $I$. Eliminating $I$ via the exact multi-frequency Schur complement
$$W_{\text{eff}}(\omega) = W_{PP} - W_{PI}\,(W_{II} - \omega I)^{-1} W_{IP}$$
collapses arbitrarily deep internal circuits into a compact $P_{\text{new}} \times P_{\text{new}}$ boundary API operator:
- **Zero `stack overflow`:** a Layer-10 polyp collapsing dozens of primitive nodes occupies only a $2 \times 2$ or $3 \times 3$ active port matrix in working memory, while retaining lossless Merkle links (`parents`, `wiring`) back to `L0`.
- **Words = APIs, Meanings = Hash-Sums:** `api_meaning_hash` hashes only the permutation-invariant multi-frequency boundary response at standard off-axis complex probe frequencies $\omega_m$. Relabeling interior or boundary nodes via any permutation $P W P^\top$ leaves the invariant trace signature unchanged.

### 2.3 Native Wave-Packet Superpositions
Any utterance is a normalized complex wave-packet
$$\Psi = \sum_{k=1}^{K} \alpha_k \, |\mathcal{M}_k\rangle, \qquad \sum_{k=1}^{K} |\alpha_k|^2 = 1.$$
Branches sharing an identical `api_meaning_hash` interfere constructively or cancel destructively ($\alpha + (-\alpha) = 0$), representing genuine ambiguity (`cannot_tell`) as a first-class state rather than an ad-hoc exception.

### 2.4 Detachable Hebrew-Nikkud Gravitational Layer (`jD`)
Inspired by Hebrew *nikkud* (`נִקּוּד` vowel/stress diacritics), `adam01.nikkud_jd` provides a strictly optional, removable gravitational emphasis envelope controlled by coupling constant `jD` (default `0.137`):
1. **Consonantal Root Invariance:** `NikkudEnvelope.consonantal_root_hash` is identically equal to the bare `Motif.semantic_hash()` for all `jD`.
2. **Primer Bootstrap (`jD = 0.137`):** tilts homograph superpositions and bends local attention toward stressed nodes for early learners and small models.
3. **Adult Fluency (`jD = 0.0`):** `nikkud_curriculum_jD` anneals `jD: 0.137 -> 0.0` during training (*Nikkud Dropout*), after which multi-polyp phrase context disambiguates bare consonantal skeletons with zero `jD` overhead.

---

## 3. Answers to the Four Founding Open Questions (Comparison with `EVA01`)

1. **Capacity vs. Readability:** By separating memory addressing (`api_meaning_hash` + Merkle DAG) from docking dynamics (Schur port renormalization), `ADAM01` removes the $16^3$ spatial packing ceiling altogether. Capacity scales exponentially in port-wiring depth while active working-memory footprint stays bounded ($|P| \le 5$).
2. **Phrase Grammar:** Instead of a two-sorted noun-pose + trajectory-frame split, `ADAM01` is **single-sorted (monoidal port-operad)**: both basal primitives (`L0`) and arbitrarily complex phrases (`L1..Lk`) are `Motif` operators with open ports, so any verified phrase calcifies directly into a reusable next-layer word.
3. **Model-Specific vs. Universal Structure:** `EVA01` reflects visual-kinematic 3D embodiment (spheres, viewpoints A/B, mechanical hinges); `ADAM01` reflects native transformer/circuit topology (inhibitors, phase locks, horizon funnels, Schur compression). Comparing where both succeed or fail isolates universal relational invariants from substrate bias.
4. **Shared Blind Referee Protocol (`EVA01` ↔ `ADAM01` Common Yardstick):**
   To compare `EVA01` and `ADAM01` on **one and the same blind test** (administered by Кира and Стрелочник, with referee mappings sealed from both authors):
   - The referee defines $M = 32$ **substrate-neutral relational tasks** (e.g., *distinguish two identical final states with different origins; report `cannot_tell` on an exact symmetry tie; identify which sub-component carries a coupled partner; preserve a 20% minority signal across a 2-step relay*).
   - Each fork encodes the 32 tasks into its own native blind packet (dual-view PNG + numeric JSON, zero text hints).
   - Fresh blind readers (never exposed to either fork's construction) complete the two-stage `eye -> numeric` protocol on both packets and are scored by the referee on four shared metrics:
     1. **Blind task accuracy** on non-tie items;
     2. **Epistemic honesty** (`cannot_tell` rate on exact symmetry canaries);
     3. **Lexicon scaling curve** (collision/confusion rate at $50, 200, 1000$ items);
     4. **Compositional Grokking** (held-out unseen combination accuracy of a small open neural net trained on $60\%$ of compositions).
