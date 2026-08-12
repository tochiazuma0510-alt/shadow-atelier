"""
AT-2 P1 -- u-residue-coset test (rederived from existing cert only, no GAP run).
Spec: docs/notes/ideas_arith_torsor_v1.md sec AT-2, P1.
Input: search/certs/set_surgery_fixture_v1_20260813.json (裁定1084, already committed).

Reads:
  check_a_kernel_census.classes[*].member_shadow_indices  (the two kernel classes,
    settled = the one containing rep_m=0, non-settled = the other)
  check_b_twist_survival.results[tag=Cx].per_shadow[*].m   (per-shadow m value,
    index i (0-based) <-> shadow index i+1, same order as shadowsFix used to build
    classFix -- verified: class rep_m matches m value of its first listed member).

u := 2*m + 1 (charming/multiplicative coordinate, definition note L180/200:
  "m の法 N_ord と u = 2m+1 の法 2n を混同しない" -- reduce u mod 2*n_ord, NOT mod n_ord).

Prediction (SUBTOR / P1): u-multiset of non-settled class == u(settled class) * u_{t0}
  (mod 2*n_ord), where u_{t0} = 2*rep_m(non-settled) + 1.

This script performs ONLY arithmetic re-tabulation on the already-published cert's
JSON values -- no new group-theoretic computation, no GAP invocation, u/c not
touched beyond the u=2m+1 coordinate that is already public in the 1084 cert's
method (m field). Output is machine-generated values only; no verdict language.
"""
import json
import hashlib
import sys
from collections import Counter

CERT_PATH = "search/certs/set_surgery_fixture_v1_20260813.json"

with open(CERT_PATH, "rb") as fb:
    raw = fb.read()
input_sha256 = hashlib.sha256(raw).hexdigest()

d = json.loads(raw.decode("utf-8"))
a = d["check_a_kernel_census"]
n_ord = a["n_ord"]
mod = 2 * n_ord
classes = a["classes"]

b = d["check_b_twist_survival"]
tag_cx = [r for r in b["results"] if r["tag"] == "Cx"][0]
per_shadow = tag_cx["per_shadow"]
m_by_idx = {i + 1: per_shadow[i]["m"] for i in range(len(per_shadow))}

# sanity: check_b per_shadow order corresponds 1:1 to check_a shadow indices
# (same shadowsFix list order in the source script -- verify first member of each
# class has m == class rep_m, as an internal consistency check, not a new computation)
consistency_checks = []
for c in classes:
    first_idx = c["member_shadow_indices"][0]
    consistency_checks.append({
        "class_rep_m": c["rep_m"],
        "first_member_shadow_index": first_idx,
        "first_member_m_from_check_b": m_by_idx[first_idx],
        "matches": (m_by_idx[first_idx] == c["rep_m"]),
    })

if not all(cc["matches"] for cc in consistency_checks):
    print("CONSISTENCY CHECK FAILED -- per_shadow ordering assumption is wrong", file=sys.stderr)
    print(json.dumps(consistency_checks, indent=2))
    sys.exit(1)

# classify settled vs non-settled: settled class is the one whose rep_m=0 (the
# class containing the identity [0,1] representative -- rep_f_perm_string=="()")
settled_class = None
other_classes = []
for c in classes:
    if c["rep_m"] == 0 and c["rep_f_perm_string"] == "()":
        settled_class = c
    else:
        other_classes.append(c)

if settled_class is None or len(other_classes) != 1:
    print("UNEXPECTED CLASS STRUCTURE (not the 2-class 24/24 fixture this script assumes)", file=sys.stderr)
    sys.exit(1)

nonsettled_class = other_classes[0]

def u_multiset(cls):
    ms = [m_by_idx[idx] for idx in cls["member_shadow_indices"]]
    us = [(2 * m + 1) % mod for m in ms]
    return ms, us

settled_m, settled_u = u_multiset(settled_class)
nonsettled_m, nonsettled_u = u_multiset(nonsettled_class)

u_t0 = (2 * nonsettled_class["rep_m"] + 1) % mod

predicted_u = sorted([(u * u_t0) % mod for u in settled_u])
actual_nonsettled_u = sorted(nonsettled_u)

match = (predicted_u == actual_nonsettled_u)

result = {
    "schema": "shadow-atelier/at2_p1_u_residue_coset_v1",
    "spec_ref": "docs/notes/ideas_arith_torsor_v1.md 札AT-2 P1",
    "input_cert": CERT_PATH,
    "input_cert_sha256": input_sha256,
    "n_ord": n_ord,
    "modulus_2n": mod,
    "settled_class": {
        "size": settled_class["size"],
        "rep_m": settled_class["rep_m"],
        "m_multiset": sorted(settled_m),
        "u_multiset": sorted(settled_u),
    },
    "nonsettled_class": {
        "size": nonsettled_class["size"],
        "rep_m": nonsettled_class["rep_m"],
        "m_multiset": sorted(nonsettled_m),
        "u_multiset": sorted(nonsettled_u),
    },
    "u_t0": u_t0,
    "predicted_nonsettled_u_multiset": predicted_u,
    "actual_nonsettled_u_multiset": actual_nonsettled_u,
    "predicted_equals_actual": match,
    "consistency_checks": consistency_checks,
    "u_touched": True,
    "u_touch_note": "u=2m+1 is the charming/multiplicative coordinate already public in the 1084 cert's own definition (definition note L180); this is NOT the sealed K(5) instance quantity (NAME-COLLIDE note applies: this u is a K(9)-window-family instance object, distinct from the sealed K(5) quantities).",
    "status_note": "既観測(census83)の独立再確認 -- 数学者が census83 の既存データで厳密一致を確認済み(set_surgery_vetting_v1.md: {1,7,13,19}*5 == {5,11,17,23} mod 24)。本スクリプトはその一致を1084certの再集計のみから独立に再導出したもの(独立クロスチェック格)。",
}

out_path = "search/certs/at2_p1_u_residue_coset_v1_20260813.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print("wrote", out_path, "predicted_equals_actual =", match)

