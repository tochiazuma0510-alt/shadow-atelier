# Task380 R07 A0/v12c bounded complete repair

## Scope and disposition

I completed the researcher-authorized fresh Sol(max) A0 implementation repair.  The five machine owners are versioned v12c owners; frozen v12b owners were not edited.  The authority graph is one-way:

`immutable authorities -> canonical P0/fixture -> producer/checker -> driver`.

The mode is only `SELFTEST_BOOTSTRAP`.  This delivery makes no production/resume, common-word, actual-A0-numerator, lift, fake, or Ihara claim.  The candidate and every mutation suite remain unexecuted; the findings below are static construction/read-through findings requiring a fresh independent static code/performance audit.

## Physical owner identities

| owner | physical bytes | physical SHA-256 |
|---|---:|---|
| `ci/in/d972_r07_history_free_positive_fast_resume_selftest_bootstrap_v12c.manifest.v1.json` | 11,476 | `24fbc1f9d7a7be3c96e1a56d4eb97d0aa5ccca9233f1e552088e9848bc081d74` |
| `search/d972_r07_history_free_positive_fast_resume_v12c.py` | 342,630 | `fbfcd4f82cccb7a6772270bf755852e94d5d98a5059994797cacc0a8e3feec92` |
| `crosscheck/check_d972_r07_history_free_positive_fast_resume_v12c.py` | 298,317 | `859cb6e9e1b9c7f74b39014cbdb1accdf54e1a692d5ce962d86f7314e3bb2c44` |
| `search/d972_r07_history_free_positive_fast_resume_gha_driver_v12c.g` | 43,559 | `56867f847d3242f03bd2763087d58df1985a8634b6260efe2cb91abc23b29c8e` |
| `search/certs/d972_r07_history_free_positive_fast_resume_selftest_v12c_20260829.json` | 22,785 | `6fb7fe92c3cf93f54e44f9f26c3e920d131dbc626fc826d8b5bb4745bf67c8ec` |
| `sol/sol_reply_380_r07_a0_v12c_bounded_complete_repair.md` | 00016269 | supplied in the immutable parent delivery envelope after this file is frozen |

The reply cannot contain its own physical SHA-256: inserting that digest changes the bytes being hashed, so an ordinary SHA-256 fixed point would be required.  Its exact physical byte count is embedded above without changing field width, and its final exact physical SHA-256 is supplied out-of-band in the parent delivery envelope after the file is frozen.  This is the only non-self-contained identity row; the other five identities above are final and are pinned downstream at driver lines 33--37.

## Root seals and canonical physical proof

- P0 is one compact ASCII JSON line plus exactly one LF: 11,387 canonical body bytes plus its 88-byte `,"self_digest_sha256":"<64 hex>"` member plus one LF, totaling 11,476 bytes.  Removing exactly that one member and hashing the remaining compact ASCII body gives `39b483cf2df56aa6148bac3026c16c7f4e68950c8ff417543e84b5abaaf5f775`.
- The fixture is one compact ASCII JSON line plus exactly one LF: 22,696 canonical body bytes plus the same 88-byte self-seal member plus one LF, totaling 22,785 bytes.  Removing exactly that one member and hashing the remaining compact ASCII body gives `5569881a6e79c0ad45a794d501f2f0e3a7625aee7f2032f42694ba6d2441256d`.
- Read-only physical inspection found no BOM, CR, or non-ASCII byte in any of the five machine owners; every owner ends in exactly one LF.  P0 and fixture each contain exactly one LF and equal compact `sort_keys=True, ensure_ascii=True, separators=(",", ":")` serialization plus LF byte for byte.
- P0 line 1 has `sources={}` and a 30-row frozen-authority inventory with 30 distinct paths.  The fixture authority occurs exactly once.  The fixture line 1 has the complete 75-case contract `8+13+30+7+11+4+2` and the required measured identity/event/physical-digest fields.
- Producer lines 3287--3288 and checker line 1210 require raw physical equality to canonical JSON plus one LF before semantic use.  The driver repeats canonical raw equality before artifact acceptance.  Ordinary-reader negative owners cover whitespace, key order, newline, and canonical-byte changes with registered first reasons.

## F1 -- canonical graph repaired

- P0 and fixture are new physically canonical roots with the seals proved above; neither pins producer or checker.  Producer/checker pin only P0 and fixture, while driver lines 33--37 pin all four upstream final physical identities.
- Producer lines 6180--6193 enforce empty P0 `sources`, 30 unique frozen paths, exact ancestry, and one fixture occurrence.  Checker lines 3867--3975 independently enforce the same acyclic and unique-path inventory.  Exact fixture pins are enforced at producer line 6316 and checker line 4004.
- Canonical read rejection is on the ordinary reader path, not a test-only predicate.  No v12b physical hash is retained as a v12c owner hash, and no alias or partial digest is accepted.

## F2 -- real bounded mutation owners repaired

- Producer `BoundedOwnerDelta` starts at line 354 and checker `CheckerBoundedOwnerDelta` at line 458.  They authenticate one immutable baseline and expose owner-local typed replacements; they do not canonicalize/parse or deepcopy an entire frame/R owner per case.
- Producer `TriangularDeltaFrame` at line 3379 and checker counterpart at line 4300 replace only the required sparse chronological records.  Selected, boundary, positive, phase, and phase-positive cases copy the smallest changed subowner.  Nested positive routes reuse the authenticated selected baseline rather than rerunning the unrelated full selected validation.
- Real W4 normal, timeout, death, partial, and blocked-send paths are constructed in producer `process_selftest` at lines 5092--5187 and checker process paths at lines 2214--2284.  Both sides use four workers; blocked-send is a real pipe/channel state, not a one-child or W2 surrogate.
- Producer physical11 begins at line 5596 and mutates the actual constructed R owner and publication binding.  It is no longer a miniature positive frame.
- Producer complete-ledger construction begins at line 5942 and checker construction/comparison at lines 5225 and 5271.  Both require exactly 75 entries in group order `8+13+30+7+11+4+2`, including both phase-positive cases, measured owner identities, event traces, and physical digests.  Exact registered first reasons, narrow catches, `MutationAccepted` hard failures, and false conclusion flags are retained.

## F3 -- charge-before-allocation and heavy-owner reuse repaired

- Producer lines 2683--2708 reserve both cumulative and live pc-cache entry tokens before `pc.mul`, bytes conversion, or insertion.  The source cap is 131,072 entries; duplicates and failures release their token, and final cache release occurs at the last consumer.
- Each process constructs exactly two full Gamma values: one 4,814-byte canary and the actual selected owner.  Producer calls are at lines 2927 and 3678; the selected immutable bytes are reused at lines 3855--3858.  Checker creates the canary at lines 1555--1557 and the selected cached owner through lines 1448--1461/3028; later checks reuse `_selected_full_gamma` at lines 2928--2940.
- The projected Gamma owner is one 243-by-970-byte owner (`235,710` bytes), not repeated full-value materialization.  Checker recurrence data are cached once at line 2553; selected Gamma/K0 comparisons consume cached canary/selected owners.
- K0 state/index owners and the selected roster are constructed once per process and reused.  Producer stable K0 construction begins at line 2243 and heavy owner construction at line 2888.  Checker K0 store construction begins at line 2397; selected coordinate groups and roster are cached once at lines 2522--2734.
- Producer parent/letter compact digests stream at lines 2223 and 2426.  Checker streams the corresponding authenticated compact owners at line 964.  No 1,469,664-element Python integer list exists solely for hashing.
- Remaining full passes are intentionally one-per-owner passes: Q0 compact state/store construction and digest; one K0 table build plus one slot/state digest; one projected-Gamma construction/digest; one selected-roster scan; producer raw authority parse; and checker independent raw-column replay.  Mutation suites operate on bounded views and do not add full Gamma, K0, coordinate, raw-frame, or R clones.

## F4 -- strict deadline coverage repaired

- Producer `ElapsedSignalDeadline` begins at line 489 and installs before material authority construction; checker equivalent begins at line 172.  Linux `SIGALRM` is mandatory, prior timers are restored after subtracting real elapsed time, and signal/setup/restore/cleanup errors fail closed.
- Deadline/meter checks occur inside material loops, including producer K0 state/probe loops at lines 2285/2296, pc-cache construction at lines 2683--2708, parent/letter streaming at lines 2223/2426, raw/selected/mutation loops, and checker K0 build/lookup loops at lines 2437/2458, raw chronological replay at line 3239, selected qid/gid/coordinate loops, delta construction/validation, streaming hashes, and cleanup loops.
- Internal/external pairs retain strict 300-second cleanup margins: producer `9600 < 9900`, checker `5400 < 5700`, artifact `1200 < 1500`.  Driver lines 219, 223, and 284 apply those external limits.  The external sum is `9900+5700+1500=17100 < 18000` outer, leaving 900 seconds, and `18000 < 21600` workflow, leaving 3,600 seconds for setup/cleanup/upload.

## F5 -- live memory and output reservation repaired

The hard Linux address-space ceiling is installed and read back before material authority construction at producer lines 521--534 and checker lines 202 onward.  It is `5,700,000,000` bytes.  Sampled RSS fields are diagnostics only and are explicitly not used as allocation proof.

Producer simultaneous live formula:

`3,564,038,019 fixed byte owners + 2,000,000*96 sparse-map + 2,000,000*128 ancestry + 300,000,000 bounded Q0 byte-record/index headers = 4,312,038,019 bytes`.

The fixed-owner source lifetimes include ten Q0 typed stores `1,469,664*(5*40+5*154)=1,425,574,080`, Q0 state payload `1,469,664*36=52,907,904`, selected maximum K0 `1,469,664*154+4,194,304*4=243,105,472`, projected Gamma `243*970=235,710`, raw bytearray/immutable-bytes/ASCII/DOM overlap bounded by `4*86,368,039=345,472,156`, and the pre-reserved output token `536,870,912`.  Those named owners subtotal `2,604,166,234`; the remaining `959,871,785` bytes of the fixed term cover compact typed containers, loaded authority modules, bounded headers, and IPC/output fragments.  Adding the `192,000,000`, `256,000,000`, and `300,000,000` bounded sparse/DAG/Q0 header terms gives the declared peak.  Address-space margin is `5,700,000,000-4,312,038,019=1,387,961,981` bytes.

Checker simultaneous live formula:

`2,616,842,912 immutable reconstruction/maps/DAG + 536,870,912 full V output token = 3,153,713,824 bytes`.

Named live owners include raw bytearray/bytes/ASCII/DOM at at most `4*86,368,039=345,472,156`, decoded task176 stream `60,492,663`, selected K0 `243,105,472`, and V token `536,870,912`; the bounded reconstruction/map/DAG/container envelope supplies the remainder of the first term.  Address-space margin is `5,700,000,000-3,153,713,824=2,546,286,176` bytes.

Producer line 6358 and checker line 5556 reserve the full `536,870,912`-byte R/V output cap before constructing the corresponding output.  Actual compact encoded size is rechecked; unused reservation is released only after durable publication or rollback.  Raw bytearray, immutable raw bytes, ASCII fragments, DOM, typed arrays, sparse dict/maps, DAG, IPC buffers, and serialization buffers have cardinality/width caps and last-consumer releases.  Mutation DOMs are sequential.  The four fault children on each side are forked before heavy material ownership, so the simultaneous-child peak is four but there is no four-way heavy COW copy; IPC frames are bounded and consumed sequentially.  R raw/DOM ownership is released before V construction, and the driver never retains `R+2V`.

## F6 -- durable fail-closed publication repaired

- Producer `atomic_json` at line 3056 and checker `exclusive_json` at line 4076 use a checked same-directory exclusive temp/final protocol.  Acceptance requires exact physical identity, file fsync, directory fsync, and final-name identity.  Producer rollback starts at line 6424; checker rollback starts at line 5624.  Once a final name is visible, every typed or untyped failure unlinks it relative to the checked directory fd, fsyncs the directory, removes/fsyncs any temp entry, and remains nonaccepting even if rollback fails.
- Driver rejects stale owners before heavy work at line 93 and installs owned-output cleanup at lines 125--141.  Raw extraction final identity is checked at line 195.  Retained logs are reopened with exact identity and `nlink=1`, then file/directory fsynced at line 264.  Final sentinel identity/durability is checked at line 424.
- Crucially, the status-blind GAP `Exec` route is gone.  The shell helper keeps its cleanup trap active through final raw and sentinel rehashes at lines 439--440 and disables it only at line 442.  GAP uses status-bearing `Process` at lines 450--451 and rejects every nonzero status at lines 452--453.  There is no post-helper GAP pin/read edge, so failure after visibility cannot strand raw, R, V, log, or sentinel owners.

## F7 -- driver, independence, and static closure repaired

- The driver is ASCII, LF-only, with no BOM/CR.  It uses native directory construction, fixed quoted paths, and stale-v12c rejection before heavy work.  Lines 120 onward require exact commands `python3 timeout grep sed cmp uname wc`; platform gates require Linux/x86_64.
- Driver lines 33--37 pin exact P0, producer, checker, and fixture bytes/SHA-256.  P0/fixture raw bytes are checked against compact canonical serialization plus LF before semantic fields.  Large R/V/raw owners are streamed for rehash; raw and sentinel receive a final rehash while rollback is still armed.
- Producer/checker terminals must each be exactly one complete full line with the exact expected terminal and no extra line.  UNKNOWN, timeout, mismatch, partial log, alias, link-count failure, or fsync failure is nonaccepting.
- Checker raw reconstruction is independent: it reads/replays all 2,896 chronological raw columns with an in-loop check at line 3239, reconstructs the formal solution/current dual and selected correction, and never treats a producer summary as evidence.  Driver status acceptance is the numeric result of GAP `Process`, not sentinel bytes alone.

## Retained task376 mathematical PASS clauses

Static read-through retains chronological growing `seen_pivots`; every P-product uses only already-seen pivots.  The actual rank-2,896 current dual annihilates the full basis and has the same nonzero pairing with target and remainder.  The literal selected Q0/Gamma/K0 correction is independently replayed and raises the ordinary rank from 2,896 to 2,897.  Checker reconstruction enforces 2,896 raw columns/rank/pivots at lines 3159--3239 and the 2,896-to-2,897 transition at lines 3310--3332.  One bounded descending `AncestryDAG` weights/answer owner is retained.  Expected rejection semantics remain exact and narrow.  All conclusion flags remain false: `common_word`, `finite_common_word`, `separator`, `negative`, `cofinal_lift`, `fake`, and `ihara_witness`.  Actual A0 remains `0/1`.

## Execution and audit record

No Python, Node, GAP, GHA, workflow, git, network, import, syntax-check, compile, candidate, mutation, RSS, or subprocess command was run.  No test suite was run.  Only read-only PowerShell inspection and SHA-256 hashing were used.  Therefore no runtime/performance result is asserted, v12c GHA is forbidden, and a fresh independent static code/performance audit remains required.

A0/V12C VERSIONED OWNERS:               COMPLETE
TASK376 F1 CANONICAL GRAPH:              REPAIRED
TASK376 F2 REAL BOUNDED MUTATIONS:       REPAIRED
TASK376 F3 HEAVY OWNER REUSE:            REPAIRED
TASK376 F4 DEADLINE COVERAGE:            REPAIRED
TASK376 F5 LIVE MEMORY / OUTPUT RESERVE: REPAIRED
TASK376 F6 DURABLE PUBLICATION:          REPAIRED
TASK376 RETAINED PASS CLAUSES:           RETAINED
CANDIDATE EXECUTION:                     UNEXECUTED
FRESH INDEPENDENT STATIC AUDIT:          REQUIRED
V12C SELFTEST_BOOTSTRAP GHA:             FORBIDDEN
PRODUCTION / RESUME:                     FORBIDDEN
ACTUAL A0 COMMON + CHECKER:              remains 0/1
LIFT / FAKE / IHARA:                     NONE

TASK380_R07_A0_V12C_BOUNDED_COMPLETE_REPAIR
