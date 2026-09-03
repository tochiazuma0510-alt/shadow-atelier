# Sol(max) Task644: Task640/643 fresh-rho2 v3 final static audit

## Verdict

`FAIL`

`SAFE_TO_DISPATCH_GHA=no`

The quartet is not dispatchable.  The compositional Task625 parent ruling is
mathematically sound, and neither child needs to repeat the accepted
graph-to-leaf traversal.  The frozen implementation nevertheless has the
following finite, live-path blockers.  No production program, GHA workflow,
or git command was run; this was a static audit.  `verified=false`.

## Exact audited inputs

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 26,491 | `f7ce3f23a60a626e8a297017c7f898b92ac7c6b626e09ebc84501e6d97f9b826` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 79,461 | `662ae5797581be4c08f45787c43b1cb58e9a3ac5ecd81d2621a7a5b572731a98` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v3.yml` | 8,724 | `deace59ca2d2dc8999f68aca44737887873edf2e6a6742529af11c3386298104` |
| `sol/luna_reply_640_r07_fresh_precision2_endpoint_signature_v3.md` | 5,690 | `a61b3abeae798eaff5536de1a870485731c223a1448ba5a7cb7b8c1982f56a94` |

The Task644 instruction is 3,837 bytes with SHA-256
`d6304399bd73d70424cd698a9a5aff3586a55594c1d29deaa71cb2326cb72d96`.
I read Task640, Task643, Task627, Task630, Task639 and Task641 completely and
used Task643 only for its stated graph-to-leaf supersession.

## Blocking defects and smallest repairs

### F644-1 — the Task595 artifact name is nonexistent

Workflow line 106 downloads
`task595-grade1-decision-v3-candidate-33707397894-1`.  The actual Task595
workflow uploads
`task595-grade1-decision-v2-candidate-33707397894-1`
(`d972-r07-a0-first-rung-grade1-decision-v2-recovery.yml:118-123`), and the
accepted Task625 workflow also consumes that exact `v2` name
(`d972-r07-a0-grade1-selected-slp-v3.yml:80-86`).  Thus the present route
stops before the parent-checker rerun.

Smallest repair: change only `decision-v3-candidate` to
`decision-v2-candidate` at workflow line 106.

### F644-2 — the accepted parent envelope is not authenticated

Workflow lines 84-87 authenticate the Task625 run attempt, head, conclusion
and name.  `TASK625_JOB=100582244001` at line 29 is never used, and no API
gate checks payload artifact id `9885925239`, archive size `50,793,121`, or
digest
`sha256:ac3121f3bc1a7e2a6c267f20352e953b7343f9085015dd74e4a67e4b90129a75`.
Downloading by run and name and then checking extracted receipts authenticates
the contents, but it does not satisfy Task630 Sections 7/8 and Task640 Section
1's exact job/artifact-envelope binding.  Merely hashing the Task639 prose
does not make these live API equalities true.

Smallest repair: before download, query the exact job and artifact metadata;
require job id/run/attempt/head/conclusion and artifact id/name/size/digest,
`expired=false`, and its workflow-run id/head to equal the Task639 constants.
Then retain the existing exact-name/run download and fifteen content hashes.

### F644-3 — endpoint/canary ordering can hide a source seed

The producer first replaces the ordered roots by
`complete=terms(prior+replaced)` at line 215 and derives `reached_seeds` from
that cancelled map at line 222.  The checker does the same at lines 297 and
302.  A seed occurring in an authenticated raw root but cancelling on an
equal `(seed,path)` key can therefore evade all eleven endpoint-one gates,
contrary to Task630 item 5.  Moreover, both programs construct and cancel the
signature buckets before running the direct all-seven canary
(producer 229-236; checker 325-333), while Task644 expressly requires the
canary before grouping.

Smallest repair: derive the endpoint-gate seed set from the separately
validated raw `C_<1` terms and raw `R07LEAF1` terms, before exact-key
cancellation.  Exact-key cancellation remains permitted for the evaluation
map.  Run the direct canary for every nonzero key of that complete evaluation
map before constructing signature buckets; no canary is required for keys
which cancel exactly to zero.

### F644-4 — checker dense replay uses the wrong domain

The checker independently constructs `buckets` at lines 325-330 but discards
them for arithmetic: line 334 calls
`independent_replay(..., complete)`.  The accepted parent has 19,393 literal
leaves and 2,622 prior terms, so this sends roughly twenty thousand keys
through a 241,928-trit dense action.  It violates Task640 Section 4's rule
that dense action is charged only to nonzero signature buckets and makes the
45-minute checker route needlessly implausible.  This is not the mandatory
per-key sparse all-seven canary; that separate loop must remain.

Smallest repair: form replay terms from the checker's own recomputed nonzero
`buckets`, using each bucket's coefficient and retained representative path,
and pass those to `independent_replay`.  Do not read producer bucket values as
arithmetic authority.

### F644-5 — the endpoint checker is not independent

`SevenSources.load` dynamically compiles and executes the pinned source
modules at checker lines 79-83.  `build_checker_light` then obtains the E3/E4
quotients, contexts, joint roster, substitutions, Fox gradients, PB3 rows and
PB4 rows by calling those modules at lines 1080-1121.  The live
`IndependentAllSeven` continues to call `self.old.f2_substitute`,
`embed_f2_pb3`, `fox_gradient_without_sections`, `translate_vector`,
`hexagon_words` and related word routines at lines 1181-1353.  In particular,
the `old` module is the exact
`search/d972_b345_seedspan_triple4_v1.py` semantic owner also loaded by the
producer's pinned v12f path.  Wrapping `exec` in a differently named module is
runtime reuse, not an independent group/word/endpoint implementation.

Smallest repair: transplant/implement the required quotient, group/word,
substitution, Fox, translation, PB3/PB4 and endpoint operations locally in
the checker and remove execution of producer-shared semantic modules from its
live path.  Exact pinned JSON/tables may remain data inputs.  The checker-local
truncated-ring, dense target/action, aggregation and packing code can remain.

### F644-6 — the checker accepts false result and receipt metadata

`validate_payload` checks the file bytes and recomputes the dense result, but
it does not equality-check the manifest's `root`, `occurrence`, `compression`,
most `parent` fields, `degree1_task625_physical_replay`,
`degree1_task595_member_equation_zero`, `member_coefficient_count`, or
`lower_all_zero` (lines 277-343).  For example, changing either degree-one
gate to false, changing `L/U/G`, or changing the declared parent run/head/name
while leaving the receipt files untouched still reaches the PASS verdict.
The verdict merely seals the mutated manifest hash.  This violates the
requirement to recompute and compare every manifest receipt and leaves the two
separate grade-one gates as unchecked producer assertions.

Smallest repair: give the manifest an exact key/schema contract and have the
checker compare the full parent identity, root, eleven-context ledger,
first-six restriction receipt, `L/U/G`, seed count, positive grade-one gates,
member count, lower gate, dimensions, rho2 receipts and all false/null claims
to independently recomputed or exact pinned values.  The already mandated
exact Task625 checker rerun plus byte-equal verdict may compositionally witness
the Task625 physical and Task595 MEMBER equations; another graph traversal is
not required.  Seal and check that exact verdict digest rather than accepting
bare booleans.

### F644-7 — the 149 MB receipt is rebuilt in memory and the declared caps are inert

Both consumers first stream-hash `source-ancestry.json`, then read all
149,359,882 bytes again and `json.loads`/canonicalize it
(producer 164, 168-169; checker 210, 213-214).  The parsed object is unused by
the live consumer after Task643 removed graph traversal.  This is precisely
the hidden production-sized copy prohibited by Task640 Section 6.

In addition, the workflow declares `TASK640_PATH_CAP`, `TRIE_CAP`,
`STATE_CAP` and `RECORD_CAP` at lines 23-26, but neither executable reads any
of them.  Task643 explicitly retained Task640's resource gates.  Exact parent
sizes happen to bound this run, but dead environment declarations are not the
required fail-closed adjustable caps.

Smallest repair: retain only the streaming digest and the already accepted
ancestry receipt/header binding; do not load or canonicalize the ancestry
JSON, and use the authenticated digest in the output checks.  Wire the record
cap into `R07LEAF1` parsing and the path/trie/live-state caps into their actual
counters in both programs, with `UNKNOWN_RESOURCE` on exhaustion.  No dead
graph traversal needs to be restored.

### F644-8 — the mandatory live-predicate fixtures are absent

Producer `selftest` at lines 269-280 and checker `fixture_rejects/selftest` at
lines 258-276 and 344-356 mostly compare toy tuples, tiny lists, or unequal
byte strings and call `fail` themselves.  Apart from the leaf parser and a
standalone claim dictionary, they do not route mutations through the live
E3/E4, all-seven, trie, dense, root, parent and payload validators.  The
required slot-1/5, E3/E4, sign/inverse/PP/block/prefix/multiplication-order,
failed-seed, root, target/lower/top/packing and receipt mutations are therefore
not release-tested.

Smallest repair: add bounded tiny fixtures which invoke the same live
predicates used by production and reject the Task640 Section 5 mutation list.
They need not contain production-sized roots, rows, or ancestry.

## Scope and claim boundary

Task643's compositional acceptance remains valid: the dead
`recompute_leaves`/`independent_leaf_replay` definitions are not called, the
source graph remains bound by its exact receipt, and a repaired route need not
duplicate Task625's graph traversal.  Producer-side use of the exact-pinned
v12f all-seven owner is permitted.  The frozen dimensions 32,260 / 48,384 /
12,096, immutable action SHAs, serial layout, 120-minute job, external process
guards, success-only residual upload and always-step log upload are not the
source of this FAIL.

This audit establishes no `rho2`, grade-two MEMBER/NONMEMBER, A0,
order-54,432/full-Q0, COMMON, cofinal lift, FAKE, IHARA, cross-checking, or
Lean verification.  A repaired and newly hashed quartet requires a fresh
bounded static re-audit before dispatch.
