# Sol(max) reply 507 — rank99 nonzero-constant global prefix v431 audit

## Verdict

`GO_FOR_IMPLEMENTATION`.

The theorem and the exact v5-to-v6 boundary are sound within the stated
tau-free, coordinates-0--2 branch.  This audit changes no mathematics and
makes no implementation change.

## Frozen inputs and bounded method

The subject pin was reproduced exactly:

```text
sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md
9592 7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4
```

The four premises also reproduced exactly:

```text
v143  5253 aae57d5481d7e649d449b58d06ade2d9cbf90fa48d50a8ae43650da5243cf259
v414  7117 ece8df53d96783a854193776abe7e03707c945220b55a5daa291d18d44e4298b
v426  9165 5c3176011ea64235196587ed19720ad5d5a5c542c2896e46fe33ef3df3a3977a
v427  6602 b958a164dfc78c77596876227b31a39467e077c9666d4a7be9033a58ee4c0ec5
```

The audited v5 call-site pins reproduced as

```text
producer 104031 25c308ec11b9f36cc9779dfec46058a4956068969d664ee582a26f9cb0db7c09
checker   71589 970ffe3a78687f3a27a222e089ae3d5e928bbfa048b9aef9f51fcf4c0b5d578d
```

I used source inspection plus one in-memory, bounded reconstruction.  It
authenticated C99, constructed a v5-valid one-segment state, changed only
top-level `schema`, `binding`, and `state_sha256`, reran the v5 prefix/segment
chain gates, then appended a synthetic next segment whose input identity was
the actual-resume lane.  Result:

```json
{"additional_rebound_field":null,"bounded_roster_pairs":4096,"historical_segments":1,"migration_changed":["schema","binding","state_sha256"],"next_segments":2,"pins":7,"status":"PASS"}
```

No production, GHA, GAP, git, or unbounded search was run.

## Findings

### F1. Exact formula and the W+1 theorem — PASS

The v5 `tau_free_adjoint` discards physical `N` keys and constructs its raw
dual only from typed old `R` keys.  Hence the raw occurrence constant is zero.
`formula_bundle` separately computes

```text
K = n1*(ex/18) + n2*(ey/18) mod 3
```

and copies the occurrence dictionary only after mod-3 merging and deletion of
zero entries.  Both producer and independently written checker then evaluate
the compiled ABI as exactly

```text
K + sum c_(j,t) * 1[blob[j] == t] mod 3.
```

For every retained target on coordinates 0--2, a nonempty fibre has the
corresponding kernel size nine.  Therefore

```text
|union_(j,t) pi_j^-1(t)| <= sum_(j,t) 9 = 9|R| = W.
```

Subject to the explicit runtime guard `W < 357128352`, any `W+1` distinct
roster elements include one outside this union.  All indicators vanish there,
so the compiled value is `K != 0`.  Empty fibres only make the bound looser.

### F2. Roster, literal word, and all ten coordinates — PASS

For `0 <= cursor < 1469664*243`, `divmod(cursor,243)` is a bijection onto the
frozen q-major, Gamma-minor pair order, with inverse `243*qid+gid`.  The pinned
Task176 section code and Task179 consumer use precisely

```text
reduce(Gamma.section_word(gid) + Q0.section_word(qid)).
```

The cross-checked extension premise makes the resulting 357,128,352 elements
distinct; this is not inferred from word or row digests.

The current direct `coordinate_blobs` calls the pinned full coordinate word
evaluator and returns all ten blobs.  By contrast, the selective runtime
builds exactly three Q0 stores.  Inherited `sf.global_candidate` obtains its
Q0 row from those stores and combines by `zip`; its result therefore has
length three, while its own direct replay has length ten.  It is mistyped in
this runtime and must not be called.  Constructing the word first and directly
evaluating it is the correct contract and requires no omitted stores.

### F3. Fresh-anchor boundary — PASS

Freshness is essential.  At a fresh anchor, the separating functional
annihilates the current physical span, so nonzero pairing forces a nonzero
remainder and a rank rise.  After one insertion, the same functional need not
annihilate the enlarged span, so a later nonzero pairing alone would not prove
independence.

The proposed boundary is sufficient:

- If certified `rows` already exist, their nonempty v427 close records one or
  more actual rises and recomputes the dual before restarting.
- If `rows` is empty, the finite `0..W` scan has a guaranteed nonzero literal;
  the unchanged nonmutating reduction/direct-pair/pivot gates retain its
  actual rise, and a one-row v427 close immediately refreshes the anchor.

Every restart is thus preceded by a positive rank increase.  The outer round
again performs action-first and visits freshly compiled formulas in printed
seed order.  A path can only make such a rise, reach `COMMON`, or encounter an
existing typed time/RSS/cap stop; it cannot cycle at fixed rank.

### F4. Cursor reconstruction and disjointness — PASS

```text
["global_nonzero_constant", seed_index, cursor, W]
```

is disjoint from the old integer-first four-field support cursor.  From it the
checker selects the independently recompiled seed formula, recomputes `W`,
derives `(qid,gid)`, reconstructs the section word, evaluates all ten
coordinates, and recomputes the scalar and physical row.  The separately
recorded one-based qid/gid values are redundant checks, not trusted inputs.
No `(coordinate,target,ordinal)` is required or valid for an outside point.

### F5. v5-to-v6 migration and durable ledger — PASS

Exact v5 schema, binding, canonical state seal, C99 prefix, batches, segments,
profiles, rolling prefix, ready cores, and ledger must be validated before
mutation.  After that validation:

- `prefix_digest` depends only on C99 plus chronological appended rows;
- `ready_core_digest` depends on tuple, prefix, historical segment input
  identity, profile, and ledger;
- `ledger_digest` depends on the segment descriptor, which excludes the
  top-level schema, binding, and state seal.

Thus changing only top-level `schema` and `binding` and recomputing the
top-level seal leaves every historical row, batch, segment identity,
`prior_state_seal`, prefix, ready core, and ledger byte-for-byte unchanged.
In particular, the historical top-level `input_checkpoint` must **not** be
rebound during migration.

The actual v5 resume file identity is held as the invocation input and becomes
the `input_checkpoint` of the first newly created v6 segment.  That new
segment's newly populated `prior_state_seal` binds the migrated v6 predecessor
seal.  The flat segment gate then checks the old chain plus this new boundary
without reopening any ancestor.  This new-segment field population is not a
historical migration rewrite.

There is no additional field that must be rebound.

### F6. Claim boundary — PASS

The construction is positive-only.  Each durable partial prefix merely adds
independently replayable rank rises.  A time/RSS/cap stop remains
`UNKNOWN_RESOURCE` with no negative conclusion.  `A0` remains 0/1 and may be
promoted only after the terminal positive object receives the independent
literal replay required by the existing producer/checker boundary.  No
COMMON, nonmembership, compatibility, fake, or Ihara claim is introduced by
v431.

TASK507_R07_RANK99_NONZERO_CONSTANT_GLOBAL_PREFIX_V431_AUDIT_GO
