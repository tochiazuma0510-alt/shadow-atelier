# R07 post-selection heavy carrier and two-version bootstrap theorem (v296)

## 0. Scope and claim boundary

This note fixes the semantic carrier which A0-v12a must place between the
ordinary selected-correction computation and the candidate receipt/verdict
pair.  It complements the physical DAG theorem v293 and the selected-K0
reconstruction theorem v295.  It is a paper contract only: it does not accept
the current implementation, authorize SELFTEST or production, prove A0
COMMON, or construct a lift, fake, or Ihara witness.

The specific defect removed here is the use of a digest formed *before* the
selected Q0/Gamma/K0/dual state exists as though it authenticated that later
state.  Such a digest may identify the common heavy input, but it cannot
identify the actual selected correction.

## 1. Three different identities

The implementation must distinguish the following objects.

1. `preselection_heavy` is the deterministic public summary obtained after
   reconstructing the frozen Q0/Gamma authorities but before any selected
   K0 fibre or active dual is fixed.  Its digest is denoted `h_pre`.
2. `selected_statement` is the canonical claim about one actual correction.
   It contains the selected search key and every value required to replay
   that correction.
3. `final_heavy_carrier` is the canonical body which binds the physical
   authorities, code identities, `h_pre`, and `selected_statement`.  Its
   digest is denoted `h_final`.

The names and types are load bearing.  A field named `heavy_input_sha256`
which equals `h_pre` must not be accepted in a slot whose contract requires
`h_final`.  A 64-hex shape test establishes neither identity.

## 2. Canonical selected statement

For a selected correction record `r`, let `Sel(r)` be the following sorted
ASCII canonical JSON object.  Binary values are lower-case hexadecimal;
sparse maps are sorted lists of `(typed-key, nonzero F3 coefficient)` pairs.

```text
Sel(r) = {
  search_key:
    (roster ordinal, support ordinal, coordinate, target, qid, gid,
     kernel cursor),
  q0:
    (complete selected state, ten-coordinate state, parent word,
     table capacity, width, state count, build count,
     cached state digest, cached slot digest, cached public digest),
  gamma:
    (complete selected state, complete ten-coordinate state, parent record,
     parent word, first-gid roster digest),
  k0:
    (ordered generator digest, ordered BFS state digest,
     ordered BFS word digest, expected order, cursor state, cursor word),
  dual:
    (canonical active dual, dual digest, selected row, row digest,
     nonzero pairing, pivot/epoch owner),
  correction:
    (Q,c,s, weighted formula, support-hitting summary,
     base word, delta word, ten-coordinate replay, direct-column replay),
  validator_result:
    (ordinary validator schema, exact positive local predicate set)
}.
```

Every convenience digest in `Sel(r)` accompanies, rather than replaces, the
typed value authenticated by the ordinary validator.  The Q0 table digests
refer to the complete 40/154-byte states and the complete fixed open-address
slot array of v295.  The K0 state digest refers to all ten-coordinate states,
including the identity-only rosters for the registered trivial kernels.

The producer's chronological search order is not changed.  The independent
checker may read the `search_key` as an untrusted claim and reconstruct the
corresponding local fibre, but it must establish qid/gid leastness, the
kernel word, the active dual pairing, and every replay itself.  Merely hashing
the producer's `Sel(r)` is not independent reconstruction.

## 3. Final carrier

Let `I(F)=(path,bytes,SHA256)` denote the physical identity of a file.  Define

```text
H = {
  schema: "r07-a0-final-heavy-carrier/v1",
  p0: (I(P0), P0 canonical self seal),
  sources: P0's exact producer/checker/fixture rows,
  frozen_authorities: sorted registry of every opened frozen owner,
  algorithms: {
    selected_k0: "v295-full-state-open-address-first-gid-bfs",
    correction_validator: <versioned ordinary schema>,
    canonical_json: <versioned encoding>,
    digest_framing: <versioned framing>
  },
  preselection_heavy: (preselection public body, h_pre),
  selected_statement: Sel(r)
}.

h_final = SHA256(canonical(H)).
```

`sources` binds both program texts through P0; a validator-name string is not
a substitute for those physical code identities.  `frozen_authorities`
contains the physical registry rather than a copied producer digest.  `H`
contains neither its own digest nor the receipt/verdict identities.

The candidate receipt `R` must expose `(H,h_final)` at top level.  If a copy
also occurs in the SELFTEST seed, exact canonical equality with the top-level
owner is required.  The independent verdict `V` exposes its separately
constructed `(H_check,h_final_check)` and requires

```text
H_check = H,             h_final_check = h_final,
I(R) = the physically opened receipt identity.
```

The checker must not import the producer constructor.  Sharing frozen group
primitives is allowed only under their exact physical identities; the
composite `Sel` and `H_check` constructors are separately written.

## 4. One-pass digest rule

The full-state K0 index must not be rescanned once per mutation or again at
coordinate release.  During the one chronological build, maintain a
domain-separated streaming state hash

```text
SHA256("v12a-k0-state-stream/v1\0" ||
       frame(state_1) || ... || frame(state_N)),
frame(x) = uint64_le(length(x)) || x.
```

After the fixed `2^22` slot array has been built, scan that array once in
increasing slot order with an analogous `v12a-k0-slot-stream/v1` framing.
Freeze both results in immutable index metadata.  The public digest is then
the hash of bounded metadata containing those two digests, not a third scan
of the million-state payload.

### Lemma 4.1 (cached digest soundness)

Assume the full-state equality and deterministic insertion theorem v295.
Then the cached state and slot digests are deterministic functions of the
physical chronological Q0 roster.  Reusing them for later selected-record
validation and coordinate release changes no accepted value and reduces
each coordinate's digest work from one scan per query/mutation to one state
stream plus one final slot stream.

**Proof.**  The state stream is fixed by chronological replay.  V295 makes
the slot array a deterministic function of that stream.  Both framing and
scan orders are injectively specified before SHA-256 is applied.  Later
readers consume immutable arrays and the frozen results, so rescanning could
only reproduce the same bytes.  QED.

The producer may retain all ten tables under v295's exact
`1,593,346,240`-byte payload ledger or release them by coordinate after
freezing the metadata.  The checker uses v295's coordinate grouping and
builds each visited coordinate at most once.  Neither side may implement an
`A,B,A`-rejecting last-coordinate cache.

## 5. Acyclic bootstrap theorem

### Theorem 5.1 (post-selection candidate binding)

Assume:

1. v293's physical open/path/no-follow and acyclic identity conditions;
2. P0 pins the final v12a producer/checker/fixture and frozen authorities but
   uses only prospective placeholders for R/V;
3. producer and checker separately perform the ordinary validation described
   above and construct `H` and `H_check`;
4. all canonical encodings, full-state comparisons, cached digests and self
   seals pass; and
5. SHA-256 collision or second-preimage attacks are outside the registered
   finite threat model.

Then a verdict which accepts `H_check=H`, `h_final_check=h_final`, and the
physical identity `I(R)` binds one and the same actual selected
Q0/Gamma/K0/dual correction to the frozen authorities and both v12a code
texts.  No cryptographic dependency cycle is introduced.

**Proof.**  P0 is built after the three sources and is opened before the
heavy reconstruction.  `H` is built only after the selected state exists and
points backward to P0 and the frozen authorities.  R contains `H`; V is built
after opening R.  Hence the physical order is

```text
producer/checker/fixture, authorities -> P0 -> driver -> R -> V,
                                      \-> H -----------^
```

with the driver rooted externally as in v293.  There is no edge from an
earlier node to R or V and no node contains its own physical digest.
Independent ordinary replay establishes every typed component of
`H_check`; canonical equality then identifies it with the producer body.
The physical R comparison binds that body to the opened receipt.  QED.

This theorem authenticates a candidate SELFTEST carrier.  It does not prove
that the selected correction is the first global production success, that a
COMMON word exists, or that the 48+ physical mutation ledgers are complete.
Those are separate ordinary-validator, Sol(max), and GHA obligations.

## 6. Mandatory v12a implementation consequences

1. Rename or label the current pre-selection digest honestly; never expose it
   as the final selected identity.
2. Construct `Sel(r)` only after an actual K=0 selected-correction baseline
   passes and all required owner fields exist.
3. Cache K0 state/slot/public digests once; mutation validators compare the
   selected claim with those immutable cached owners rather than rescanning
   all states and slots.
4. Put `(H,h_final)` at receipt top level and require exact equality with any
   nested copy.
5. The checker parses only `SELFTEST_BOOTSTRAP`, independently rebuilds the
   ordinary baseline and every mutation ledger, derives `H_check`, and binds
   `I(R)`.  Old SELFTEST/COMMON/UNKNOWN production branches and v10 producer
   pins are not admissible in v12a.
6. R and V remain deterministic candidate-only artifacts.  V12a neither
   rewrites P0 nor claims acceptance.  Only a later v12b may pin exact R/V
   physical identities and expose production/resume.

## 7. Fixed frontier

```text
PRESELECTION / FINAL HEAVY IDENTITIES SEPARATED:  PAPER PROOF
POST-SELECTION CARRIER CONTENT:                   FIXED
ONE-PASS K0 DIGEST REUSE:                         PAPER PROOF
P0 -> R -> V ACYCLICITY:                          PAPER PROOF
V12A IMPLEMENTATION / SOL(MAX) AUDIT / GHA:       PENDING
ACTUAL A0 COMMON:                                 0/1
LIFT / FAKE / IHARA:                              NONE
```

`R07_POSTSELECTION_HEAVY_CARRIER_BOOTSTRAP_V296_PAPER_GRADE`
