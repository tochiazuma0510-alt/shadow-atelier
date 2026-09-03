# Sol(max) Task616: final release re-audit of Task601 selected SLP

Role: independent adversarial static re-audit.  Read in full:

1. `sol/sol_reply_614_audit_r07_grade1_selected_slp_v1.md`;
2. `sol/luna_task_615_r07_grade1_selected_slp_final_release_repair_v1.md`;
3. the exact repaired Task601 quartet below.

| file | SHA-256 |
|---|---|
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | `4cc5d6ccb1bfdcb441b801a4826af04bbbdc9dc7f21d6f7c860d05929e64bfe9` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | `8355fda531b9de41b37df811af932352f07546d6d0ec445764fedaced2595595` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | `3ddd2f53fb10d698713e2a44a27cd894f4a02120727bb58db65beef9ac4a6fbd` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | `f360beb5a7c70608b48683183d01af3e262e0ce4b687c0cdb5ccb48c9cb31609` |

Write only
`sol/sol_reply_616_audit_r07_grade1_selected_slp_final_release_v1.md`.
Do not repair files, run production/GHA/git, or run a full local 8,059-row
route.  Tiny serial static/selftests with cache outside the repository are
allowed.

Return `PASS` or `FAIL`.  Confirm all four Task614 repair groups exactly:

1. the unique canonical graph is built only from selected physical refs;
   old nodes add no surplus expressions; only reached block defects add the
   exact particular seed/transition expression; block insertion receipts and
   quotient-derived states cannot enlarge the source graph;
2. the semantic roots bytes are the canonical authenticated roots receipt,
   the manifest pointer is identical, the verdict records that digest, and
   all eight false/null claim fields are required in both objects;
3. frozen v3 is hashed before every execution and the workflow preflight
   actually checks its pin;
4. the 8 claim, 3 root, 13 source and 11 transcript mutations invoke the
   production gates and include internally canonical dependency deletion,
   acted-old-root omission, same-key duplication, expression deletion/
   mutation and pointer aliasing; all byte counts and workflow SHA pins are
   current.

Also confirm the repair did not change the frozen 8,059-offer route,
lower/grade ranks 1,661/5,044, 3,317 MEMBER equation, physical replay,
independent router, resource envelope or honest candidate-only claim.  Flag
only a concrete load-bearing defect; do not request a new framework.  This
is a static release audit, not an execution receipt or Lean verification.
