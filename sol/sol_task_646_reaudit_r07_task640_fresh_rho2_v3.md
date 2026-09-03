# Sol(max) Task646: finite release re-audit of repaired Task640 v3

Role: Sol mathematical/code auditor.  This is the final finite re-audit after
Task644 `FAIL` and Luna Task645's bounded repair.  Read the complete Task644
reply and Task645 instruction/reply, then audit the exact frozen quartet below.
Do not implement, edit the quartet, run production/GHA, use git, or introduce
new optional design requirements.  Write only
`sol/sol_reply_646_reaudit_r07_task640_fresh_rho2_v3.md`.

## 1. Frozen inputs

| file | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 27,227 | 299 | `d8957511167f3ace568f59fd2d50dfcdbd7a16fc50bd4475077fcd73dbc3a5b9` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 85,627 | 1,490 | `3b8b335da4a2233977464fc553e040a3a0f0c79d5bf58451255d8370e63e88af` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 9,974 | 161 | `0f8df3e4bfd22024ffd0f3c5841717441dc03dedb8834cec9fe46a460634826f` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 2,833 | 53 | `508c28e322dae868f2dd7043a3ed4a01c4110fffb8fbe4154b4d25c29577896f` |

Required context:

- `sol/sol_reply_644_audit_r07_task640_fresh_rho2_v3.md`;
- `sol/luna_task_645_r07_task640_finite_release_repair.md`;
- Task640/643 instructions and the paper/audit pins named by the programs.

Abort with `INPUT_MISMATCH` if any frozen byte count or digest differs.

## 2. Finite audit questions R1--R8

Re-audit exactly the eight Task645 repair groups.  For each, give `PASS` or a
specific blocking counterexample with file/line evidence.

1. **R1:** the workflow fetches the real Task595 v2 artifact, not v3.
2. **R2:** the Task625 run/attempt/head/job/artifact live envelope is queried
   and fixed exactly, then the complete parent binding is sealed by producer
   and required by checker.
3. **R3:** reached seeds come from ordered raw sources before cancellation;
   exact-key cancellation follows; every surviving exact key gets the direct
   all-seven canary before signature grouping, independently on both sides.
4. **R4:** checker dense replay acts only its independently reconstructed
   nonzero signature buckets, while retaining the separate exact-key canary.
5. **R5:** checker executes/imports no producer-shared semantic module.  Its
   endpoint authority is local and sufficient for marked quotient/group,
   words/substitution, E3/E4, Fox/translation, PB3 lift, hexagon/pentagon and
   direct-versus-occurrence comparison.  Merely hash-reading pinned sources is
   allowed.  Producer-side pinned v12f remains explicitly allowed.
6. **R6:** manifest allowed keys and complete equality cover the full parent,
   roots/digests, occurrence data, exact `L/U/G/cache`, dimensions, degree-one
   gates, coefficient/lower-zero gates, all payload receipts/rho2 fields and
   all false/null later claims.
7. **R7:** `source-ancestry.json` is stream-hashed rather than DOM-loaded;
   record/path-length/path/trie/live-state caps are attached to actual live
   counters and fail closed.  Give a static peak-memory assessment and flag
   only a concrete production-sized risk.
8. **R8:** tiny serial selftests exercise live validation predicates and reject
   the required occurrence/order/type/sign/endpoint/merge/seed/root/leaf,
   parent/manifest/receipt/claim mutations.  Do not demand a large fixture.

Also rerun bounded serial `py_compile`, both `--selftest`s, YAML safe parse,
immutable action-pin scan and forbidden shared-exec/import scan.  Confirm the
workflow remains inert (`false &&`) pending root release.

## 3. Decision boundary

Return exactly one verdict:

- `PASS` and `SAFE_TO_DISPATCH_GHA=yes` if all finite blockers F644-1..8 are
  closed; or
- `FAIL` and `SAFE_TO_DISPATCH_GHA=no`, listing only concrete release blockers.

Do not treat style, generic refactoring, stronger future independence, a full
grade-two membership owner, graph traversal, SAT, checkpointing, or a
production-sized local run as blockers.  A PASS authorizes only the one
fresh-rho2 GHA consumer.  It does not declare grade2 MEMBER/NONMEMBER, A0,
order 54,432, a cofinal lift, fake, Ihara, cross-check or Lean verification.
Report reply bytes/lines/SHA-256 and `verified=false`.
