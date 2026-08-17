# Luna task 154 — GF(5) finite Burau fiber continuation

## Division and scope

This is a versioned continuation of task 153, prepared while the corrected
GF(3)/GF(4) v1 lanes run on GHA.  Do not modify the v1 producer/checker.

- Producer Luna: implement `search/d972_b4_burau_fiber_v2.g` and report in
  `sol/luna_reply_154_burau_gf5.md`.
- Independent-checker Luna: implement
  `search/check_d972_b4_burau_fiber_v2.py` without importing GAP, the
  producer, or producer helpers; report in
  `sol/luna_reply_154b_burau_gf5_crosscheck.md`.

No local GAP run, commit, push, or workflow dispatch.  The parent is the sole
broker.  Temporary checks belong outside the repository.

## Frozen mathematical contract

Use the same fixed D972 roof, 972-row word/key artifact, five literal A.18
cofaces, opposite/paper product convention, and one-way finite obstruction as
task 153.  The new map is one common-word homomorphism

`E_5 : F2 -> P x GL(4,GF(5))^5`

at `(q,a)=(5,2)`, with optional explicitly selected `(5,4)` support.  The
permutation degree at either parameter is `36 + 5*5^4 = 3161`.

Let `H=im(E_5)`, `H'=[H,H]`, and `K=ker(H'->P)`.  For every frozen roof row,
enumerate the complete nonempty exact coset `h0*K` and evaluate

`D=(h5*h3)^-1*h2*h4*h1`

using the existing paper convention.  A row with zero identity defects is
only `CANDIDATE_B4_A_BURAU_FINITE_ZERO_FIBER`; only agreement with the
independent checker may promote it.  All-pass, timeout, cap, empty/broken
fiber, or incomplete enumeration is UNKNOWN and never B.

## Producer requirements

1. Copy the repaired v1 structure into a new v2 file.  Generalize prime-field
   vector digits correctly to all of `[0..q-1]`; do not retain the v1
   three-digit shortcut.
2. Default/accept only the preregistered GF(5) parameters above.  Reject zero
   and unsupported q/a values.
3. Preserve exact common-word provenance, `E(F2')=[H,H]`, all 972 word/key
   replays, complete kernel/coset enumeration, and the semantic premise
   digest.
4. Selftest the GF(5) vector bijection, braid/determinant relations,
   one-line serializer, `PaperProd`, `x13`, swapped A.18 factors, deleted
   kernel element, and corrupt word/key canaries.  Use parse-safe branching;
   no top-level conditional `QUIT`.
5. Emit a versioned receipt and final marker with q/a, degree, `|H|`, `|H'|`,
   projection order, kernel order, every exact fiber representative and both
   defect counts.  Producer status remains candidate-only.

## Independent checker requirements

1. Independently reconstruct GF(5) arithmetic/matrices, the compact roof,
   all six pure generators, five coface maps, `H`, `H'`, the pointwise roof
   kernel, every exact coset, and all defect counts.
2. Do not trust producer orders, kernel generators, representatives, counts,
   status, or witnesses.  Recompute and compare them.
3. Bind the exact source/artifact/semantic SHA values and reject producer
   self-promotion, empty fibers, metadata drift, missing rows, duplicate keys,
   truncation, syntax/error receipts, and malformed one-line permutations.
4. Provide lightweight selftests and negative mutations, but do not run the
   full q=5 scan locally during implementation.

## Acceptance

Report exact changed files, hashes, selftest commands/results, and resource
risks.  No A/B verdict is authorized from implementation or selftest alone.
