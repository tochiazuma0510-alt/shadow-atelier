#!/usr/bin/env python3
"""
edim_c4_crosscheck.py -- independent final confirmation that C-4's lifeline
condition holds: compares search/certs/edim_semidirect_c1c4_v1_20260806.json
(this session's NEW semidirect-model implementation) directly against
search/certs/edim56_20260806.json (the EXISTING, prior-session ideal-
quotient-method result) byte-for-byte on H_dim/S_dim for k=3..6. Does not
reuse any code from edim_semidirect_v1.py or edim_run_c1c4.py -- reads only
the two committed JSON certs.
"""
import json

NEW = json.load(open("search/certs/edim_semidirect_c1c4_v1_20260806.json", encoding="utf-8"))
OLD = json.load(open("search/certs/edim56_20260806.json", encoding="utf-8"))

new_H = NEW["per_prime"][0]["H_dim"]
new_S = NEW["per_prime"][0]["S_dim"]

old_H = OLD["results"]["2147483647"]["H_dim"]
old_S = OLD["results"]["2147483647"]["S_dim"]
old_t = OLD["results"]["2147483647"]["t_dim"]
new_t = NEW["per_prime"][0]["t_dim"]

problems = []
for k in [3, 4, 5, 6]:
    if new_H.get(str(k), new_H.get(k)) != old_H[str(k)]:
        problems.append(f"H_dim k={k}: new={new_H.get(k)} old={old_H[str(k)]}")
    if new_S.get(str(k), new_S.get(k)) != old_S[str(k)]:
        problems.append(f"S_dim k={k}: new={new_S.get(k)} old={old_S[str(k)]}")
for k in [2, 3, 4, 5, 6]:
    if new_t.get(str(k), new_t.get(k)) != old_t[str(k)]:
        problems.append(f"t_dim k={k}: new={new_t.get(k)} old={old_t[str(k)]}")

result = {
    "schema": "edim-c4-crosscheck/v1",
    "note": "Direct byte-level comparison of the NEW semidirect-model cert against the EXISTING "
            "ideal-quotient-method cert (edim56_20260806.json) -- independent second implementation "
            "cross-check for E-DIM5/6 (design doc SS5.3 C-4's stated purpose).",
    "new_cert": "search/certs/edim_semidirect_c1c4_v1_20260806.json",
    "old_cert": "search/certs/edim56_20260806.json",
    "problems": problems,
    "MATCH": len(problems) == 0,
    "H_dim_new": new_H, "H_dim_old": old_H,
    "S_dim_new": new_S, "S_dim_old": old_S,
}
print(json.dumps(result, indent=2, ensure_ascii=False))
with open("search/certs/edim_c4_crosscheck_v1_20260806.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
