# Luna reply — Task436 actual-b72 first-active v1

Implemented only the four authorized Task436 outputs:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_actual_b72_first_active_v1.py` | 24643 | `5eecdfbce8c3224e52e990fcb3e923e01394b22f0da106d2969aa7e1fb8436cc` |
| `crosscheck/check_d972_r07_a0_actual_b72_first_active_v1.py` | 13834 | `3c58382737317aa31fd5e94039730d8dc0c152a9c2be8f4c263ef31f90004916` |
| `search/d972_r07_a0_actual_b72_first_active_gha_driver_v1.g` | 2349 | `0be621eb16a11a0d17c02a18be4a428010ccaa7d86b365c1b0eb1c678f8759ce` |

The producer rebuilds the pinned Task435/v12 physical prefix, checks rank
43, payload nnz 1,813,674, the 24-key dual and digest
`c75895737537f157fbbfedcdc2c41ed31c8bf0ca9bddda060079ffcda7604efd`, then
constructs the merged 72-point quotient adjoint and the <=144-point old
Tietze adjoint.  It compiles all 44 actual eleven-occurrence formulas with
K=0, coordinates restricted to 0/1/2, and formula/direct scalar equality.

The positive consumer uses a selective Task176 adapter: Gamma 243, shared
Q0 state order 1,469,664, and only S0/S1/S2 40-byte stores (total
176,359,680 bytes).  It does not import Task175, build the 6,441-row roster,
run occurrence closure, boundary correlation, or a global Delta scan.  The
S0/S1/S2 kernel fibres are closed and checked at order 9.  A candidate is
rebuilt through v12 `replay_atom`/`aggregate`, compared with fresh
`seed_v12(conjugate)`, normalized N1/N2, the eleven-occurrence quotient row,
and a strict physical rank rise.  No A0 membership or COMMON claim is made.

The independent checker repeats the physical prefix, adjoint, and all 44
formulae for every receipt status; EMPTY is never accepted, and UNKNOWN_RESOURCE
requires an explicit completed phase. ACTIVE rows additionally replay the
formula, target, all ten direct coordinates, v12 conjugate/normalized-N row,
quotient row, scalar, and rank pivot. Its bounded self-test rejects ten
mutations: omitted dual, tau, exponent, central phase, orientation/sign,
formula term, kernel state, fake rank, missing ACTIVE receipt, and forged EMPTY.

The reverse-neighbourhood canary is evaluated in the new coordinates: PB3
components 0, 1, 2 at each selected `r z^j`, plus components 0 and 1 at the
predecessor points `r z^j s_0^-1` and `r z^j s_1^-1`. Overlaps are merged
modulo 3; the expected coefficient is the merged component-0 adjoint and
zero for the other components. Q0 and S0/S1/S2 membership emit only
low-frequency flushed state-count progress lines (131072 states), with no
inner-loop logging. The checker uses the selector's delta prefix for its
ten-coordinate replay and reserves the conjugate for the v12 physical-row
and exact-exponent replay.

The reverse-neighbourhood canary is evaluated in the new coordinates: PB3
components 0, 1, 2 at each selected `r z^j`, plus components 0 and 1 at the
predecessor points `r z^j s_0^-1` and `r z^j s_1^-1`. Overlaps are merged
modulo 3; the expected coefficient is the merged component-0 adjoint and
zero for the other components. Q0 and S0/S1/S2 membership emit only
low-frequency flushed state-count progress lines (131072 states), with no
inner-loop logging. The checker uses the selector's delta prefix for its
ten-coordinate replay and reserves the conjugate for the v12 physical-row
and exact-exponent replay.

Gates:

- external-PYTHONPYCACHEPREFIX `py_compile`: PASS;
- producer FIXTURE: PASS (`candidate_count=72`, tau/exponents zero);
- checker self-test: PASS (10 mutation rejections);
- `git diff --check` on the four outputs: PASS;
- GAP wrapper invocation was attempted but Windows GAP failed before parsing
  with `couldn't create signal pipe, Win32 error 5`; no production run was
  started.

No local production/bootstrap, checkpoint load, download, commit, push,
dispatch, workflow edit, or modification of Task435/v12/task179/v220 was
performed.  If selective Q0/fibre construction reaches a cap in GHA, the
producer emits `UNKNOWN_RESOURCE` with its phase; it never promotes an
uncompleted prefix to EMPTY or ACTIVE.

Checkpoint semantics are terminal-only for this positive-first owner: the
checkpoint records compact counters, digests, and phase, but there is no
mid-run resume path.  An interrupted selective scan therefore remains
`UNKNOWN_RESOURCE` and is rebuilt from the authenticated prefix on a later
run.

## Parent broker dispatch

- committed and pushed source commit
  `695310b7a7c28462145fe3827eb5181869020701` on
  `sol/r07-explicit-lift-20260825`;
- dispatched unchanged `gap-run.yml` as run `33403284390`, job
  `99524587327`;
- inputs: driver
  `search/d972_r07_a0_actual_b72_first_active_gha_driver_v1.g`, external
  preamble `D972_R07_A0_ACTUAL_B72_FIRST_ACTIVE_V1_RUN:=true;;`, output
  directory `ci/out`, job timeout 90 minutes;
- production result: workflow failure after 239 seconds.  The authenticated
  prefix completed, then producer returned fail-closed `UNKNOWN` with exact
  reason `'dict' object has no attribute 'value_from_blob'`; the checker
  rejected that nonproduction status.  Artifact `9762238011` contains the
  234-byte JSON at SHA-256
  `e3aa185fc8ca34b73ed4253f234eabe85c638e5694e3bb4b70b2bca3edbf3e72`.
  This is a task179 `AllSevenModel` attribute/dictionary adapter mismatch,
  not a selector result, cap, memory failure, ACTIVE, or EMPTY.  Versioned
  Task437 v2 repairs only that ABI boundary.
