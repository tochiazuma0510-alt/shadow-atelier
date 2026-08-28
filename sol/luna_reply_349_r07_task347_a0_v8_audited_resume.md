# Luna reply — task349 / task347 audit / v8

## Scope and authority

The complete task mail was read in numbered order, including the task347
first-stop findings and the subsequent mandatory corrections.  No
SELFTEST, PRODUCTION, Python, Node, GAP, workflow, network, or git execution
was performed.  This is a static implementation/audit report only.

The five permitted outputs are the v8 producer, checker, driver, frozen
SELFTEST fixture, and this reply.  The fixture is unchanged except for its
versioned v8 schema pin.

## Implemented static repairs

* Fresh PRODUCTION no longer invokes the real-owner SELFTEST.  It requires a
  separately sealed v8 SELFTEST receipt; SELFTEST and PRODUCTION have distinct
  routes and terminals.
* The triangular product gate uses chronological `seen_pivots` for the
  earlier-pivot condition, retains an all-pivot uniqueness set, preserves
  `min(P_j)=pivot_j` and coefficient one, and charges every support inspection
  (the declared valid total is 289,774; no short-circuit predicate is used).
* Reduction carries hash-consed DAG node ids internally; target/remainder and
  dual derivation are reused, with expansion confined to the selected result
  and bounded checkpoint/canary boundaries.  The pivot-2 actual-row
  normalization no longer receives a second inverse scale.
* Boundary IPC now constructs disjoint per-worker descriptor/support slices,
  binds each slice to an exact digest and global ordinal interval, and records
  explicit disjoint/coverage metadata.  The parent private support is retained
  only for ACTIVE winner reconstruction.
* Pinned source reads and selftest identity reads use bounded no-follow fd
  ownership and compare opened-before/opened-after/path-after
  `(dev,ino,size,mtime,nlink)` identities.  Raw ZIP publication remains
  temp-first: size and digest are checked before replace and directory fsync.
* Resource-stop handling does not dereference unbuilt owners; clean-owner
  checks precede checkpoint serialization.  Checkpoint writes are pre-sized,
  atomic, and phase-versioned after the first checkpoint.  Resume manifest and
  checkpoint probes use bounded physical reads with bytes/SHA binding.
* COMMON binds selected old `o:NNNN` records to one authenticated raw source
  owner, separate from the producer receipt bytes.  The checker performs the
  existing selected correction word/formula/fibre/schedule replay and checks
  the producer's Q0/Gamma state bindings.

## Remaining load-bearing blocker

The exact task347 §F7 requirement is not yet met: checker
`validate_correction_provenance` still validates producer-supplied Q0/Gamma
hex/hash and membership/schedule fields rather than independently rebuilding
the selected Q0 state, Gamma state, membership, section word, K=0 fibre or
K!=0 schedule, and heavy-owner identity from selected inputs.  In addition,
the formal checkpoint public shape still carries legacy flat
`pivot_expression` records for new rows and the formal-entry counter is not a
fully separate DAG-node/support-allocation meter.  Consequently no literal
static trace establishes the requested authenticated resume contract.

## Frozen identities (static)

| output | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_history_free_positive_fast_resume_v8.py` | 140467 | `8499a50d5fc05a5d850de0d4a1ea80d3ddbc0a37c2cfd8b8a28cb3c6f95d5a0e` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v8.py` | 102497 | `219c42baf0829c41e6f7cdb9376693632162fdd9ca0828e311c7396d80795262` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v8.g` | 11811 | `6a916246edb62b15a1142057f114cabc04452d6141f7d71e54548ad606ffffa6` |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v8_20260829.json` | 2784 | `a96d7e400b5f71a03975b9d223b98fe6cc6c22ef8e17fe59f0eac07f4bc7e641` |

The v8 fixture pin is `2784` bytes and the fixture SHA above.  The producer
and checker pins in the driver/checker were refreshed to the identities above.

IMPLEMENTATION:                  BLOCKED
SELFTEST / PRODUCTION:           UNEXECUTED
FROZEN INPUTS:                   PASS
FRESH SEARCH ROUTE:              BLOCKED
AUTHENTICATED RESUME ROUTE:      BLOCKED
ACTUAL A0 COMMON + CHECKER:      0/1
SEPARATOR / NEGATIVE CLAIM:      FORBIDDEN
LIFT / FAKE / IHARA:             NONE
