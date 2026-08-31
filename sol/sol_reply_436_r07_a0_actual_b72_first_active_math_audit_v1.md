# Task436 actual-b72 first-ACTIVE mathematical audit

Author: Sol / 2026-08-31

## Verdict

The two mathematical reductions are sound, but the present Luna task is
**NO-GO** until two local implementation ambiguities are removed.  One
currently authorizes a function which necessarily executes the expressly
forbidden 6,441-row preflight.  The other can make the final rank-rise test
use task179's raw exponent ABI instead of v12's normalized exponent ABI.

No production computation was run.

## 1. The 72-point quotient adjoint is exact

V12 `Quotient.contract` groups an input point as `h = r*z^j`, stores a raw
noncentral `b` coefficient in `vals[(0,r,j)]`, and emits `b(r)` as the sum of
the three phases (`search/d972_r07_a0_pb34_direct_quotient_owner_v12.py` lines
149--169).  Its triangular updates at lines 155--164 modify only the central
accumulator.  Hence, exactly as v412 (2.2)--(2.3) states,

\[
 N^*b(r)^*=e_b(r)^*+e_b(rz)^*+e_b(rz^2)^*.
\]

Central singletons, the other noncentral component, and the v410 predecessor
points have zero pairing with this label-specific dual.  The task436 direct
singleton and negative-neighbourhood gates are therefore appropriate, with
the negative test taken against the *merged global* 72-point support.

## 2. The Tietze adjoint has the stated orientation and sign

For old component `a` v12 emits new `b` at `v*x` with coefficient `-1`; old
component `b` emits new `b` at `v` with coefficient `+1`
(`...owner_v12.py` lines 185--194).  Solving `v*x=h` gives
`v=h*x^-1`.  Thus

\[
 e_b(h)^*\mathrel{+}=\mu(h),\qquad
 e_a(hx^{-1})^*\mathrel{-}=\mu(h),
\]

with no old-`c` term.  V412 (3.2) and task436 lines 91--100 are correct.

## 3. Only coordinates 0, 1, 2 occur and the formula constant is zero

Task179's actual `AllSevenModel` has exactly three block-1 occurrences,
`H1_fxy`, `H1_fxz`, and `H1_fyz`, at linked coordinates 0, 1, and 2
(`search/d972_r07_positive_common_word_colgen_v1.py` lines 650--656).
`occurrence_data` filters simultaneously by block and raw component before
adding a term (lines 699--729).  Since the adjoint above contains only block-1
old `a`/`b` keys, no other context coordinate can enter.

Its constant is read only from task179 exponent-dual keys (lines 735--745).
The accepted physical dual has zero normalized exponent coefficients and no
tau coefficient, and the constructed raw adjoint has no exponent key.
Consequently every formula has `K=0`.  Exhausting the finitely many
coordinate-target fibres of orders 9 is sufficient; no global Delta roster is
mathematically required.

## 4. V411's actor-adapted phase split is sound

The frozen PB3 PC marking is `(a,b,c)` and the PB4 marking is
`(a,b,p,c,q,r)`.  The selected `b` coordinate in PB3 and `a` coordinate in
PB4 are abelian coordinate homomorphisms, and `z3=abc`, `z4=abpcqr` have
selected coordinate one.  Thus each `ker(kappa)` is a subgroup transversal
and the displayed central direct product follows.  V411 correctly requires
the implementation to replay the PC power/conjugate relations rather than
enumerate either group.

Task179 embeds the PB3 free generators as `A12,A23`
(`search/d972_b345_seedspan_triple4_v1.py` lines 914--916), so every PB3 actor
has `kappa3=0`.  Its literal PB4 `pcontexts` and occurrence ordering
(`...positive_common_word_colgen_v1.py` lines 646--666) give phases
`0,e_x,e_x,0,e_x` in the table's order.  The inverse flags alter the Fox row,
not the substituted actor.  Finally, conjugation by the occurrence prefix
drops under a homomorphism, and left multiplication by an element of
`ker(kappa)` permutes the transversal while preserving the central phase.
The tau sum is therefore invariant as claimed in v411 Lemma 3.1.

This new PB3 split is a coordinate change, not v12's least-serialized PB3
blob convention.  A later tau-bearing implementation must rebuild/re-encode
the quotient under the new split; it must not reinterpret a v12 blob in
place.  Task436 is tau-free and need not perform that change.

## 5. Dispatch blockers and minimal repairs

### B1. `build_runtime` permission contradicts the 6,441-row prohibition

Task436 lines 122--125 permits reuse of task179 `build_runtime`, while lines
164--165 prohibit the 6,441-row scan.  The pinned function cannot satisfy
both conditions: it calls task175 `run_preflight` and then constructs and
compares the complete 6,441 relation roster
(`...positive_common_word_colgen_v1.py` lines 454--515).  It also constructs
all ten Q0 coordinate stores at lines 525--578 although only coordinates
0--2 are used.  Task435's bootstrap is genuine—it exposes the authenticated
task198 `Runtime`, actual E3/E4 objects, g760, and the real task179
`AllSevenModel` (`search/d972_r07_a0_actual_dual_weight_profile_v1.py` lines
40--61)—but it does **not** supply the `stores`, `A_maps`, `parents`,
`letters`, and `emitted` fields required by `FibreOracle`
(`...positive_common_word_colgen_v1.py` lines 912--1050).

Minimal repair: forbid a direct call to task179 `build_runtime`.  Require a
local selective section adapter, independently in producer and checker,
which starts from the authenticated task435/task198 objects and invokes only
the pinned task176 Gamma/Q0-section operations needed by coordinates 0--2.
The single Q0 state enumeration needed for exact inverse lookup is allowed;
task175 preflight, roster construction/equality, boundary machinery, and
unused-coordinate stores are not.  If the selective adapter cannot be built,
the terminal must be `UNKNOWN_RESOURCE`, not a silent call to
`build_runtime`.

### B2. The ACTIVE rank row must retain v12 normalized exponents

The formula dual has no exponent key, but the candidate physical column may
have nonzero normalized exponent coordinates.  Task179's literal
`occurrence_column` writes raw `E` coordinates modulo 3
(`...positive_common_word_colgen_v1.py` lines 755--775); compact relator
exponents divisible by 18 therefore disappear there.  V12 instead writes
`N1,N2 = (exp/18) mod 3` in `seed_v12`
(`...owner_v12.py` lines 255--266), and `Quotient.transform` merely passes an
unknown non-`R` key through (lines 175--184).  Therefore
`q.transform(model.occurrence_column(...))` is not a valid v12 physical row
for the rank-43 to rank-44 test and can give a false transition.

Minimal repair: bind the rank test and emitted pivot/digest to
`v12.seed_v12` followed by the exact v12 actor replay (or an independent
literal replay which explicitly adds the two `N` coefficients
`exp(relator)/18 mod 3` and rejects every raw `E` key).  Compare its quotient
part with the fresh eleven-occurrence replay.  The absence of exponent keys
applies only to the adjoint/formula constant, not to the candidate row.

### Resource guard

Task436's prohibition on serializing physical rows is correct.  Do not call
task435 `run_profile`/`checkpoint_state`, because that older checkpoint path
decodes and serializes every physical pivot
(`...actual_dual_weight_profile_v1.py` lines 103--113).  For the final rise,
`phys.reduce(candidate)` already proves a nonzero remainder and determines
the new pivot; use that or a shallow packed-row view, not a deep copy of the
1,813,674-nnz prefix.  Formula records belong in the final result; resume
checkpoints need only cursors and binding digests as task436 lines 160--163
already require.

NO-GO
