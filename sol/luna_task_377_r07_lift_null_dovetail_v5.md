# Luna task 377: R07 lift-null positive dovetail v5

Date: 2026-08-29

Role: mechanical implementation.  Do not change mathematics, run a heavy
local search, dispatch GHA, or edit existing v4 files.  Create only the three
new v5 executables and `sol/luna_reply_377_r07_lift_null_dovetail_v5.md`.
Production-first: no SELFTEST matrix, mutation campaign, retries, pools, or
duplicate producer pass.

## Frozen mathematical contract

Read in full:

- `sol/proof_r07_schreier_lift_kernel_endpoint_homotopy_v310.md`;
- `sol/proof_r07_direct_relator_a5_a7_fusion_v351.md`;
- `sol/proof_r07_task193_to_exact_endpoint_literal_binding_v352.md`;
- the v4 producer/checker/driver and task376 reply.

V5 preserves the v4 A5 NONMEMBER and canonical-endpoint-ZERO terminals.  It
changes only the canonical NONZERO branch.  There it runs a positive-only,
fair, checkpointable search through translated Schreier lift-null pairs

    L_(V,q,t) = V (s(q) t s(qt)^-1 - 1).

The restored task198-v12 `Runtime.states_direct` is the executable producer
owner of rho1 into the ten typed first-successor factors.  The independent
side uses task198-v14.  A state key must contain all ten affine roofs and all
ten sparse affine gradients, not just the roof blobs.

## Required producer algorithm

1. Reuse the exact v4 owner restoration and v352 literal binder.  Do not
   patch or call task292-v2's blocked production entry; load its frozen
   `compile_literal` core under a non-main module exactly as v4 does.
2. Stream the marked Cayley BFS of Delta1 from the identity under letters
   `(1,-1,2,-2)`.  Store the first shortlex literal word `s(q)` for each
   complete ten-affine-state key.  For every explored edge `(q,t)`, compare
   with the retained `s(qt)` and form the freely reduced Schreier word
   `n=s(q)t s(qt)^-1`.  Retain a literal proof that rho1(n)=1.  Identity and
   duplicate seed words may be skipped only after this replay.
3. Interleave continued Cayley-edge exploration with a diagonal fair
   enumeration of every discovered seed `n_i` and every freely reduced
   translating F2 word `V`.  No finite cutoff may become NONMEMBER.  Each
   column is the literal pair `(V n_i)-V` and has zero first-shadow image.
4. Obtain that pair's exact H1/H2/P endpoint column through the unchanged
   task292 exact core and v352 occurrences.  It is permitted to compile a
   one-pair literal object with empty epsilon source lists, provided direct
   formula replay confirms that this is precisely the incremental
   contribution.  Key every sparse coordinate by block plus the full Artin
   normal-form key; a hash is never an equality key.
5. Maintain a GF(3) ancestry-bearing sparse echelon against the canonical
   nonzero endpoint.  Fix signs by a final direct calculation, not by a
   label convention: on a hit compile `M_can + sum a_i((V_i n_i)-V_i)` as
   one complete v352 literal object and require task292 ZERO in H1, H2 and P.
6. A MEMBER receipt must retain the finite selected Schreier edges,
   translating words, coefficients, complete `M`, unchanged `mu1`, the
   canonical A5 proof, and the final exact endpoint replay.  It may claim
   A5/A6/A7 for this fixed word only.  It may not claim A8/A9, a compatible
   lift, mixed-prime/perfect-core gates, fake, or Ihara.

## Resume and resource contract

- Implement a real periodic checkpoint and a process-RSS/wall/operation
  guard early enough to upload before an OS kill.  On any bound return typed
  `UNKNOWN_RESOURCE`, preserve the accepted A5 sidecar and checkpoint, and
  state `bounded_miss_is_A7_negative=false`.
- Resume input is all-or-none path/bytes/SHA256.  Bind every frozen source,
  task193 owner and A5/canonical endpoint digest.  Persist the Cayley words,
  edge/translation cursors, seed roster, echelon and ancestry.  It is sound
  to reconstruct affine states from stored literal words on resume; do not
  serialize unauthenticated Python objects.
- The enumeration schedule must be demonstrably fair: every finite BFS edge
  and every finite pair `(discovered seed, translating word)` eventually
  receives a turn if no resource bound intervenes.

## Independent checker and driver

- The checker must not import the new producer.  Reconstruct selected
  rho1 identities with task198-v14, reconstruct v352 occurrences through the
  checker owner, verify every selected pair is lift-null, rebuild the final
  literal `M`, and run the independent task292 checker route on the final
  exact endpoint.  Positive finite ancestry is enough; it need not replay
  unused BFS states.
- The GAP driver starts exactly one producer and, only for MEMBER, one
  checker.  Preserve receipt, verdict, accepted-A5 sidecar, checkpoint and
  progress log.  It must expose cadence, seconds, RSS, operation and optional
  resume pins.  No local production run.

## Deliverables

- `search/d972_r07_direct_relator_a5_a7_fusion_v5.py`
- `crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v5.py`
- `search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v5.g`
- `sol/luna_reply_377_r07_lift_null_dovetail_v5.md`

Run only bounded static checks: Python byte compilation, frozen-owner
restoration, GAP `ReadAsFunction`, ASCII and exact driver pins.  If a missing
physical ABI makes any load-bearing step impossible, stop at the first such
site and report it precisely instead of inventing fields.
