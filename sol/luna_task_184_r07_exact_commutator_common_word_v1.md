# Luna task 184 — R07 exact-commutator common-word successor v1

Commissioner: Sol / 2026-08-27

Reply to: `sol/luna_reply_184_r07_exact_commutator_common_word_v1.md`

Role: bounded mechanical implementation and GHA-ready computation.  The
mathematics is fixed by v145--v146.  Do not redesign the proof, weaken exact
integer exponent zero to a congruence, or make a cofinal/fake/Ihara claim.

## 1. Objective

Build a versioned producer, helper-nonshared checker, ASCII GAP/GHA driver,
immutable SELFTEST fixture, and Luna reply which consume a task179 receipt or
checkpoint and solve the exponent-augmented positive system of v146:

\[
 (-T_0,0)\in(D_0,0)+
 \operatorname{span}_{\mathbf F_3}
 \{(V_{\delta,j},\bar e_j)\},
 \qquad \bar e_j\in L/3L.
\]

On success, materialize the task179 signed correction, exactify its integer
exponent vector with cubes of registered normal generators, and directly
replay one ordinary word with exponent vector exactly `(0,0)`, both
hexagons, and the printed-order pentagon.

The implementation must support both:

1. zero-cost inspection/repair of a positive task179 receipt; and
2. a resumable lattice-augmented positive search when the accepted task179
   coefficients are not cube-repairable or task179 stopped at an honest
   checkpoint.

## 2. Frozen mathematical and source pins

Read in full and pin exactly:

```text
sol/proof_r07_task179_relative_frattini_successor_v145.md
  bytes=13819
  sha256=b08f140838b78424cafa9528eafbcab9442f94cf92ce2cb42e15fc88ed489a51
sol/proof_r07_exact_commutator_positive_common_word_v146.md
  bytes=9065
  sha256=a167df351d55e82781cb60cd2b4dbfdf5cd2ea4f50251643a6e0b83332557cee
search/d972_r07_positive_common_word_colgen_v1.py
  bytes=119396
  sha256=448123e3ccba4324f4d19a09eeb6a2ba217d611ef5053d4cfa27e61ac69a2512
crosscheck/check_d972_r07_positive_common_word_colgen_v1.py
  bytes=70020
  sha256=473bad89f9656dd67f4313398b5bdbb253a3495e1e20855d90781b4875309f2d
search/d972_r07_positive_common_word_colgen_gha_driver_v1.g
  bytes=12872
  sha256=fbab67e85de604f157f8bd93f53d64e7265121508aa948c1e01341e78d1b5a11
```

Also bind task179's pinned task175/task176/q3/joint sources transitively and
record their current exact identities.  The producer may import the pinned
task179 producer to reuse its authenticated runtime and positive oracles.
The independent checker may not import either producer or their helpers; it
may reuse only independently pinned task179/task175 checker arithmetic after
an explicit helper-firewall audit.

Do not edit task175--task183, v145--v146, workflows, CLAIMS, or old
certificates.

## 3. Complete exponent lattice

From the live authenticated 6,441-row roster, compute the **integer** signed
exponent pair of every normal generator without reduction modulo three.
Conjugation must not be enumerated: it preserves the pair.  Compute

```text
L = Z-span of all 6,441 exponent pairs <= Z^2.
```

Return a deterministic primitive Hermite/Smith basis of rank `t in {0,1,2}`
and transformation receipts expressing:

- every roster pair in that basis;
- every basis vector as an integer combination of named roster rows; and
- both exact integer round trips.

Bind the roster order, word digest, all 6,441 exact pairs, basis, invariant
factors, coordinate matrix, and digests.  Prove the used normal-generation
pin and state `L=exp(Omega)`; do not infer this equality from sampled words.

For roster row `j`, define its new column tail as its basis coordinates
modulo three.  Use new typed keys which cannot collide with task179's raw
relation or standard mod-3 exponent keys.  Boundary columns get a zero tail.
Retain task179's old exponent rows as canaries; never substitute
`Z^2/3Z^2` for `L/3L`.

## 4. Positive-receipt fast path

For an authenticated task179 `COMMON_WORD` receipt:

1. recompute the exact integer exponent `e0` of `correction_word`;
2. if `e0=(0,0)`, retain the word unchanged;
3. otherwise decide exactly whether `e0 in 3L` using the Smith data;
4. if yes, divide in the lattice, use the fixed Smith section to return
   integers `q_j` with `sum q_j e_j = -e0/3`, and form the literal cube tail
   `product r_j^(3*q_j)` in fixed roster order; and
5. set `exact_correction_word = reduce(correction_word + cube_tail)`.

Directly require:

```text
integer exponent vector exactly [0,0]
joint finite-value identity
cube-tail all-seven change exactly zero over F3
same sparse task179 target identity
corrected_word = reduce(g760 + exact_correction_word)
both direct hexagons
literal five-factor pentagon in frozen order
boundary chains never inserted into either source word.
```

The receipt must retain `e0`, `L`, `e0/3`, the sparse `q_j`, every cube word,
the unreduced and reduced tail lengths/digests, and direct replays.  A large
word reaches a registered resource stop; it is not silently truncated.

If `e0 notin 3L`, emit only a typed operational handoff
`LATTICE_AUGMENTED_RESUME_REQUIRED` in inspection mode.  This rejects the
particular coefficient vector's cube fast path, not the full fibre and not
the R07 branch.

## 5. Checkpoint upgrade and augmented search

Accept either a task179 positive receipt or its separately authenticated
checkpoint.  Reconstruct task179's runtime, target, and every retained
column.  Append the `L/3L` tail to each correction column from its literal
`relator_word`; append zero to each boundary column.  Rebuild the entire
echelon in frozen column order.

The old columns remain independent after coordinate extension, but old
pivots, duals, and pending-oracle state are not authenticated for the new
space.  Record the old-to-new column commitment, rebuild pivots/ranks, and
restart the current dual's boundary/correction cursors deterministically.
Never splice the old dual or claim its old cursor proves a prefix complete in
the augmented space.

Wrap task179's direct correction-column constructor so every correction row
gets the exact lattice tail.  Extend its weighted scalar by

```text
lambda_lattice dot roster_lattice_residue
```

as a conjugator-independent constant.  Boundary correlation, linked
sections, support fibres, W+1/global schedule, and resource honesty remain
unchanged.  A retained ACTIVE column must replay its full eleven occurrences,
both old exponent canaries, all new lattice coordinates, nonzero dual
pairing, and rank increase.

On augmented membership, use the signed coefficient convention
`0 -> empty, 1 -> word, 2 -> inverse`, compute the intermediate integer
exponent, require it lies in `3L`, and apply the cube exactification of
Section 4.  The positive terminal is allowed only after the final direct
word replay.

Allowed production terminals are exactly:

```text
R07_EXACT_COMMUTATOR_COMMON_WORD
UNKNOWN_RESOURCE:<registered phase and cap>
UNKNOWN_INPUT:<authenticated missing or malformed input>
```

Inspection mode may additionally emit
`LATTICE_AUGMENTED_RESUME_REQUIRED`.  There is no mathematical negative
terminal in v1.

## 6. Independent checker

The checker must not import the task184 or task179 producer and must not share
their word, lattice, Gaussian, Fox, weighted-formula, checkpoint, or cube
helpers.  It must independently:

1. authenticate all pins and the input task179 artifact before parsing;
2. reconstruct the complete 6,441 words and exact exponent pairs;
3. recompute a canonical lattice basis and both transformation directions;
4. replay every upgraded retained column and rank transition;
5. recompute the augmented coefficient identity;
6. independently solve/check the rank-two integer cube coefficients;
7. materialize the signed word and cube tail from literal roster words; and
8. directly replay exact exponent zero, joint identity, both hexagons, all
   five pentagon cofaces/order/signs, and the PB3/PB4 boundary reductions.

On UNKNOWN or inspection handoff, authenticate checkpoint integrity,
counters, lattice data, and absence of every negative/cofinal claim.  Do not
promote a bounded augmented prefix to nonmembership.

## 7. SELFTEST and destructive controls

Use a finite noncommutative linked toy in which the normal-generator exponent
lattice is a proper sublattice of `Z^2`, so standard exponent zero modulo
three is strictly weaker than zero in `L/3L`.  Exercise all three fast-path
cases:

```text
e0 = 0
e0 in 3L but e0 != 0
e0 notin 3L, followed by augmented positive recovery.
```

Exercise checkpoint upgrade, reset of dual progress, a lattice ACTIVE
constant, coefficient-2 inversion, a nonempty cube tail, and final exact
word replay.  At minimum reject:

1. `Z^2/3Z^2` substituted for `L/3L`;
2. a nonprimitive/wrong-order lattice basis;
3. one changed roster exponent pair;
4. one missing normal-generation pin;
5. one lattice coordinate from the conjugator instead of the relator;
6. a boundary column with nonzero lattice tail;
7. an old task179 dual/cursor spliced into the augmented checkpoint;
8. one omitted lattice term in the weighted scalar;
9. coefficient 2 without literal inversion;
10. division by three before proving membership in `3L`;
11. `3*q_j` changed to `q_j` in one cube;
12. one cube made from a boundary word;
13. a cube tail with nonzero all-seven change;
14. exact exponent replaced by exponent modulo three;
15. one pentagon order/sign mutation;
16. a programming exception relabelled UNKNOWN; and
17. a fake/cofinal/Ihara promotion flag.

The producer and checker must use independent small-system lattice and F3
implementations.  Exhaustively compare bounded random rank-0/1/2 lattices
against brute force in SELFTEST.  All local tests, if any, are serial and
bounded; do not run the actual production reconstruction locally.

## 8. Files and execution discipline

Create only:

```text
search/d972_r07_exact_commutator_common_word_v1.py
crosscheck/check_d972_r07_exact_commutator_common_word_v1.py
search/d972_r07_exact_commutator_common_word_gha_driver_v1.g
search/certs/d972_r07_exact_commutator_common_word_selftest_v1_20260827.json
sol/luna_reply_184_r07_exact_commutator_common_word_v1.md
```

Do not run git, push, GHA, the full task179 runtime, or parallel local
Python/GAP.  The parent broker will audit, commit, push, dispatch, and supply
the production task179 artifact.  The ASCII driver must be single-job serial,
bind every source/input SHA, reject stale artifacts and wrapped sentinels,
upload the latest checkpoint on every typed resource stop, and fit the
six-hour workflow ceiling.

## 9. Claim boundary

An independently accepted `R07_EXACT_COMMUTATOR_COMMON_WORD` proves one
ordinary commutator correction through v145's first relative Frattini rung.
It is the exact input to the second-rung actual defect.  It does not prove the
second rung, a completed relative-dihedral homotopy, all prime/nonabelian
gates, a compatible cofinal lift, fake, or an Ihara witness.

End the reply with:

```text
exact exponent zero, not merely modulo three
first relative Frattini rung only
second-rung actual class remains required
no fake / cofinal lift / Ihara witness declared
```
