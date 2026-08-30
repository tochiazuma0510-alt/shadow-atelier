# Luna task 421 - make the A0 direct-quotient selector production-correct

## Verdict and scope

You are Luna, the implementation/calculation owner.  Task420 v2 is **NO-GO
for production**.  Do not patch or dispatch it.  Produce a versioned v3 with
the smallest corrections below.  Read completely v401--v405, task420 and
its addendum, the four task420 outputs, and the occurrence owner already
implemented in
`search/d972_r07_a0_compact_pc_invariant_owner_v1.py` lines 549--868.

Do not modify existing files, workflows, checkpoints, proofs, or v220.  Do
not run actual A0 locally, commit, push, or dispatch GHA.

Allowed new outputs only:

1. `search/d972_r07_a0_pb34_direct_quotient_owner_v3.py`;
2. `crosscheck/check_d972_r07_a0_pb34_direct_quotient_owner_v3.py`;
3. `search/d972_r07_a0_pb34_direct_quotient_owner_gha_driver_v3.g`;
4. `sol/luna_reply_421_r07_a0_pb34_direct_quotient_owner_v3_production_repair.md`.

## Confirmed v2 blockers

1. Lines 337--349 put raw old-coordinate occurrence rows into the occurrence
   echelon.  The normal maps are called only after physical aggregation.
   This is not v405 and recreates the large raw occurrence closure.
2. The occurrence actor uses `q.eval([abs(letter)])`.  Each occurrence has a
   different substitution.  The actor must be the frozen
   prefix-conjugate of

   ```text
   q.eval(model._substitute([letter], spec.left, spec.right, spec.lift)).
   ```

3. The same first-PC `kappa` transversal is used for PB3 and PB4.  Only PB4
   has the task418 `H0` split.  PB3 must retain v401's deterministic
   least-serialized central-orbit representative.
4. `pure_relations(4)[2:8]` selects the three old-A12 and three old-A13
   action rows.  The six v402 rows are exactly
   `pure_relations(4)[5:11]` in the frozen old order.  Construct them
   explicitly and require equality to that slice.
5. Target zero returns `UNKNOWN`; v403 strict positive reconstruction and
   independent replay are absent.  Thus this owner cannot produce the A0
   common word it is meant to find.
6. A resource stop during the seed loop writes `seed_cursor<44`, but every
   resume skips the seed loop entirely.
7. Checkpoint writing materializes several complete copies
   (`marshal.dumps`, compressed bytes, `header+packed`), and the live queue
   uses `pop(0)`.  These are avoidable memory/time regressions.
8. The checker verifies symbolic strings and accepts only incomplete
   terminals.  It does not reconstruct the normal maps, occurrence actors,
   closure, action ancestry, or a positive word.
9. Production does not byte-read the task418 certificate, does not assert
   that the six action rows have zero closed survivor, and does not compare
   the support accumulator scalar with a direct row pairing.

## Exact occurrence quotient and actor

Use separate quotient rows for all eleven occurrences before the occurrence
echelon.  For a raw occurrence gradient:

1. keep its occurrence tag;
2. apply the appropriate old-to-new Tietze map;
3. PB3: contract using the least serialized representative of
   `{h,h*z3,h*z3^2}`;
4. PB4: contract using `h0=h*z4^(-kappa(h))` and require the accepted
   task418 certificate;
5. prefix every resulting normal coordinate with its occurrence ordinal;
6. append the normalized exponent pair once, not once per occurrence.

Implement the induced actor directly on normal coordinates using a sparse
section, never by acting on an aggregated row:

- a noncentral normal coordinate is lifted at its stored representative;
- `u0` lifts to the central coordinate at `h0`, `u1` at `h0*z`;
- `tau=1` lifts to the constant central vector on the identity central
  orbit, namely central coefficients at `r,r*z,r*z^2` for PB3's canonical
  identity-orbit representative and at `1,z,z^2` for PB4;
- left translate that new-basis lift by the correct prefix-conjugated
  occurrence actor; then apply the same central contraction again.

This realizes `Q_o L_actor iota_o` from v405 (1.6).  A bounded gate must
check `normal -> section -> normal` is identity for every coordinate type
and that acting before/after taking a different kernel representative gives
the same normal row on nontrivial samples.

Run the exact 44-seed plus four-actor queue in this eleven-tag quotient.
Use a queue list plus cursor/deque, never `pop(0)`.  A physical aggregate is
inserted only for an occurrence pivot and must be computed from the stored
normalized row `occ.rows[pivot]`, never from the unreduced incoming candidate.
Physical dependence must not control its four children.  Preserve the
occurrence pivot's normalized linear ancestry.

## Exact six-action roster

In old PB4 generator indices `(A12,A13,A14,A23,A24,A34)`, define

```text
b=2, c=4, p=3, q=5, r=6
phi_b(p) = [3,6,3,-6,-3]
phi_b(q) = [3,6,-3,-6,5,6,3,-6,-3]
phi_b(r) = [3,6,-3]
phi_c(p) = [3]
phi_c(q) = [5,6,5,-6,-5]
phi_c(r) = [5,6,-5]
rho_su    = [-s,u,s] + inverse(phi_s(u)).
```

Require the resulting six rows, with lengths `(8,12,6,4,8,6)`, to equal
`runtime.old.pure_relations(4)[5:11]`.  Transform each base row and fail
unless every retained coordinate is a PB4 `b,c,p,q,r` coordinate: all
`u0,u1,tau`, PB3 and exponent components must be zero.  Use v404's
same-translation-merged `t=g*h^-1` accumulator; for every materialized hit
compare the accumulated scalar with the direct dual pairing before insertion.

## Positive terminal

Extend reduction to return source coefficients with the same sign convention
as task413.  From selected physical sources:

1. recursively expand each selected occurrence pivot through its normalized
   seed/actor/elimination ancestry into a finite product of conjugates of the
   44 literal relators; coefficient two means inverse;
2. retain the selected six-action family, canonical H0 translation and
   coefficient as boundary ancestry, never as part of the correction word;
3. apply the registered v399 `(u0,v0)` cube exactification and require exact
   integer exponent pair `(0,0)`;
4. require the exact word's value to be identity in every joint state;
5. freshly evaluate the unquotiented H1/H2/pentagon Fox difference between
   `g760` and `g760*c_exact`, apply the three normal maps, and compare it with
   the selected correction source sum;
6. freshly replay every selected six-action translate and require
   `target + correction + selected_actions = 0`, including all PB3 normal,
   PB4 survivor and exponent coordinates.

Only these gates may emit `COMMON_WORD`, set `A0_membership=true` and
`common_word=true`, and serialize the literal word plus all selected
ancestry.  `fake`, `Ihara_witness`, `compatible_lift`, and `verified` remain
false.  If an independently replayable negative certificate is not
implemented, an exhausted nonmember-looking branch remains
`UNKNOWN_RESOURCE` as allowed by task420.

The helper-nonshared checker must not import the producer.  For a positive
artifact it independently reconstructs the 44 roster, the literal word,
all joint values, the old Fox rows, both central normal maps, the exact six
action roster/translations, survivor coordinates, exponent pair and final
zero equality.  It must reject mutations to the word, one occurrence actor,
PB3 transversal, PB4 kappa, `tau`, one action family/translation/coefficient,
and one survivor coordinate.

## Resume, memory and bounded gates

- Stream marshal into gzip and stream-hash/copy into the atomic seal as in
  task413/v1; never hold a second full checkpoint in bytes.
- Persist both complete echelons, normalized ancestry, source DAG, all
  sources, seed cursor, queue plus queue cursor, phase and action state.
  Continue seeds from `seed_cursor`; do not assume 44 on resume.
- A split-run fixture interrupted during seeds and another during actors must
  reproduce the uninterrupted rank, remainder and source coefficients.
- Print preflight/runtime progress immediately and at least every 60 seconds
  or 32 occurrence pivots; do not serialize the full checkpoint on every
  rank rise.
- The GHA driver pins both bytes and SHA-256, passes `--resume` whenever the
  authenticated checkpoint already exists (it must not delete it), requires
  a fresh checkpoint on every `UNKNOWN_RESOURCE`, streams logs and invokes
  the independent checker.
- Run only compile/help and seconds-scale fixtures locally.  No full A0,
  multiprocessing, SAT, profiling framework, workflow edit, commit, push or
  dispatch.

`TASK421_R07_A0_PB34_DIRECT_QUOTIENT_OWNER_V3_PRODUCTION_REPAIR`
