# Luna task 157da — construct the matched q=3 B3/B4/B5 chief manifest

Date: 2026-08-18

## 1. Role and fixed state

You are Luna. Implement the next finite construction isolated by task/reply 157cz.
This is not another inventory-only task. Read `docs/対話帳.md` T-29 and T-30,
`sol/luna_reply_157cz_b345_power_syzygy.md`, and the typed horn contract in
`sol/luna_reply_157cr_b5_kernel_surgery.md` before editing.

Keep the following conclusions fixed unless an explicit word/table contradiction is
found:

1. the full/non-gentle B4 target and literal (2.18)--(2.20)/A.18 gates;
2. `A <= I_K <= X`, `[X:A]=3`, the one-outside lemma, stage-dependent seeds, and
   finite-fibre compactness;
3. the roles of power, surgery, and torsor;
4. strict `ker(PB5 -> PB4)` corrections have zero retained B4 defect; only a typed
   horn/common-correction construction may be used;
5. the coset `S3` from the index-three action is not strand relabelling `S3` without
   a proved comparison;
6. 157cz's universal untwisted `PB3ab -> PB4ab -> PB5ab` split exactness and its
   six-pentagon/three-square K5 skeleton;
7. run 32106551371 decides only the registered roof powers `{1,2}` times 64 slice.

Do not run local GAP, Git, or GHA. Do not edit a workflow. One short, single-process
Python syntax/self-test is allowed. The parent is the sole Git/GHA broker and will use
the already registered `.github/workflows/gap-run.yml` with the ANUPQ option.

## 2. Exact objective

Create a fail-closed GAP producer and independent Python checker for one concrete
matched exponent-three level

```text
Pi_r[3] = profinite(PB_r) / closure(<g^3 : g in profinite(PB_r)>), r=3,4,5,
```

and emit schema `d972-b345-q-chief/v1`. The intended output is not merely three
abstract group orders. It must retain enough marked data to derive, at the first
actual elementary F3 chief layer compatible with the frozen roof,

```text
C_adm --d1--> R_A18 --d2--> S_B5,
```

the actual beta, the roof-coset action on this same complex, and any honest comparison
with T-29's relative sign class.

If the full roof-compatible chief cannot yet be constructed, still construct and
authenticate every preceding finite object, and name exactly the first missing map.
Do not replace a missing typed object by the untwisted H1 tensor complex.

## 3. Exact PB presentations and q=3 completeness

For each `r=3,4,5`:

1. construct the Artin braid presentation `B_r`, its map to `S_r`, and the pure
   kernel `PB_r`;
2. construct the standard marked pure generators
   `A_ij = sigma_(j-1)...sigma_(i+1) sigma_i^2
   sigma_(i+1)^-1...sigma_(j-1)^-1` in a declared convention;
3. obtain an fp presentation of `PB_r` while retaining exact words both ways for
   every `A_ij`; replay the original fp relators in the Artin action on `F_r`;
4. construct the exponent-three quotient with ANUPQ using an epimorphism-returning
   API so every marked generator image is retained;
5. certify why the class bound is terminal for exponent-three groups. Use a precise
   theorem/source for the nilpotency-class bound, and additionally request the next
   ANUPQ class when the API permits; a changed order/map is a hard STOP. Do not call a
   merely truncated lower-exponent-3 quotient `Pi_r[3]`;
6. export a lossless pc presentation: relative orders, power relations, conjugate
   relations, marked `A_ij` coordinates, order, exponent, nilpotency class, and the
   original-relator replay. Full multiplication tables are not required when their
   size is unreasonable, but the pc collector data must be complete.

The producer must print `Runtime()` phase markers and use explicit caps. Timeout or
ANUPQ failure is `UNKNOWN_RESOURCE`, never a mathematical obstruction.

## 4. All cofaces, faces, and cosimplicial identities

Derive rather than paste the five `PB3 -> PB4` and six `PB4 -> PB5` cofaces on the
standard `A_ij`. Derive every deletion needed for endpoint retractions and the K5
faces. Check before quotienting, using the faithful Artin representation, and again
in all q=3 pc quotients:

1. each generator formula and each source relator;
2. all coface/coface identities with the declared index convention;
3. all face/coface identities actually used;
4. endpoint insertion/deletion retractions;
5. the exact five A.18 word maps already frozen in row18;
6. the six-pentagon and three-square oriented K5 boundary from 157cz.

An orientation mismatch is a hard type failure, not an inverse convention to repair
silently. Bind all formulas and matrices by SHA256.

## 5. Roof-compatible diagonal construction

Use the frozen row18 source/target data only through hash-gated inputs. Keep
`q=3` distinct from roof power `a mod 9`.

The registered source is the **v2** row18 pipeline, not the stale v1 files:

```text
search/d972_b4_literal_row18_stage_v2.g
  sha256 8f8b429b5725b244a214cc6a4cf59daa186e4ee2d4d6eee6df18e580d88ef2a1
search/check_d972_b4_literal_row18_stage_v2.py
  sha256 bf85cfd142f6c640e96af77aa5f580caa206439329d17ed18ac342ac6acdcd19
```

Do not import semantics or certificates from the v1 raw-row implementation.

Construct, where the data permit, the diagonal images which combine the q=3 pure
quotients with the existing marked roof quotients. The kernel must be proved to be
the intended `closure(M_r) intersection N_r(3)`; do not infer an intersection from
matching orders.

For arity five, do **not** construct a separate coarse `M_5` or a coarse-by-q3
diagonal group. It is unnecessary for this relative first-refinement test. Write

```text
Q4 = PB4/M4,  P4 = PB4/N4(3),  C4 = PB4/(M4*N4(3)),
K4 = M4 intersection N4(3),  E4 = PB4/K4.
```

Certify the pullback square `E4 = Q4 x_C4 P4`. For
`V=ker(E4->Q4)=M4/K4`, certify that `V -> P4` is injective. A coarse-trivial
fine A.18 defect lies in `V`, so its q3 image retains all information. Each of the
six cofaces preserves `N4(3)` and therefore gives the typed relative map
`E4 -> P4 -> P5`; compute the ordered/prefix-transported B5 syzygy entirely in
`P5=Pi5[3]`.

For effectivity, construct

```text
M3 = intersection_j coface_j^-1(M4),
K3 = intersection_j coface_j^-1(K4) = M3 intersection N3(3),
```

and certify the correction square from the actual coarse-trivial correction domain
in `E3` to `V`, versus its q3 image in `P3` to `P4`. A correction in arbitrary
`P3` is not sufficient. If a relative horn `gamma in P5` is used, require its
retained face to lie in the embedded copy of `V` in `P4`, recover the unique B4
correction through that injection, check every other face in `P4`, and replay all
final side gates in `E4`.

Thus `MISSING_TYPED_M5` is not an allowed early stop in this task. The honest next
missing object, if any, is `Q3_TYPED_D2`, the relative-horn effectivity map, or the
comparison `Phi`; name that exact first failure without inventing a coarse `M5`.

For every constructed arity, emit exact projection maps, kernels, sections where
used, marked-generator coordinates, and commuting diagrams. Recheck the five A.18
maps and six arity-five maps on these diagonal images.

## 6. First actual F3 chief and the typed Fox complex

If the diagonal construction supplies compatible finite groups `E3,E4,E5`:

1. compute a characteristic/refinement-compatible chief series of the relevant
   kernels and select the first actual elementary F3 factor; record predecessor,
   successor, basis, dimension, and the full base-group action matrices;
2. emit exact sections/base words and every prefix-conjugation transport used by
   Fox linearization;
3. derive `d1` from both hexagons and literal ordered A.18 pentagon;
4. derive `d2` from all six transported pentagon faces and all three square faces;
5. derive the admissible correction subspace `C_adm` after marking, charming, onto,
   representative, reduction, and settlement linear side gates;
6. derive the actual base residual `beta`, and independently check
   `d2*d1=0`, `d2*beta=0`, and `im(d1|C_adm) <= ker(d2)`;
7. compute explicit bases for kernel, image, quotient, correction or a dual
   obstruction. Dimension-only receipts are forbidden.

No nonlinear side gate may be silently replaced by its tangent condition. A linear
correction is candidate-grade until the corresponding exact word replay passes.

## 7. Coset-sign and nonabelian comparison gate

Use the recent fixed mathematical distinction:

```text
orbit of a complete typed datum has size 3
  -> nonzero class in H^1(X,A;F3_sign),
```

but this class is not automatically the A.18 `H2` class. If the manifest contains a
complete typed datum `omega`, compute its full stabilizer and require

```text
Stab_X(omega) = I_K,
```

where `omega` includes all cofaces, marking, literal relations, and side gates—not
only an outer action.

Construct a comparison

```text
Phi_* : H^1(X,A;F3_sign) ->
        (ker d2)_coset-sign / im(d1|C_adm)_coset-sign
```

only from explicit finite transports/cofaces. Prove equivariance and non-circularity;
do not use the desired outside lift to define `Phi_*`. Report the image of the unique
relative sign generator. If no canonical chain map is determined by the data, emit
`MISSING_TYPED_COMPARISON_PHI` with the exact missing transport.

Do not claim that centerless/Schreier alone absorbs nonabelian `S^t`. The abstract
`A5`/`V4` compatible-pair countermodel rules out that shortcut. A positive finite
comparison is evidence for the present typed stage only until a uniform theorem is
proved.

## 8. Independent checker

The Python checker must not import the producer or GAP helpers. It must:

1. independently reconstruct all standard braid/coface/deletion signed words using
   its own free-word reducer and faithful Artin automorphism implementation;
2. replay the complete exported pc collector, marked generator images, maps,
   relators, and commuting diagrams. Reuse no source code from existing collectors,
   though their receipt contracts may be inspected;
3. reconstruct every F3 matrix, chief action, `d1`, `d2`, `C_adm`, beta, kernel,
   image, quotient, and coset-action comparison from the exported word/table data;
4. reject mutated coface orientation, one pc relation, one chief action entry, one
   square face, one side-gate row, and a falsely promoted terminal token;
5. distinguish a genuine mathematical empty fibre from missing data/resource failure.

If full independent nonabelian pc collection is impractical, the checker must at
least replay all used marked words and homomorphism relations from the lossless pc
presentation and state the remaining ANUPQ contract explicitly. It must not call the
result Lean-verified.

## 9. Performance and dispatch contract

Only one GAP process is permitted. Do **not** run three independent production
ANUPQ constructions. Use the proved endpoint insertion/retraction identity
`i^-1 N_(r+1)(3)=N_r(3)`: construct the terminal PB5 exponent-three quotient once,
then recover the marked PB4 and PB3 quotients as the generated insertion images and
certify them with the deletion retractions. Independent PB3/PB4 ANUPQ calls are
allowed only as short bounded canaries when demonstrably cheap. Write atomic
checkpoints after presentation, PB5 q-quotient, PB4/PB3 recovery, cofaces, and each
chief/Fox phase so a timeout identifies the exact phase.

Avoid enumerating all elements of a large q=3 quotient. Use pc coordinates, linear
algebra on chief factors, and cached word evaluation. Never construct a full Cayley
table or a huge diagonal direct product merely for convenience. Prefer a directly
generated standard PB5 fp presentation with faithful Artin replay over the
high-variance `IsomorphismFpGroupByGenerators(PB5)` route; if the latter is
unavoidable, isolate it behind its own wall-clock cap and phase receipt.

The producer must support:

```text
D972_B345_Q3_SELFTEST:=true   # tiny synthetic/API/orientation canaries only
D972_B345_Q3_RUN:=true        # bounded full GHA construction
D972_B345_Q3_OUTPUT:="..."    # artifact path
```

and print unique final markers. Supply the exact `gap-run.yml` dispatch inputs in the
reply, but do not dispatch.

## 10. Verdict discipline

Allowed terminal tokens are:

```text
B345_Q3_MANIFEST_READY_FOR_GHA
B345_Q3_TYPED_SIGN_EXACT_WITH_WORD_CORRECTION
B345_Q3_TYPED_SIGN_NONZERO_OBSTRUCTION
B345_Q3_NO_ACTUAL_F3_CHIEF
B345_Q3_MISSING_TYPED_D2
B345_Q3_MISSING_RELATIVE_HORN_EFFECTIVITY
B345_Q3_MISSING_TYPED_COMPARISON_PHI
B345_Q3_UNKNOWN_RESOURCE
```

Only `...EXACT_WITH_WORD_CORRECTION` may feed the elementary-chief induction, and
only for the explicitly authenticated stage. None of these alone declares B4-B or
covers every cofinal stage/nonabelian chief.

## 11. Authorized files

Create or edit only:

```text
search/d972_b345_q3_chief_v1.g
search/check_d972_b345_q3_chief_v1.py
sol/luna_reply_157da_b345_q3_chief.md
```

Do not modify 157cz files, the row18 pipeline, any workflow, or any certificate.
Temporary files belong outside the repository. The reply must give source hashes,
static/self-test commands and runtimes, expected artifact path, exact generic-workflow
dispatch inputs, all honest dependency boundaries, and the precise B4 impact.
