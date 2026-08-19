# Luna reply 157dw — full-4096 typed WordExpr/Fox lane v8

## 1. Scope and frozen sources

I implemented only the four paths authorized by task 157dw.  The controlling
task is `sol/luna_task_157dw_relfrat3_wordexpr_v8.md`, SHA-256
`03d4548d62c1b38e59b693d0e43097cabd69aaafe57ca513bd000580bf98f23a`,
21163 bytes, frozen at commit
`c023ff5a0eafcf469f49d5c67fa8ded0a8f47c1c`.

The three executable files are frozen as follows:

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_b345_relfrat3_wordexpr_v8.py` | 347171 | `ea2c2901e316bfaa1c42d3f9966de5ec76323139728dfef46d2032608997e8db` |
| `search/check_d972_b345_relfrat3_wordexpr_v8.py` | 375934 | `9d3368504953862e688f474871e72cdc1ae4153e4737b8b6260ba260804db413` |
| `search/d972_b345_relfrat3_wordexpr_gha_driver_v8.g` | 14534 | `63e9a8dcc87c446fb130665dfe94c29cbe0836f1b87682f9b5ac4a7eb7c25018` |

The driver pins these final producer/checker hashes.  I did not edit v1--v7,
q3, any workflow, receipt, claim ledger, or dialogue file.  I did not run the
full producer, production GAP, Git, or GHA.

## 2. Implemented search contract

The producer rebuilds the registered 4096-word correction dictionary in its
frozen order: identity first, followed by BFS first-seen products using the
authenticated signed commutator seeds and reduction order.  Candidate `i` is
`reduce(FIXED_WORD + correction[i])`, with `m=0`, `lambda=1`, and the frozen
row37/exponent-2 roof.

Before constructing the 32768-translation sparse basis, it computes the six
ordered E4 source images for every dictionary entry by the fixed-context DP.
The receipt binds the complete 4096-entry tuple ledger, exponent sums, count,
and digests.  The scan is allowed to reuse the one frozen inverse only if all
4096 tuples equal the frozen tuple.  A first difference terminates with
`B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE`, reason
`fixed_inverse_not_uniform`, `scan_evaluated=0`, and the lossless first
difference/prefix record.  It is neither an input error nor an obstruction.
No production result for this preflight has yet been obtained; this paragraph
states the enforced result contract.

If preflight passes, the lane fresh-reconstructs the full v7 basis and the
saturated 32-round directed prefix.  It independently gates the stable rounds
projection
`75a2894da0f19d0e541e27924ee63e220a6eca35e852b21088ee304ba42fc42d`,
translations
`a4b952bce888713e293587cd63d710465121e782448a3e2a571d80b992ea363f`,
columns
`cb57176146b926df16e508429db5aa1ff6b5b0ec691f2328371973681089b343`,
blocker history
`b5f100e45e874ce5ee3270cd31350b4318cf40931055571ac70066e69d62de53`,
and final blocker
`0cd653ee0966ccc83d270802bbb5d00b61731f28e27eec1918bb5ea282e00903`.
The volatile full-round digest remains provenance-only.

Candidate 1 is an unconditional drift canary: its outcome must be a missing
pivot at acceptance target 6, `hexagon_1_coface_0`, component 4, with the
frozen final blocker digest.  The fixed saturated basis is then used once, in
candidate order 1 through 4096, with no checkpoint-major retry schedule.

## 3. Typed WordExpr and corrected predicate

The candidate-local, hash-consed typed DAG implements `IDENTITY`,
`FLAT_WORD`, `PRODUCT`, `INVERSE`, and `SUBSTITUTE_WORD`.  Nodes carry their
free-group rank, reference only earlier nodes, and are keyed by their complete
typed payload rather than by a digest.  Products use the registered balanced
association.  Expansion length is an integer recurrence; substituted
descendants are never materialized merely to compute a value or derivative.

The exact left-Fox orientation is:

```text
D(uv)   = D(u) + value(u) * D(v)
D(u^-1) = -value(u)^-1 * D(u)
```

For a negative outer letter in `SUBSTITUTE_WORD`, the prefix is first updated
by the inverse image value and only then its translated image gradient is
subtracted.  Prefix action is on the left.  Producer and checker have separate
implementations and reject the reversed product law, right action, or
post-subtraction negative-prefix update.

The corrected Def. 2.9 IF-FIRST predicate is frozen at 33 acceptance targets
and 17 diagnostic targets.  Acceptance consists of five charming-error
cofaces, ten hexagon cofaces, the ordered A.18 pentagon, eleven S relations,
and six S(T_i) generator-recovery residuals.  The eleven T relations and six
T(S_i) residuals are lossless diagnostics only; they do not feed acceptance,
proof roots, `all_pass`, or terminal selection, and may be false on PASS.
Candidate exponent sums, five correction-coface identities, charming,
friendly/marking, outside-roof, hexagon, pentagon, S-relation, and S(T_i)
recovery gates remain explicit.

Candidate 1 also executes the mandatory production flat bridge: all 33+17
old literal words fit the cap there, so their quotient values and left-Fox
gradients must equal the WordExpr evaluations exactly.

## 4. Transactions, caps, and receipts

Each candidate snapshots the element pool and proof DAG before its first
candidate-specific intern.  Six source gradients may remain live within that
transaction, but no expression, value, gradient, pool suffix, or proof node
survives a failed candidate.  Candidate evaluation first performs quotient
gates, then streams one acceptance target at a time and runs membership-only
reduction against the immutable basis.  It creates provenance only after all
33 membership tests pass; the selected candidate is rebuilt and all
expression/value/gradient bindings are required again before proof-producing
reductions.

The new registered caps are 262144 expression nodes, 1048576 expression
edges, 4096 dictionary records, 16384 flat leaves, an expansion-count ceiling
of 4194304 per target without allocation, 1000000 live gradient entries,
1000000 candidate pool-suffix elements, and 4096 scan records.  The 100000
flat-word cap and every v7 sparse/pool/pivot/DAG/section/RSS cap are unchanged.
Producer and checker each have an independent 7200-second soft bound.

The scan prefix is packed with exact outcome, failed ordinal, component,
fixed-width blocker value, evaluated order, failure distribution, lengths,
and digests.  Resource stops preserve a typed current phase and completed
prefix.  Dedicated fail-closed schemas cover pre-saturation, post-saturation
pre-scan, candidate-transaction, between-candidate, and positive-certificate
serialization stops.  Rollback clears pool-ID LRUs before ID reuse.  No
non-PASS receipt retains a positive boundary proof root.

## 5. Independent checker

The checker imports no producer helper.  It independently reconstructs q3,
all pinned v1--v7 inputs, presentations/cofaces and collectors, the normalized
27-fibre inverse, the 4096 dictionary and source-tuple DP, the complete basis,
the fresh saturated v7 prefix, the typed expression evaluator, every completed
candidate outcome, rollback/accounting, and all terminal/claim schemas.  Its
own monotonic 7200-second deadline is checked in the dominant translation,
directed-round, column, WordExpr, source-preflight, candidate, and proof-DAG
loops.

After the hostile audit, the terminal/schema envelope, packed scan
decoder/replay/transaction checks, and selected WordExpr/proof checks were
factored into production functions used by both `main()` and the in-memory
self-test provider.  The bounded provider injects a toy quotient, toy candidate
builder, toy flat-bridge result, a completed source-preflight plus its 4096
tuples, a toy basis, and a zero-leaf proof provider.  This injection is
in-process only and cannot be selected by production `main()`, which never
passes the sealed flag; it also cannot be represented by the JSON artifact.
The provider does not replace the production exact envelope, packed scan
decoder, membership reduction and transaction checks, corrected 33/17 split,
selected WordExpr validator, or packed proof evaluator.  Its receipt uses the
production `SCHEMA`, exact top-level key discipline, packed scan schema,
selected-pair schema, and packed proof format.  There is no sealed-schema early
return.  Entry counters bind envelope, source-preflight, scan, selected, and
proof execution; positive opcode/child/gradient/proof/S/ST mutations enter
those same functions.

On PASS it independently regenerates the selected candidate, replays all 33
gradients, checks the six source roots and five correction-coface roots, and
decodes/replays only the reachable packed proof DAG.  Diagnostic roots are
renumbered and bound to the selected WordExpr DAG but remain outside the proof
predicate.  Exact top-level keysets and claim-boundary records reject injected
negative, global, or B4-A/B language.

## 6. Differential self-test history and present gate

The original first combined attempt stopped at the `ToyQ` tuple/bytes fixture
representation mismatch.  The then-authorized corrective run passed, but the
hostile audit correctly found that its `sealed_selftest=True` branch returned
before the production scan/selected-proof core.  The former
`production_validator=1` description is therefore withdrawn; it was not
evidence for the task §G requirement.

I removed that early branch and the legacy fixture validator, introduced the
shared production core described above, and used the additional explicitly
authorized combined run exactly once.  Producer passed, while checker stopped
at a self-test trace assertion:

```text
D972_B345_RELFRAT3_WORDEXPR_V8_PRODUCER_SELFTEST_PASS product=1 inverse=1 substitution=1 negative_prefix=1 long_unflattened=262144 scan=4096 terminals=4
B345_RELFRAT3_WORDEXPR_V8_CHECKER_FAIL v8 mutation source core entry: source tuple
```

This failure was in instrumentation, not in the production predicate or scan:
the mutated receipt did enter the shared source-preflight core, but the entry
counter was incremented after the exact receipt/provider equality check, so
the intended rejection occurred before the counter changed.  I moved the
source counter to the core entry and, by the same reasoning, moved the envelope
counter ahead of claim validation so the forged-global-claim mutation records
its entry.  No production predicate/search field changed.  Per that run's
instruction, I did not silently rerun.

The parent then explicitly authorized one final confirmation because the prior
run preceded completion of the trace-entry placement.  I statically confirmed
the shared entry connections and ran the combined test exactly once.  It
passed on the final checker hash:

```text
D972_B345_RELFRAT3_WORDEXPR_V8_PRODUCER_SELFTEST_PASS product=1 inverse=1 substitution=1 negative_prefix=1 long_unflattened=262144 scan=4096 terminals=4
D972_B345_RELFRAT3_WORDEXPR_V8_CHECKER_SELFTEST_PASS envelope_entries=14 source_preflight_entries=11 scan_entries=10 selected_entries=10 proof_entries=5 positive_mutations_shared_core=9 product=1 inverse=1 substitution=1 negative_prefix=1 long_unflattened=262144 source_tuples=4096 rollback_ID_reuse=1 acceptance=33 diagnostics=17 mutations=11 terminal_fixtures=5
```

No execution followed that PASS.  Static audit finds the legacy sealed
schema/early return absent, the shared production entries connected from both
providers, driver ASCII-only, no hash placeholders, the final checker pin
installed, exactly four driver terminal markers, no trailing whitespace, and
no out-of-scope tracked edit.

## 7. Runtime and proposed dispatch

The measured predecessor basis+saturation cost is about 232 seconds and 702
MB.  The source-only estimate is 1--3 minutes for dictionary/source-tuple
preflight, followed by an uncertain 10--60 minutes for a positive or complete
scan in each of producer and checker.  These are planning estimates, not
mathematical claims.  The driver retains the 330-minute job limit and requires
`with_pquot_packages=true` because the checked q3 child needs the pinned GAP
packages.

Proposed canary inputs:

```gap
D972_B345_RELFRAT3_WORDEXPR_V8_SELFTEST:=true;
D972_B345_RELFRAT3_WORDEXPR_V8_RUN:=false;
```

Proposed full inputs:

```gap
D972_B345_RELFRAT3_WORDEXPR_V8_RUN:=true;
D972_B345_RELFRAT3_WORDEXPR_V8_OUTPUT:="ci/out/d972_b345_relfrat3_wordexpr_v8.json";
```

The parent broker alone may commit, push, or dispatch GHA.  The current checker
hash has the required authorized combined self-test PASS.

## 8. Terminal boundary

Allowed terminals are exactly:

```text
B345_RELFRAT3_WORDEXPR_PASS
B345_RELFRAT3_WORDEXPR_SEARCH_INCOMPLETE
B345_RELFRAT3_WORDEXPR_UNKNOWN_RESOURCE
B345_RELFRAT3_WORDEXPR_UNKNOWN_INPUT
```

All 4096 registered candidates failing is only the second registered
SEARCH_INCOMPLETE reason.  Every non-PASS is
`unknown_not_obstruction`, scoped to
`registered_4096_wordexpr_positive_search_only`, with no mathematical
obstruction, full-universe, negative, earliest-global-candidate, B4-A, B4-B,
or uniform/cofinal claim.  This implementation has not yet produced a
production receipt and makes no A/B decision.

B345_RELFRAT3_WORDEXPR_V8_READY_FOR_GHA
