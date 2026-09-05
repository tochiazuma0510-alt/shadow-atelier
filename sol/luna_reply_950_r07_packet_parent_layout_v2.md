# Task950 -- exact mixed-generation parent layout repair v2

## F1. Executed failure and repair scope

Run33963515077/1, commit `25501f62c326290bafd223fe3b7a1d7b0ba51f0c`,
passed source/data pins, parent staging and seven synthetic canaries, then
failed after the initial1356-row lambda sweep at v1's blanket rho2 flag lookup.
No packet or new step completed. This account is the actual workshop express
`ops/express/20260905_fable_astra_packet_loop_run1_keyerror.md` / ruling2123,
not a locally executed result. The reported diagnostic artifact is9968702711
(18902 bytes). No new numerical outcome is inferred from that failure.

I read Task950/947 and that express in full, inspected the real base/seed30/
seed34 result/target/rho2 JSON shapes, and copied the published producer to
`search/d972_r07_fixed_root_packet_loop_v2.py`. The repair admits exactly:

| Parent | Result schema | Target schema | Actual rho2 flag |
| --- | --- | --- | --- |
| base | d972.r07.physical-state.Separator.v1 | d972.r07.physical-state.target-reduction.v1 | no rho2 parent block |
| seed30 | d972.r07.actual-seed30-materializer.v1.result | d972.r07.actual-seed30-materializer.v1.target-update | absent |
| seed34 | d972.r07.actual-root-seed-materializer.v3.result | d972.r07.actual-root-seed-materializer.v3.target-update | present, true |

The common original-rho2 packed identity is
`b41b9e69fc1257bb1542062a2496bc94bd3cbe6b01e03aba653dae2e4af17c2e`;
its accepted manifest identity is
`55c42f06e70b2150d324ed8649fe4af0e6db1bf0e87e315db570d1fa80f61488`.
The base target is joined to state manifest
`d11d551c2b1a127bd900c013cbc684eef698372660ff733b10f82bb4793f227b`,
and its state head/rank/generation and original-rho2 identity are checked.

`saved_parent_layout` is the same strict validator used in production and
the new actual-parent metadata CLI. It rejects unregistered result/target
schemas, a present legacy flag, missing/false v3 flag, unexpected rho2 keys,
and any difference in the full accepted rho2 artifact/manifest/packed identity.
The legacy layout is admitted only with its exact accepted result/target and
manifest-authenticated payload bytes, joined to the base target and explicitly
named DERIVED chain. No frozen parent is modified, backfilled or interpreted
with a default-true lookup.

## F2. Frozen files and unchanged arithmetic

New source: `search/d972_r07_fixed_root_packet_loop_v2.py`, **84173 bytes**,
SHA256 `e040c7b3cf5f96fe33c0e36a00ba8dd887784e0f5a1e6fa036d407c0ceba65e6`.
Only this source and `sol/luna_reply_950_r07_packet_parent_layout_v2.md`
were written for Task950. Published v1 remains70509 bytes,
SHA256 `65169d7a26b6daf29152d5afa1352387766ac4024b078caf82a295ca57fbc3fd`.

A read-only source-text comparison found these20 existing function bodies
identical to v1: collect_relations, raw_accumulators, subtract_p1,
subtract_lower, projector_receipts, build_packet, authenticated_directory,
decoded_sealed, load_packet, packet_row, scan_roots, derived_rho2,
next_separator, literal_reference, head_record, append_step, load_prefix,
terminal_for, run_actual, selftest. This is a source comparison, not numerical
execution or a claim that v2 has passed runtime checks.

Changed code is limited to the module docstring/schema-v2 constant, exact
metadata fixtures/identity constants, six metadata helpers, production layout
wiring in load_saved_delta/load_start/owner_and_tables, and the new CLI branch.
The start receipt now includes a sealed `parent_layout`; all other packet,
root/step/HEAD/result fields retain the public v1 layout under schema v2.
The v2 same-owner resume contract is for v2 output. No v1 migration is added.

The executed numerical module set remains the four own accepted modules
and two source-data pins in reply945 F2 and v2 `MODULE_PINS`/`DATA_PINS`.
No new numerical dependency, checker import, sibling arithmetic read/copy,
or global-constant monkeypatch was introduced. The new metadata code uses
hashing, canonical JSON, schema/identity joins and byte receipts only.

M3-1 remains DERIVED: original rho2 is not directly read; old target histories
are not replayed. The accepted base span identity and seed30/34 subtractive
target-delta identities remain named premises. Both new direct target pairings,
full final-row sweep, all four fresh adjoints, ordered fixed44 packet, full lower
zero gate, raw seed2 pin, saved seed30/34 byte joins, conservative176 append cap
and durable-prefix behavior are retained. No packet rank, further append count
or next seed is forecast from the old run.

## F3. Public ABI and actual-parent canary

Schema prefix: `d972.r07.fixed-root-packet-loop.v2`.
Production CLI is unchanged except the filename. The added metadata-only CLI is:

```text
python -B search/d972_r07_fixed_root_packet_loop_v2.py --parent-layout-selftest --state-root BASE --delta-root SEED30 --seed34-root SEED34
```

It accepts only those three actual roots, rejects simultaneous synthetic or
resume/packet inputs, and does not call dependencies(), unpack, source-context,
P1/lower streaming or physical/target arithmetic. Exact byte/SHA pins load:

- Base: state/manifest.json, output/result.json, checker-result.json.
- Each saved delta: output/manifest.json, output/result.json,
  output/instruction.json, checker-result.json, source-receipt.json, and every
  output payload named by its fixed manifest. These bytes are hashed, not decoded
  as trit rows. The original rho2 artifact, P1 cache, Task554 bodies/blobs and
  base physical/instruction matrices are not read by this CLI.

The fixture identities are base run33891714539/1 artifact9944214057,
seed30 run33946247365/1 artifact9963533999, and seed34 run33956437467/1
artifact9966542166. Their pins are `LAYOUT_BASE_FILES`, `LAYOUT_SEED30_FILES`
and `SEED34_FILES`; the existing exact pins are retained.

The CLI result has schema `.parent-layout-selftest`, status PASS on actual
success, metadata_only=true, fixtures with identities/file receipts,
parent_layout, rejected_cases, cross_checked=false and verified=false.
The five required in-memory mutation cases are exactly:

1. `v3-flag-false` -> layout_v3_explicit_premise_flag.
2. `v3-flag-missing` -> layout_v3_explicit_premise_flag.
3. `rho2-packed-identity` -> layout_original_rho2_identity.
4. `unexpected-parent-schema` -> layout_materializer_schema.
5. `base-target-manifest` -> layout_base_target_manifest.

Each mutation invokes the production validator and must fail for its intended
reason. Parent files remain untouched. This is a focused regression for the
actual failure; the old target solve and old numerical suites are not rerun.

The agreed sealed `.parent-layout` in start.json and the CLI has these fields:

```text
base: {result_schema, target_schema, state_manifest_sha256,
       result_sha256, target_sha256, rho2_sha256}
deltas: [seed30_record, seed34_record]
derivation_mode: "derived"
original_rho2_directly_read: false
old_target_history_replayed: false
```

Each plain delta record has role, result_schema, target_schema,
manifest_sha256, result_sha256, target_sha256, rho2_identity (the copied three
actual identity fields), target_derivation_flag_present (false/true),
target_derivation_flag_value (null/true), admission
(`exact-accepted-legacy-target-chain` / `exact-accepted-v3-explicit-target-premise`),
and payloads={source_d_sha256,physical_normalized_sha256,target_remainder_sha256}.
Target hashes mean full canonical target bytes. Outer sealing uses the unchanged
canonical-ASCII/sorted-keys/compact/final-LF convention. This normalized receipt
records the parent layouts; it does not alter either parent.

Task951's workflow agreement is to run both actual-parent metadata CLIs on the
downloaded parents, require PASS and at least five rejected cases from each,
and compare exact canonical parent_layout receipts before packet production.
Only public schema/receipt facts were coordinated between workers.

## F4. Remaining gates and claim boundary

No local Python/GAP execution, network, credentials, git, dispatch or new agent
was used. The local evidence is source/JSON inspection and file/hash metadata.
No local metadata-canary PASS or numerical PASS is claimed.

Root/Task951 must freeze the v2 source/workflow tuple, run GHA syntax and
source/data checks, both actual-parent metadata canaries with equal receipts,
the inherited bounded synthetic canaries, and then actual fixed44 production,
real same-output resume and independent whole-packet/new-prefix replay.
Candidate upload remains contingent on checker PASS; incremental CV-9 follows
an actual run. No new run id/commit SHA was created by this worker.

The v1 run established no packet or new rank result. V2 packet rank, root values,
append count, terminal, timings/RSS and checker result remain unknown until the
new run. ROOT_SEEDS_ZERO stays within the fixed finite list, MEMBER_CANDIDATE
retains the unfinished word gates, and no grade2/full-A0, COMMON, cofinal lift,
fake or Ihara conclusion is asserted.

TASK950_STATUS: SOURCE_FROZEN_RUNTIME_PENDING; cross_checked=false; verified=false.
