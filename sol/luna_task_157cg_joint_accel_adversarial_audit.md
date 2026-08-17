# Luna task 157cg: adversarial audit of synchronized Burau accelerator

## Scope

Audit these new files read-only and write only
`sol/luna_reply_157cg_joint_accel_adversarial_audit.md`:

- `search/d972_b4_burau_joint_accel_v1.py`
- `search/check_d972_b4_burau_joint_accel_v1.py`
- `.github/workflows/d972-burau-joint-accel-v1.yml`
- task/reply 157cd

No GAP, heavy local enumeration, edits to the bundle, Git, or GHA.

## Required checks

Adversarially verify exact joint-kernel completeness, discovery-witness
closure, deterministic source/config hashes, independent checker
reconstruction, pentagon + H10 + H11 + common CRT/unit-m witness semantics,
candidate-only prefix stopping, full 972 all-pass requirement, and workflow
matrix/source/status/artifact gates. Mutate bounded fixtures for incomplete K,
partial all-pass, candidate with pentagon-only zero but positive full count,
missing/duplicate terminal zero row, config substitution, source hash drift,
and status disagreement. Check YAML/embedded Python and all path names.

Return `JOINT_ACCEL_AUDIT_PASS` or `..._FAIL`, exact hashes, and line-referenced
findings. A pass authorizes parent commit/push only; it is not A/B.
