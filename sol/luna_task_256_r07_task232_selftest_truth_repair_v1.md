# Luna task 256 — task232 SELFTEST truth repair v1

Role: bounded implementation repair only.  Read task252 and all current five
task232 files in full.  Do not run Python, Node, GAP, git, GHA, or network.
Edit only the same producer, checker, driver, fixture, and reply named in
task252.

## Exact parent static rejection

The task252 return cannot enter GHA yet:

1. Producer `run_toy()` serializes
   `digest([item["row"] for item in basis_rows])`, but `basis_rows` is
   undefined in that function.  SELFTEST will raise `NameError` before a
   terminal.
2. The second toy projection receipt uses source word `[1]` while claiming
   `d1_value=[0,0,0]`.  The commissioned H2(9) evaluator gives
   `h2_signed_word([1])=(1,0,0)`.  Producer and checker validate only receipt
   zero, so this false second row is hidden.
3. Toy basis ancestry terms contain no `source_word`, although producer
   semantic validation requires every ancestry term to have a nonempty one.
4. The three named anchor mutations `delta0_identity`, `d1_z0_target`, and
   `k_z_source_word` currently alter `basis_receipts[0]`, not the selected
   `projection_anchor`.  Hence they do not own the fields named by task244b /
   task252.

## Required repair

1. Remove the undefined name and calculate `basis_digest` from the exact toy
   basis object actually serialized.  The checker must reconstruct that digest
   independently.
2. Replace the second toy source word by a nonempty word whose independently
   evaluated H2(9) value is exactly `(0,0,0)`; do not merely change the claimed
   value.  Re-evaluate **every** basis receipt in producer and checker:
   - source word is a nonempty signed word over x,y;
   - computed D1 value equals the serialized value;
   - it is central with r in `{0,3,6}`;
   - projected exponent equals `r/3 mod 3`;
   - all ten roof rows are present and identity;
   - actual/toy membership evidence is positive.
   Require the serialized `basis_projections` and `basis_d1_values` to be the
   lists reconstructed from all receipts, not hard-coded evidence checked only
   at index zero.
3. Give each serialized toy basis ancestry term a nonempty literal source word
   consistent with its owning seed/conjugation, without changing the toy row
   algebra.  Retain exact ancestry replay.
4. Make the seven projection-anchor mutations own the seven selected-anchor
   objects.  In particular mutate `projection_anchor.delta0_identity`,
   `projection_anchor.d1_z0`, and `projection_anchor.source_word` for the last
   three names, in producer and checker independently.  Validation must
   reconstruct the selected least index, inverse scalar, concatenated/free-
   reduced source word, H2 target, ten roof identities, and membership evidence;
   do not accept unrelated Boolean changes as rejection evidence.
5. Inspect for any other undefined toy name or producer/checker index-zero-only
   projection check.  Preserve the actual production path, H2 law, A4
   mathematics, 57-name roster, terminal vocabulary, and false downstream
   flags.
6. Refresh driver pins and reply identities.  Remain `UNEXECUTED`; parent Sol
   will execute only after another static audit.

Report exact byte counts and SHA-256 for all five files.
