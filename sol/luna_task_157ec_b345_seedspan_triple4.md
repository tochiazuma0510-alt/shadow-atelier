# Luna task 157ec - four preregistered triple-cube seeds and a lossless affine dual

## Role and objective

You are Luna.  Implement a new versioned successor to 157eb.  Rebuild the same
fixed D2 prefix and the same ordered 104-seed family, append exactly four
preregistered positive triple-cube words, and solve the corrected-Def2.9 affine
system over `F3^108` in target order.  If the system is inconsistent, export a
lossless normalized dual contradiction witness rather than only a row-space
digest.  If it stays consistent, continue through all 33 acceptance targets and
perform the same literal positive replay as 157eb.

This is the highest-information successor to cross-checked run `32317468871`.
That run proved only that target 6 is inconsistent for the fixed prefix and the
old 104-seed span: 33,293 coordinate equations, rank 50, nullity 54.  Its
receipt SHA is

```text
dfb0627849e29bd9be83e8dc74de6845e8263ed3fe5ced5d04e37bb7d9b9076a
```

The old receipt is provenance and calibration only.  It is not an input and
contains neither the matrix nor a dual witness.  Do not resume or import its
basis, rows, pool IDs, or Gaussian state.

## Authorized files

Create only these four new files:

```text
search/d972_b345_seedspan_triple4_v1.py
search/check_d972_b345_seedspan_triple4_v1.py
search/d972_b345_seedspan_triple4_gha_driver_v1.g
sol/luna_reply_157ec_b345_seedspan_triple4.md
```

Do not edit the 157eb files, workflow, q3 files, claims ledger, dialogue book,
or any other worktree file.  Temporary selftest files belong outside the repo.
Do not run GAP, GHA, Git, or a full production scan.  The parent session owns
commit/push/dispatch.

## A. Frozen inputs and same-job reconstruction

Pin and fail closed on the following sources and metadata:

```text
157eb producer  804414e69155f2b8d9aa2a2412b0120d64eb373945a0fa6163f1214b4673e19a
157eb checker   67ad8d8227f1a8a60e481977fd2d07d819d532deb2651cd28667db997ec46081
157eb driver    1c7a6169292146ada37007d2e5b9a48f21b7f1ae545fe84a969409d8b9741057
q3 producer     b95fc29b326c3d6a378249cdeb03595eed8d0211a7fe0358fc02447d70d5f755
q3 checker      ddb52ddae18327209692f0f6eb8b4f65cbdd446155be660a621de24274cc3f73
q3 driver       c397cd837ff6814f7b7a8ca0604c6aed54fa0bc85bb577516ea1c6e7df83a831
q3 artifact     3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72
v9 producer     7dede323c3c52bc7cf7d99af6d542b3683823879a4bb3e340aca8ce53dcf196f
strong prefix  d41123a8c4803f6ac67387ac9bbf1a32f797b90d6233605a5511713f215244be
formula         b43284edac5b4dae945bb3b30ac0f177dc47df8724cb32acd6057b26d82a27ef
old 104 digest  e99602b0981251e4bb81ab0d2113791563bc9ec9df2a45828aea2880ec6d2f9e
```

Run the q3 producer and its independent checker exactly once in a child GAP
process, then fresh-rebuild the immutable prefix.  The required prefix binding
is unchanged:

```text
BFS translations       32768
directed translations    207
columns                362725
pivots                 362709
dependent columns          16
stable rounds SHA      75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d
translations SHA       a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f
columns SHA            cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343
blocker history SHA    b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53
```

Keep the 18,000-second / 4.5-GiB soft guards, exact ResourceStop observed/cap
ledger, phase/seed/target coordinates, transactional target absorption, and the
four terminal/claim discipline from 157eb.

## B. Exact 108-word manifest

Rebuild the old 104 words byte-for-byte in their 157eb order.  Then append the
following four words in the displayed order.

Let

```python
records = q3["correction_fibre"]["records"]       # frozen JSON order
cubes = [
    reduce_word(r["word"] + r["word"] + r["word"])
    for r in records[1:]                           # record 1 is the empty word
]
```

Require exactly 27 frozen records, record 1 exactly empty, 26 nonempty records,
26 pairwise distinct reduced cubes, and

```text
digest_obj(cubes) = 3d26302d01b3c202350fdb8b9ea81badeaf9c62913c9e94be7e049ad7c391463
```

Also require this literal record-tail order to equal the old 157eb
first-occurrence/deduplicated cube order; do not silently choose one order when
they differ.

Use these 1-based positions in `cubes`:

```text
(2,  9, 18)
(9,  9, 10)
(9, 11, 11)
(18,18, 20)
```

Equivalently, these are 1-based `correction_fibre.records` positions

```text
(3,10,19)
(10,10,11)
(10,12,12)
(19,19,21)
```

For each tuple `(a,b,c)`, construct exactly

```python
seed = reduce_word(cubes[a-1] + cubes[b-1] + cubes[c-1])
```

This is an ordinary left-to-right product.  Do not invert, sort, commute, or
deduplicate factors.  Repeated indices are literal repeated copies.  Require
the following exact length/SHA rows:

```text
(3,10,19)   408  d810d557ca1128924da9ab04f0f304dfbf4d60503db187dfde531085b43a124f
(10,10,11)  816  0fb7a48541e413091779494e54d351e745569859e1d8ed68fe24301b8ae0f3b6
(10,12,12)  816  05fff82ae07daf70997f9164fbbd2a6a22d7340b277eb9203d4c890ae98bb44b
(19,19,21)  408  8d68e311a631fdc8d94e9729a273aefb6ff25f5bab99c7b59e4c9488c0080e5c
```

The SHA is the same canonical `digest_obj(word)` convention as 157eb.
Independently reconstruct and gate all four in the checker.  Reject a
zero-based/one-based drift, any factor permutation, replacement of a repeated
factor by one copy, inverse/reversal, or a different reduction order.

Require all 108 literal words to be pairwise distinct.  The four appended
words must be distinct from the old 104 and from one another.  Record, for
each word, lossless provenance:

```text
family = commutator104 | cube_triple4
global seed index 1..108
source record tuple and cube-position tuple
ordered product rule and repeated-index flag
reduced length and canonical word SHA
exponent sums
E3 value
31 unique E4 occurrence-context values / 46 named-use coverage digest
```

Require every new word to have exponent sums `(0,0)`, E3 identity, and identity
in all 31 exact E4 contexts covering the same 46 named source/occurrence uses as
157eb.  Reconstruct the context registry; do not import booleans.  These gates
make arbitrary ordered coefficient products source-typed and preserve the raw
Fox affine theorem.

The formal registered universe is exactly `old104 + these4`.  The four were
preregistered before this 108-variable solve, but they are **not** asserted to
exhaust all triple products or all depth-3 corrections.  Do not claim a minimal
depth unless an explicit earlier-universe equality test is added; the receipt
should call them `four_preregistered_positive_triple_cube_words`.

## C. Raw affine theorem and 108-variable solve

Use the same raw left-Fox theorem as 157eb, before any D2 quotient:

```text
D(R_j(f0*c(a))) = z_j + sum(k=1..108) a_k delta_j,k in C1,
c(a) = seed_1^a1 ... seed_108^a108,  a_k in F3.
```

For every target and every seed, preserve the independent formula/direct raw
Fox equality.  Coefficient `2` means two literal copies in the fixed product
order; it is not an inverse shorthand.  The typed WordExpr route and the flat
or independently streamed route must agree.

Targets remain in the corrected-Def2.9 order: 33 acceptance targets followed
by 17 T/TS diagnostics.  The 17 diagnostics never enter acceptance.

Do not apply the old target-1--5 identity shortcut to the four new columns.
Compute their exact raw gradients and fixed-prefix remainders.  It is allowed
to reuse the already proved zero columns for the old 104 only if the new
checker independently repeats the old zero-row binding.  Absorb equations
target-major, canonical coordinate-major, with seed columns 1..108.

If targets 1--6 remain consistent, continue all 33 targets.  If all 33 are
consistent, choose the same canonical free-variable-zero solution, materialize
the literal 108-seed correction, and replay all quotient, raw-Fox, fixed-prefix
proof, source, charming, hexagon, pentagon, and corrected-Def2.9 gates.  Then
run and record the 17 diagnostics without promoting them.

## D. Lossless dual contradiction witness

Augment the affine Gaussian solver with exact provenance for each input
coordinate equation.  Label an original equation by

```text
(target ordinal, target name, component, canonical E4 bytes)
```

Never use transient pool IDs in the public witness.  Preserve F3 provenance
through row normalization and elimination.  On the first reduced contradiction
`0 = c`, normalize by `c^-1` so the public witness `y` satisfies

```text
A_(q,k) = delta_(k,q),
b_q     = -z_q,
A a     = b,
y^T A   = 0 in F3^108,
y^T b   = 1 in F3,
equivalently y^T z = 2 in F3.
```

This RHS/sign convention is load-bearing and must be explicit in the receipt;
reject the opposite-sign convention in producer/checker selftests.  Here `A`,
`b`, and `z` are the exact accumulated coordinate equations through the first
inconsistent target.  Store the ordered sparse support of `y`, with
coefficient `1` or `2`, the originating equation labels, target boundary,
support count, support digest, all-108 annihilation digest, and normalized RHS.

Use the standard incremental-echelon provenance invariant rather than keeping
unit provenance for all 33,293 equations.  A stored pivot row may reference
only the selected pivot-origin labels introduced up through that row; with rank
at most 108 its support is at most the current rank.  A contradiction adds the
current input label, so its support is at most rank+1, hence at most 109.
Gate this invariant after every normalization/elimination and account the total
live provenance entries.  Register a dual-support cap of `128`; a cap hit is
`UNKNOWN_RESOURCE`, never a mathematical negative.  Never fabricate or
truncate provenance.

Freeze the first normalized contradiction witness when it appears, but finish
absorbing the remaining canonical coordinate rows of that target so the public
coordinate count, rank, row-space digest, and target boundary retain the 157eb
meaning.  Do not replace the first witness with a later contradiction.  Emit
the terminal only after the whole first-inconsistent target is committed.

The checker must independently rebuild all base/seed remainders and directly
verify both equations above from the public coordinate labels.  It must also
recompute the affine rank/nullity/consistency and row-space digest.  A digest
alone is not the dual certificate.

If the first contradiction is target 6 and every dual coordinate is in target
6, additionally record it as a normalized `target6_fixed_prefix_functional`.
That phrase remains prefix-only.  Do **not** claim a full-D2 obstruction unless
a separate future lane proves E4-action closure and annihilation of every D2
translate.

## E. Terminals and exact scope

Use exactly four terminals:

```text
B345_SEEDSPAN_TRIPLE4_POSITIVE
B345_SEEDSPAN_TRIPLE4_SEARCH_INCOMPLETE
B345_SEEDSPAN_TRIPLE4_UNKNOWN_RESOURCE
B345_SEEDSPAN_TRIPLE4_UNKNOWN_INPUT
```

`POSITIVE` means one literal correction in the registered 108-word subgroup
passed all 33 acceptance gates with independently replayed prefix proofs.  It
is one finite-stage witness, not B4-B or a cofinal/profinite theorem.

`SEARCH_INCOMPLETE` is allowed only for a failed registered source/occurrence
preflight or an exact affine inconsistency.  For an inconsistency it must carry
the normalized dual witness and say exactly:

```text
claim_classification = unknown_not_obstruction
claim_scope = registered_old104_plus_four_triple_cube_affine_span_against_fixed_D2_prefix
full_D2_claimed = false
full_H3_claimed = false
all_triple_products_claimed = false
all_depth3_claimed = false
negative_claimed = false
B4_A_claimed = false
B4_B_claimed = false
```

`UNKNOWN_INPUT` remains restricted to missing/drifted authenticated external
input, schema, or pins.  Internal theorem/order drift is a hard failure.
`UNKNOWN_RESOURCE` uses the closed registered reason list and exact attempted
count/cap/comparator plus current phase/target/seed and completed-target state.

## F. Independent checker, schema, and selftest

The checker must be independently implemented and must not trust producer
helpers, booleans, pool IDs, or row digests.  It must reconstruct q3, all 108
words, all occurrence contexts, the immutable prefix, raw/direct gradients,
remainders, affine equations, the dual witness, and any selected positive
proof.

Use exact stage-aware top-level/nested key sets.  Pin producer, checker, driver,
task, all frozen sources, q3 artifact, and output paths.  Retain pipefail/tee,
stale artifact cleanup, exactly-one producer/checker/terminal markers, and
runtime-only q3 normalization discipline.

The single combined bounded selftest must exercise the same production
validator core and reject, at minimum:

- cube-position versus record-position off by one;
- tuple factor permutation, inverse, or repeated-index collapse;
- any of the four length/word-SHA rows;
- old/new family boundary or global seed order drift;
- a new word equal to an old word;
- one failed E3/context/named-use gate;
- target1--5 shortcut applied to a new column;
- formula/direct raw gradient drift for an old and a new seed;
- coefficient-two interpreted as inverse or one copy;
- dual coordinate target/component/E4-byte/coefficient mutation;
- `y^T A`, normalized `y^T b`, `y^T z`, or RHS-sign mutation;
- row-space/rank/nullity/consistency drift;
- a diagnostic promoted into acceptance;
- positive proof, terminal, claim-scope, pin, and resource-partial mutations.

One fixture must contain a nonzero base vector, 108 columns, and a genuine
inconsistency whose normalized dual has support greater than one.  Another must
be consistent and reach the literal selected replay.

## G. Performance contract

The cross-checked 157eb producer used 664.01 seconds and 738.7 MB peak RSS;
the fresh prefix itself ended near 344.5 seconds and target 6 used about 315
seconds for 104 columns.  Four extra columns should add only a small fraction.
Keep the target-major streaming/rollback design; do not retain 108 times 33
full sparse vectors.  Add monitor cadence inside full remainder elimination,
new-word preflight, coordinate absorption, and dual-provenance operations.

Expected source-only producer time is roughly 12--18 minutes and the same-job
producer+independent-checker time roughly 22--35 minutes if target 6 is still
inconsistent.  A consistent route may be longer.  These are estimates, not
claims.  Preserve the 300-minute soft stop, 330-minute job budget, 4.5-GiB RSS
guard, and honest UNKNOWN_RESOURCE.

Freeze hashes/bytes in the reply, run only the one authorized combined
selftest, and end the reply with exactly:

```text
B345_SEEDSPAN_TRIPLE4_V1_READY_FOR_GHA
```
