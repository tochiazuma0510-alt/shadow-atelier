# R07 checker-local preselection carrier theorem (v299)

## 0. Scope

This note closes a narrow gap between v278 and v296.  The current A0-v12a
draft correctly reconstructs the selected Q0/Gamma/K0/dual statement on the
checker side, but its candidate `H_check` still copies the producer receipt's
preselection `heavy_public` object.  Task353 explicitly forbids that object or
its digest from being an authority.

The repair below does **not** require the checker to construct a second copy
of all ten 1,469,664-state runtime tables.  It separates the producer's
internal search-completion summary from the finite acceptance carrier which
both sides can derive from independently opened frozen owners.  This is a
paper theorem only.  It does not accept v12a, authorize execution, prove A0
COMMON, or construct a lift, fake, or Ihara witness.

## 1. Runtime completion is not an acceptance premise

Let `RunPre` denote the producer's internal summary of the complete heavy
search image: Q0 state and parent tables, ten coordinate stores, all family
membership bitsets, duplicate-edge accounting, shared proofs, and lazy K0
index metadata.  `RunPre` is useful for proving that the producer ran its
registered search algorithm.  It is not by itself an independently checked
mathematical authority.

Let `T176` be the canonical task176 receipt opened from its registered path,
together with its manifest, crosscheck verdict, recovery-v2 manifest, exact
physical identities, canonical self seal, and the source/code identities to
which that chain points.  The accepted task176 chain already owns the complete
Q0 roster and parents/letters, the 243 full ten-coordinate Gamma states and
parents/records, every registered family membership bitset, the literal
`A`-family tables, word generators, deletion data, and their exact typed
metadata.

V278 proves that an accepted positive word depends on the actual target and
the selected nonzero rows and correction factors, not on unselected discovery
rows or the producer's search trajectory.  Consequently a positive checker
must replay the complete selected statement, but it need not reproduce an
unselected global search image merely to obtain the same digest as the
producer.

## 2. Canonical authority projection

For an independently opened and validated task176 chain define
`OwnerPre(T176)` to be the following canonical projection.  Every list is in
the order fixed by task176; every mapping is encoded as sorted ASCII JSON.

```text
OwnerPre(T176) = {
  schema: "r07-a0-checker-local-preselection/v1",
  physical_chain: {
    task176_receipt, task176_manifest, task176_crosscheck,
    task176_recovery_v2
  },
  q0_owner: {
    order,
    canonical_roster: (raw_bytes, raw_sha256, record_count, record_width),
    parents:          (raw_bytes, raw_sha256, record_count, record_width),
    letters:          (raw_bytes, raw_sha256, record_count, record_width),
    marked_generators,
    complete_presentation_relators_sha256
  },
  gamma_owner: {
    order,
    ten_coordinate_states:
        (raw_bytes, raw_sha256, record_count, record_width),
    parents: (raw_bytes, raw_sha256, record_count, record_width),
    records: (raw_bytes, raw_sha256, record_count, record_width),
    record_words
  },
  family_owners: [
    (name, coordinate_indices, A_order, L_order,
     membership_bitset_metadata,
     A_literal_table_sha256,
     canonical_word_generator_digest)
  ],
  deletion_owner_sha256,
  primitive_registry,
  algorithms: {
    task176_decoder,
    selected_k0: "v295-full-state-open-address-first-gid-bfs",
    canonical_json,
    digest_framing
  }
}.
```

Here `physical_chain` contains `(registered logical path, bytes, SHA-256,
canonical self seal where present)`, never a producer-supplied digest.
`membership_bitset_metadata` contains the typed raw and compressed byte
lengths/digests/count/width from the opened task176 owner.  The decoder must
check those values against the decompressed bytes before forming the
projection.  The word-generator digest is computed from the canonical opened
subobject, not copied from A0's receipt.  `primitive_registry` is the sorted
physical registry opened by that side, including q3, E3/E4/joint, raw,
recovery, task176 code, and the task176 chain.

Define

```text
h_owner = SHA256(canonical(OwnerPre(T176))).
```

The producer and checker each construct this object from their own opened
handles and their own composite constructor.  They may share the versioned
field schema and frozen primitive meanings; they may not share an A0
constructor or read `OwnerPre` from R.

## 3. Selected carrier and final identity

Let `Sel(r)` be exactly v296's selected statement.  In particular it includes
the selected complete Q0 state and ten-coordinate state, the selected complete
Gamma state and parent word, the selected-coordinate v295 K0 state/slot/public
digests, the exact kernel BFS and cursor, the active dual and pairing, and the
direct correction replay.

The load-bearing final carrier is

```text
H* = {
  schema: "r07-a0-final-heavy-carrier/v2",
  p0,
  sources,
  frozen_authorities,
  algorithms,
  preselection_owner: {
    public: OwnerPre(T176),
    sha256: h_owner
  },
  selected_statement: Sel(r)
}.

h_final* = SHA256(canonical(H*)).
```

The producer may expose `RunPre` separately as candidate diagnostic or search
completion evidence, and may require its recomputed Q0/Gamma/family digests to
agree with the corresponding opened task176 owners.  `RunPre` is not inserted
into `H*`.  Thus changing runtime accounting cannot silently change the
mathematical identity, while changing an authenticated owner or the selected
statement necessarily changes `H*`.

## 4. Independence and sufficiency theorem

### Theorem 4.1

Assume:

1. the complete task176 physical chain and canonical self seals are accepted;
2. producer and checker separately open and validate that chain and construct
   `OwnerPre` as in Section 2;
3. the checker independently reconstructs and validates every field of
   `Sel(r)` as required by v295/v296;
4. the final selected-support equality and word/boundary side gates of v278
   pass; and
5. the P0/source graph and physical receipt binding satisfy v293/v296.

Then equality

```text
OwnerPre_check = OwnerPre_producer,
Sel_check       = Sel_producer,
H*_check        = H*,
h_final_check   = h_final*
```

binds the accepted explicit positive candidate to the same frozen global
owners and the same actual selected Q0/Gamma/K0/dual correction, without
copying producer `heavy_public` and without rebuilding all unselected ten-
coordinate tables on the checker side.

### Proof

By (1)--(2), each `OwnerPre` is a deterministic function of independently
opened physical bytes and checked decompressions.  Canonical equality
therefore identifies the same task176 global owner chain, rather than a value
asserted by R.  By (3), equality of `Sel` identifies the selected full states,
least Q0/Gamma base, K0 table and kernel cursor, active dual, and correction
replay through checker-local computation.  By v278 and (4), unselected search
states are not premises of the accepted positive equality; they can affect
which candidate is proposed but cannot make a false selected equality pass.
Condition (5) binds both composite constructors and the physically opened R.
Canonical equality then gives equality of `H*` and its digest.  No second
global Q0 enumeration is used in any inference.  QED.

## 5. Mutation and cost consequences

1. A mutation of a task176 chain owner, its decoded Q0/Gamma/family metadata,
   or its physical identity is rejected while constructing `OwnerPre`, before
   selected correction acceptance.
2. A mutation of selected Q0/Gamma/K0/kernel/dual/correction data is rejected
   by checker-local `Sel` replay.  Resealing R cannot replace either route.
3. The checker builds the selected v295 coordinate table at most once and
   reuses its cached state/slot/public digests across mutation cases.  It does
   not build the other nine coordinate tables merely to hash producer search
   telemetry.
4. The opened task176 receipt and decoded immutable blobs are parsed once per
   side.  Mutation validators compare candidates with the frozen canonical
   projection; they do not reopen or decompress the 13-MB owner per row.
5. The ordinary producer can still require complete `RunPre` before proposing
   a correction.  This theorem removes work only from independent acceptance;
   it does not weaken the registered producer search.

## 6. Mandatory A0-v12a repair

- Reject any construction of `H_check` whose preselection body or digest is
  read from `receipt.heavy_public` / `receipt.heavy_input_sha256`.
- Construct and seal `OwnerPre_check` before reading the selected carrier from
  R; then independently replay `Sel` and compare the two final canonical
  objects.
- Either migrate H to the v2 schema above, or make v1's
  `preselection_heavy.public` exactly this authority projection.  In both
  cases the producer's complete runtime `heavy_public` must be kept outside
  the load-bearing final carrier.
- A self-hash test
  `SHA256(canonical(receipt.heavy_public)) == receipt.heavy_input_sha256` is a
  useful transport check but is not an independence proof.
- Record exact source lines and a static one-pass cost formula in the v12a
  reply.  Fresh Sol(max) audit remains mandatory before GHA.

```text
CHECKER-LOCAL GLOBAL OWNER CARRIER:       PAPER PROOF
SELECTED-STATE ACCEPTANCE SUFFICIENCY:    PAPER PROOF (v278 + v295 + v296)
SECOND TEN-COORDINATE GLOBAL BUILD:       NOT REQUIRED
PRODUCER HEAVY_PUBLIC AS AUTHORITY:       FORBIDDEN
V12A IMPLEMENTATION / AUDIT / GHA:        PENDING
ACTUAL A0 COMMON:                         0/1
LIFT / FAKE / IHARA:                      NONE
```

`R07_CHECKER_LOCAL_PRESELECTION_CARRIER_V299_PAPER_GRADE`
