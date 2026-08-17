# Luna task 157bo — joint Burau hexagon/CRT adversarial soundness audit

Role: Luna independent mathematical/runtime auditor.  Do not edit producer,
checker, workflow, or any other tree file.  Write only
`sol/luna_reply_157bo_joint_hexagon_soundness.md`.  Do not run local GAP, Git,
push, or GHA.

Audit the frozen candidate bundle:

- `search/d972_b4_burau_joint_v1.py`
- `search/check_d972_b4_burau_joint_v1.py`
- `.github/workflows/d972-burau-joint-v1.yml`
- `search/certs/d972_b4_word_key_artifact_v1_20260816.json`

The decisive question is fail-closed soundness: if a row has
`full_GT_identity_count = 0`, does this really exclude every genuine
profinite GT lift of that D972 roof target?

Required numbered audit:

1. Page-image-check `papers/2401.06870-gt-shadows-gentle-version.pdf`, especially
   equations (1.14), (1.15), Proposition 3.4 equations (3.10), (3.11), and
   identify exact PDF pages.  Check the repository `PaperProd` convention and
   the implementation of theta, tau, tau^2, H10, and H11 factor order.  Do not
   rely only on extracted text.
2. Prove or refute that the joint tuple is the image of one common source
   element under all specializations/transforms, and that the computed
   `h0*K_S` is the complete finite image of the required F2' fiber rather than
   a Cartesian product or a bounded word sample.
3. Prove or refute the `m` gate.  A genuine lift supplies one profinite m with
   m congruent to the roof m modulo 18 and lambda=2m+1 a profinite unit.  Check
   whether enumerating residues modulo L=lcm(18,ord(joint y)) and requiring
   gcd(2m+1,L)=1 is a necessary finite shadow condition, and whether using one
   residue simultaneously across all specs is correct.  Look especially for
   missing prime-power or negative-representative issues.
4. Check pentagon A.18 orientation, transform block slicing, normal-closure /
   Schreier kernel completeness, row fiber binding, producer/checker
   independence, and workflow fail-closed behavior.  Static Python tests are
   allowed; no full heavy run locally.
5. State exactly one terminal marker:
   - `JOINT_HEXAGON_SOUNDNESS_PASS`, or
   - `JOINT_HEXAGON_SOUNDNESS_BLOCKED: <precise reason>`.

Do not infer B4-A/B from an all-pass finite run.  A zero row is only a direct
genuine-lift obstruction, with the separate 972/324/index-3 premise bundle
handled by task 157bn.
