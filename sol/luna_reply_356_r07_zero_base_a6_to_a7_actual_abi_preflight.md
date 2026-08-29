# Luna reply 356 — zero-base A6 to A7 ABI preflight

## 1. Scope and result

This is a bounded static ABI preflight.  I read the v345 zero-base
specialization, v281 compressed endpoint specification, v228 all-rung
theorem, the v2 producer/checker and SELFTEST fixture, the v292 report, and
the v285 fused-compiler report.  No machine code, fixture, computation,
workflow, or git state was changed except this reply.

The conclusion is an ABI boundary, not an A5/A6 or A7 result.  The v2
literal input is an A7-side object.  Its `M_terms` must be supplied by a
future accepted zero-base A5/A6 handoff, while its occurrence and epsilon
data must be rebuilt from the authenticated common input cone.  The v2
SELFTEST canary is not an actual upstream package.

## 2. Exact v2 literal-input schema

The producer accepts a dictionary whose only schema discriminator is

```text
schema = d972-r07-actual-three-exact-pb-endpoints/v2/literal-input
```

The production-shaped top-level fields used by `compile_literal` are:

```text
schema                 exact discriminator above
mode                   copied into the result; actual mode is supplied by the new adapter
source_words           source-word identity object, copied and later authenticated by the cone
M_terms                ordered finite pair records
M_immutable_digest_sha256  optional digest of the canonical collected M payload
occurrences            exactly 11 typed occurrence records
epsilon_sources        map with lists for exactly H1, H2, and P
```

This is the exact field use in producer v2, lines 600–608 and 660–684; the
SELFTEST constructor is the concrete shape at lines 749–775.  The checker
compares the same fields independently (checker lines 600–629), rather than
importing the producer's evaluator.

Each `M_terms` record has the following literal fields:

```text
coefficient       integer, reduced modulo 3 during collection
U                 free word on the two F2 source generators, as integer letters
V                 free word on the two F2 source generators, as integer letters
ancestry          provenance carried through collection; not an equality oracle
```

`U` and `V` must be distinct after free reduction.  Every pair must have
equal roof value.  Collection is ordered as `U_minus_V`; equal literal
`(U,V)` keys may cancel modulo 3, with the cancelled records retained as
zero-deletion provenance.  The optional immutable digest is checked against
the producer's canonical collected payload (producer lines 403–435 and
600–607).

Each of the eleven `occurrences` records has these input fields:

```text
ordinal             1..11 in the fixed order
block               H1 for ordinals 1..3, H2 for 4..6, P for 7..11
position            [1,2,3,1,2,3,1,2,3,5,4]
type                E3 for 1..6, E4 for 7..11
registry_label      typed registry identity; C21 occurs at E3 ordinals 1,5 and E4 ordinal 9
repeated_e3_key     E3_xy exactly at ordinals 1 and 5
rank                PB3 for H1/H2, PB4 for P
rho                 two literal source images, keys x and y
sigma               signed occurrence transport, +1 or -1
prefix_word         literal prefix word
inverse_slot        inverse/direct occurrence flag
orientation         corresponding inverse/direct label
d_sources           literal Fox source records for d1 under this occurrence
```

The fixed roster and the repeated-E3/C21 distinction are enforced by
producer lines 438–460 and checker `check_roster`; the input-to-output
reconstruction is at producer lines 463–488 and checker lines 382–402.
Each `d_sources` record is a literal Fox source with `coefficient`,
`left_word`, `fox_word`, and `provenance`.  The producer derives from it the
uncollected chain, exact endpoint terms, collected `xi_terms`, and deletion
provenance; those derived fields are not additional v2 input fields.

`epsilon_sources` is a dictionary with exactly three lists, one per block.
Its entries use the same literal Fox-source shape.  The producer independently
expands each list and computes the epsilon endpoint (lines 609–620); the
checker does the corresponding replay at lines 520–532.

The v2 literal schema does not contain an A5 anchor, adapted matrix, base-pair
roster, A6 prefix DAG, or trusted endpoint Boolean.  The result additionally
records the typed occurrence ledger, the ten-to-eleven map
`[0,1,2,3,0,4,5,6,7,8,9]`, exact endpoint collections, full-C1 replay,
complete PB3/PB4 presentation data, and the non-finite-quotient Artin normal
form (producer lines 660–710).  These are A7 computation outputs, not fields
that a future A5/A6 receipt may simply assert.

## 3. Zero-base A5/A6 ownership versus A7 reconstruction

The zero-base specialization changes the handoff materially.  By v345
sections 1–4, the accepted A3 target gives `kappa0=0`; the A5 condition is
`e1(c) in H d1`, and on MEMBER the coefficient is `mu1=theta`.  There is no
nonzero anchor, adapted A4 basis, or local A3 base-pair summand in this
branch.  The complete closure still starts from the original A4
word-bearing basis and its marked actions (v345, theorem 2.1).

### A5/A6 must derive and own

The future accepted A5 MEMBER/A6 receipt must expose enough authenticated
literal ancestry for an independent consumer to reconstruct, at minimum:

1. the common input identities: lower word, roof/tower, Delta edge, typed
   occurrence convention, and field convention;
2. the accepted A4 ordered word-bearing basis `(u_i,k_i)` and its completeness
   certificate, with each literal `u_i` and its index;
3. the zero-base A3/A5 target ancestry, including the actual `d1`, `e1`,
   `w`, the complete pre-C joint closure, post-C nullspace/Hd1 basis, and the
   MEMBER equality `e1=theta*d1` with `theta in H`; these are derived objects,
   not free status flags;
4. the complete accepted closure ancestry: seed identity, marked action,
   parent, pre/post rank data, reduction representation, and the distinction
   between accepted and dependent rows;
5. the A6 factored language from v345 section 4 and v281 section 1:
   `(coefficient, prefix_DAG_node, original_A4_kernel_word_index)`, together
   with the authenticated prefix-DAG parent/letter records and the kernel-word
   dictionary.  In this zero-base branch there is no base-pair summand;
6. the derived canonical pair provenance and roof-fibre ancestry, including
   the coefficient/order needed to reconstruct the finite polynomial `M`;
   and
7. the accepted A5/A6 producer terminal, independent checker terminal,
   receipt/verdict seals, exact source identities, and a manifest digest.

The A5/A6 receipt may include the materialized `M_terms` as a convenience,
but A7 must treat them as derived and replay them from the prefix DAG and
kernel dictionary.  A copied `M` list, a supplied rank, a supplied MEMBER
bit, or a digest without its literal owners is not sufficient.  This follows
v281 sections 1, 3, 5, and 7 and v345 section 4.

### A7 must reconstruct and own

Given the authenticated A5/A6 ancestry plus the common input cone, A7 must
construct the v2 literal input and then independently replay:

1. every `A` prefix and every `red(Au_i)` / `A` pair, preserving literal
   source words rather than identifying words only in a finite shadow;
2. the ordered `M_terms`, modulo-3 collection and zero deletions, and the
   roof-fibre equality;
3. all eleven typed occurrences, including the repeated E3 insertion,
   E3-C21 versus E4-C21 distinction, signs, inverse slots, prefixes, rho
   maps, and the `d_sources`/`xi` endpoint chains;
4. the three `epsilon_sources` chains and their exact PB endpoints;
5. all three endpoint collections using the exact pointwise Artin action on
   PB3/PB4 free-basis words, without a hash or finite quotient as an equality
   key;
6. for a candidate ZERO, the full-C1 expansion, complete fixed presentation
   boundary replay, and equality of the full-C1 and endpoint collections;
7. the exact terminal `R07_THREE_EXACT_PB_ENDPOINTS_ZERO` or the typed
   block-specific NONZERO/UNKNOWN terminal; and
8. only after the three exact endpoint zeros, the v228 promotion input for
   the all-rung theorem.  v228 explicitly leaves the nonlinear word gates,
   mixed-prime gate, perfect-core gate, fake, and Ihara witness open.

Thus A5/A6 owns the *source and ancestry of the candidate polynomial*;
A7 owns the *literal endpoint identity*.  This is the minimal separation
needed to preserve v281's warning that compressed evaluation is not itself
an authoritative ZERO.

## 4. Obsolete task285 assumptions

The following task285/v1 assumptions must not cross into the new boundary:

- a six-role task285 manifest whose roles are task192, task193, task226,
  task227, task232, and task198, with the old v1 receipt/verdict shape;
- task285 source pins, task285 `ci/in` paths, or any task285 accepted
  MEMBER/M object.  v292 deliberately removed these and makes production a
  typed UNKNOWN_INPUT until a new explicit binding exists;
- a standalone anchor, supplied anchor exponent/index, adapted A4 basis,
  or copied `base_pairs` list.  v345 removes these for the actual zero-base
  branch;
- literal width-13/occurrence00 objects, SELFTEST canaries, or any synthetic
  `future_a5_a6` seal as an actual package;
- accepting producer-supplied `M`, ranks, pivots, nullspaces, endpoint
  buckets, terminal strings, or Booleans as mathematical evidence;
- treating the v2 `source_words`, occurrence ledger, or endpoint transcript as
  a replacement for the authenticated A5/A6 ancestry; and
- promoting a v2 SELFTEST ZERO to actual A7 ZERO, A8, A9, a lift, fake, or
  Ihara witness.

The v285 report is therefore historical only: its six-predecessor actual ABI
was absent and its implementation remained STATIC_BLOCKED.  v292's
`future_a5_a6` field is a SELFTEST canary, not a usable production binding.

## 5. Minimal new v3 manifest/adapter boundary

The smallest sound successor is a new, explicitly versioned manifest rather
than a patch to the v2 blocker.  Its production schema should be named, for
example,

```text
d972-r07-actual-three-exact-pb-endpoints/v3/actual-input-manifest
```

It should contain only authenticated member descriptors and common identity
data, with no copied mathematical decision fields:

```text
schema
members: {
  a5a6_receipt: {path, bytes, sha256, schema, terminal, self_digest_sha256},
  a5a6_verdict: {path, bytes, sha256, schema, terminal, self_digest_sha256},
  a5a6_producer_source: {path, bytes, sha256},
  a5a6_checker_source: {path, bytes, sha256},
  common_input_members: [authenticated task192/task193/task198/task232/A2/A3/A4 owners]
}
common_identity: {
  lower_word_id,
  roof_tower_id,
  delta_edge_id,
  typed_occurrence_roster_id,
  field_convention_id
}
```

The `members` array must be repository-relative, opened and hashed from the
physical bytes by both adapters.  `path`, byte count, SHA, schema, terminal,
and self seal are provenance gates; the copied values never replace the
physical-byte checks.  The manifest must bind one accepted A5 MEMBER/A6
receipt-checker pair and the exact common members needed to reconstruct
`d1`, `e1`, `w`, `rho`, `sigma`, prefixes, and epsilon sources.  The new
adapter rejects any missing owner, identity mismatch, traversal/link path,
malformed JSON, or terminal inconsistent with the bytes as `UNKNOWN_INPUT`.

The producer adapter reads the accepted A5/A6 receipt, reconstructs the
zero-base A6 pair language, and emits the v2 `literal-input` object for the
exact endpoint engine.  The checker adapter independently reads the same
manifest bytes and A5/A6 ancestry, rebuilds the literal object, and compares
the endpoint result.  Neither adapter may consume the v2 `future_a5_a6`
SELFTEST canary, task285 ABI, a copied pair list, or a placeholder Boolean.

The v3 boundary deliberately does **not** bind A7 output fields such as
`endpoints`, `full_C1_replay`, `complete_presentations`, or the final ZERO
terminal into the input manifest.  Those are reconstructed by A7.  It also
does not claim a compatible lift, fake, or Ihara witness; v228 section 5 and
v281 section 8 leave those downstream gates separate.

## 6. Fixed handoff status

```text
V2 literal-input field extraction:                 COMPLETE (static)
Zero-base A5/A6 ownership boundary:                 COMPLETE (static)
Task285 binding assumptions retired:                COMPLETE (static)
Minimal v3 manifest/adapter boundary:               SPECIFIED (not implemented)
Accepted actual A5 MEMBER/A6 receipt:               NOT PRESENT in inspected inputs
Actual v2 literal input / A7 endpoint run:          NOT AUTHORIZED or performed
Exact PB ZERO / all-rung lift / fake / Ihara:       NOT ESTABLISHED
```

`R07_ZERO_BASE_A6_TO_A7_ACTUAL_ABI_PREFLIGHT_V356_STATIC`
