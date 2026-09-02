# Sol(max) reply 528 -- independent audit of the actual rank111 lazy K=0 successor

## Verdict

`STOP_DO_NOT_ADOPT`

The mathematical positive selector, physical admission path, legacy anchor,
and v13 transport are otherwise consistent with the commissioned current
task445 K=0 lane.  Dispatch is nevertheless blocked by two small, exact
checkpoint/checker defects in the new-record schema boundary:

1. new v5 record rounds are not required to be strictly later than the
   legacy terminal round or strictly increasing; and
2. several promised integer fields accept JSON booleans/floats, and the
   independent replay's ordinary Python equality does not distinguish those
   mutations from the recomputed integers.

Both defects survive recomputation of the public v5 state seal.  They violate
the commissioned exact round/counter/exponent typing and mutation boundary.
This STOP does not allege a false physical row and does not revive the
quarantined rank99 lane.

## F1. Exact audited identities and owner boundary -- PASS

The audited candidate is actual local/pushed HEAD
`3d98bab1c934cd90ae5a0cf644bb8d8b470524d7` (the earlier expanded SHA supplied
in chat was corrected by the parent as a transcription error).  The exact
subject blobs are:

| subject | bytes | SHA-256 |
|---|---:|---|
| producer v5 | 34773 | `94e9079c36592414d394f816d0d1190822157c017afecd9e75c9e19f8c7aa5aa` |
| checker v9 | 27570 | `9b9bfbf72a312ed759861c854f1f5513342c037c2eb74b89bee8e09caa2f29c0` |
| driver v13 | 8683 | `8f034abce4f469542206338e14502281dcc7ae1862338bafef5d431d74e5f63e` |

V5 pins the current task445 producer v3, 12215 bytes /
`0140447110cfa568a77300bd7d43d51c622597704b7b91ed5209c63168c9ef37`,
and v9 pins the current independent checker v7, 3653 bytes /
`e1b80c586985f5113b300508f6bc78d055a37243e3fd6795b8f81148b0988de1`.
There is no import or call to Task416/rank99 state, `formula_bundle`,
`compiled_formula_scalar`, `retain_correction_candidate`, a rank99 global
selector, batch/segment/ledger state, or source-rewrite machinery.  The
occurrence model named `model179` in this route is the pinned current task445
`AllSevenModel`, not the quarantined rank99 custom wrapper.

The new schema/checkpoint binding independently agrees in producer and
checker:

```text
schema   d972-r07-a0-actual-tau-free-lazy-k0-seed/v5
CP       d972-r07-a0-actual-tau-free-lazy-k0-seed/v5/checkpoint
binding  0df6177cb0c5c16f21b20b3c7582c0162a520b4fdf33784f2215140339566584
```

## F2. Legacy authentication and physical reconstruction -- PASS

The downloaded member 5 was independently reparsed:

```text
outer bytes/SHA       85934 / 69a7ec3da4907f24af0f68c1975538b9ff9b6102f14e334f7c0725d2542dfd93
legacy schema         d972-r07-a0-actual-tau-free-rank-ladder/v3/checkpoint
legacy binding        6f179b061a010bb2a9b427dda6564c7418b18f44da17ea2f28e9e080655326a3
legacy state seal     3e0d4bc8e2f9a467a0e50ad8435a7360e1953c2baee369225d8aa6fd71379610
prefix count/digest   68 / 684039158b841d607aa40617778b9267ea96d64a38d952f74e63791b23ea3932
rank / round          111 / 73
dual digest           56ccd1f3cc6b54fe340a69ce6a0ec99f5aeb3358ae80288c6b11c3f1ec664864
remainder digest      9eed8114d9e3172c7a11153d9c5cd6e5fc2e5184a8d6e3681cce5c82a83b4326
N1,N2                 0,0
tau 1,2,3             0,0,0
unrecognized keys     []
```

The raw legacy route requires the exact outer identity before parsing.  Both
legacy migration and sealed-v5 resume keep the canonical 68-source prefix,
replay it with current task445, and require the same rank-111 dual/remainder
anchor before any new selector work.  The v5 checkpoint rank relation
`rank = 43 + accepted_count`, per-record old/new rank chain, cumulative
selector counters, binding and internal/outer seals are otherwise present.
Bounded mutations of the legacy count/prefix/rank/round/profile N/tau/bad-key
fields and state seal, and sealed-v5 prefix/rank/binding/seal mutations, were
all rejected.

## F3. Selector and update semantics -- PASS

The imported production call graph does the following:

1. enumerates exactly `pure_relations(4)[5:11]` before adjoint/formula work;
2. constructs one current task445 tau-free adjoint after a six-action miss;
3. visits compact relators 1 through 44 in their pinned printed order and
   constructs only the current seed formula;
4. stops claims-false `UNKNOWN_RESOURCE` on nonzero tau, K nonzero,
   unsupported coordinates, non-nine S0--S2 kernel support, no hit, time or
   RSS;
5. evaluates the full merged formula at every candidate, so coincident terms
   can cancel and support membership alone is never a hit;
6. continues on scalar zero and, at the first nonzero, reconstructs the
   literal conjugate, `replay_atom` row and fresh `seed_v12` row, exponent/18,
   N/E typing, direct nonzero pairing, nonzero reduction and predicted pivot;
7. performs one physical add and one current task445 `update`, checkpoints by
   flushed temporary file plus atomic replacement, clears only the selective
   canonical cache, and returns to seed 1 under the new dual.

V9 does not import v5 or a producer selector validator.  It independently
drives action-first selection, its reverse-order low adjoint, formula/K/support
schedule, literal/fresh row, direct pair, pivot/rank, one add/update and
post-state digests.  It compares the result with the external checkpoint and
keeps `UNKNOWN` invariant failures distinct from claims-false
`UNKNOWN_RESOURCE`.  COMMON remains only the pre-existing fully replayed
task445 candidate boundary (`A0=true`, `COMMON=false`); no negative branch is
promoted.

Bounded reruns, using the actual final functions with only the expensive
group setup stubbed, returned:

```text
AST_PARSE_PASS
producer FIXTURE status=FIXTURE; roster 43/45/6441/digest rejected
checker v9 SELFTEST_PASS; producer_selector_imported=false
CRITICAL_DIRECT_REJECTIONS
  formula_direct,row_fresh,exponent,forbidden_E,bad_N,dependent,K!=0
COMMIT_REJECTIONS stale_dual,second_insert,pivot adds=1 updates=1
```

A coordinated mutation of a legacy row/scalar followed by recomputation of
the v5 seal remains rejected by the frozen prefix digest.  For a new record,
v9 reconstructs the row/scalar rather than trusting their stored values; an
actual mod-3 row/scalar change is therefore rejected.  The type-equivalent
boolean/float mutation in F6 is the exception to the promised exact schema
typing.

## F4. Transport and hot path -- PASS

The locally retained permanent-release ZIP is 37586 bytes /
`8b740dbbc81f5d2e659371a81453ded56c6711ce8ace35a4af5255303e0095de`.
Independent `ZipArchive` traversal reproduced the ordered eight-member
manifest and all member sizes/SHA-256 values; the selected one-indexed member
is exactly member 5 above.  V13 retains run/job/head
`33564845217 / 100045550767 / c582f8d786012a668783790007b72c5c422c3db8`,
artifact `9826862037 / gap-run-out / API size 96198`, the permanent release
URL, stale-output checks, `set -euo pipefail`, `umask 077`, `ci/out`, and
`ulimit -v 5200000`.

A GAP capture of the generated command passed `bash -n`.  After removal of
GAP's printed line continuations it contained exactly one v5 producer and one
v9 checker, producer limits `7500 / 7200 / 4800000000 / 64`, checker limit
`3600`, one checker marker, and no `SELFTEST`.  Pipefail prevents the checker
from starting until the producer pipeline completes; the result/checkpoint
existence gates and exact one-line checker marker remain intact.

The production critical path has no eager 44-formula list, all-seed coordinate
union, un-conjugated identity replay, full PB3/PB4 closure call, rank99 global
roster, duplicate update, deep/full state copy, `gc.collect`, or checker-before-
producer route.  Exact unavoidable per-process cost remains substantial and
must not be called a measured speedup: current task445 rebuilds the compact
44-seed/rank-43 physical base, replays all 68 legacy rows with their state
updates, replays any sealed-v5 rows, and on first fibre use constructs the
1,469,664-state selective Q0 data, S0--S2 membership data, Gamma data and
authenticated order-nine kernels.  After that setup, each new unchanged-dual
round is the six actions, one adjoint, lazy seed-by-seed occurrence formulae,
nine kernel candidates per visited support fibre, and only the nominated
literal/fresh physical replay.

## F5. Blocking defect 1 -- new-record round chain is unauthenticated

Producer lines 231--240 and checker lines 177--186 require only a checkpoint
round at least 73 and at least the maximum stored source round.  Neither
requires the first new round to exceed 73 nor later new rounds to increase.
Producer resume then calls

```python
commit(P, m, [], record["round"], state, selected)
```

so its regenerated-record equality merely copies the untrusted round back
into the regenerated record.  Checker v9 never uses a new record's round after
the weak checkpoint maximum test.

The bounded counterexample started with the exact 68-source prefix, appended
a structurally valid rank `111 -> 112` v5 record with `round=1`, set checkpoint
`round=73`, recomputed the v5 seal, and obtained:

```text
MALFORMED_NEW_ROUND_ACCEPTED_BY_BOTH 1 legacy_terminal_round 73 state_round 73
round_chain_tail [72, 1]
```

Thus an otherwise independently replayable new row can have its round changed
to a decreasing/duplicate value and be resealed without v9 detecting it.  The
small repair is to enforce, in both owner and checker, first-new-round `>73`
and strict increase over all subsequent new records, with a mutation test that
reaches the independent replay path.

## F6. Blocking defect 2 -- exact integer typing is not enforced

The new validators use `isinstance(x, int)` and membership/equality against
`0,1,2`.  In Python, booleans are integers and compare equal to 0/1; floats
such as `0.0` also compare equal to integer zero.  In particular,
`normalized_exponent_quotients` has no element-type test.  The checker later
compares recomputed integer dictionaries using ordinary equality, so the same
equivalences persist through independent replay and cumulative-counter
reconstruction.

All of these mutations were accepted by v9's `validate_new_source`:

```text
NONINTEGER_TYPED_MUTATION_ACCEPTED bool_scalars
NONINTEGER_TYPED_MUTATION_ACCEPTED float_exponents
NONINTEGER_TYPED_MUTATION_ACCEPTED bool_counters
NONINTEGER_TYPED_MUTATION_ACCEPTED bool_cursor
```

Concretely, stored `scalar/formula_scalar/direct_scalar=true` compares equal
to recomputed scalar 1; boolean selector counters compare equal to recomputed
0/1 counters; and float N coefficients/epsilon quotients compare equal to
recomputed integers.  Recomputing the public checkpoint/result seal does not
repair that missing type check.  The small repair is exact `type(x) is int`
validation for every new integer field (including scalar, ranks/round,
exponent/N values, cursors, checked counts and all counters), followed by
resealed boolean/float mutation tests through v9's full new-record replay.

## Commands and limitations

Representative bounded commands were:

```text
Get-FileHash -Algorithm SHA256 <subject/member>
python -B -c <AST parse / legacy parser / selector mutation harness>
python -B search/d972_r07_a0_actual_tau_free_lazy_k0_seed_v5.py --mode FIXTURE --output <TEMP>
python -B crosscheck/check_d972_r07_a0_actual_tau_free_lazy_k0_seed_v9.py --self-test
.\gap.ps1 <TEMP driver-capture.g>
bash -n <TEMP generated-command.sh>
git diff --no-index <driver-v11> <driver-v13>
```

All writable fixtures were outside the repository.  I did not run the full
task445/rank111 replay, production, GHA, network, workflow, release or git
mutation, and I did not edit any subject file.  Tool output and bounded tests
remain candidate evidence, not Lean verification.

## v220 consequence

No numerator changes.  Relative to v220 Delta369, A0 actual COMMON remains
`0/1`; the stable single-row prefix remains exactly 68 sources / rank 111 /
round 73; no new row is adopted from this unaudited successor; and A4, COMMON,
NONMEMBER, compatible lift, fake and Ihara claims are unchanged.  This STOP
authorizes no v13 dispatch.

`STOP_DO_NOT_ADOPT`
