# Luna task 157cd: exact synchronized Burau early-candidate accelerator

## Role and scope

You are Luna. Implement a new versioned synchronized Burau producer/checker/
workflow without editing any existing producer, checker, or workflow. You may
write only:

- `search/d972_b4_burau_joint_accel_v1.py`
- `search/check_d972_b4_burau_joint_accel_v1.py`
- `.github/workflows/d972-burau-joint-accel-v1.yml`
- `sol/luna_reply_157cd_joint_early_acceleration.md`

Do not run GAP, heavy local enumeration, Git, or GHA.

## Objective

Port the exact sound accelerations from task 157by to the synchronized joint
Burau obstruction, preserving the current joint-v1/v2 semantics and complete
finite-fiber implication.

Required properties:

1. Exact projected section and exact joint kernel; no sampling, word bound,
   Cartesian-product assumption, Bloom filter, or timeout acceptance.
2. Extract kernel generators as discovery-edge witnesses from the already
   exhaustive single BFS, and retain exact `kernel_elements`. The independent
   checker must rebuild the joint kernel and prove closure(witnesses)=K.
3. Candidate-only early stop: once a row's entire `h0*K` fiber has been checked
   and its `full_GT_identity_count` is zero, the producer may serialize the
   complete prefix ending in that zero row and stop. A partial all-pass receipt
   must be rejected. Add explicit negative selftests.
4. Independently replay pentagon plus both hexagon/`m` compatibility gates.
   A pentagon-only zero is not enough if the established joint contract uses
   `full_GT_identity_count`; preserve the strongest sound finite necessary
   condition.
5. Pre-register a compact, high-value parallel matrix drawn from existing
   configs, prioritizing `q3a2_full`, `q4a2_full`, `q3a2_q4a2`,
   `q3a2_q4a2_q5a2`, and `q3a2_q4a2_q5a4`. Do not introduce an unregistered
   field/parameter. `fail-fast: false`, 360-minute cap, exact source/hash/schema
   gates, independently checked artifacts.
6. Candidate means finite obstruction only and requires parent audit. All-pass
   remains nonterminal.

Report exact hashes, light tests, semantic implication, and resource limits.
