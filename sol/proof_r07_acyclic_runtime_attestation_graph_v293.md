# R07 acyclic runtime attestation graph (v293)

## 0. Status and purpose

This note fixes the provenance graph used by the current A0 bootstrap and A4
successor-kernel implementations.  It is a finite, syntactic attestation
lemma.  It does **not** prove that either implementation is correct, does not
authorize SELFTEST or production, and does not change any v220 numerator.

The defect removed here is a cryptographic construction cycle: a driver cannot
contain the SHA-256 of its own final physical bytes while that very literal is
part of those bytes.  Searching for such a SHA-256 fixed point is neither a
bounded build procedure nor an acceptance condition.

## 1. Physical identities and dependency edges

For a physical file `F`, write

```text
I(F) = (repository-relative path, byte length, SHA-256 of the exact bytes).
```

Write `A -> F` when the final bytes of `A` contain the expected value `I(F)`
and runtime acceptance of `A` compares the opened physical bytes of `F` with
that value.  A source that contains only a fixed path, schema name, and field
roster for a later manifest does not have such an edge: it has no physical
digest of that manifest.

Every finite build must orient the physical-identity edges from a later-built
owner to an earlier-frozen owner.  Thus the graph of `->` edges must be a DAG.
In particular, `F -> F` is forbidden.

Canonical self seals are different.  A JSON owner may contain

```text
self_digest_sha256 = SHA256(canonical JSON of the object with this field removed).
```

This is noncircular because its operand is explicitly the body without the
seal field.  It authenticates internal transport integrity, not the external
physical identity `I(F)`.

## 2. Acyclic source/manifest/driver construction

Let `P`, `C`, and `X` be the final producer, independent checker, and fixture.
Let `M` be an optional static manifest and `D` the GAP driver.  The admissible
construction order is

```text
freeze P,C,X
      |
      v
build M containing I(P), I(C), I(X) and frozen authority identities
      |
      v
build D containing I(M), I(P), I(C), I(X)
      |
      v
bind I(D) by the immutable git commit and workflow run; report I(D)
```

The programs may name `M` and validate its schema, source-field roster, and
their own entry after opening it, but they must not hard-code `I(M)`.  The
manifest must not contain `I(D)` if `D` contains `I(M)`.  The driver must not
contain `I(D)`.

When no separate manifest is authorized, the shorter admissible graph is

```text
freeze P,C,X -> build D containing I(P),I(C),I(X)
             -> bind I(D) by immutable commit/run and report I(D).
```

This is the correct graph for A4-v5.  Therefore the driver's runtime pin table
contains the producer, checker, fixture, and frozen authorities, but not the
driver itself.

For A0-v12a, `M=P0` preregisters only the already frozen source/fixture and
authority identities.  It may use placeholders for future candidate receipt
and verdict identities because neither artifact is accepted at v12a.  The
driver is built after `P0` and pins it; `P0` does not pin the driver.

## 3. Receipt and verdict edges

After execution is authorized, a deterministic candidate receipt `R` may
record the runtime-recomputed identities of `P,C,X,M,D` and all frozen input
owners.  This creates edges `R -> P,C,X,M,D`, but none of those earlier files
contains `I(R)`.  An independently generated verdict `V` may then bind the
exact physical and semantic identity of `R`:

```text
P,C,X -> M -> D -> R -> V.
```

The last sentinel is written only after `V` is sealed and nonempty.  It owns
no mathematical fact and is not an alternative source of any digest.

If a later production version must preregister exact `I(R),I(V)`, it is a new
version built after the candidate artifacts have been generated and audited.
It cannot rewrite the old manifest in place.

## 4. Tamper-detection lemma

Assume:

1. the checkout commit and workflow run are immutable external roots for
   `I(D)`;
2. every `A -> F` comparison opens `F` under the registered repository path,
   rejects traversal and links/reparse points according to the platform
   contract, and hashes the same opened handle whose identity it rechecks;
3. canonical self seals are recomputed after parsing with the seal field
   removed; and
4. SHA-256 collision or second-preimage attacks are outside the registered
   finite threat model.

Then replacing any node reachable from `D` changes the first incoming
physical-identity comparison, unless the replacement has identical physical
bytes.  Replacing `D` changes the externally rooted commit/run identity.
Hence every physical owner in the DAG is bound without a self-hash fixed
point.

Proof.  Topologically order the finite DAG.  For a replaced nonroot node take
the earliest incoming edge from an unchanged predecessor in the rooted
reachable subgraph.  Its length or SHA comparison fails.  If every predecessor
was also replaced, ascend toward the root; finiteness ends at `D`, whose
external identity fails.  Canonical self-seal checks separately reject an
unresealed internal change.  No step uses a cyclic expected digest.  QED.

## 5. What the lemma does not establish

This lemma establishes only an auditable, constructible identity graph.  It
does not establish:

- that the ordinary mathematical validators are sound or independent;
- that a mutation reaches its claimed first validator/reason;
- that a checkpoint is replayable or resource accounting is correct;
- that SELFTEST, production, COMMON, A4 closure, a compatible lift, fake, or
  an Ihara counterexample exists.

Those remain subject to the existing Sol(max) audit and GHA gates.

## 6. Mandatory implementation checklist

1. No runtime pin table contains the physical identity of its own file.
2. A manifest pinned by a driver does not contain the driver's identity.
3. Programs which read that manifest hard-code only its path/schema contract,
   not its physical SHA.
4. Exact source/fixture identities are frozen before the manifest/driver.
5. Exact receipt/verdict identities are frozen only in a later version after
   their audited generation.
6. The reply records all final physical identities and the immutable commit;
   a GHA reply additionally records run id and commit SHA.
7. A self seal is always labelled as a canonical-body seal, never as the
   physical SHA of the file containing it.

`R07_ACYCLIC_RUNTIME_ATTESTATION_GRAPH_V293`
