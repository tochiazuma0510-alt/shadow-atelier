# Luna task 436 - actual A0 72-point adjoint and first ACTIVE correction

Task435 GHA run `33391325650` completed at source commit
`cadbe6eda7159889279fbf63c24641d026df97d9` and passed its independent
checker.  Its actual normalized dual has:

```text
physical rank / payload nnz          43 / 1,813,674
identity compact attempted/retained  44 / 43
v404 candidates/retained/final       0 / 0 / empty
dual support                         24
dual key types                       exactly 24 x (block 1, label b, blob 40)
three tau coefficients               0,0,0
normalized exponent coefficients     0,0
dual digest                          c75895737537f157fbbfedcdc2c41ed31c8bf0ca9bddda060079ffcda7604efd
target/remainder pairing              1
```

This is the tau-free, label-specific specialization of v410.  Build the
smallest exact consumer that compiles all 44 weighted formulae and then uses
the accepted v142/v143 singleton-fibre machinery to return the first literal
ACTIVE correction if it fits the registered cap.  Do not restart occurrence
closure and do not serialize the 43 large physical source rows.

## 1. Allowed outputs

Create only:

1. `search/d972_r07_a0_actual_b72_first_active_v1.py`
2. `crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py`
3. `search/d972_r07_a0_actual_b72_first_active_gha_driver_v1.g`
4. `sol/luna_reply_436_r07_a0_actual_b72_first_active_v1.md`

Do not modify task435, v12, task179, v220, a workflow, or any running A0
job.  No local production run, commit, push, dispatch, artifact download, or
release.

## 2. Rebuild the exact cheap physical prefix

Import the byte-pinned task435 producer and v12 owner.  Reuse task435's exact
bootstrap and repeat only:

- the 44 identity compact physical columns;
- the exact v404 action oracle until empty; and
- normalized `phys.dual(target)`.

Require every numeric/type/digest row displayed above.  These are now a
cross-checked input receipt, not a value to manufacture.  On drift fail
closed.  Keep the 43 rows only in memory.  The output/checkpoint must contain
only ranks, digests, compact formula records, and a selected literal source;
never the full rows or decoded runtime objects.

## 3. Exact label-specific quotient adjoint

Let the 24 dual keys be

\[
 \lambda=\sum_r a_r\,b(r)^*.
\]

For v12 `contract`, the noncentral output `b(r)` is exactly the orbit sum of
the raw new-`b` coordinate.  Therefore

\[
 N^*b(r)^*=\sum_{j=0}^2 e_b(rz_3^j)^*.
\]

Construct the merged new-coordinate adjoint by the 72 candidate evaluations

```text
for each actual dual b(r), for j=0,1,2: h = r*z3^j
```

and merge modulo 3.  Report candidate count 72 and actual merged support.
For every candidate directly evaluate a singleton through `q.contract` and
check its pairing with the physical dual.  Also use the complete v410 reverse
neighbourhood as a negative canary: central, other-component, and predecessor
singletons not selected by the displayed formula must pair zero.

Do not enumerate an E3/PB3 roster.

## 4. Apply the PB3 Tietze adjoint exactly

V12 lines 186--188 give

\[
 e_a(v)\mapsto e_z(v)-e_c(vxy)-e_b(vx),\qquad
 e_b(v)\mapsto e_b(v),\qquad e_c(v)\mapsto e_c(v).
\]

Thus one new-`b` adjoint coefficient `mu(h)` gives exactly

```text
old component b at h          += mu(h)
old component a at h*x^-1     -= mu(h)
```

in block 1.  Build these actual task179 `R` keys with the owner ABI and merge
modulo 3.  For every retained old key check directly that its coefficient is
the pairing of the physical dual with `q.transform` of that old singleton.
Report candidate/merged counts and a digest.  There are no exponent keys.

## 5. Compile all 44 exact formulae

Use the already loaded actual `AllSevenModel.occurrence_data` with the raw
old-coordinate adjoint.  For every compact relator, emit:

- seed index and literal word digest;
- exact public formula and digest;
- `K`, distinct merged target count, coordinate histogram, and
  `W=sum(kernel_order[coordinate])` using
  `(9,9,9,9,9,1,1,1,3,3)`;
- eleven occurrence term counts; and
- identity-state formula scalar and direct physical-dual scalar.

Require `K=0`, coordinates contained in `{0,1,2}`, and equality of formula
and direct scalar.  Do not drop equal targets before mod-3 merging and do not
use one occurrence as a proxy for the eleven.

## 6. Find the first literal ACTIVE state

After all 44 formulae are durably emitted in memory, load only the accepted
task176 v142--v143 section machinery.  **Do not call task179 `build_runtime`:**
that function necessarily reconstructs task175 and the complete 6,441-row
roster before returning.  Instead build a local selective section adapter,
independently in producer and checker, from the authenticated task435/task198
objects and the pinned task176 primitives.  It must reconstruct the 243 Gamma
states, enumerate the shared 1,469,664-state Q0 section once, retain only the
coordinate-0/1/2 section stores and `S0`/`S1`/`S2` A/L/kernel data, and expose
the v142 least-singleton plus complete order-9 kernel fibres.  A selected
literal word is replayed in all ten task198 coordinates; the seven unused
section stores are never materialized.  Task175 preflight, roster
construction/equality, boundary machinery, and a 6,441-row loop are forbidden.
Use task176's direct ten-coordinate word evaluator once for a singleton
representative and once per cached kernel state, then multiply the packed
rows.  Do not spend task198's bounded `states_direct` meter on every fibre
candidate; reserve it for the final selected ACTIVE replay.
If this selective adapter cannot be completed within the cap, return
`UNKNOWN_RESOURCE` at that exact phase.  Scan exactly the 44 formulae in seed
order.  Since every `K=0`:

1. visit merged `(coordinate,target)` in canonical order;
2. obtain the v142 least literal singleton representative;
3. enumerate the complete registered kernel fibre (order 9 here);
4. evaluate the merged formula; and
5. stop at the first nonzero value.

For a hit, independently construct the literal conjugate and replay all ten
linked coordinates and all eleven Fox occurrences.  The physical row and its
rank transition must be constructed with v12 `seed_v12` followed by the exact
v12 actor/conjugation replay, so that its normalized exponent coordinates are

```text
N1 = (exp_x/18) mod 3,   N2 = (exp_y/18) mod 3.
```

Task179 `occurrence_column` uses raw exponent keys modulo 3 and is therefore
not an admissible physical row for this test.  Require that the v12 row's
quotient part agrees with the fresh eleven-occurrence replay, reject every raw
`E` key, apply the direct v12 quotient, and require both

\[
 \langle\lambda,\bar C_i(\delta)\rangle=F_i(\delta)\ne0
\]

and a strict rise from physical rank 43 to 44.  Use `phys.reduce(candidate)`
or insert once into the live prefix and stop; do not deep-copy the
1,813,674-nnz echelon.  Emit the literal `delta_word`, seed word/index, formula,
ten coordinate blobs, direct physical row digest, scalar, new pivot, and
rank transition.  Status is `ACTIVE_COLUMN_READY`; it is genuine A0 rank
progress but not A0 membership or a common word.

This v1 is positive-first.  If all 44 complete fibres are exhausted, emit
`CURRENT_DUAL_CORRECTION_EMPTY` **only if** the independent checker also owns
and repeats the selective enumeration.  Otherwise downgrade the producer's
complete-but-unpromoted exhaustion to
`UNKNOWN_RESOURCE:empty_requires_independent_exhaustion`, retaining exact
formula/target/kernel counters and digests.  This is preferable to delaying an
ACTIVE-capable implementation merely to duplicate the large Q0 selector in
the checker.  Together with the already empty v404 oracle, a genuinely
cross-checked empty result would be an A0 separator and therefore requires a
dedicated promotion task.  If any cap fires, emit only `UNKNOWN_RESOURCE` with
phase/counter/limit.  Never call a prefix cap empty.

## 7. Cost and checkpoint discipline

- Producer wall cap: 2,400 seconds; RSS cap: 4.8 GB.
- The three selected fixed-width section stores occupy exactly
  `3*40*1,469,664 = 176,359,680` bytes.  This, rather than task176's ten-store
  1.43-GB payload, is the memory contract; report the observed selected-store
  bytes and peak RSS.
- Print progress after the prefix, adjoint, each formula, runtime section
  build, and each completed seed fibre.
- No occurrence queue or descendants.
- No physical rows, Q0 stores, group objects, or duplicate echelons in a
  checkpoint/artifact.  The 108-second prefix and selective runtime are
  rebuilt after resume; persist only the last completed formula/seed/target
  cursor and exact digests.
- The selective coordinate-0/1/2 task176 adapter is built at most once.  No
  task179 full runtime, task175 preflight, boundary correlation, boundary
  closure, global Delta scan, or 6,441-row scan is allowed.

## 8. Independent checker and bounded local tests

The checker independently repeats the prefix, 72-point adjoint, Tietze
adjoint, 44 formulae, and any selected literal/direct row.  For an ACTIVE
receipt it need not repeat the selector search: directly evaluate the literal
word in all ten linked coordinates, require the claimed singleton target,
evaluate the rebuilt formula, and replay the full physical row/rank rise.  It
must not trust serialized raw duals or formula targets.  The checker may
accept `CURRENT_DUAL_CORRECTION_EMPTY` only after its own complete selective
enumeration; otherwise that producer outcome must already have been typed
`UNKNOWN_RESOURCE`.  Include mutations for:

- one omitted physical dual key;
- a nonzero tau/exponent key entering this specialized owner;
- one omitted central power;
- wrong `h*x^-1` orientation or sign;
- one omitted/altered merged target;
- one skipped kernel-fibre state; and
- a fake ACTIVE scalar or non-rank-raising row.

Run locally only compile, bootstrap-free fixtures, algebraic toy mutations,
checker self-test, reconstructed GAP command, and `git diff --check`.  The
driver requires an external preamble and runs production plus checker under
the stated caps.
