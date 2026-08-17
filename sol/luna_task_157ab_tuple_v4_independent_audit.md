# Luna task 157ab - independent audit of tuple-v4 semantic repair

Role: adversarial independent implementation/mathematical auditor. You did
not implement v4. Do not edit its producer/checker/workflow, do not run local
GAP, and do not use git/GHA.

Allowed write only:

- `sol/luna_reply_157ab_tuple_v4_independent_audit.md`

Audit in full:

- `search/d972_b4_burau_fiber_v4.py`
- `search/check_d972_b4_burau_fiber_v4.py`
- `.github/workflows/d972-burau-tuple-v4.yml`
- `sol/luna_reply_157u_tuple_v4_semantic_repair.md`

The central semantic requirement is that the frozen 972 source word binds
only the roof/key. It need not lie in H'. For each row, v4 must construct an
exact h0 in H' over the same roof image and enumerate the complete right fiber
h0*K, where K is the exact kernel of H' -> P'.

Required checks:

1. Re-derive the group/fiber orientation. Verify h0*K (rather than K*h0 or a
   word coset) is the full fiber for the producer's multiplication convention,
   and that the raw five-A.18 defect is evaluated on precisely those elements.
2. Confirm H, H', projected sections, Schreier generators, normal closure,
   kernel enumeration, quotient cosets, and all stated order identities are
   exact and uncapped. Reject sampling or word bounds.
3. Verify the row-2 (-4,-8) and 956/972 nonzero-abelianization regression
   really prevents reintroduction of the invalid source-word-in-H' premise.
4. Adversarially check checker independence: no producer import/shared tuple
   helpers, lossless receipt replay, independent finite-field arithmetic,
   orientation negative tests, full K deletion test, h0 corruption tests, and
   status/count consistency.
5. Check q3/q4 calibration values and workflow dependency/artifact paths,
   SHA bindings, package hashes, resource stops, q5 a=2/4 matrix, final marker,
   and that all-pass stays UNKNOWN while a zero finite fiber is only a
   cross-checked finite-image candidate.
6. Run light Python compile/self-tests and YAML parse only. No local GAP/full
   campaign. Record exact hashes and commands. Any semantic or workflow flaw
   is a blocker and must stop dispatch.

Return PASS/FAIL for dispatch readiness, never an A/B conclusion.
