# Sol(max) Task726: Task724 independent P1 checker v2 release re-audit

## Verdict

```text
VERDICT=PASS_P1_INDEPENDENT_CHECKER_V2_SAFE_FOR_GHA
SAFE_TO_DISPATCH_GHA=yes
ACTUAL_FIVE_ARTIFACT_CHECK=DEFERRED_TO_GHA
verified=false
```

All six finite Task718 blockers are closed.  The checker now has one exact
producer-v4 interface consisting of the canonical prepare receipt, ordered
block receipts 0--3, and the canonical join receipt.  Its actual route pins
the producer bytes before artifact work, independently replays the five
Task554 phases, validates all six receipts, and records all six raw receipt
digests before emitting its atomic success result.

This verdict authorizes only a bounded GHA replay against the five Task554
artifact roots and the six producer-v4 receipts.  No real artifact was opened
in this audit, and no P1 equality, precision-two result, A0, COMMON,
compatible lift, fake, Ihara, or Lean verification claim is promoted here.

## Exact audited inputs

| path | bytes | LF | final LF | SHA-256 |
|---|---:|---:|:---:|---|
| `sol/sol_task_726_audit_r07_task724_p1_checker_v2.txt` | `3469` | `58` | yes | `5457db6f0de0b8407cd63ba40f4ae18caa13b4956577dbfef34159e30ab691e9` |
| `sol/sol_reply_718_audit_r07_task713_p1_independent_checker.md` | `14004` | `275` | yes | `3571e46f622b7aeffc4420f3b8669df33c54f64620fab6dfd3b12c6c619d469c` |
| `sol/sol_reply_721_audit_r07_task720_p1_semantic_v4.md` | `5391` | `120` | yes | `922a7da011820f0ff2def256613767f565cfc987d8563265df5a15b2df9f9aa6` |
| `sol/luna_task_724_r07_p1_independent_checker_finite_repair_v2.md` | `5836` | `146` | yes | `856f4668c4a9311363b09329b9065802996de0ef59aa3d8c7227206415a6b4d7` |
| `sol/luna_reply_724_r07_p1_independent_checker_finite_repair_v2.md` | `2945` | `60` | yes | `ce2bbaae75a01d25272e22a1e9f179b03d2eba04bbf1c27840e4822298af4bd3` |
| `search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py` | `41259` | `381` | yes | `ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v1.py` | `120896` | `2502` | yes | `8bdf4b915a7e1db04d2ba25c967d37e383293e70d7112e3f8e8ff195a0352c4f` |
| `crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py` | `130683` | `2689` | yes | `8636440c5e51d71a1f06d20d89a3d60c588453e741b17fbbd61735c76a9d3e88` |

The checker-v2 receipt exactly matches the parent-remeasured frozen input.

## F718-1: production block schema is satisfiable - PASS

`BLOCK_BODY_KEYS` at checker-v2 lines 1373--1379 now includes exactly
`origin_reductions`.  `validate_block_body_keys` is called by
`validate_block_body` at lines 1382--1388, and `authenticate_block` calls that
complete validator at lines 1497--1505 before semantic replay.  The list is
then required to contain exactly 8,232 typed expressions at lines 1414--1426.
Thus a production block with the exact Task554 schema can reach semantics;
deleting or renaming the key rejects, while retaining it no longer creates
the former impossible key-set/lookup pair.

The bounded fixture constructs the exact key set and passes the same helper at
lines 2473--2474.  It then deletes the key and renames it to `origins`; both
mutated dictionaries reach that helper and reject at lines 2475--2482.

## F718-2: packet origin i is compared with stored origin i - PASS

`replay_block_kernel` fixes `expected_origin_count` once, enumerates the packet
stream once, sets `origin_index=packet_count-1`, bounds that index, and compares
the computed expression with `expected_origin_reductions[origin_index]`
(lines 1629--1648).  It neither uses `[-1]` nor slices the expected list.  At
EOF it requires `packet_count==expected_origin_count` (lines 1694--1695).
The production call passes the authenticated body's complete list at lines
1904--1913; its generator emits exactly origins 0--8231 and separately rejects
trailing packet bytes.

The fixture creates two distinct nonzero packet origins, first accepts their
computed ordered expressions through every expected-value branch, then swaps
the two stored expressions and observes rejection (lines 2406--2424 and
2468--2472).  This directly exercises the repaired production kernel.

## F718-3 and exact v4 six-receipt integration - PASS

The only producer provenance path is
`search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py`, paired at
checker lines 101--102 with immutable literal
`ff50d0ad50e080a15075bb52365987d9e389bf59e5e39666002b710947287a17`.
`validate_producer_source` hashes the actual bytes and requires that literal;
`producer_source_digest` has no dynamic fallback (lines 1711--1721).
`run_actual_check` invokes it at line 2179, before `authenticate_prepare` opens
the first artifact root at line 2181.

The compact CLI has exactly twelve arguments:

```text
five artifact roots + five ordered phase receipts + join receipt + output.
```

The named CLI requires the same five roots, exactly five phase receipt paths,
one join receipt, and one output.  Both routes converge on the same
`run_actual_check` call (lines 2606--2673).  There is no v1 wrapper/list parser,
join omission, or alternative `producer-receipt` option.

`read_peer_chain` requires five phase paths, canonically parses each, then
canonically parses the separate join, preserving the six raw byte strings
(lines 2082--2091).  The prepare and block key sets at lines 1952--1967 match
the actual v4 returns at producer lines 168 and 202.  The exact join key set at
checker lines 1968--1975 matches producer-v4 line 270.

`validate_join_receipt` requires:

```text
schema=d972.r07.p1.componentwise.v1
terminal=TASK554_P1_COMPONENTWISE_SEMANTICS_REPLAYED
global_relations=32280
old_ranks=2014
new_ranks=6045
dag_nodes=8059
old_local_relations=8232
direct_packet_halves=32928
packet_basis_halves=32928
new_actor_identities=24180
compound_obligations=65340
resident_global_matrix=false
independent_checker=false
precision2=false
A0=false
COMMON=false
COMPATIBLE_LIFT=false
FAKE=false
IHARA=false
verified=false
producer_sha256=<immutable v4 SHA>
```

All count fields are `plain_int`, not bool.  Lines 2112--2124 bind the join
values to the prepare and four block receipts; lines 2142--2160 independently
bind those phase totals to `176+8056+32928+24180=65340`, 2,014 old DAGs and
6,045 new DAGs.  `compare_semantic_receipts` at lines 2127--2139 then binds
the five producer phase values to the checker's independently replayed values.
The join therefore agrees transitively with both all five phase receipts and
the independent replay.

After all checks, the result records

```text
producer_receipts.prepare = SHA256(raw prepare receipt)
producer_receipts.blocks  = [SHA256(raw block 0),...,SHA256(raw block 3)]
producer_receipts.join    = SHA256(raw join receipt)
```

at lines 2202--2209 and exposes the same object as
`producer_receipt_sha256` at line 2232.  No one-digest wrapper can substitute
for the six canonical receipts.

## F718-4: nested Walsh types and digest - PASS

`validate_projector_receipt` at lines 1991--2009 requires `cv_sum_table` to be
a list of length four, every entry to satisfy `plain_int`, and the exact value
`[1,0,0,0]`.  It recomputes SHA-256 from that received typed list.  The peer
projector object is also compared with the checker's independently recomputed
object at lines 2133--2135.  The mutation
`[true,false,false,false]` retains the old integer digest but rejects through
this production validator in the live fixture at lines 2500--2502.

## F718-5: CLI modes are mutually exclusive - PASS

`validate_cli` at lines 2622--2635 accepts exactly one of:

1. bare `--selftest`;
2. one twelve-field compact `--check`; or
3. the complete named form with four block roots, five phase receipts, join,
   prepare root, and output.

Every cross-mode field must be absent.  `main` calls this validator before any
mode-specific work at lines 2638--2647.  Argparse rejects unknown or wrong-
cardinality arguments, and the validator rejects partial or mixed recognized
forms; no option is silently ignored.

The internal fixture accepts all three complete shapes and rejects selftest
plus compact, partial named, and compact plus named (lines 2575--2591).  The
three external bounded CLI probes below independently returned exit 1 and
`error=usage_mode`.

## F718-6: repaired fixtures reach live production helpers - PASS

The repaired selftest does not claim `run_actual_check` or a real artifact
replay.  Its factored calls are nevertheless the exact helpers used by that
route:

- the block-key mutations use `validate_block_body_keys`, called from the
  production block body validator;
- the two-origin accept/swap uses `replay_block_kernel` with all five expected
  objects, the same call shape used by `replay_block`;
- the sign fixture gives two nonzero grade rows to `evaluate_old_lifts`, with
  a nonzero reduction `[[0,1]]`; the live result is `grade1-grade0`, and the
  `grade1+grade0` mutation rejects through the same byte comparator used by
  `replay_prepare`;
- wrong block parent and true A0/COMMON/COMPATIBLE_LIFT/FAKE/IHARA/verified
  mutations are copies of complete receipts passed to `validate_peer_block`
  or `validate_peer_prepare`, rather than assertions about good constants;
- wrong join terminal/count/claim, missing join, reordered blocks, boolean
  Walsh entries, modified producer bytes, wrong producer SHA, and all three
  CLI-shape mutations enter their respective production validators;
- the perfect prepare + four ordered blocks + join chain passes the same
  `validate_producer_chain` used by the actual route.

The remaining small arithmetic/root/EOF fixtures from v1 remain live.  No
advertised Task718 repair is supported only by a toy dictionary assertion.

## v1 core regression and claim boundary - PASS

The v1/v2 comparison changes only the charged block schema/indexing, producer
pin, six-receipt join, typed Walsh validation, CLI selection, output receipt
digests, and corresponding live fixtures.  The independent core remains
unchanged:

- imports are standard-library modules plus NumPy only; producer v4 is read as
  bytes and is never imported or executed;
- quotient, affine/Fox, packed GF(3), projector, old closure/lift, packet and
  new-block FIFO arithmetic remain local to the checker;
- the actual loops still discharge 65,340 componentwise obligations and all
  8,059 DAG nodes, with authenticated packet ranges and terminal EOF;
- Q1 endpoints, actor order `(1,-1,2,-2)`, four complete FIFO transition slots,
  non-following roots, exact rosters and stable packet identities remain;
- only one old/block owner is live at a time; no resident
  `8059 x 96776` global matrix was introduced;
- resource caps still map only to `UNKNOWN_RESOURCE`, and the success result
  is atomically written only after five semantic replays and all six peer
  receipts pass.

`independent_checker=true` is result metadata only.  Every producer receipt
has `independent_checker=false`, and all producer/checker levels retain
`precision2=false`, `A0=false`, `COMMON=false`, `COMPATIBLE_LIFT=false`,
`FAKE=false`, `IHARA=false`, and `verified=false`.

## Bounded commands and results

An external temporary pycache was used; no implementation file was changed.

```text
python -m py_compile crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py
exit 0

python -B crosscheck/check_d972_r07_grade2_p1_componentwise_semantics_v2.py --selftest
exit 0
status=PASS
fixture_accept=6
rejections=41
all 38 named rejection_table entries=REJECT
actual_five_artifact_check=DEFERRED_TO_GHA
verified=false

python -B ...v2.py --selftest --out %TEMP%/task726-forbidden-output.json
exit 1; error=usage_mode; output file absent

python -B ...v2.py --prepare-root fixture
exit 1; error=usage_mode

python -B ...v2.py --check r0 r1 r2 r3 r4 p b0 b1 b2 b3 j o --out extra
exit 1; error=usage_mode
```

No real Task554 artifact, artifact-scale arithmetic, GHA, implementation edit,
or git operation was performed.

```text
ACTUAL_FIVE_ARTIFACT_CHECK=DEFERRED_TO_GHA
INDEPENDENT_P1_RESULT=NOT_RUN
precision2=false
A0=false
COMMON=false
COMPATIBLE_LIFT=false
FAKE=false
IHARA=false
verified=false
```

The sealed reply receipt is supplied in the task handoff after this file is
written; embedding its own SHA-256 would be self-referential.
