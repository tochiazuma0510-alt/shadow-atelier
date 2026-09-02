# Sol Reply 563 — narrow audit of first-grade merge hot-loop v4

Role: Sol(max), mathematical/static auditor. I read every listed input in full
and audited only the v3-to-v4 merge-hot-loop delta requested by Task563. I did
not edit producer/checker code, run a real phase, access production state, use
git/GHA, run parallel Python, or add tests. The result is PASS: the optimization
is semantics-preserving, retains the v3 state contract, and is correctly bound
to the versioned v4 producer/checker pair.

## 1. Complete scope and receipts

The frozen inputs authenticate as follows.

| input | bytes | SHA-256 |
|---|---:|---|
| `sol/luna_task_562_r07_a0_first_grade_merge_hotloop_v4.md` | 5,845 | `be22958cab0748b1dc6f17f0e88e25197e45affbc0a510253a489142abc12653` |
| `sol/luna_reply_562_r07_a0_first_grade_merge_hotloop_v4.md` | 8,049 | `3a719c2d77bf0683ec6f16a23b6ffce7ca15686af392d2f275fa276a968bdf0c` |
| `search/d972_r07_a0_first_rung_grade1_v3.py` | 138,202 | `bf872b30149e1351762b243d590d7a1f876e048b92a053d8f9c17bba5c45bcff` |
| `search/check_d972_r07_a0_first_rung_grade1_v3.py` | 69,193 | `67f56ee92aea7e17ce88303657ca519ee9539269eef44e6e5550da63d6a4a012` |
| `search/d972_r07_a0_first_rung_grade1_v4.py` | 144,552 | `1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4` |
| `search/check_d972_r07_a0_first_rung_grade1_v4.py` | 69,184 | `ffd78b41fc9f7a1f59925eb8f07db7278b704c3580bb7e8fa3a586e85db9fe06` |
| `sol/sol_reply_560_audit_r07_a0_first_rung_grade1_engine_v3.md` | 10,225 | `5ba42f2aadcf216a75df298d05657ce3fff27bbfd5c40226e6fcf2e7cee4ed64` |

These agree with the Task562 report and the frozen Task560 v3 receipts. The
production certificate
`search/certs/d972_r07_a0_first_rung_grade1_v4.json` was absent before and
after the bounded checks.

## 2. Exact semantic diff

The complete producer comparison has 89 top-level function/class blocks in
both versions, with no added or removed top-level block. Exactly four common
blocks differ: `PackedEchelon`, `run_merge_core`,
`install_or_validate_terminal_certificate`, and `phase_fixture`. Outside
those blocks the only production-source differences are the Task562 docstring
and the explicit comment explaining retention of the v3 schema.

### 2.1 Monotone packed-byte cursor

The old and new reducers can be compared inductively at each loop head. They
start from identical copied packed bytes and cursor zero. In v3,
`mask/any/argmax` selects the least nonzero byte at or after the cursor. In v4,
the cursor advances across exactly those zero bytes and stops at the same
byte. Both then use the same `_PACKED_FIRST` entry, the same actual trit lead,
the same `lead_to_pivot` lookup and coefficient, and the same full-row
`_PACKED_AXPY` table. A missing pivot stops both on the identical remainder;
an existing pivot appends the identical `[pivot, coefficient]` pair.

After elimination v3 assigns `cursor = byte_index`; v4 deliberately leaves
the cursor on that byte. Thus both revisit the current byte. If cancellation
reveals a later nonzero trit in the same packed byte, it is selected next and
cannot be skipped. If the byte becomes zero, v4 advances to exactly the byte
which v3's next suffix search would select. Exhaustion also gives the same
zero remainder and ordered expression.

Freshly accepted v4 rows use the first nonzero trit of the reduced remainder,
normalize its coefficient to one, and therefore have zero coordinates before
their declared lead. Exact sealed v3 block rows have the same property because
they were produced by the byte-identical v3 acceptance tail. `from_bytes`
preserves their packed bytes and insertion-order leads, rejects duplicate
leads, and checks coefficient one at every declared pivot. V4 retains the
full-row AXPY, so it does not introduce the stronger prefix assumption that a
suffix-only AXPY would have required. Consequently both freshly inserted rows
and authenticated v3-loaded rows follow the same first-nonzero reduction
sequence, including nonmonotone pivot IDs.

### 2.2 Acceptance factoring and lower-first merge

`_accept_remainder` is the former post-`reduce_packed` portion of `insert`
verbatim: the dependent record, first nonzero byte/trit, original leading
coefficient, scale, normalized row copy, insertion-order pivot ID,
lead-sorted auxiliary index, and returned dictionary are unchanged. Ordinary
`insert` still packs as before, reduces once, and passes that exact pair to the
helper.

In the lower-first merge, v3 first computed
`remainder, reductions = lower_owner.reduce_packed(pack_trits(physical_lower))`
and, when the remainder was nonzero, immediately invoked
`lower_owner.insert(physical_lower)`, repeating the same reduction before any
owner mutation. V4 passes the already computed pair to `_accept_remainder`.
Since the owner and input are unchanged between the two old reductions, the
accepted row, pivot ID, scale, lower/grade pairing, physical roster entry and
lower DAG expression are exactly the same. The existing agreement guard on
`accepted` and `reductions` remains.

### 2.3 Remaining producer delta and exclusions

The default public certificate path alone changes from the v3 filename to
`search/certs/d972_r07_a0_first_rung_grade1_v4.json`. The remaining added
producer code is local to `phase_fixture`: a tiny copy of the frozen v3
reducer and its deterministic equivalence cases. It is unreachable from
`--merge` and every other production phase.

All affine/Fourier action and accumulation, row construction and traversal,
aggregation, dimensions, pivot map/IDs, physical roster, DAG ancestry,
terminal membership test, separating dual, literal expansion, direct replay,
and next-degree residual functions are byte-identical top-level blocks. There
is no RREF, batch/reordered elimination, new split, or mathematical shortcut.

## 3. V3 state and v4 certificate/checker compatibility

Both v4 files deliberately retain

```python
SCHEMA = "d972.r07.a0.first-rung-grade1.v3"
STATE_SCHEMA = SCHEMA + ".state"
```

The state reader, prepare/block/merge validators, fixed dimensions, input
pins, HEAD/body canonicalization, blob receipts, and phase CLI are unchanged.
Therefore the exact content-addressed v3 prepare state and four v3 block
states are accepted directly; neither their bodies nor their blob contract is
rewritten. Only `--merge <state-dir>` over those five saved phases is
authorized by this audit. Rebuilding prepare or blocks is outside the recovery
authorization.

The certificate builder remains complete and now obtains
`producer_sha256` from the actual v4 file, whose digest is
`1fb4b29691f448782e7f7f2e2282e7067282bc619fb34b7214089c5a73e24dc4`.
The default producer and checker paths both name the v4 public certificate.
The certificate/state object schema intentionally remains on the v3
compatibility contract.

The complete checker diff contains only four changes: its version docstring,
the pinned producer digest, the producer filename checked by `pins()`, and the
public certificate filename. Every independent algebra, validator, complete
certificate equality test, MEMBER replay, and NONMEMBER fibre/dual check is
otherwise byte-identical to v3. Its pin equals the frozen v4 producer digest.
It does not import the producer or share the new reducer/helper; reading the
producer bytes solely to enforce the hash pin is not a code import.

## 4. Bounded checks and performance relevance

Only the prescribed commands were run, serially, with bytecode redirected to
`%TEMP%\task563_pycache`.

1. `$task563Cache = Join-Path $env:TEMP 'task563_pycache'; $env:PYTHONPYCACHEPREFIX = $task563Cache; python -B -m py_compile search/d972_r07_a0_first_rung_grade1_v4.py search/check_d972_r07_a0_first_rung_grade1_v4.py`

   Exit 0, no stdout/stderr, outer wall `0.3074591 s`.

2. `$task563Cache = Join-Path $env:TEMP 'task563_pycache'; $env:PYTHONPYCACHEPREFIX = $task563Cache; python -B -u search/d972_r07_a0_first_rung_grade1_v4.py --fixture`

   Exit 0, outer wall `1.243019 s`; exact stdout:

```json
{"block_ranks": [1, 1, 1, 1], "certificate_recovery": "PASS", "elapsed_seconds": 0.3607120999949984, "fixture": "PASS", "merge_sha256": "6dffb93678b81514a338e4b020a3f7eecaa8d148296ff392e79e2027c0f9734a", "nonmonotone_leads": [5, 3], "packet_projector_ancestry": "PASS", "physical_rank": 4, "reducer_equivalence": {"cases": 6, "dependent": "REJECTED", "status": "PASS"}, "semantic_mutations_rejected": 3, "state_validators": "PASS", "terminal": "FIXTURE_MEMBER", "v443_actor_accumulation": "PASS"}
```

3. `$task563Cache = Join-Path $env:TEMP 'task563_pycache'; $env:PYTHONPYCACHEPREFIX = $task563Cache; python -B -u search/check_d972_r07_a0_first_rung_grade1_v4.py --fixture`

   Exit 0, outer wall `0.8981846 s`; exact stdout:

```json
{"canonical_terms": 2622, "fixture": "PASS", "mutations_rejected": 3, "pinned_inputs": 18, "projectors": 16, "raw_terms": 3936, "truncated_origin_reduction": "REJECTED", "v443_actor_accumulation": "PASS"}
```

The reached six-case reducer gate covers a zero row, a missing pivot,
multiple pivots in one packed byte, nonmonotone insertion leads `[5,3]`, an
accepted coefficient-two/scale-two row, and a dependent insertion. Against
the local frozen-v3 reference it compares exact packed remainder bytes and
ordered reductions on each reduction path; insert cases additionally compare
the complete acceptance record, lead list, and stored matrix bytes after each
operation. The dependent case reaches same-byte revisit and reduces in actual
lead order as `[[1,1],[0,2],[2,2]]`, then is rejected identically. The
coefficient-two and dependent cases reach `_accept_remainder` directly, so the
lower-first factoring branch is exercised as well as ordinary `insert`.

This change is qualitatively load-bearing for the observed merge. V3 allocated
and scanned the remaining packed suffix with `!= 0`, `any`, and `argmax` after
every pivot elimination; v4's byte cursor is monotone and avoids that repeated
suffix work. Each newly independent physical-lower row also avoids an entire
duplicate lower reduction, including its AXPYs. The full-row AXPY cost remains,
so this audit makes no runtime promise and requests no further optimization or
profiling.

## 5. Verdict and claim boundary

The exact v4 pair passes this bounded release audit. It authorizes one
parent-owned GHA recovery `--merge` using the already saved authenticated v3
prepare and four block artifacts, followed by the exact v4 checker. It does
not authorize rebuilding those phases, and neither this audit nor the fixture
decides or promotes a mathematical terminal.

FIRST_GRADE_MERGE_V4_PASS
FIRST RUNG: 0/6 GRADES DECIDED UNTIL A PRODUCTION CHECKER TERMINATES
A0: 0/1 ACTUAL
ORDER-54,432 / FULL-Q0 / COMMON / COMPATIBLE LIFT / FAKE / IHARA: NOT DECLARED
verified=false
