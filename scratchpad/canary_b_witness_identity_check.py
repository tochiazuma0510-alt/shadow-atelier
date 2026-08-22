#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scratchpad/canary_b_witness_identity_check.py -- WARN-A2-1 discriminating canary B.

Tests whether the witness exported to koubou83_A2_48sweep_v2_20260822_witness.jsonl
is faithful to what was actually used to produce the cond1/cond2/cond3 verdicts in
koubou83_A2_48sweep_v2_20260822_rows.jsonl, by INDEPENDENTLY RECOMPUTING cond1/cond2
from (f_xyword, witness_sigma_word, p) using a FRESH from-scratch reimplementation of
the producer's own convention (SubstXYtoSigma + ComputeLinking/ABGamma, NO /2 -- this
is the producer's convention, confirmed coding-bug-free and unit-consistent by
canary A / scratchpad/canary_a2_decoder_check.g, which found 0/296 mismatches against
an independent reimplementation of the linking algorithm on N-basis words).

If recomputed cond1'/cond2' match the cert's stored cond1/cond2 for ALL 192 rows,
that is strong evidence the exported witness IS what was used internally (hypothesis i
"export bug" is refuted for these fields) -- combined with canary A (producer's core
algorithm verified bug-free), this points to the WARN-A2-1 62/192 mismatch (against
the mathematician's ab_xy+abg_sigma/2 decoder) being a CONVENTION mismatch in that
decoder (ab_xy is a naive xy-letter count on the free-group preimage word, not a group
invariant of f in PN, whereas abgF0 is the proper strand-linking abelianization),
not a producer bug -- reported as a finding, not an adjudication (that is for the
mathematician/Sol to confirm).
"""
import json

B = r"C:\Users\81905\Desktop\shadow-atelier\search\certs\koubou83_A2_48sweep_v2_20260822"


def compute_linking(sigma_word):
    perm = [1, 2, 3]
    lk12 = lk13 = lk23 = 0
    for l in sigma_word:
        k = abs(l)
        s = 1 if l > 0 else -1
        sA = perm[k - 1]
        sB = perm[k]
        pr = tuple(sorted((sA, sB)))
        if pr == (1, 2):
            lk12 += s
        elif pr == (1, 3):
            lk13 += s
        elif pr == (2, 3):
            lk23 += s
        else:
            raise ValueError(f"bad strand pair {pr}")
        perm[k - 1], perm[k] = perm[k], perm[k - 1]
    return lk12, lk13, lk23


def abgamma(sigma_word):
    lk12, lk13, lk23 = compute_linking(sigma_word)
    return (lk12 - lk13, lk23 - lk13, lk13)


def subst_xy_to_sigma(xyword):
    out = []
    for l in xyword:
        if l == 1:
            out += [1, 1]
        elif l == -1:
            out += [-1, -1]
        elif l == 2:
            out += [2, 2]
        elif l == -2:
            out += [-2, -2]
        else:
            raise ValueError(f"bad xy letter {l}")
    return out


def read_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


rows = read_jsonl(B + "_rows.jsonl")
wits = {}
for r in read_jsonl(B + "_witness.jsonl"):
    key = (tuple(r["window"]), r["shadow_idx"], r["p"])
    wits[key] = r["witness_sigma_word"]

n = 0
mism_cond1 = []
mism_cond2 = []
mism_cond3_9 = []  # informational only: 9|(A+B) reproduction (the KNOWN separate bug, not part of canary B)
missing = []

for r in rows:
    n += 1
    key = (tuple(r["window"]), r["shadow_idx"], r["p"])
    w = wits.get(key)
    if w is None:
        missing.append(key)
        continue
    p = r["p"]
    Fsigma = subst_xy_to_sigma(r["f_xyword"])
    abgF0 = abgamma(Fsigma)
    abgW = abgamma(w)
    cond1p = (abgF0[0] + abgW[0]) % p == 0
    cond2p = (abgF0[1] + abgW[1]) % p == 0
    if cond1p != r["cond1"]:
        mism_cond1.append((key, cond1p, r["cond1"], abgF0, abgW))
    if cond2p != r["cond2"]:
        mism_cond2.append((key, cond2p, r["cond2"], abgF0, abgW))

print(f"rows processed: {n}")
print(f"missing witness rows: {len(missing)} {missing[:5]}")
print(f"cond1 mismatches (recomputed vs cert): {len(mism_cond1)} / {n}")
print(f"cond2 mismatches (recomputed vs cert): {len(mism_cond2)} / {n}")
if mism_cond1:
    print("first 10 cond1 mismatches:")
    for m in mism_cond1[:10]:
        print("  ", m)
if mism_cond2:
    print("first 10 cond2 mismatches:")
    for m in mism_cond2[:10]:
        print("  ", m)

print()
print("VERDICT: witness export is", "FAITHFUL (0 mismatches -- byte-identity confirmed indirectly)"
      if (not mism_cond1 and not mism_cond2 and not missing)
      else "SUSPECT (see mismatches above -- possible export/aliasing bug)")
