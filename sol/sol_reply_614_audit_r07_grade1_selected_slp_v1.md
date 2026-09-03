# Task 614 — final static audit of Task601 selected SLP

## Verdict

`PASS_AFTER_REPAIR`

The frozen routing and selected physical-replay path is structurally sound,
and the exact quartet matches the commissioned SHA-256 values.  The producer
routes and proves the 8,059/1,661/5,044/3,317 terminal facts before creating
the payload, the checker has a genuinely standalone full-route comparator,
and the scale, sign, lower-link, companion and root orders agree with v469.

Release nevertheless needs four small, load-bearing repairs.  The current
canonical source table contains expressions which are not reachable source
dependencies; the checker does not bind the semantic roots path to the roots
receipt and does not gate the false/null claim fields; frozen v3 is executed
before its hash is checked; and the required mutation fixtures and reply byte
receipts are incomplete or stale.  These are local repairs, not a request for
a new framework.

This is only a static audit.  I did not run production, GHA, git, or a local
8,059-row route.  Nothing below is an execution receipt, a cross-check claim,
or Lean verification.

## Inputs and exact receipts

I restarted from the current files and read every numbered input in full.

| input | bytes | lines | SHA-256 |
|---|---:|---:|---|
| `sol/sol_task_614_audit_r07_grade1_selected_slp_v1.md` | 4,250 | 69 | `ce4a1a3d8154cd5b38def1e2ff00418b18afb8cc741be6013dd1ec9cf0d7f0d5` |
| `sol/luna_task_601_r07_grade1_selected_slp_extraction_v1.md` | 5,347 | 101 | `3d4c069c0800454bf03866f6ae682fb7608cfab43b9a8f91bc0776b0f5575ced` |
| `sol/luna_task_608_r07_grade1_selected_slp_unique_structure_repair_v1.md` | 3,824 | 75 | `e77e9db4f02aaea5502be8968009665f1955598ee74466f5fa166ab2ea7d933f` |
| `sol/proof_r07_canonical_selected_dependency_slp_v468.md` | 12,016 | 284 | `b1e0f09ae0c6f136804e37bc8db8cba85bccede0880ed5f26afed880d28829a6` |
| `sol/sol_reply_607_audit_r07_canonical_selected_dependency_slp_v1.md` | 13,098 | 274 | `2a7165dcde06a7fc0ef7df064185a128a7c7596c3a0571f1a4b21079e8960008` |
| `sol/proof_r07_canonical_selected_dependency_slp_physical_replay_v469.md` | 8,865 | 234 | `bae6864e6f00f65bfd3ff18a4c5676d5afe190ad0f2c6ffaf83cd9683d3f26f6` |
| `sol/sol_reply_609_audit_r07_canonical_selected_slp_physical_replay_v1.md` | 8,455 | 179 | `f9f8fcf088e17d81a4980332aac22d04c3723f648984de91b0577ca028e1837f` |
| `search/d972_r07_a0_grade1_selected_slp_v1.py` | 26,549 | 240 | `7ef865a3f55741d8d4c06f66440f3234923d7134aead73ec4e17437a48dc0104` |
| `search/check_d972_r07_a0_grade1_selected_slp_v1.py` | 52,043 | 572 | `e6e368a204d24690c7be117c2afd019d92cbe3bc9b822cdceedf06311e5556b2` |
| `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml` | 5,381 | 110 | `cc5ef08877c0380b40478b0d0ba4ef9e08a1f0c3299aab1d445cced322e8069d` |
| `sol/luna_reply_601_r07_grade1_selected_slp_v1.md` | 3,669 | 63 | `ad54bca1280910411d26b9a49d300144d3c6f0984d5e2e9631b75b3be9b54841` |

The independently authored router used by the checker is
`crosscheck/check_d972_r07_a0_first_rung_grade1_full_routing_v2.py`, 27,778
bytes, 399 lines, SHA-256
`a0504ae6a2562aab3b9af5ba7ed672bcc87bbd1cfdf5cc9fd3489240e51008e3`.
It imports neither the Task601 producer nor its parser/serializer and contains
its own arithmetic, aggregation and packed-echelon implementation.

## Audit of the eight release conditions

### 1. Frozen route and physical transcript — pass

The producer authenticates the exact decision and sealed prepare/four-block
parents, reroutes old offers followed by the four block owners, and requires
before `out.mkdir` that

```text
cursor / lower rank / grade offers / grade rank = 8059 / 1661 / 6398 / 5044
basis SHA-256 = b562c980c22a25a932bae1b548f72aeede5637b9612afc908fff9a9aecff069d
MEMBER coefficient list = the exact decision list of length 3317
remainder = the authenticated zero remainder
```

Lower acceptance applies its scale to both the lower pivot and grade
companion.  An old grade origin subtracts the ordered lower companions before
the grade reducer, while the grade pivot applies its separate scale only
after its grade reductions.  Every reducer child uses the `-c` word exponent,
so coefficient two has the v468/v469 inverse convention.  The old-origin
lower interval precedes the grade interval.  The former double-pack bug is
closed: `lower.rows[-1].tobytes()` is emitted directly as the already packed
stored lower row.

### 2. Canonical source graph — repair required

The block/old node closure itself is unique, deterministic and follows every
actor-parent and ordered reduction edge without scalar pruning.  It starts
from `selected_refs`, and the checker independently derives an exact expected
key/record set from those refs rather than from `derived`.

The emitted expression set is not, however, the least Task608/v468 source
closure.  For every reached old projected-seed node, `old_node` adds a
`seed_reduction` expression; for every reached old actor node it adds the
entire four-entry `actor_transition_row` and links it as that node's
`expression_key`.  Neither is a child in v468 Section 2.3.  An old node uses
only its literal projected-seed or actor-parent origin and its own ordered
reductions.  Only a reached **block defect** introduces the particular
`seed_reductions[seed-1]` or the single
`actor_transitions[pivot][ACTORS.index(letter)]` expression.  The checker
recreates the same surplus records, so exact producer/checker agreement does
not cure the canonical-minimality error.  The block-specific
`origin_reductions[oi]` stored in a globally keyed defect record is likewise a
block insertion receipt, not a source child; it should be removed from the
canonical syntax or typed outside it as non-authoritative metadata.

Also remove the producer's second source-graph augmentation from `states`.
The current independent equality gate prevents that redundant loop from
enlarging an accepted graph, but Task608 expressly requires construction from
selected physical refs without consulting quotient-specific states.

Smallest repair: make old nodes carry only their literal origin,
actor-parent/reduction children and scale; create expression records only in
the defect branch, one exact expression per reached defect; and construct the
canonical tables only from `selected_refs`.  Mirror that definition in the
checker.  No physical route or source-word architecture changes.

### 3. Derived traversal and roots — pass

`roots` is compared with the complete ordered Task595 coefficient list, not
merely its support.  For each typed grade, lower, block, defect and old state,
the checker reconstructs the whole ordered child list and finally requires
literal list equality.  In particular the grade-old list is exactly

```text
old origin, complete lower interval, complete grade interval
```

so an inserted, deleted or arbitrary middle child cannot survive.  Transition
defects place the acted old pivot first and then the particular old-expression
children.  The coalesced leaf map is recomputed from the accepted states only
after the canonical graph has independently passed; it is not authority for
source reachability.

### 4. Independent 8,059-offer transcript — pass

The checker hashes the standalone routing-v2 source before importing it and
then independently rebuilds every old and block offer.  It compares all
lower/grade node tuples, complete ordered edge streams, scales, old lower
links, lower origins, already-packed stored rows, equally scaled companions,
grade origins, all old lower-zero receipts, and the complete routed basis.
The fixed counts are checked again.  The MEMBER equation and authenticated
zero remainder are checked only after that comparison.

### 5. Selected sealed-origin replay — pass

Selected old origins are reconstructed from the sealed lower/lift blobs and
selected block origins from a cached sealed block owner.  The lower origin is
joined with its stored packed row, and its grade companion is independently
rebuilt with the same reductions and normalization.  An old grade origin is
then rebuilt with its exact lower interval; block grade origins are rebuilt
from their sealed basis rows.  These gates all precede the MEMBER acceptance.
The code makes no source-filtration or relative-kernel inference from a zero
physical lower row.  The `direct_occurrence_replay=false` boundary is therefore
mathematically honest, subject to the missing flag gate below.

### 6. Authentication, flags and roots receipt — repair required

Most gates are fail-closed: candidate and parent digests are fixed, receipt
sizes and hashes are checked, physical grade/lower edges are earlier-pivot
acyclic, selected bitsets are recomputed exactly, and exceptions return a
nonzero rejection before a verdict is written.

There is a concrete split between the roots object which is semantically
checked and the roots receipt which is reported.  The checker reads
`payload / m['roots']`, but the verdict reports
`files['roots']['sha256']`; it never requires
`m['roots'] == files['roots']['file']`.  Canonical serialization of the
manifest does not imply that equality.  A distinct or unreceipted roots file
can therefore supply the checked semantics while the verdict names another
receipt, and `m['roots']` also bypasses the receipt filename confinement.

Moreover, neither the manifest nor roots object is checked for the required
claim boundary.  The checker never rejects mutations of
`direct_occurrence_replay`, `next_degree2_residual`, `cross_checked`,
`verified`, `A0`, `COMMON`, `FAKE` or `IHARA`.

Smallest repair: require the manifest root pointer to equal the authenticated
roots receipt filename; parse and canonical-check `loaded['roots']`; use those
same bytes for both semantic checks and the verdict SHA; and require the exact
false/null flag map in both manifest and roots.  A tiny alias/flag mutation
fixture should call this same production gate.

Finally, frozen v3 is imported and executed before its hash test in both the
producer's module initialization and the checker's selected-source replay.
The workflow declares `V3_PRODUCER_SHA256` but does not test it in the
preflight.  For this workflow, the minimal repair is one preflight
`sha256sum` equality for v3 before either Python script is executed.  Moving
the checks before `exec_module` as well makes the scripts independently safe.

### 7. Runtime and memory — pass for the stated envelope

No concrete 60-minute/8-GiB blocker is visible.  The producer loads each of
the four source blocks once.  The checker has a four-key `block_owner_cache`,
and the old-row cache likewise loads each character once; there is no
per-selected-origin block reload.  The producer materializes
`grade_basis_bytes` once and the independent checker materializes
`routed_basis` once.  There is no degree-two dense row, flat word, dual or
transition-presentation copy.  Only the selected source graph is serialized;
the fixed 8,059-entry routing metadata is transient.  Time, RSS and durable
size guards fail as `UNKNOWN_RESOURCE`/rejection rather than sealing a partial
success.

### 8. Selftests, workflow and reporting — repair required

Both current `--selftest` commands returned exit 0 in this audit, with the
reported 1 root, 8 source and 11 transcript mutations.  The checker tests do
call the same three comparison functions used by production.  Their coverage
does not implement Task608's four commissioned adversarial cases: the tiny
source fixture has no defect, transition or cancellation edge, so it does not
actually test cancellation-edge deletion, seed/transition-expression
deletion or mutation, omission of the acted old root, or per-root duplication
of one source node.  Add those four bounded mutations through the existing
production comparator, plus the root-alias/claim-flag mutations above, and
report the resulting limited counts honestly.

The workflow otherwise has the right source/candidate run and attempt,
candidate commit `93f746ad1b649796e1bc28e00ff34993498929ee`, exact-SHA
checkout, Python 3.13, NumPy 2.5.1, 40/45/60-minute and 7/8-GiB envelopes,
success marker, success-only payload/verdict artifact, and always-uploaded
logs.  Actions are commit-pinned and the current producer/checker/reply hashes
are checked.

The pinned Luna reply's byte receipts are stale: it reports producer/checker
sizes 26,535/41,468, whereas the exact commissioned files are
26,549/52,043 bytes.  Correct those two numbers and refresh the reply,
checker and workflow pins after the repairs.

```text
TASK614_STATIC_AUDIT:                         PASS_AFTER_REPAIR
FROZEN_ROUTE_AND_MEMBER_PREEXPORT:            SOUND
LOWER_DOUBLE_PACK_REPAIR:                     CLOSED
CANONICAL_SOURCE_GRAPH_MINIMAL:               NO; LOCAL REPAIR ABOVE
DERIVED_COMPLETE_CHILD_AND_ROOT_ORDER:        SOUND
STANDALONE_ALL_8059_TRANSCRIPT:               SOUND
SELECTED_SEALED_PHYSICAL_REPLAY:              SOUND
ROOT_RECEIPT_AND_FALSE_FLAG_AUTHENTICATION:    INCOMPLETE
RESOURCE_ENVELOPE:                            NO CONCRETE BLOCKER FOUND
PRODUCTION / GHA / CROSS_CHECK:                NOT RUN BY THIS AUDIT
verified:                                     false
```
