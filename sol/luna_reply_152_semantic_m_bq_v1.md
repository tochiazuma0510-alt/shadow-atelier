# Luna reply 152 — semantic-M finite receipt v1

## 結論

The semantic-M binding is now fail-closed and versioned.  It does not call
`IsomorphismFpGroupByGenerators`, construct an infinite PB3 quotient, or trust
an operator-supplied digest/boolean.  An actual GHA calibration must emit the
finite GAP marker before the campaign can unlock; no local GAP was run.

## Exact finite marker

`search/check_d972_dovetail_v2.py` builds the frozen marked permutation BQ and
prints exactly one `D972_SEMANTIC_M` marker.  The marker contains the six
orders

```text
|K9_pure|=2916, |PSL(2,8)_pure|=504, |M|=1469664,
|BQ|=8817984, |ker(epsilon)|=1469664, [BQ:M]=6.
```

Before printing, GAP independently checks `Size(pureK9)=2916`,
`Size(purePSL)=504`, `Size(pureJoint)=Size(pureK9)*Size(purePSL)`, both
component projection homomorphisms are onto, `epsilon:BQ -> S3` is onto, and
the generators of `pureJoint` lie in `Kernel(epsilon)` with equal kernel/order
(hence exact subgroup equality).  It also compares both sides of the Artin
bridge using the worker's `PaperProd` convention:

```text
x12=s1^2, x13=s2*s1^2*s2^-1, x23=s2^2,
PaperProd([x12,x13,x23]) = PaperProd([s1,s2,s1])^2,
```

and checks both central relators in BQ and in each component.  The marker now
has 11 raw booleans (bridge, centrality, component relators, two projections,
joint order, epsilon, exact kernel, full order, and reverse-conjugate
orientation canary), all required to be `true`.

The parser stores the complete raw token vector in the receipt and recomputes
`marker_sha256` from it.  It stores the calibration q-relator digest and the
canonical 972-target-key digest as well.  At every unlocked checkpoint and at
final-A sealing, the v2 checker requires these two digests and
`source_script_sha256` to equal the corresponding independent calibration
receipt fields.  Thus a resealed semantic receipt cannot be detached from the
same q-relator/target/script calibration that produced the state.

## State and code binding

The calibration transition inserts `state.receipts.semantic_m_binding`; an
unlocked resume validates it, and final-A sealing includes its digest and
receipt schema.  The semantic checker and manifest are included in the v2
runtime code binding.  The state schema rejects terminal witnesses and active
cursor/ledger rows below `k=8`; its repaired `k_ledger.prefixItems` applies the
full row schema and the `k=8` constant to the first row.  The v1 seed manifest
contains the exact `skipped_prefix` contract for frozen k=3..7, with no B or
completeness authority.

## Static evidence and blocker

Executed without GAP:

```text
python -B -m py_compile search/check_d972_dovetail_v1.py search/check_d972_dovetail_v2.py search/check_d972_semantic_m_v1.py search/d972_dovetail_producer_v2.py search/check_d972_dovetail_v3.py
python search/check_d972_semantic_m_v1.py --self-test
python search/check_d972_dovetail_v1.py --self-test
python search/check_d972_dovetail_v2.py --self-test
python search/d972_dovetail_producer_v2.py --self-test
python search/check_d972_dovetail_v3.py --self-test
```

All passed.  The synthetic parser cross-check also passed with the 18-token
marker, including source-digest binding; the forbidden infinite-PB3 API scan
was clean.  Schema SHA-256 is
`945ca3b20ac6f9efe5199756567569b73b3d768932dd60fed3fbcc0f120443c1`, and the
v2 manifest/v3 anchor pair remains
`e3214710442d7a6755939c001b76993eb3899fa5e727503c6edf304690527455`.

Evidence count for this lane: A witnesses `0`; B/completeness witnesses `0`;
GHA finite semantic receipts `0` (the marker has not been executed here).
The static selftests are implementation evidence only.  Therefore terminal A
remains blocked until GHA emits and independently parses the raw marker,
followed by the existing exact direct-BQ candidate zero-fiber postcheck.

No workflow YAML, GAP run, commit, push, or dispatch was performed.
