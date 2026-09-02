# Sol(max) reply 531 -- independent re-audit of the rank111 lazy K=0 schema repair

## Verdict

`GO_FOR_GHA_DISPATCH_ACTUAL_K0`

The v6/v10 repair closes both Task528 blockers.  This GO authorizes parent
adoption and one v14 GHA dispatch only.  It is not an A0, COMMON, compatible
lift, fake, Ihara, or other mathematical-progress result.

## Exact audited identities

The named files were clean at audited HEAD
`22eec63821ec4b64e5030b7a48dcb28480c910e8`:

| subject | bytes | SHA-256 |
|---|---:|---|
| producer v6 | 42434 | `43f5dac842fd4025d714b99a1e16f63ecf7cc2a35c53d8f106748a4d06a13b1c` |
| checker v10 | 33455 | `36db2a4e5eafb9a2c6a23d0ec9d280f22503b033fcf098f1c2ee19f32db5dd78` |
| driver v14 | 8692 | `c46fedb85495128a6e1f5e84c13ffc55d95cb2ece7b565050ba5777cfc868bd4` |
| Task529 reply | 6790 | `012e7c21744eb63cc0c0b04e3fbf7f653b2b7f799dba4ba48bae37738a770fcf` |

Producer and checker independently compute schema binding
`c76189ad8f5b43eefea62f92ff1942e097be57802babe2622ee6c1bf13fb6050`.

## F1. Authenticated round chain -- PASS

Both owners use exact `type(value) is int` and anchor new records at legacy
round 73.  The first v6 round must be greater than 73, every later round must
be strictly greater than its predecessor, and checkpoint/result round must be
an exact integer at least as large as the authenticated last new record (or
at least 73 when none exists).  They deliberately impose no unit-step rule,
so gaps remain valid.

The producer applies the gate to checkpoint construction/validation, resume
replay, every prospective production commit, and terminal construction.  Its
replay first authenticates the chain, names the stored value
`authenticated_round`, commits with that value, and then requires both
`generated["round"] == authenticated_round` and full generated-record
equality.  Thus the old unconstrained copy-back route is gone.  V10 gates the
checkpoint/result and again enters `replay_new` through the strict chain gate.

An exact-prefix, re-sealed harness accepted first round 74, the gapped chain
`74,76` with terminal round 80, and the empty chain at terminal round 73.  Both
owners rejected re-sealed first rounds 1 and 73, duplicate/decreasing rounds,
float round, and a terminal round below the authenticated tail.  V10's own
self-test reaches `replay_new` and rejects its five round mutations before
physical setup.

## F2. Exact integer boundary -- PASS

Every v6 record is recursively rejected if any JSON value is a boolean or
float.  Explicit exact-integer gates cover common rank/round/scalar/version
fields, all correction word/exponent/N/quotient/coordinate/cursor/count
fields, every selector counter, and action-source `family_index` and
`scalar`.  Counter addition validates both operands instead of normalizing
them with `int(...)`.

Checkpoint accepted count/rank/round, completed and attempt counters, and
progress data receive the corresponding exact gates in both owners.  V10
also exact-checks result count/rank/round and durable bytes/count/rank before
using checkpoint/result equality.  `legacy_accepted_count` is exact-checked
at the checker entry.  The result's `elapsed_seconds` remains outside these
integer gates and a float value was accepted at the live checkpoint/result
boundary.

After every checkpoint mutation the public state seal was recomputed.  Both
owners rejected all 18 cases:

```text
round_first_1, round_first_73, round_duplicate, round_decreasing,
round_noninteger, round_terminal_tail, scalar_bool, direct_float,
exponent_float, N_float, counter_bool, cursor_float, cp_count_bool,
cp_rank_float, cp_round_bool, cp_counter_float, cp_attempt_bool,
cp_progress_bool
```

A valid action record passed both validators; boolean `family_index` and
float action scalar were rejected by both.  V10 additionally rejected six
durable/result mutations (`bytes`, durable count/rank, result count/rank/round)
while accepting `elapsed_seconds=1.25`.

## F3. Independence and confinement -- PASS

V10 imports neither v6 nor any producer selector validator.  It pins the
independent v7/lower chain and retains its own formula, support, literal-row,
direct-pair, pivot, insertion and post-state replay.

Mechanical source comparison found the producer's `formula_for_seed`,
`formula_scalar`, `kernel_digest`, `support_states`, `write_checkpoint`,
`roster_gate` and `authenticate_roster` byte-identical to v5.  Its
`direct_correction` and `select_one` become byte-identical after only the
required record-version 6-to-5 normalization.  The checker's
`formula_for_seed`, `formula_scalar`, `support_states`, `kernel_digest`,
`public_source`, `first_action`, `replay_correction` and `reason_type` are
byte-identical to v9.  The remaining executable differences classify as
schema/module aliases, exact numeric/round gates, and bounded fixtures.

Consequently there is no concrete regression in the Task528-passed current
task445 formula/selector, physical admission and single-update gates, legacy
anchor, resource/claims semantics, atomic checkpoint algorithm, or lazy hot
path.  Those passed issues were not reopened.

## F4. V14 transport -- PASS

After normalizing only v14/v6/v10 paths, preamble, task markers, byte/SHA
pins and final markers, v14 is exactly v13.  The independently downloaded
permanent-release ZIP was 37586 bytes /
`8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de`.
All eight archive entries matched v14's ordered name/byte/SHA manifest, and
member 5 was exactly the 85934-byte checkpoint /
`69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93`.

V14 retains `ulimit -v 5200000`, producer limits
`7500/7200/4800000000/64`, checker timeout 3600, stale-output and survival
gates, producer-before-checker sequencing, and exact one-line checker-marker
cardinality.  It contains no `SELFTEST`.  A repository-external GAP capture
parsed and constructed `D527Cmd`; the captured command passed `bash -n`.

## Bounded commands and limitations

Representative commands were:

```text
Get-FileHash -Algorithm SHA256 <four named inputs>
python -B <producer-v6> --mode FIXTURE --output <TEMP>
python -B <checker-v10> --self-test
python -B - <external exact-prefix/re-seal and AST-confinement harnesses>
.\gap.ps1 <external v14 capture.g>
bash -n <external captured.sh>
```

No full task445/rank111 replay, production execution, workflow dispatch,
implementation edit, git/release mutation, or claim adoption was performed.
The bounded outputs are candidate audit evidence, not Lean verification.  All
previously unsupported branches and all claims-false semantics remain
unchanged; mathematical status stays at the exact 68-source, rank-111,
round-73 legacy prefix until an independently checked production artifact
exists.

`GO_FOR_GHA_DISPATCH_ACTUAL_K0`
