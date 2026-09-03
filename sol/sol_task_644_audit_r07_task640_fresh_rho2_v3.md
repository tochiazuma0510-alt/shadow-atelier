# Sol(max) Task644: Task640/643 fresh-rho2 v3 final static audit

Role: independent mathematical/code auditor. Read this mail completely and
then audit the finished Task640 quartet against the cited contracts. Do not
implement, run production/GHA, edit the quartet, or perform git operations.
Create only:

`sol/sol_reply_644_audit_r07_task640_fresh_rho2_v3.md`.

## 1. Frozen implementation

Audit these exact files:

```text
search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py
  26,491 bytes
  f7ce3f23a60a626e8a297017c7f898b92ac7c6b626e09ebc84501e6d97f9b826
search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py
  79,461 bytes
  662ae5797581be4c08f45787c43b1cb58e9a3ac5ecd81d2621a7a5b572731a98
.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml
  8,724 bytes
  deace59ca2d2dc8999f68aca44737887873edf2e6a6742529af11c3386298104
sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md
  5,690 bytes
  a61b3abeae798eaff5536de1a870485731c223a1448ba5a7cb7b8c1982f56a94
```

Mandatory contracts are Task640, Task643, Task627, Task630, Task639 and
Task641. In a conflict, Task643's compositional-parent ruling supersedes only
the duplicated Task625 graph-to-leaf traversal requirement.

## 2. Finite audit questions

Return `PASS`, or `FAIL` with only concrete blocking defects and the smallest
repair for each. Do not propose optional refactors or stronger infrastructure.

1. Parent composition: exact Task625 run/artifact/15 receipts and uploaded
   verdict are authenticated; workflow reruns the exact checker against exact
   Task554/595 parents and byte-compares the verdict. Both consumers really
   parse `R07LEAF1`, reconstruct the prior/root order, and do not silently
   restore the removed graph traversal or replace the source witness.
2. Fresh semantics: actual typed `E3^6 x E4^5` eleven contexts, signs,
   coordinates, endpoints, right-trie, all-seven H1/H2/pentagon canary and the
   typed first-six restriction are on the live path. The direct canary must
   run before grouping for every nonzero exact complete key `(s,P)`, not only
   one signature-bucket representative.
3. Arithmetic: producer uses the allowed pinned Task565 arithmetic owner and
   any v12f producer-side endpoint import is exact-pinned and semantically
   admissible. Checker has genuinely independent live group/word, endpoint,
   truncated-ring, negative/inverse action, PB3/boundary, target,
   occurrence-first aggregation and packing arithmetic; it must not import
   producer, Task565, shared floor, former grade-two checker or runtime v13.
4. Result gates: separate Task625 physical and Task595 MEMBER-zero gates;
   all 32,260 lower coordinates; all 48,384 top trits; exact 12,096-byte
   pack/decode; complete receipts and every false/null claim guard.
5. Workflow: exact hashes and artifact layouts are usable; unique PASS is
   required before residual upload; logs always upload; immutable actions,
   serial execution, 120-minute job and bounded process limits are coherent.
6. Resource audit: flag only an actual unnecessary production-sized rebuild,
   dense-per-node/path allocation, hidden large copy/densification, repeated
   direct computation that violates the contracts, or a cap that makes the
   intended live route impossible. Bounded exact per-leaf canaries required
   by Task630 are not optional overhead.
7. Fixtures: success path and listed semantic mutations exercise live
   validators sufficiently for a static dispatch decision. Do not demand
   production-sized selftests.

## 3. Claim boundary

This static audit cannot establish rho2, grade2 MEMBER/NONMEMBER, A0,
order-54432/full-Q0, COMMON, a cofinal lift, FAKE, IHARA, cross-checking or
Lean verification. State this boundary. Include exact audited hashes and a
single dispatch ruling: `SAFE_TO_DISPATCH_GHA=yes/no`.
