# Sol(max) Task652 — final release re-audit of Task640's three live fixtures

## Role and bounded scope

You are Sol(max), the independent mathematical/code auditor. Read the complete
Task649 reply, Task651 mail, and Task651 reply first to last. Audit only whether
the three remaining F646-C blockers are now closed without regression of the
already accepted F646-A/B and R1/R3/R4/R5/R7 surface. Do not request optional
hardening or a redesign. Do not edit implementation, run production work,
dispatch GHA, or perform git operations.

Frozen quartet:

| file | bytes | LF lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,474 | 304 | `060202458e8643acb1ed42d2ad94b9f192406c57b803dc7f3b07897c39115ef7` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 91,687 | 1,557 | `354218ecbb89ad9f80baa5ea3c4fd605e7fe44dc7e8f86301e9d72cd9d4e7905` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `ec098e294bbbaef958a984bd050a0d049ede17bd4d624bb4ad1053ac88bb7205` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,972 | 58 | `6cc0d60259f9b760e2f3a6ea9d67867ed1e5dfa573462bb97d67a0af0705749b` |

Task651 reply is 1,770 bytes / 36 LF lines / SHA-256
`65a54d65555f124a537080e0bcbcb82b1c836ed7e734fae58e84a7b4b463f649`.
If any frozen value differs, stop with `INPUT_MISMATCH`.

## Required decisions

1. Confirm that the wrong ancestry binding fixture calls the exact live
   `parse_literal_leaves` and that deleting/breaking its binding comparison
   makes selftest fail.
2. Confirm that production and selftest both call the same
   `occurrence_prefix_gate`; its S3 fixture must independently distinguish
   reverse traversal, sign/inverse choice, and multiplication side/order. Check
   the fixed expected `[id,C,C]` directly rather than trusting its declaration.
3. Confirm that the packing fixture passes preceding target/lower/dense/packed
   byte equalities and is rejected only by the live unpacking/roundtrip branch.
4. Recheck exact parent typing and receipt names, the endpoint/all-seven and
   direct-occurrence path, streaming ancestry/no DOM, claim flags, resource
   caps, checker independence, pinned actions, checker/workflow/reply hashes,
   and the inert `false &&` guard for regression only.
5. Run only bounded serial checks: both py_compile/selftests, safe YAML parse,
   forbidden import/exec scan, immutable-action scan, and any tiny mutation of
   the three charged helpers needed to substantiate the verdict. No full graph
   or production-scale calculation.

Write only
`sol/sol_reply_652_final_reaudit_r07_task640_three_live_fixtures.md`.
Give exact evidence and one terminal verdict:

- `PASS / SAFE_TO_DISPATCH_GHA=yes`, or
- `FAIL / SAFE_TO_DISPATCH_GHA=no` with a concrete required blocker and the
  smallest finite repair.

Preserve the claim boundary: even PASS authorizes only the fresh-rho2 Task640
GHA run. It proves no rho2 value, grade-two MEMBER/NONMEMBER, A0, compatible
cofinal lift, fake, Ihara, cross-check, or Lean verification.
