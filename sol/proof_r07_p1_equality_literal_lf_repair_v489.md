# R07 P1 equality literal-LF repair v489

## Scope

This note classifies the only failure reached by the actual Task729 semantic
prepare run `33811487696/1` (head
`b805d4089d76ca98b3bbbc63594ce053ec90e5fa`).  The run authenticated the
Task554 parents, rebuilt all four old blocks, and compared the record, lower
basis and lifted-grade bytes before stopping at `equality_record_pin`.

The failure is not a new mathematical mismatch.  It is a finite pin-extraction
encoding error in
`search/d972_r07_grade2_p1_componentwise_semantic_replay_v4.py`.

## Authenticated source and exact diagnosis

Artifact `9865061266`,
`task554-grade1-v3-prepare-33677346616-1`, contains the canonical body

```text
prepare.1f191d88a0453360021ec57d253a7d16c9a66ac059ddaaadb6db3e2b9293c865.json
```

whose recomputed SHA-256 is exactly the digest in its sealed `prepare.HEAD`.
For canonical JSON bytes `C(r)` of each `old_blocks[i].record`, v4's live
`canonical` function hashes `C(r) || 0a`.  The four correct hashes are

```text
0  5b3f5dfd965861f33ec9cb2c2ac2e7401629b73b3571491110d063f47398cb4f
1  75aa31bfcd4ec622ff985afb6e92bfa16707206508683b012eeb9be1ab2544a6
2  d732aa55163be06b50199d864761ec0f1eeb5f29fcea171d4e674616c40d7e75
3  ad89a5738a65e6b1340816534b4dca8b82d3127ae82765a718eec6f6a1025022
```

The four v4 literals instead equal `SHA256(C(r) || 5c 6e)`: the extractor
hashed the two ASCII characters backslash and `n`, not one LF byte.  The lower
and lifted blob literals are already exact and require no change.

With the four corrected record hashes, the canonical equality-list digest is

```text
e04c0d8de2cfbd264d3c93d915dc19e613a001c5278c8efdb704f06d1abb3565
```

namely `SHA256(C(equality) || 0a)`.  The old aggregate literal
`99da0c4a42a0c747cde28cd91797d7c655d797c27f8f78a7423142bf56bc5dbf`
is internally consistent only with the four wrong backslash-`n` record
hashes.

## Finite repair and claim boundary

A producer v5 may change only the four `record_sha256` literals and
`EQUALITY_SHA` above, plus version comments.  No source universe, record,
lower basis, lifted grade, projector, DAG, packet, arithmetic, resource path,
or claim flag changes.  The independent checker must be versioned only to pin
the new producer path/SHA; it already recomputes record hashes through its own
canonical-LF function and must not import these literals.

The fixed run must still rebuild the four records and compare all bytes; the
artifact-derived literals do not replace replay.  Success remains a candidate
semantic receipt requiring the independent checker.  It proves neither the
degree-two lift nor A0/COMMON/cofinal/fake/Ihara.

```text
CLASSIFICATION=FINITE_LITERAL_LF_REPAIR
P1_SEMANTIC_REPLAY=NOT_YET_ACCEPTED
A0/COMMON/COFINAL/FAKE/IHARA=NOT_DECLARED
verified=false
```
