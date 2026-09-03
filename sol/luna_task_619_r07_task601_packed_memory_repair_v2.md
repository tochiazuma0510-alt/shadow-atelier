# Luna Task619: bounded packed-memory repair of Task601

Role: Luna implementation.  This is a resource repair of the already audited
Task601 mathematics, not a new search.  Read Task618 in full before editing:

- `sol/sol_reply_618_audit_r07_task601_memory_terminal_v1.md`
  (`e97c2cfc3e7c02ec385245f670335088fe42f128ae3b2ba0c96dd4b46bbdcc88`).

Run `33717064826` at
`69e95d7fc50f04691a41417c495e27f7064f470d` ended after 421 seconds with a
producer `MemoryError`; it produced no payload and no checker result.  Repair
only the materialization and object lifetimes described below.  Do not run a
full route, production, GHA or git.

## 1. Exclusive edit scope

Edit only these existing four files:

1. `search/d972_r07_a0_grade1_selected_slp_v1.py`;
2. `search/check_d972_r07_a0_grade1_selected_slp_v1.py`;
3. `.github/workflows/d972-r07-a0-grade1-selected-slp-v1.yml`;
4. `sol/luna_reply_601_r07_grade1_selected_slp_v1.md`.

Do not create a new framework, router, proof, workflow, task or reply.  Report
all final byte counts, line counts and SHA-256 values in the existing Task601
reply.

## 2. Frozen mathematical obligations

All of the following remain exact and complete:

- all 8,059 offers in the registered order;
- 2,014 old/lower offers and 6,398 grade offers;
- ranks 1,661 and 5,044;
- the 3,317 Task595 MEMBER coefficients and zero remainder;
- every physical node, ordered reduction edge, origin, stored row, companion
  row and old-lower-zero receipt;
- the reverse least selected physical closure;
- the unique canonical selected source graph built only from selected physical
  refs, its expressions and literal dictionary;
- roots `C_<1`, `C_T`, `C_1` and every existing false/null claim gate;
- a complete independent reroute of all 8,059 offers by the pinned standalone
  router and the final basis/MEMBER comparison.

No sampling, changed pivot order, smaller roster, weaker equality, trusted
producer transcript, raised memory/time limit, or mathematical NONMEMBER
interpretation is allowed.

## 3. Producer: one compact physical representation

During routing append every `<HB` reduction directly to final `bytearray`
edge streams.  Append origin/stored/companion/old-lower-zero packed rows to
their final byte streams.  Do not retain tuple edge lists, lists of separate
row `bytes`, or later `b''.join` copies.  Small node records may remain mutable
through MEMBER and reverse closure, then must be packed once and accessed by
fixed-width indexed accessors.  Release route-only Python node records,
unselected source descriptors, `lower_comp`, owners, matrices and other
temporaries immediately after their last use.

Do not parse and retain four block JSON bodies simultaneously.  Authenticate
and route one character block, retain only compact `(logical, kind,
character/block, pivot)` source descriptors, then release its owner and body.
After the selected origin set is known, make at most one second authenticated
pass per character to copy the selected canonical DAG closure.  Never reload a
block per selected origin.  Preserve and check the four parent digests.

## 4. Producer: remove states, retain exact leaf receipt

Delete the quotient-specific `derived.states` history and all accumulated
child dictionaries.  The live coalescing `pending` map may pop one state,
expand it and discard it.  Keep numerical processed/pending/maximum-path
counters only.

Retain the complete coalesced exact leaf result, sorted canonically by
`(seed, freely reduced signed-letter path)`, as a separate compact binary
receipt.  Use a fixed documented header/version and length-prefixed records
containing seed, coefficient, path length and signed `int8` letters.  The
stream must be uniquely decodable and reject zero coefficients/letters,
trailing bytes, duplicate/out-of-order keys and non-reduced adjacent inverse
pairs.  Bind it to the exact `source-ancestry.json` SHA-256 and mark its
metadata

```text
quotient_specific_evaluation = true
common_source_witness = false
states_exported = false
```

without a digest cycle.  `source-ancestry.json` may carry the fixed leaf
filename/schema/flags but not the leaf contents; the leaf stream header or a
small canonical side record then binds the already computed ancestry digest.
Add the leaf receipt to the manifest's authenticated files.  It is a derived
comparison receipt, never the authority for the canonical graph.

Do not materialize the leaf table as JSON or make a second whole-stream copy
merely to hash it.  Write/hash compactly.  Preserve the exact root emission
order and complete leaf semantics of the current recurrence.

## 5. Checker: independent compact replay

Authenticate each payload receipt once.  Parse the canonical ancestry JSON
exactly once and pass that object through all validators; do not parse it
again to fetch `structure`.  There is no `derived.states` field to trust or
validate.

Use raw bytes/memoryviews and `struct.unpack_from` (or an equivalent zero-copy
fixed-width view) for node/edge access.  Never construct `gedges`, `ledges`,
`gedges+ledges`, or Python expected edge/row lists.  Check coefficients,
intervals, acyclicity, reverse closure and selected physical replay through
indexed iterators.

Independently recompute the entire exact leaf map from the authenticated
member roots, physical recurrence and independently checked canonical source
graph.  Do not call or import the producer implementation.  Encode the result
with the checker's own compact encoder and compare the complete canonical
leaf stream byte-for-byte, including its ancestry binding and flags.

Run sealed canonical/source and selected physical-origin replay first,
grouped by character with one block body and one owner live.  Release each
body/owner after its character and release all checker-side block caches
before loading the standalone router.  Only then perform the independent
all-8,059 reroute.

In that reroute compare each accepted node, ordered edge and packed row online
against the authenticated candidate stream with exact cursors.  At terminal
require exact exhaustion of every node/edge/origin/stored/companion/zero-row
stream.  A single compact expected `bytearray` is acceptable only if online
comparison is impractical; Python tuple/row lists and final joins are not.
The independently built final basis and its pinned SHA remain mandatory.

## 6. Diagnostics and resource contract

Add a small phase reporter to producer and checker.  Each normal record has
monotonic elapsed seconds, current Linux RSS from `/proc/self/statm`, peak RSS
from `ru_maxrss`, and only relevant cursors/counts.  Required producer phases:

- prepare/old complete;
- each block routed and released;
- route, MEMBER and physical closure complete;
- packed physical temporaries released;
- adjoint progress every 65,536 expansions (processed, pending, leaves,
  maximum path length);
- canonical graph/leaf sealed;
- payload sealed.

Required checker phases:

- receipts and the single ancestry parse complete;
- each character selected replay and release;
- before standalone router;
- each old-character/block boundary during the independent reroute, with all
  relevant stream cursors;
- basis/MEMBER complete;
- verdict sealed.

No per-row logging.  Reserve a small emergency buffer at process start.  A
`MemoryError` handler must first release it and then use `os.write(2, ...)` to
emit one bounded ASCII diagnostic containing the last phase/RSS/cursors and
return nonzero as `UNKNOWN_RESOURCE`; do not build JSON while exhausted.

Keep the current 60-minute job, 8-GiB VM/7-GiB internal RSS envelope and
producer/checker timeouts.  Change only the workflow fire marker to
`[fire-grade1-selected-slp-v2]`, refresh exact file SHA gates after the quartet
is stable, and retain the success-only payload/verdict upload plus
always-uploaded logs.

## 7. Small local gates only

Run serially:

```text
python -B -m py_compile <producer> <checker>
python -B <producer> --selftest
python -B <checker> --selftest
```

Extend the existing small fixtures only enough to cover compact leaf
round-trip/order/mutation, absent `derived.states`, zero-copy transcript
cursor exhaustion, and false/null claim gates.  Parse the YAML and inspect its
pins/marker statically.  Do not run the real route locally.

The reply must state exactly what was removed, what evidence remains, the
normal/selftest results, frozen counts, workflow marker, and `NOT_RUN` for
production/GHA/git.  A fresh Sol(max) static audit is mandatory before root
may make the one justified GHA rerun.
