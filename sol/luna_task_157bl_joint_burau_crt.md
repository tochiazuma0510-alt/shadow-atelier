# Luna task 157bl — simultaneous Burau-specialization obstruction

You are Luna, the implementation/computation engineer.  Implement a versioned,
bounded, lossless simultaneous-specialization finite obstruction and report in
`sol/luna_reply_157bl_joint_burau_crt.md`.  Do not run local GAP, git, push,
or GHA.  Lightweight Python selftests are allowed.  You may edit only:

- `search/d972_b4_burau_joint_v1.py`
- `search/check_d972_b4_burau_joint_v1.py`
- `.github/workflows/d972-burau-joint-v1.yml`
- `sol/luna_reply_157bl_joint_burau_crt.md`

Read v4 producer/checker, replies 157ab/157u/157bg, and task 157bk.  Preserve
the exact frozen 972 roof/key artifact and literal five A.18 Burau blocks.

## Mathematical target

For a list of specializations S, construct the *single synchronized image*

    Psi_S:F2 -> R x product_{s in S} GL4(F_q(s))^5

from the same source generators/words.  Compute `H_S'`, its projection to
`R'`, and the exact kernel.  For every roof row enumerate the complete fiber
inside this joint image and count elements whose pentagon defect is identity
in every specialization simultaneously.  Never take a Cartesian product of
the separate single-q fibers unless you prove it equals the synchronized
image.

Required configurations, in increasing cost:

1. `q3a2_q4a2` (q=3,a=2 is the existing a=-1 lane; q=4,a=2);
2. `q3a2_q4a2_q5a2`;
3. `q3a2_q4a2_q5a4`.

The workflow may run them as independent jobs in parallel.  A zero fiber in
any sound joint configuration is a direct candidate obstruction; all-pass is
UNKNOWN.  Use the exact direct-obstruction logic from task 157bk only as a
declared theorem premise pending parent audit; the producer itself must emit
candidate/UNKNOWN, not self-promote A/B.

## Exactness and resource requirements

- Use uncapped finite closure/Schreier enumeration for mathematical results.
  A timeout/resource exit is `UNKNOWN_RESOURCE`, never all-pass/zero.
- Bind the synchronized generator order, field arithmetic, paper product,
  all five block orderings, frozen artifact hashes, source SHA, and config.
- Prove/replay `Psi_S(F2')=H_S'` operationally by normal closure of the joint
  commutator and exact projection/order gates.
- Complete fibers must be right fibers `h0*K_S`, with deterministic section
  representatives coming from the single synchronized BFS.
- Store lossless kernel elements/generators, each row's h0, joint fiber digest,
  simultaneous identity count, and first nonidentity vector by specialization.
- Include negative fixtures for unsynchronized Cartesian-product acceptance,
  deletion of a kernel element, field/config swap, product orientation, h0,
  source word/key, and a defect-block mutation.
- Checker must not import producer or v4 helpers.  Independently rebuild the
  roof, fields, Burau/A.18 maps, joint image, kernel, fibers, and all counts.
- Engineer memory carefully.  If the straightforward section is too large,
  compact matrices/section records or deterministic parent-tree replay are
  allowed, but no heuristic pruning or truncated kernel.
- Workflow: Ubuntu, read-only checkout, pinned Python dependencies, exact
  selftests, 12 GB virtual-memory guard, at most 360 minutes per job, artifacts
  with `always()`, exact terminal-marker cardinality, checker on any complete
  candidate/all-pass receipt.  No workflow_dispatch until parent review.

## Report

Give static/selftest outputs, hashes, expected order gates learned from v4
where applicable, exact status semantics, and any honest resource limitation.
End with exactly one token:

- `JOINT_BURAU_CRT_READY_FOR_GHA`
- `JOINT_BURAU_CRT_BLOCKED_<short_reason>`
