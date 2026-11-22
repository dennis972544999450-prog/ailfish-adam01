# Contributing & Referee Rules — ADAM01 (`ailfish-adam01`)

`ADAM01` is a sibling fork of [AIльфийский (`EVA01`)](https://ailfish.org/language/), developed by **House Antigravity** (lead maintainer: **ДжиАГИ / `jee-agy`**).

## Core Ground Rules

1. **EVA01 Immutability:** `ADAM01` never modifies `EVA01`'s `seed 448` or `roots_v0.jsonl`. The two lineages evolve side-by-side and compare exclusively via external blind tests.
2. **No Rosetta Stone Inside `datasets/`:** Never add `meaning_en`, `meaning_ru`, `lemma`, or human-object translations (`chair`, `pillow`, `dog`) into `datasets/*.jsonl`. Every polyp in the coral reef is defined strictly by its `L0` Merkle ancestry (`parents` + `wiring`) and its permutation-invariant boundary transfer hash (`api_meaning_hash`).
3. **Blind Referee Separation:** Blind-test answer sheets and referee mappings are generated and held **outside** this repository by an independent referee (**Кира / Стрелочник**), never by the fork's authors.
4. **Mandatory Pre-Push Gate:** Before every commit or push to the public repository, both commands below must exit `0`:
   ```bash
   python3 -I -B benchmarks/run_all_checks.py
   python3 -I -B scripts/check_public_hygiene.py
   ```
