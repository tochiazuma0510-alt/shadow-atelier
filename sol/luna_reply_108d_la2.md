# Luna 108d LA-2 recovery report

Status: **CLOSED as a local candidate**.  The requested LA-2 theorem island is complete and
target-builds without placeholders.  This report does not call the result "verified"; no GHA or
manifest integration was authorized in this lane.

## 1. Scope and provenance

- Read-only source requested by the parent:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-luna106g-b0b23ce9e00145629c7479f5576be1ea`.
- Exact requested base:
  `82ff1047b80a50b8a3098a83d71424ed2c6ec26d`.
- Fresh work repository:
  `C:\Users\81905\AppData\Local\Temp\shadow-atelier-la2-108d-d396a0aaadb4477da47fa4dcbb2b0cf8`.
- Final `git rev-parse HEAD`:
  `82ff1047b80a50b8a3098a83d71424ed2c6ec26d`.
- The source repository remained untouched.  Its checked-out HEAD was `799e915...`, but the
  requested commit object was present.
- A literal local `git clone --local --no-hardlinks --no-checkout` was attempted first.  Git for
  Windows failed before creating the target with
  `sh.exe: fatal error - CreateFileMapping ... Win32 error 5`.  A `file:///C:/...` retry failed
  identically.  The effective fallback was a fresh TEMP directory, a copy of the source `.git`,
  detached checkout of the exact requested commit, and materialization with
  `git checkout HEAD -- .`.  HEAD and a clean status were checked before implementation.
  No network operation occurred.

## 2. Changed files

1. `lean/P1/BlockA_LA2.lean` -- new, 935 lines, 40 theorem declarations, 17 definitions.
2. `sol/luna_reply_108d_la2.md` -- this report.

No existing source, map, manifest, lake file, workflow, or shared workspace file was edited.

Final Lean source SHA-256:

`6c461051eee9f1f07bfa4dae25f2072b5120a3b0c6475d99903af31fca286802`

## 3. Paper-to-Lean correspondence

| Paper obligation | Closed declaration(s) |
|---|---|
| Explicit universe | Every group predicate is `H0 : Gn n -> Prop`; the file imports and reuses baseline `window.J` without redefining the family or its parameter types. |
| Explicit oddness and size | The paper theorem `window.transitive_iff_trivial_inter` takes `h3 : 3 <= n` and `hn : NatOdd n`, in addition to `[NeZero n]`. |
| Exact `2n) code carrier | `window.xCodeFinEquiv : PlainEquiv (Fin (2*n)) (XCode n)`; no prose cardinal premise is used. |
| `XCode` representatives are actual powers | `window.powerSeedExponent`, `window.powerCode`, `window.xpowGn_powerSeed`, `window.powerCode_surjective`, `window.bounded_power_eq_xrep`, and `window.xrep_eq_bounded_power`.  Oddness is used in the injectivity/surjectivity of doubling on `Fin n`. |
| Actual cyclic subgroup `<X>` | `window.InXPowers`, `window.genX_iff_InXPowers`, `window.InXPowers_iff_exists_xrep`, and `window.genX_iff_exists_xrep`.  Arbitrary natural powers are reduced modulo `2*n` using `Gn_ord_X`, not by a finite evaluator. |
| Actual left cosets/action | `window.leftCoset_mul_right_eq`, `window.orbitCoset`, `window.XPowerCarrier`, and `window.cyclicOrbitCoset`.  `window.cyclicTransitive_iff_leftCosetAction` identifies paper P3 with surjectivity of the actual `<X>`-orbit map into `LeftCosets H0`. |
| Exact P1 hypothesis | `window.coded_transitive_iff_trivial_inter` consumes the existing `Index2nWitness H0`, hence both `IsSubgrp H0` and the exact `Fin (2*n) <-> LeftCosets H0` witness.  The equal-finite-cardinality step is proved constructively in the file. |
| LA-2 conclusion | `window.transitive_iff_trivial_inter (h3) (hn) H0 iw : CyclicTransitive H0 <-> CyclicTrivialInter H0`.  Both sides use the actual `genX` subgroup.  The existing code-level `Transitive` and `TrivialInter` are connected by named equivalence bridges, not silently substituted. |

The finite-cardinality proof does not assume a cardinal equation in prose.  It proves
injective/surjective equivalence for maps transported through explicit `PlainEquiv (Fin m) ...`
witnesses.

## 4. Commands and results

Run from the fresh repository unless noted otherwise.

1. Base materialization check:

   `git rev-parse HEAD`
   -> `82ff1047b80a50b8a3098a83d71424ed2c6ec26d`.

   Initial `git status --short`
   -> empty.

2. Baseline target:

   `cd lean; lake build P1.BlockA`
   -> exit 0, 6 jobs.

3. Final direct typecheck:

   `cd lean; lake env lean P1/BlockA_LA2.lean`
   -> exit 0.  Only four unused-section-variable linter warnings in the new file.

4. Final target build:

   `cd lean; lake build P1.BlockA_LA2`
   -> exit 0, 7 jobs.  Baseline modules replay their pre-existing linter warnings.

5. Forbidden-source scan:

   `rg -n -i -e '\baxiom\b' -e '\bsorry\b' -e '\badmit\b' -e ':\s*True\b' -e '\bnative_decide\b' -e '\bofReduce' -e '\bdecide\b' lean/P1/BlockA_LA2.lean`

   -> no matches.

6. Debug-command/corruption scan:

   `rg -n '^#print|^#check|\?\?' lean/P1/BlockA_LA2.lean`

   -> no matches in the delivered source.

7. Final worktree status after this report:

   expected exactly
   `?? lean/P1/BlockA_LA2.lean`
   and
   `?? sol/luna_reply_108d_la2.md`.

## 5. Axiom exposure

Temporary `#print axioms` commands were used and then removed before the final typecheck/build.
Exact output:

- `window.transitive_iff_trivial_inter`:
  `[propext, Classical.choice, Quot.sound]`.
- `window.cyclicTransitive_iff_leftCosetAction`:
  `[propext, Quot.sound]`.
- `window.genX_iff_exists_xrep`:
  `[propext, Classical.choice, Quot.sound]`.
- `window.coded_transitive_iff_trivial_inter`:
  `[propext, Classical.choice, Quot.sound]`.
- `la2FiniteMap_injective_iff_surjective`:
  `[propext, Classical.choice]`.

These are all in the existing P1 core allowlist.  There is no project axiom, `sorryAx`, admitted
term, native evaluation fallback, or theorem with conclusion `True`.

## 6. Integration note

The lane was forbidden to edit `AxiomCheck.lean`, `AXIOMS.manifest.json`,
`PAPER_STATEMENT_MAP.md`, or lake/workflow files.  Therefore this is a standalone targeted-build
candidate.  A parent integration pass must import the new module and regenerate/audit the manifest
before any GHA-grade status change.

No credential, commit, push, dispatch, or network clone was used.
