# Luna task 419 - fresh A0 owner using the PB3/PB4 direct quotients

## Role and objective

You are Luna, the implementation/calculation owner. Implement the smallest
fresh production owner which applies Sol v401 and v402 before positive-first
column generation. The purpose is to decide A0 substantially faster and
with bounded memory; it is not a refactor or a new framework.

Read completely:

- `sol/proof_r07_a0_pb3_central_orbit_direct_quotient_v401.md`;
- `sol/proof_r07_a0_pb4_central_split_direct_quotient_v402.md`;
- `sol/luna_reply_418_r07_pb4_central_split_crosscheck.md`;
- `search/d972_r07_a0_compact_positive_lazy_owner_v2.py`;
- `search/d972_r07_a0_batch_lazy_owner_v4.py`.

Do not modify any existing producer, checker, proof, workflow, checkpoint, or
v220 file. Do not decode or transform the 129 MB task416 checkpoint. Do not
run actual A0 locally, commit, push, or dispatch GHA.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v1.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v1.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v1.g`;
4. `sol/luna_reply_419_r07_a0_pb34_direct_quotient_owner.md`.

## Frozen source and mathematical contract

Reuse and byte-pin the authenticated task413/v2 runtime, compact 44-relator
roster, occurrence semantics, normalized exponent coordinates, exactification,
and sparse positive-first loop. Reuse task416's same-dual batch insertion
only if it remains simpler than single insertion. Never build a PB3 or PB4
translated boundary closure.

For each of the two E3 occurrence blocks, transform every target/correction
row by the exact map `Pi3*J_T` of v401. Construct central
`z=A12*A13*A23` from the marked E3 images and fail closed unless it is
central, nontrivial, and order three. Use deterministic three-point orbit
coordinates. The two PB3 translated boundary families must disappear
completely from the live oracle.

For the E4 block, use marked order
`A12,A13,A14,A23,A24,A34`, new order `b,c,p,q,r,z`, and literal
`z=[1,2,4,3,5,6]`. Byte-pin and require the accepted task418 certificate.
Apply the six-sparse Fox map (v402 (2.2)), then the constructive quotient

```text
(F3[H0]^5 / D0) direct_sum F3[H] / (N I_H0).
```

Compute `kappa` from the first PC coordinate and canonicalize
`h=h0*z^j` without subgroup enumeration. The five central commutator
families must disappear from the live oracle. Generate the remaining six
action relators directly from the literal substitutions in v402 (1.4), and
run the exact support-hitting lazy oracle only for their H0 translates.
Translations differing by a central power must canonicalize to the same H0
translation. Do not keep the old eleven-family scan under another name.

All target columns and all compact correction columns must pass through the
same occurrence-tagged quotient maps before aggregation. Keep the two E3
tags and the E4 tag distinct. Preserve the v400/v396 prohibition on early
physical aggregation.

## Positive terminal and claims

Zero in the direct quotient is allowed to become `COMMON_WORD` only after:

1. reconstructing the selected literal compact correction and v399
   exactification;
2. checking joint-kernel identity and exact exponent pair `(0,0)`;
3. independently recomputing the unquotiented target and correction Fox
   rows, applying `J_T/Pi3` and `J4/Pi4`, and checking their quotient equality;
4. replaying every selected one of the six action-boundary columns and its
   H0 translation;
5. checking the two closed survivor components and global scalar exactly.

The kernel equalities proved in v401/v402 are the membership theorem; do not
rebuild the eliminated translated boundary closures merely to issue the
positive terminal. The receipt must retain enough quotient/action ancestry
for the independent checker. On any incomplete schedule or resource cap,
return `UNKNOWN_RESOURCE` with a fresh resumable checkpoint. Never emit
NONMEMBER from an unfinished lazy schedule, and never claim fake, compatible
cofinal lift, Ihara witness, or `verified`.

The helper-nonshared checker must not import the producer. It may byte-pin
and reuse the already independent q3 PC/permutation implementation, but it
must reconstruct both normal maps, the six action relators, the selected
literal word, and the final quotient identity itself.

## Bounded gates and production handoff

Locally run only compile/help plus fixtures lasting seconds:

- exhaustive tiny `F2 x C3` comparison of `ker(Pi3)` with the two translated
  commutator columns;
- exhaustive tiny `(finite H0) x C3` comparison of the v402 central quotient
  kernel with the five translated commutator families;
- actual frozen E3 and E4 finite split gates, without matched-group BFS;
- direct-versus-quotient translation equality for all marked-generator
  translates of every base row;
- wrong central word, wrong translation orientation, dropped survivor, and
  checkpoint-corruption rejection.

The GHA driver must start fresh, print progress within 60 seconds and after
each rank increase, use a controlled RSS cap, and write a resumable artifact
on every `UNKNOWN_RESOURCE`. Report exact byte/SHA pins, fixture wall time,
the literal driver path, and a conservative GHA time/RSS estimate. Avoid
profiling infrastructure, multiprocessing, SAT, broad mutation campaigns,
or unrelated repairs.

`TASK419_R07_A0_PB34_DIRECT_QUOTIENT_OWNER`
