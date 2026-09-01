# Task 511 -- independent Sol(max) audit of Task503 A4 actual-production shard wiring

Role: adversarial mathematics/software-contract auditor only.  Do not edit
implementation, run the 6,441-row production, dispatch GHA, commit, push, or
write any file except the reply named below.  Use static/generated-source
inspection and small bounded fixtures/mutations only.  Reject any helper-only
PASS, but do not reconstruct the production universe merely for extra audit.

Read fully and pin before judging:

1. `sol/proof_r07_a4_actual_production_shard_wiring_v430.md`, 7137 /
   `acea72aea1a8f62a3de1c84a7bf4cab95fc4da85162bbe226b1a5f158755a904`;
2. `sol/sol_reply_502_audit_r07_a4_intraquery_physical_shard_resume_v1.md`,
   including both dead-code counterexamples;
3. `sol/luna_task_503_r07_a4_actual_production_shard_wiring_v1.md` and
   `sol/luna_reply_503_r07_a4_actual_production_shard_wiring_v1.md`, 3579 /
   `fc5b35b026c56016e6ba1a537501caf3d66948296da416784b60e1c743489d38`;
4. Task503 subjects:
   - producer v24, 34535 /
     `8dc698e43fa7971dff4af3a5a19a7ac309ab5d43a19bb1f5189c0c222df01dfe`;
   - checker v33, 24033 /
     `44e79864424a21d836d0b61dbe066889e3567d250e722026143a2eb8f7d87ccf`;
   - driver v43, 15449 /
     `36be6a635fa7399c37048ef45debb5c25d5ede8cc1414fa153a7e8bb0dd7c8bb`;
   - generated producer, 285814 /
     `9e3619f2e83dc7bea2e58d250bff3fafc24b8e09910c389b7a402a3b2d0d2d6a`;
   - generated checker, 312046 /
     `cb1d2b390beb3bdbd71d2175983310971d0669f6a6d7b77e1e64f29ceae61f57`;
5. frozen v22/v31/v41, rejected v23/v32/v42, Task483 checker-only v3
   transport, v423/v425/v429, and every row-26 release/member pin referenced
   by v43.

Audit actual generated executable paths rather than wrapper prose.  Decide:

F1. Both wrapper-local generated-result pins are nonzero and active, all
patch cardinalities are exact, and deleting only helper definitions cannot
restore the old owner because live call sites are patched.  Production
`main -> build_kernel -> consume_row -> Oracle.query` must construct one
controller, call prepare, close batches, direct-restore, and commit with
positive non-SELFTEST call counts.

F2. A batch owns exactly `m=min(64,len(private_candidates))` fully examined
candidates, not 64 accepted rows.  Its ordered identities/coefficients,
accepted mask and Hamming-weight entry list are complete.  Every accepted
entry comes from the real `LiveBasis.add_boundary` path and records the full
boundary/combined reductions, formals, events, epochs, ranks and semantic
counters; zero decisions create no entry and cannot omit a true rise.

F3. `prepare` seals the open row before query work, while bridge/row/chunk/
sample completed prefixes are appended exactly once only after the unique
MEMBER/ZERO commit.  Each closed shard is atomically installed before HEAD;
an open/partial batch is never named by HEAD; commit writes the ordinary row
delta once and marks the physical HEAD obsolete.

F4. CLI restore authenticates the ordinary completed-row base plus exact
HEAD/shard chain and directly restores physical maps, formals, events,
records, duals, epoch and counters before continuing the open query.  Use
instrumentation that fails if admitted entries call insert, reduce,
correlate, or raw-boundary replay.  Interrupted-after-three-batches restore
must equal uninterrupted completion on the real bounded route.

F5. ResourceStop emits `physical_shard_chain` iff at least one closed batch
exists and binds ordinary base/HEAD, open query, physical HEAD, ordered shard
identities and counts.  Before the first close it retains the ordinary row-26
reference.  It must not promote MEMBER, NONMEMBER, A4, fake or Ihara.

F6. V33 does not import v24 or call its validation helper.  Its actual
`validate_terminal_checkpoint`/acceptance route independently rebuilds each
dual, roster and exact m-prefix, sequentially recomputes mask and accepted
entries, and checks all full values/counter transitions.  Fully re-sealed
mutations must reject at least omitted rise, extra entry, mask drift, raw
identity/physical row drift, reorder/missing/mixed-row shard, stale/open-query
drift, HEAD-ahead, completed-prefix open row and duplicate terminal.  Preserve
v423 unique resource excess and v429 completed-counter relation.  Ordinary
positive replay must remain extensionally v31.

F7. V43's reached shell authenticates wrapper/generated pins, the immutable
56,410-byte release and all six members (including exact HEAD and delta2),
installs them, and starts exactly one v24 producer from the row-26 HEAD with a
distinct physical root.  It preserves 14,400-second/8-GB internal limits and
external margin, rejects stale outputs and UNKNOWN_INPUT/HARD_STOP/ERROR/
Traceback, uploads typed RESOURCE without launching a checker for a producer
RESOURCE, and invokes at most one v33 checker only after a producer positive
terminal.  Exact one-line owned markers and output nonemptiness are live
gates.  The generated shell must actually execute; assignment-only pins or a
parse-only transport are STOP.

F8. Check bounded copy/performance shape: no full physical matrix snapshot,
cumulative shard-prefix rewrite, replay of earlier shard reductions, dense
conversion, worker pool, retry search, SELFTEST before production, or extra
boundary closure.  Distinguish a real blocking traversal/copy from a cosmetic
allocation; do not request unrelated optimization.

Return exactly one verdict:

- `GO_FOR_GHA_DISPATCH`, only if F1--F8 pass on load-bearing paths; or
- `STOP_DO_NOT_ADOPT`, with the smallest concrete repair list.

Write only:

`sol/sol_reply_511_audit_r07_a4_actual_production_shard_wiring_v1.md`

Include exact pins, bounded commands/tests, findings F1--F8, claim boundary,
and final marker `TASK511_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_AUDIT_GO` or
`TASK511_R07_A4_ACTUAL_PRODUCTION_SHARD_WIRING_AUDIT_STOP`.
