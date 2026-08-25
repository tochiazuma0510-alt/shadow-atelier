# Luna 162 v10 independent literal class-six checker — GHA-ready report v1

Author: Luna independent checker / 2026-08-25

Status: **GHA-ready; full run not yet executed; mathematical verdict pending**.
This report records preparation only.  It does not claim `cross_checked`,
`verified`, a fake certificate, an Ihara witness, or an all-degree/cofinal
lift.

## 1. Independent artifact

```text
crosscheck/check_d972_r07_literal_class6_augmented_v1.g
bytes  = 44378
lines  = 1112
SHA256 = 5dabf9efc457c7ef6fca9e0a3629fc78625287f6bc3485c724eedf8191b7d735
```

The checker does not read or import the producer's v3 implementation,
certificate, helpers, or output logic.  Its transported inputs are limited to
the public literal formulas, `C5=(313599,2,-1,-2,0,1)`,
`k=(2,-4,3,4,1,-2)`, and the frozen 796-letter class-five exactifying tail.
The embedded tail is rechecked at startup:

```text
length = 796
canonical signed-list SHA256
       = 937ce63d85d9c6ab5e9dd5918e00ffd8348ba3ba8ba2def66aa3c98a8bc95c0e
```

## 2. Mechanical scope

The script independently reconstructs the following, fail-closed.

1. The marked finite quotient
   `Q=(G36 x PSL(2,8)) x C3` as a degree-120 permutation group, its marked
   generators, R07, and lower-central orders through `gamma7`.
2. A tracked normal-conjugacy generating system for `gamma6(Q)` and
   `gamma7(Q)`.  `PreImagesRepresentative` is used only against the checker’s
   own tracked epimorphism; substitution of the tracked source words produces
   an exact-mark `wk` for the degree-five kernel vector and later a gamma-seven
   exactifier for the solved degree-six Hall word.
3. Direct `t=0,1,-1` checks that `f5*wk^t` retains the exact R07 mark and is
   solved through degree five before any degree-six coordinates are collected.
4. Class-six NQ quotients of `F2` and the ordered PB4/Z presentation of
   `K(0,5)`.  The load-bearing FN basis is exactly
   `n=(x14,x24,x34), h=(x12,x23)`, of ranks `116+9=125`.
5. Genuine subgroup-Pcp conversions.  Every finite relative-order carry is
   retained as an explicit power-relation column.  The augmented change matrix
   must be square and unimodular; subgroup index, Abelian invariants, full
   forward matrix, forward/inverse digests, relation vectors, every basis-unit
   coordinate replay, defect all-coordinate replay, and group-element replay
   are printed.
6. Literal direct residuals `beta6(t)` at `t=-1,0,1,2`; the script requires
   `beta6(t)=beta6(0)+t*delta6` in all 143 integral coordinates.  The previously
   independent source theta/tau coordinates at `t=0` are pinned as an extra
   canary.
7. All nine homogeneous columns are rebuilt from group words.  The literal
   A.18 matrix in the required `(x14,x24,x34)` basis is used in the augmented
   solve.  Separately, and only as a diagnostic, the old cyclic-rho calibration
   is collected in `(x15,x25,x35)` coordinates; this separation prevents the
   frozen rho receipt from contaminating the literal solve.  Its ranks,
   canonical minor and all three frozen digests are checked, including the v1
   sorted-JSON digest
   `fadcfe12a1ba9d5d7aa1a6d4a4c2aa26aeb46aee4e537a7af5a810702c13480c`.
8. Exact Smith analysis of `[delta6 | D6_literal]`: `U*A*V=D`, determinants of
   both transformations, transformation digests, all Smith factors,
   divisibility/zero-row conditions, one canonical solution and the full
   integral kernel basis.  `NO_INTEGER_SOLUTION` is an integrity error.
9. Gamma-seven exactification of the resulting raw `C6`, exact R07 mark replay,
   and direct theta, tau, and printed-order literal A.18 identities modulo
   degree seven.  Commutator exponent sums, the finite-Q onto map and the
   class-six free-nilpotent onto index are checked directly.
10. Required mutations: coface sign, omitted coface, non-inert positive-factor
    swap, FN column swap without relabelling, dropped power-relation column, and
    a separately labelled `t=0` Smith run.  Either `t=0` solvability outcome is
    reported as `EXPECTED_INSTANCE_DEPENDENT_*`.

## 3. NQ portability and GHA invocation

The checker reuses the independent pinned bootstrap:

- GAP exactly `4.16.0`;
- NQ exactly `2.5.11`;
- one `PackageInfo("nq")` installation path directly below exactly one native
  `GAPInfo.RootPaths/pkg/` root;
- pinned `PackageInfo.g`, `configure`, and `Makefile.in` hashes;
- already built installations perform no build;
- a missing Linux executable triggers only the fixed, shell-quoted
  `./configure --with-gaproot=<authenticated-root>` and `make -j2` command;
- exact sentinel, subsequent executable discovery and `LoadPackage("nq")` are
  mandatory.

Use the existing `gap-run.yml` with:

```text
script                = crosscheck/check_d972_r07_literal_class6_augmented_v1.g
timeout_min           = 240
with_pquot_packages   = false
out_dir               = ci/out
```

The runner writes `ci/out/run.log`; NQ configure/make logs are also under
`ci/out/` if bootstrap is needed.  Success requires exactly one final marker:

```text
R07_CLASS6_FINAL_MARKER status=PASS
```

Estimated GHA wall time is 60–180 minutes.  The 240-minute timeout and the
existing 12 GiB `gap-run` heap cap are intentional because the exact class-six
`K(0,5)` NQ construction dominates the run.

## 4. Local preflight only

No heavy local mathematical run was performed.  The short driver
`%TEMP%/luna162_v10_gha_ready_selftest_20260825.g` set
`R07_CLASS6_SELFTEST_ONLY=true`, causing GAP to load/bootstrap NQ and parse the
entire checker without entering the main computation.  It returned exit code
zero with:

```text
R07_NQ_BOOTSTRAP_PASS gap_version=4.16.0 nq_version=2.5.11 built=false ...
R07_CLASS6_SELFTEST_FINAL_MARKER status=PASS
```

`git diff --check`, delimiter/quote balance, the embedded tail length/digest,
absence of producer imports, and the expected marker inventory were also
checked.  Full candidate results must come from the GHA run and remain pending.
