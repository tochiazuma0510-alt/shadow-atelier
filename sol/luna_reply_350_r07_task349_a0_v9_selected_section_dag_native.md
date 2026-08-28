# Luna reply — task350 / v9 selected-section DAG-native audit

The complete v9 mail and every numbered section were read before editing.
All listed v7/v8 sources, proofs v265/v275--v279/v284/v287, task176 receipt,
manifest, accepted checker verdict, recovery manifest, and pinned q3/E4/joint/
old owners were read in full.  No Python, Node, GAP, GHA, workflow, git, or
network execution was performed.

## Authorized v9 outputs

Only the five authorized v9 paths were created/changed:

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_v9.py` | 144091 | `7dd977b009dc3b3b2946efe569d5eb78eaf46490f875af7117471d25e69e5199` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v9.py` | 116223 | `562b1fd377c436e212199e23edf987aa418bcdb47262344c71e26c375ef05ae1` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v9.g` | 12580 | `b2f78a9161d2caccbe4326640c6c2369719f7414484b91e4cfb8b27ab4f8f583` |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v9_20260829.json` | 3336 | `c60ba21b577ad3f4475896033078a24028e26fcfed796989a10c0d666003ff64` |

The driver pins all four task176 owners exactly at the Section 3 sizes and
SHA-256 values.  The v9 fixture adds the complete selected-correction
mutation roster.

## Implemented static repairs

* v9 schemas/terminals/paths are separated from v8.  SELFTEST and PRODUCTION
  remain distinct, and PRODUCTION requires a sealed SELFTEST receipt.
* The earlier-pivot triangular gate, all-pivot uniqueness gate, exact
  `1,011,460` A*C contributions, and exact `289,774` support inspections are
  retained.  IPC frames carry disjoint descriptor/support slices with global
  ordinal intervals and slice digests.
* Actual rows now return/store `pivot_node_id`; no `pivot_expression`,
  `new_expressions`, or actual-row `ancestry.expand` path remains.  DAG node,
  sparse operation, expansion, and serialized-byte counters are separate.
  Checkpoints store DAG nodes, pivot bindings, normalized rows, and node ids
  rather than a flat formal solution.  Restore injects authenticated stored
  rows and node ids instead of replaying prior actual provenance.
* Checkpoint ownership is one exact output sidecar.  Startup stale-rejects it;
  subsequent clean writes use same-directory temporary/fsync/replace/fsync.
  No versioned checkpoint siblings are generated.
* Sources and task176 authorities use bounded no-follow physical reads with
  opened-before/opened-after/path-after identity checks.  Task176 compressed
  owners enforce strict canonical base64, bounded zlib, exact lengths, stream
  termination, compressed/raw hashes, coordinate widths (40-byte E3 and
  154-byte E4), Q0 parent-letter conventions, and Gamma record-word count 26.
* The checker has an independent task176 authority decoder and selected Q0 and
  Gamma parent-walk owner.  The producer's Gamma value is now explicitly
  named `gamma_full_state_hex`; it is not mislabeled as the 970-byte projected
  task176 row.

## First exact blocking owner/API

The strict `crosscheck/check_d972_r07_history_free_positive_fast_resume_v9.py:
validate_task176_authority` gate finds that the frozen task176 receipt's
`self_digest_sha256` is `f8f0ce...b237...`, while the recovery manifest records
`f8f0ce...b34f...` for its accepted receipt.  The v9 checker correctly rejects
this inconsistent cross-owner binding rather than accepting a digest-only
substitution.  Independently of that frozen mismatch,
`reconstruct_task176_selected` is not yet a complete v287 semantic replay: it
does not replay the ten marked-generator coordinate permutations, reconstruct
the exact 970-byte Gamma projection, solve every K=0 `a^-1*target` fibre and
least `(qid,gid)` base, or bind the complete kernel word/completion.  Therefore
the literal COMMON and authenticated-resume traces are not complete.

## Static trace index

* Fresh production and the first boundary slice: producer `main` around
  2580--2710, `build_triangular` around 800--900, and
  `PersistentBoundaryOwner.run_epoch` around 1170--1260.
* Boundary ACTIVE, Q0-LATE, correction ACTIVE, COMMON: `Search.run` around
  1980--2035 and checker `validate_common` around 1360--1450.
* Task176 authentication/decode/walk: checker
  `read_owner_bytes`, `validate_task176_authority`,
  `decode_task176_owners`, `task176_parent_walk`, and
  `reconstruct_task176_selected` around 130--300 and 1090--1160.
* DAG/reducer/checkpoint/restore: producer `FormalReducer` around 650--770,
  `Search.checkpoint_body`/`write_checkpoint` around 1670--1750,
  `restore_checkpoint` around 2070--2180, and prepool checkpoint around
  2520--2580.
* UNKNOWN and physical transport: producer `read_physical_once`,
  `read_bounded_json`, `require_selftest_identity`, and resource handler;
  checker `read_owner_bytes`, `validate_unknown`, and
  `validate_checkpoint_transport`.
* Driver stale/output/sentinel routing: v9 driver `D342Pins`, output roster,
  generated extraction shell, and terminal case around lines 1--185.

All formula counts above are static contract values, not runtime measurements;
all runtime/RSS observations are `UNEXECUTED`.  No separator, exhaustion,
nonmembership, lift, fake certificate, or Ihara witness is claimed.

IMPLEMENTATION:                  BLOCKED
SELFTEST / PRODUCTION:           UNEXECUTED
FROZEN INPUTS:                   BLOCKED
FRESH SEARCH ROUTE:              BLOCKED
AUTHENTICATED RESUME ROUTE:      BLOCKED
ACTUAL A0 COMMON + CHECKER:      0/1
SEPARATOR / NEGATIVE CLAIM:      FORBIDDEN
LIFT / FAKE / IHARA:             NONE
