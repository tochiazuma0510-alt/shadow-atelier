# Luna reply 167: g760 target6 post-closure recovery v5

Date: 2026-08-27
Role: Luna / implementation and bounded serial mechanical audit only

## 1. Result

Implemented the v5 recovery adapter and producer-only GAP driver.  The two
independent v4 failures are now reproduced and repaired:

1. the producer now carries the pinned v2 module through every completed-j
   build/validate/write/load path; and
2. the driver audits the canonical receipt structure instead of incorrectly
   requiring a legitimate duplicated field to occur once globally.

The bounded clean-overlay audit passed the exact relator-11 to completed-j
path, immutable j checkpoint write/reload, manifest inclusion, transition to
j=10, fresh/resumed safe-stop counting, all retained v4 delta/cache gates, and
four synthetic claim-free terminal receipts.  No full j=9 calculation, GHA
dispatch, workflow edit, proof/CLAIMS edit, commit, push, or checker process was
performed.

## 2. Exact v4 incident diagnosis

### Producer-side INPUT_STOP

The v4 call chain is:

```text
finish_j_row
  -> validate_terminal_header
  -> build_j_checkpoint
  -> validate_public_j_row(v3, row, summary)
  -> v3.validate_public_j_row(row, summary)
```

The pinned v3 function actually has signature

```text
validate_public_j_row(v2, row, summary)
```

Therefore the v4 wrapper omits v2 and raises
`TypeError: ... missing 1 required positional argument: 'summary'` as soon as
`build_j_checkpoint` validates the completed public row.  The generic v4
exception handler classifies this non-resource exception as
`R07_760_L3_TARGET6_INPUT_STOP`.  It occurs before `write_j_checkpoint`, which
explains the eleven authenticated relator deltas and absence of a completed-j
marker/file.

The v5 synthetic post-closure regression deliberately calls the pinned v4
wrapper and requires that exact TypeError.  The identical row then passes v5
after v2 is threaded through:

- `validate_public_j_row(v3, v2, row, summary)`;
- `build_j_checkpoint(v3, v2, ...)`;
- `validate_j_checkpoint(v3, v2, ...)`;
- `write_j_checkpoint(..., v3, v2, ...)`; and
- recursive `load_j_checkpoint_chain(..., v3, v2, ...)`.

### GAP driver receipt rejection

The canonical full receipt legitimately contains

```json
"inherited_prefix_grade":"producer_control_flow_candidate_only"
```

twice: once under `resume_contract` and once under `result`.  The v4 driver
required the global textual count to equal one, so the otherwise bound
INPUT_STOP receipt failed with `receipt envelope`.  V5 requires the
schema-specific count of two and tests both removal and a third occurrence.
Receipt SHA/bytes are checked as one paired producer-log marker, and the timing
ledger separately binds producer-log SHA/bytes and receipt SHA/bytes.

## 3. Completed-j regression receipt

The deterministic certificate records:

```json
{
  "v4_defect_reproduced": true,
  "v4_exception_class": "TypeError",
  "v4_exception_mentions_missing_summary": true,
  "v5_completed_j_validated": true,
  "completed_closure_receipts": 11,
  "terminal_relator": 11,
  "terminal_rank": 11,
  "terminal_state_commitment_sha256": "e6a9402ac1eb9daaaddd3fc844b54fc1dd98761391fddfd92dad76209be04945",
  "terminal_header_public_row_bound": true,
  "binding_mutation_rejected": true,
  "immutable_write_reload_equal": true,
  "manifest_entries": 12,
  "manifest_delta_entries": 11,
  "manifest_j_entries": 1,
  "exact_next_j": 10
}
```

The public row has `nonmember=false`, all eleven closure receipts, the v3 exact
accelerator boundary, and the v5 append-only boundary.  The terminal header is
bound to its closure roster, rank, monomial/dimension/basis data, target/legal
hashes, preceding-j progression, and cumulative state commitment.  A closure
roster mutation is rejected.  Eleven delta files plus one completed-j file are
written immutably, authenticated, reloaded, and included in the manifest.

## 4. Deterministic safe stop

The producer option is

```text
--max-new-relators N, 1 <= N <= 44
```

Only a newly computed closure whose immutable delta was written and
authenticated increments the counter.  Replayed ancestors start the counter
at zero.  For a stop before relator 11, v5 returns claim-free
`UNKNOWN_RESOURCE` immediately after that delta and records the exact next
relator.  At relator 11, it finishes and authenticates the completed-j
checkpoint before returning the resource terminal when the public row is not
a NONMEMBER.  A newly discovered NONMEMBER retains the pre-existing first
terminal rule instead of being hidden by safe stop.

The toy receipts are:

| case | replayed ancestors | new allowance/completed | stop after | exact next |
|---|---:|---:|---|---|
| fresh | 0 | 2 / 2 | j9 r2 | j9 r3 |
| resumed | 2 | 1 / 1 | j9 r3 | j9 r4 |

The resumed state commitment is
`98eb3e27de27abe3328538ed4ce5721be35fe8b7fd9bdd47a13db1e557957093`;
`ancestors_counted_as_new=false` and
`unfinished_relator_inferred=false` are explicit.

The GAP preamble variable defaults to exactly 11:

```gap
D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_MAX_NEW_RELATORS:=11;;
```

Its accepted range is 1--44.  The driver uses an inner producer budget of
19,200 seconds and an outer process timeout of 19,800 seconds, leaving at least
1,800 seconds before the 21,600-second workflow boundary for hashing and
artifact packaging.  The safe-stop counter, not elapsed-time prediction, is
the primary boundary.

## 5. Driver terminal matrix and fail-closed gates

All four synthetic full receipts pass the same structural predicate used by
the production path:

| terminal | required terminal-specific fields | operational result |
|---|---|---|
| `NONMEMBER` | named first nonmember, nonmember row, `safe_stop=false` | accepted; direct checker still mandatory |
| `MEMBER_INCONCLUSIVE` | null first nonmember, exact `[9,10,11,12]`, `safe_stop=false` | accepted as screen survival only |
| `UNKNOWN_RESOURCE` | bounded ASCII stop stage/reason; one safe-stop boolean; authenticated checkpoint/count/exact-next fields when safe stop is true | accepted claim-free |
| `INPUT_STOP` | bounded ASCII stop stage/reason and `safe_stop=false` | accepted claim-free |

The driver requires exactly one producer marker and one matching
`terminal_token`, false global claims with no true widening, the two recovery
booleans, schema-specific inherited-grade multiplicity, complete receipt
SHA/byte binding, manifest count, every checkpoint SHA/path, timing/hash
ledgers, and success sentinel.  Fifteen driver mutations were rejected,
covering extra/missing inherited-grade fields, true global or mathematical
claims, weakened recovery/grade gates, duplicate/mismatched terminals,
receipt-hash and byte mismatches, missing stop diagnostics, malformed MEMBER
and NONMEMBER fields, duplicate producer markers, and a false safe-stop
checkpoint-authentication claim.  The retained delta-chain suite rejected its
original twelve mutations.

## 6. New files and final hashes

| path | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_760_l3_target6_delta_resume_v5.py` | 108142 | `94184831ede05c78d7206e62dbdd5c564daa493330fe1c5e433be2804267652b` |
| `search/d972_r07_760_l3_target6_delta_resume_gha_driver_v5.g` | 29496 | `ff820866983c1d1bc5d0a98bb748d4a7fda4e406b3283e6c6a6ccf817011be20` |
| `search/certs/d972_r07_760_l3_target6_delta_resume_preflight_v5_20260827.json` | 36718 | `76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305` |
| `sol/luna_reply_167_r07_target6_postclosure_recovery_v5.md` | this report | computed after handoff |

The final producer mtime is
`2026-08-27T06:03:37.8898232+09:00`.  It was not touched after the two preflight
generations.  The preflight canonical self digest is
`e23749d4a097b3868c6807cc0a89eb519bb1289f01629e27b8442ff2812d14cd`;
its fixed-binding digest is
`308d557543d14a362374ffc8602c826bcdc077e3538476174af5f4da28ec339f`.
The driver is ASCII/LF-only: non-ASCII bytes = 0, CR bytes = 0, NUL bytes = 0.

## 7. Serial bounded audit record

The authoritative runs used the existing repo-external pinned-input overlay:

```text
%TEMP%\d972_task164_clean_11cbe4b89ff048a8841e48ec5f863fa9
```

This isolates the current unrelated live-tree `provenance/CLAIMS.md` drift:
the pinned input is 66,635 bytes / SHA
`174ddbb50d1579c9373482552759ed2ec822846f1dd83c8d73b13c652ae77f64`,
whereas the live dirty file is 68,363 bytes / SHA
`37325e7e7d734f7619785eb1832a051a4e35bb7409e0adaad413443a13038c00`.
No live user file was reverted or modified.

Producer selftest:

```text
python search/d972_r07_760_l3_target6_delta_resume_v5.py --self-test
R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_SELFTEST_PASS delta_mutations=12 j2_exhaustive=59049 j9_samples=260 j2_relators=11 delta_count=11 final_count=11 payload_bytes=266 toy_next_relator=4 toy_rank=4 postclosure_next_j=10 safe_resumed_new=1 left_warm_speedup=26.375 projection_warm_speedup=2.047 append_only=true exact_replay=true
```

The two final-source preflight runs produced byte-identical output:

```text
R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_DELTA_RESUME_V5_PREFLIGHT_READY grade=CANDIDATE checkpoints=0 sha256=76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305 bytes=36718
R07_760_L3_TARGET6_DELTA_RESUME_V5_PRODUCER_PASS preflight_state=R07_760_L3_TARGET6_DELTA_RESUME_V5_PREFLIGHT_READY grade=CANDIDATE checkpoints=0 sha256=76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305 bytes=36718
PREFLIGHT_BYTE_EQUAL_PASS bytes=36718 sha256=76da0c9f78f3efff305289bb864e25819a722c2362dc2dffb250c98be9244305
```

Final pinned driver selftest:

```text
.\gap.ps1 task167_driver_selftest.g
R07_760_L3_TARGET6_DELTA_RESUME_V5_GHA_DRIVER_PASS mode=selftest producer_processes=1 checker_processes=0 delta_mutations=12 driver_fixture_mutations=15 terminals=4 grade=CANDIDATE
```

The same audit passed with the preamble override `N=3`.  The `N=0` mutation
failed closed with exit code 1 and:

```text
Error, R07 delta resume v5 driver: MAX_NEW_RELATORS range 1..44
```

All Python/GAP runs were serial and bounded.  The inherited cache gate still
checks 59,049 j=2 PC vectors, 10,280 deterministic left-multiplication pairs,
260 deterministic j=9 PC samples, 103 actual j=9 row samples, and all eleven
j=2 relator closures.  No full j=9 closure was run locally.

## 8. Operation and remaining UNKNOWNs

Default first recovery invocation:

```gap
D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_RUN:=true;;
D972_R07_760_L3_TARGET6_DELTA_RESUME_V5_USE_PYTHON3:=true;;
Read("search/d972_r07_760_l3_target6_delta_resume_gha_driver_v5.g");;
QUIT_GAP(0);;
```

All receipts, logs, timing data, hash ledger, sentinel, and fixed checkpoint
directory remain below `ci/out/`, so the existing generic uploader covers
them.  The workflow itself was not changed.

Remaining UNKNOWNs:

- No full v5 GHA run was authorized, so actual j=9 runtime, compression size,
  and successful packaging of a real eleven-relator chain remain UNKNOWN.
- Generic GHA does not download a previous run's artifact automatically.
  Cross-run checkpoint ingress remains operationally blocked pending parent
  Sol authorization; v5 does not claim restart readiness without a preseeded
  complete ancestor chain.
- V5 does not convert a v4 chain into v5.  The incident run's skipped upload
  means its local runner files are not assumed available.
- A resource/input terminal is operationally accepted so artifacts upload; it
  is not a mathematical result.  Fresh NONMEMBER promotion still requires the
  helper-nonshared direct checker.

## 9. Claim boundary

```text
j=9 nonmember=false is producer survival evidence, not an A18 lift
delta checkpoint = resource recovery, not a mathematical result
fresh NONMEMBER = candidate until helper-nonshared direct checker agrees
MEMBER != actual A18 lift
no fake / cofinal lift / Ihara witness declared
```
