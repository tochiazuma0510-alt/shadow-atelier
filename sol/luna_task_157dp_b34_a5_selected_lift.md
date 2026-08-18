# Luna task 157dp — complete fixed-roof fibre through the concrete `A5^4` chief layer

## 0. Objective and authorized scope

You are Luna. Build one versioned, bounded, exact, independently checked
finite decision at the concrete FC-8* `A5^4` layer. The registered object is
not one chosen q3 pair: it is the **complete composite lift fibre of the fixed
outside roof element** represented by q3 exponent 2 / row 37.

The two outcomes are asymmetric.

- One literal charming/onto lift supplies the required outside witness at this
  computational layer and advances the B4-B induction by one layer.
- A cap-free proof that the complete composite fibre is empty gives an
  isolated audit window with image `A`, hence decides B4-A.

Authorized new files only:

1. `search/d972_b34_a5_selected_lift_v1.g`
2. `search/check_d972_b34_a5_selected_lift_v1.py`
3. `search/d972_b34_a5_selected_lift_gha_driver_v1.g`
4. `sol/luna_reply_157dp_b34_a5_selected_lift.md`

Do not edit the running relative-Frattini v1/v2 files, drivers, or workflows.
No workflow edit, git/GHA action, local GAP, or heavy local Python. The new
157dp computation itself uses no ANUPQ/PB5. One exact exception is allowed:
the same-job driver may invoke the already pinned, cross-checked q3 upstream
driver once to regenerate its exact artifact (including that driver's existing
internal call), then require its checker marker and frozen artifact SHA. This
bootstrap took about 13 seconds in run 32149051901 and avoids historical
artifact staging or a workflow edit. The pinned FC-8* upstream may likewise be
regenerated once. One lightweight producer/checker selftest is allowed.

## 1. Frozen inputs and groups

Bind and independently replay at least:

- q3 run `32135808950`, checked artifact SHA256
  `3d37c8c5f1fae47c66877090f9f73d1a8ff4a826214ed610175cf6e8ac41da72`;
- its fixed outside roof: exponent 2, canonical row 37, `m=0`, represented
  first by the selected word

  ```text
  [-2,-2,-1,-1,2,2,1,-2,-1,-1,2,2,2,-1,-2,-2,1,1,1,1]
  ```

- the q3 certificate that `E3=Q0 x B(2,3)` and the 27 registered right-fibre
  words are **all** fine pairs over that fixed coarse roof, not merely 27
  sample corrections;
- the accepted marked arithmetic/coset package behind FC-1 and the pure-axis
  classifier. Independently prove that exponent 2 / row 37 represents one
  fixed `x in X\A`; do not trust the receipt boolean
  `arithmetic_outside_by_index_three`;
- pin `sol/luna_reply_157cp_c5_surgery_torsor_chief.md` at SHA256
  `59c96e7d62a20af4207f715df8e2927a8fc373e1f12e8f3be70e535d8afe5347`
  for the accepted pure-axis theorem: `e1^n` is outside exactly when
  `3` does not divide `n`. Bind row 37 to `e1^2` through the frozen 972-key
  orbit, rather than treating the theorem name as an executable classifier;
- FC-8* run `32153799126`, checked artifact SHA256
  `558faee7864ab1162aaa40a9d2e2ad7bd1926987561cde9e3d3a9ee69690c584`;
- frozen word artifact SHA256
  `564a921be8114bdeb963f679c121e8d9aa90e148c65e95e393874fcba843e9f9`.

Let `E4=Q4 x Pi4[3]`, `H=ker(PB4->E4)`, let
`rhoA:PB4->A5^4` be the exact FC-8* deletion map, and put
`L=H intersection ker(rhoA)`. Replay the no-common-quotient argument so the
joint target is literally `E4 x A5^4` and `H/L ~= A5^4` with its checked
transitive B4 action. Do not assume `L` isolated.

## 2. Exact D1/source-image preflight

Reconstruct the five A.18 cofaces and four strand deletions from literal words
and compose all twenty maps `PB3->PB4->A5`. Producer and checker must derive
independently:

- eight components are the same onto marked map
  `(x12,x23,x13)->(X,Y,Z)` into A5;
- the other twelve are cyclic C5 maps in the three independent source classes
  `x12,x23,x13`, four occurrences each;
- the joint PB3 image is `A5_diag x C5^3`, order 7500;
- the `F2=<x12,x23>` image is `D_F=A5_diag x C5^2`, order 1500;
- `D_F' = A5_diag`, order 60;
- the four PB2 cofaces give the relative marking/m factor C5.

Bind the exact orders `H_ord=18`, `L_ord=90`. Enumerate all
`m_s=18s` for `s=0,...,4`; then `u_s=2m_s+1=36s+1`, so exactly `s=4` fails
the 5-primary friendly gate while all shifts retain the old mod-18 marking.
Keep all five in the preregistered fibre, and record the deterministic friendly
rejection rather than silently shrinking the universe.

The old F2 image is the actual subgroup `F_H=<x12,x23><=E3`, not an invented
copy of all E3. Prove the joint F2 target is the full direct product
`F_H x D_F`, so its projection kernel is exactly D_F. Likewise prove the
marked PB2 projection kernel is exactly C5. Counts alone do not prove either
fibre identity.

Do not construct or enumerate the potentially huge joint group in order to
obtain this kernel. Evaluate authenticated relator/source words for `F_H` in
the joint map, retain the coarse-identity values inside the small
`D_F=A5 x C5^2` factor, prove their normal closure has order 1500, and build
the 1500 deterministic source-word sections by BFS **inside D_F only**.
The checker must reconstruct the relator evaluations, small-factor closure,
and sections independently. A Goursat/order argument without source sections
is not enough for the literal scan.

Use structural coordinates and small BFS tables. Never enumerate A5^4 or a
huge ambient joint product.

## 3. Preregistered complete composite universe

Outer loop: all 27 authenticated q3 fine representatives over the one fixed
outside roof, in frozen receipt order. The previously selected q3 witness is
first. Do not require every outer representative to be an H-shadow; direct
literal gates decide this. Completeness means that any L-shadow over the fixed
roof reduces to one of these 27 representatives.

Inner loop for each outer representative: all five C5 marking shifts and all
1500 D_F correction classes in one deterministic structural order. Thus the
cap-free preregistered universe is exactly

```text
27 * 5 * 1500 = 202500
```

Evaluate compact quotient and exact derived-membership gates before building
long words. At most `27*5*60=8100` candidates can remain after the A5-side
charming filter, and at most 6480 after the deterministic friendly filter;
compute the actual progressive counts rather than asserting equality.
Raw free-word exponent sums are diagnostic only.

For each surviving candidate replay directly:

1. marking and friendly/unit conditions, including the new 5-primary shift;
2. both literal hexagons;
3. the ordered A.18 pentagon;
4. charming in the actual finite source quotient;
5. the required F2-onto condition and every source/target typing map;
6. exact reduction to the fixed roof and the old/new factor images.

The acceptance predicate here is `GT^heart(L)` shadow existence: literal
charming + onto with all equations. **Settlement at the non-isolated L is not
required and must not reject an otherwise valid stage witness.** It may be
computed only as a separately labelled diagnostic. This distinction is
load-bearing for a sound negative result.

Stop at the first complete positive but record exact preceding coverage and
rejection bitsets/counters. Any cap, missing word section, missing typed map,
or unevaluated candidate forces UNKNOWN and can never count as rejection.

## 4. Independent checker

Do not import producer helpers.

- Rebuild A5, the five cofaces, four deletions, twenty composites, and the
  `7500/1500/60/C5` structure independently.
- Independently reconstruct the q3 B(2,3) order-27 fibre and prove it is the
  complete fine fibre over the exact exponent-2/row-37 roof, including the
  marking coordinate; do not trust `fine_fibre_completeness=true`.
- Prove both direct-product projection-kernel identities and reconstruct all
  202500 candidate coordinates with no duplicates or omissions.
- Re-evaluate every load-bearing literal gate and reconstruct the first pass
  or the complete-empty bitset. A producer boolean is insufficient.
- Reject any negative receipt containing a resource skip, unchecked
  candidate, settlement-as-acceptance, or incomplete coverage.
- Mutation tests must reject at least: a q3 fibre word, duplicate/missing q3
  record, one coface letter, one deletion row, A5 marking, cyclic coordinate,
  m shift, direct-product kernel claim, charming substitution, literal
  residual, outside roof key, artifact hash, coverage digest, and terminal.

## 5. Exact terminals and implications

Positive terminal:

```text
B34_A5_LAYER_FIXED_OUTSIDE_ROOF_LIFT_CROSSCHECKED
```

It proves one outside shadow exists at the computational L. Mapping it to any
isolated coarser audit window gives `A<=I_K<=X` with an outside element, hence
`I_K=X`. Do not write `I_L=X` unless L is independently proved isolated. This
positive closes the registered A5^4 layer but does not alone prove cofinal
B4-B.

Negative terminal, allowed only after exact all-202500 coverage with zero
resource skips:

```text
B4_A_FIXED_OUTSIDE_ROOF_FIBRE_OBSTRUCTION_CROSSCHECKED
```

The receipt/checker must reconstruct the proof. FC-8* makes L a B4-normal
finite-index window. By Cor. 3.13 a genuine roof element must survive to every
such window, so complete roof-x fibre emptiness proves that the fixed
`x in X\A` is not genuine. The global genuine roof image
`P=im(hatGT->X)` is a subgroup with `A<=P<=X`; because `[X:A]=3` and
`x notin P`, one has `P!=X` and hence `P=A`: B4-A. As a redundant paper
fallback, Cor. 3.5 may choose isolated `N<=L`; any N-lift would reduce to L,
and Proposition 3.7/3.11 then gives the same conclusion through `I_N=A`.

Every incomplete path emits a precise `B34_A5_LAYER_UNKNOWN_*`. Never promote
a bounded miss, one-pair miss, settlement failure, or partial q3 fibre to A.

## 6. Performance and reply

- No ANUPQ/PB5/relative-Frattini solve, no Elements(A5^4), and no generic
  kernel/full-group enumeration for `F_H x D_F`, and no generic closure or
  long-word substitution in the 202500 hot loop.
- Precompute the 27, 60, 1500 and five-shift tables, compact context values,
  and literal fixed-context correction values. Materialize words only after
  cheap gates and cache all repeated evaluations.
- Driver: same-job upstream regeneration/checking, stale artifact/sentinel
  removal, exit-zero sentinels, exactly one registered marker. Progress output
  must not slow the run.
- Before parent dispatch, report exact heavy-operation counts and a
  source-based canary/full-positive/full-negative runtime and memory estimate.
- Reply with exact SHA256/bytes, selftest/static results, terminal semantics,
  and the remaining positive-branch cofinal proof boundary.
