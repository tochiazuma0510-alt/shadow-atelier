# Luna Task 604 - grade-one independent full-routing v2 terminal type repair

Role: Luna implementation.  The exact v1 GHA run `33709557095` rebuilt all
8,059 rows, matched lower/grade ranks `1661/5044`, passed the exact routed
basis/lead comparison, and then failed only at `target_reduction` because
`candidate_files` returns the candidate remainder as `bytes` while line 359
compares it directly with a NumPy array.

Create a versioned successor, adding only:

1. `crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py`
2. `.github/workflows/d972-r07-a0-grade1-independent-routing-v2.yml`
3. `sol/luna_reply_604_r07_grade1_independent_full_routing_v2.md`

Do not edit or delete v1.  Do not change group, affine, Fourier, physical
aggregation, row order, owner arithmetic, expected hashes, bounds or claim
semantics.  Do not commit, push or dispatch GHA.

The load-bearing repair is exactly to decode the authenticated candidate
remainder bytes to the same canonical `np.uint8` packed-row shape before the
comparison.  Add one bounded fixture which would reject a nonzero/mutated
candidate remainder and accepts the canonical zero byte row; do not add a
second route or optional hardening.  The workflow must use v2 names/artifacts,
trigger only on workflow_dispatch or commit marker
`[fire-grade1-independent-routing-v2]`, pin the new checker/reply hashes and
retain the exact source/candidate downloads and 40/45/60-minute bounds.

Run `py_compile` and the bounded selftest.  Report exact bytes/SHA-256 and the
v1 failure receipt distinction: basis/ranks matched, terminal adapter failed,
so v1 produced no verdict and promoted nothing.
