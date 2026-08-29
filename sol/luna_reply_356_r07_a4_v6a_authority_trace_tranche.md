# Luna reply 356 - A4/v6a authority-trace tranche

Scope is exactly task356: the v5/v6 files remain frozen; this tranche covers
only task198 authority rows 1--7 and does not claim rows 8--48 or A4
completion.  No Python, Node, GAP, GHA, workflow, git, or network command was
run.  PowerShell was used only for read-only line inspection and SHA/byte
measurement.

## Four permitted outputs

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a4_actual_owner_trace_producer_v1.py` | 43017 | `3b36dd2d59e680c864b5f25c9c5f30027ee41128e3ce7b1bff76201f645cf8b5` |
| `crosscheck/check_d972_r07_a4_actual_owner_trace_checker_v1.py` | 38528 | `d08633af80d7de6e8fbdaaacf2115490256c77616293c33366261faee401a98c` |
| `search/certs/d972_r07_a4_actual_owner_trace_authority_fixture_v1_20260829.json` | 8998 | `4ce506d8d54af17888e3250dffb3f8513068ad2c25c3df6125d1a82581259fe2` |
| `sol/luna_reply_356_r07_a4_v6a_authority_trace_tranche.md` | (this reply) | (not an input pin) |

The fixture is non-synthetic and candidate-only, with `covered_rows` exactly
`[1,2,3,4,5,6,7]`, `remaining_rows` exactly `[8..48]`, and
`full_a4_selftest=false`.  It contains separate producer/checker maps, and
each map has all seven owner, identity-kind, logical-case, ordinary-validator,
stage, exact `{validator,stage,narrow_reason}` and downstream-reseal fields.

## Import and authority graph

Both trace modules import only Python standard-library modules.  The producer
has no import edge to v5/v6, the checker, or any producer module; the checker
has no import edge to v5/v6, the producer, or any checker module.  Producer
physical pins are declared at lines 38--53 and consumed independently by
`authenticate_sources` at lines 521--525; checker pins are declared at lines
40--55 and consumed independently at lines 700--702.  The pins cover the
actual task198 receipt, manifest, both attestations, checker verdict, producer
source, checker source, and GAP driver.  The fixture is loaded and shape/
immutable-input checked by producer lines 534--557 and checker lines 680--702.

The producer baseline is ordinary route lines 488--518, invoked from
`execute` lines 802--814.  The checker baseline is ordinary route lines
445--470, invoked from `run` lines 702--712.  Each baseline emits its own
events before owner reads, parses the actual pinned row/manifest bytes, and
then performs one fresh one-handle baseline byte/SHA recheck before mutation
cases.  No 31-MB owner is reread or reparsed once per row.

## Physical substrate and evidence trace

Producer `Meter`/`EventSink` are lines 87--162; checker `Counter`/`Journal` are
lines 78--142.  Producer one-handle POSIX `O_NOFOLLOW`, bounded read,
`fstat`/pathname identity and nlink/TOCTOU checks are lines 197--260;
checker's independent implementation is lines 175--235.  Windows and a
platform without no-follow support fail closed with typed input refusal.
Producer path admission is lines 276--289 and atomic temporary owner plus
directory fsync is lines 292--316; checker equivalents are lines 246--282.
Canonical sealing is producer lines 327--335 and checker lines 304--312.

The ordinary baseline/row event extraction is producer lines 488--518 and
checker lines 445--470.  Full identity comparison is producer
`_same_identity`/`reconfirm_baseline` lines 596--617 and checker lines
522--543.  Stable v298 projection (no device, inode, mtime, random temporary
path, or empty-bytes digest) is producer lines 620--664 and checker lines
471--519.  Fixture ordinary-validator/stage is checked against an actually
entered event only after the ordinary call returns: producer lines 673--697,
checker lines 546--574.  `terminal_count` is incremented from the event route,
not hard-coded.

`MUTATION_ACCEPTED` is declared producer line 83 and checker line 74.  The
hard accepted failure is deliberately outside the only narrow rejection catch
at producer lines 753--799 and checker lines 641--677.

## Seven physical owner rows

The producer constructor is `run_mutation` lines 705--793 and checker
constructor is `run_case` lines 590--677.  In both sides, the local manifest /
receipt is atomically written outside the repository, ordinary route is then
called, and only the registered narrow rejection is caught.

| row | actual owner and physical construction | producer ordinary trace | checker ordinary trace | exact first reason |
|---:|---|---|---|---|
| 1 `per_layer_ordinal` | canonical task198 receipt clone; increment `rows[0].ordinal`; reseal receipt and local manifest | construction P730--735; row validator P467--468 | construction C616--634 plus receipt alteration C577--580; row validator C424--425 | P `producer:authority:layer_ordinal`; C `checker:authority:layer_ordinal` |
| 2 `authority_binding` | actual manifest clone; set `accepted=false`; reseal only manifest | P715--720, manifest event/validator P501--504 | C599--605, manifest event/validator C456--459 | P `producer:authority:manifest_acceptance`; C `checker:authority:manifest_acceptance` |
| 3 `canonical_input_bytes` | actual receipt bytes clone; flip one physical byte; leave baseline binding unchanged | P722--725, receipt identity/transport P505--515 | C606--613, receipt identity/transport C460--469 | P `producer:transport:receipt_sha256`; C `checker:transport:receipt_sha256` |
| 4 `resolved_path_traversal` | change the actual receipt path to an outside/missing lexical owner; no fake empty digest | P726--729 and resolver P276--289 | C614--620 and resolver C246--255 | P `producer:path:registered_containment`; C `checker:path:registered_containment` |
| 5 `normal_generation_proof` | canonical receipt clone; increment `Gamma_cayley_edge_count`; reseal downstream receipt/manifest | P730--737, validator P469--471 | C616--634 / alteration C580--581, validator C426--428 | P `producer:authority:normal_generation_proof`; C `checker:authority:normal_generation_proof` |
| 6 `bridge_typed_occurrence_ledger` | canonical receipt clone; change first bridge block; reseal downstream receipt/manifest | P730--739, validator P472--474 | C616--634 / alteration C582--583, validator C429--431 | P `producer:authority:bridge_occurrence_ledger`; C `checker:authority:bridge_occurrence_ledger` |
| 7 `evaluator_abi_canary` | canonical receipt clone; change first coordinate width; reseal downstream receipt/manifest | P730--742, validator P475--477 | C616--634 / alteration C584--585, validator C432--434 | P `producer:authority:evaluator_abi_canary`; C `checker:authority:evaluator_abi_canary` |

For rows 1 and 5--7, the changed receipt passes its locally resealed
transport manifest and reaches the semantic validator.  Row 2 reaches the
manifest validator.  Row 3 stops at the truthful receipt transport binding;
row 4 stops in the ordinary path resolver before any read.  The fixture's
reseal lists are checked exactly, and the producer/checker reasons and event
ledgers are independently generated rather than copied from one another.

## Static caps versus measurements

Both registries are explicit: `opened_bytes=250000000`,
`temporary_bytes=250000000`, `canonical_bytes=500000000`, `opens=256`,
`writes=256`, `events=10000`, and `mutations=7` (producer lines 87--115,
checker lines 78--104).  Static execute-route opened-byte accounting is
`315289 + 2*(31017244+2722) + sum(R_mutant[1,3,5,6,7]) +
sum(M_mutant[1,2,5,6,7])`, before any optional output; the R/M terms are the
actual bounded physical mutant reads (not guessed baseline sizes).  Static
temporary-owner accounting is the corresponding
`sum(R_mutant[1,3,5,6,7]) + sum(M_mutant[1,2,5,6,7])` bounded envelope sum,
checked before each allocation.
The ordinary route has 20 baseline/recheck/source opens and 10 mutant writes;
its event upper bound is 97 and mutation count is exactly 7.  These are static
cap formulas, not runtime measurements.  Every runtime/public resource field
is `UNEXECUTED`; no host/RSS/time result is claimed.

No driver or workflow was added.  Fresh Sol(max) audit and later integration
remain required; rows 8--48, the frozen v5/v6 algebra/DAG core, and the full
A4 SELFTEST are intentionally outside this tranche.

ROWS 1--7 PRODUCER TRACE:        IMPLEMENTED
ROWS 1--7 CHECKER TRACE:         IMPLEMENTED
V297 EVENT/IDENTITY SUBSTRATE:   IMPLEMENTED
STATIC TRANCHE:                  IMPLEMENTED
EXECUTION / GHA:                 UNEXECUTED
FULL 48x2 SELFTEST:              INCOMPLETE
SOL(MAX) AUDIT REQUIRED:         YES
ACTUAL A4:                       remains 1/3
LIFT / FAKE / IHARA:             NONE
TASK356_R07_A4_V6A_AUTHORITY_TRACE_TRANCHE
