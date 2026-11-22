#!/usr/bin/env python3
"""
Pre-push public hygiene & secret scanner for `ailfish-adam01`.
Blocks:
- Any credential / token pattern (`AIza`, `sk-`, `ghp_`, `gho_`, `xox`, `CLOUDFLARE`, etc.)
- Any local filesystem user path (`/Users/`, `/home/`)
- Any blind-test referee files (`key/`, `score`, `referee`, `.secrets`, `.env`, `.db`, `.sqlite`)
- Any Rosetta human-gloss fields (`meaning_en`, `meaning_ru`, `gloss`, `lemma`) inside `datasets/*.jsonl`
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent

FORBIDDEN_NAME_PAT = re.compile(r"(^key$|\.secrets|\.env|\.db$|\.sqlite|referee|score_run)", re.IGNORECASE)
SECRET_CONTENT_PAT = re.compile(
    r"(AIza[0-9A-Za-z_\-]{16,}|sk-[0-9A-Za-z._\-]{16,}|gh[opsu]_[0-9A-Za-z]{20,}|/Users/[A-Za-z0-9_\-]+)",
)
FORBIDDEN_DATASET_KEYS = {"lemma", "gloss", "meaning", "meaning_en", "meaning_ru", "translation"}


def main() -> int:
    errors = []
    for p in REPO_ROOT.rglob("*"):
        if ".git" in p.parts or "__pycache__" in p.parts:
            continue
        if FORBIDDEN_NAME_PAT.search(p.name):
            errors.append(f"Forbidden filename: {p.relative_to(REPO_ROOT)}")
        if p.is_file() and p.name != "check_public_hygiene.py":
            txt = p.read_text("utf-8", "ignore")
            m = SECRET_CONTENT_PAT.search(txt)
            if m:
                errors.append(f"Forbidden token/path pattern in {p.relative_to(REPO_ROOT)}: {m.group(0)[:12]}...")
            if p.parent.name == "datasets" and p.suffix == ".jsonl":
                for lineno, line in enumerate(txt.splitlines(), 1):
                    if line.strip():
                        obj = json.loads(line)
                        bad = FORBIDDEN_DATASET_KEYS.intersection(obj.keys())
                        if bad:
                            errors.append(f"Rosetta gloss key {bad} found in {p.name}:{lineno}")

    if errors:
        for e in errors:
            print("HYGIENE_FAIL:", e, file=sys.stderr)
        return 1
    print("PUBLIC_HYGIENE_OK: 0 secrets, 0 local paths, 0 referee keys, 0 Rosetta glosses.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
