# Luna task 375: direct-relator A5/A7 fusion v4

Role: Luna implementation only.  Do not change the mathematics, run a local
production search, dispatch GHA, commit, or push.

Authoritative theorem:

- `sol/proof_r07_direct_relator_a5_a7_fusion_v351.md`

Frozen executable base:

- `search/d972_r07_zero_base_a5_a6_compiler_v3.py`
- `crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v3.py`
- `search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v3.g`
- task198 producer-v12 / independent checker-v14 owners already pinned there
- task193-v3 physical receipt/verdict ABI already pinned there
- task292 exact PB endpoint/Artin core and its helper-nonshared checker

Create only:

1. `search/d972_r07_direct_relator_a5_a7_fusion_v4.py`
2. `crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v4.py`
3. `search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v4.g`
4. `sol/luna_reply_375_r07_direct_relator_a5_a7_fusion_v4.md`

## Required production semantics

1. Preserve v3's actual 6,441-relator owner, marked pre-`C` action closure,
   complete PB boundary slack, A5-only ancestry and exact task193 signs.
   Do not invent serialized action/context maps and do not require A4 output.
2. Maintain the A5-only result separately.  An A5 hit may be retained but
   must not stop the witness lane unless the same literal `M` has exact H1,
   H2 and P endpoint zero.
3. Add the three exact endpoint coordinates from v351 to every coefficient
   column.  PB equality-slack columns have zero endpoint coefficient and
   never enter `M`.
4. Construct the finite literal Schreier seed roster for the actual common
   source map to `Delta1`.  Dovetail literal translations of `V(n_i-1)`.
   In the raw echelon use each seed's full raw A5 row together with its exact
   endpoint row; do not substitute raw zero without a boundary ledger.
5. On augmented MEMBER emit and directly replay:
   `mu1`, the complete literal pair polynomial `M`, selected relator/action
   ancestry, selected lift-null ancestry, PB slack, and exact zero endpoints
   for H1/H2/P.  This is an A5+A6+A7 terminal only; A8+, fake and Ihara flags
   remain false.
6. A complete finite A5 NONMEMBER may retain v3's terminal.  If A5 is MEMBER
   but the infinite lift-null dovetail meets a cap, emit typed
   `UNKNOWN_RESOURCE` while preserving the accepted A5/M sidecar.  A bounded
   augmented miss must never become A7 NONZERO or NONMEMBER.
7. Add a real checkpoint/resume CLI from the first version: all-or-none
   resume path/bytes/SHA, exact source binding, one restoration call before
   workers/queues start, and an artifact-bearing controlled resource
   terminal.  Do not add SELFTEST, mutation campaigns, retries, duplicate
   full producer runs, or a worker pool beyond what the base already needs.
8. The independent checker must import no producer/helper code.  It rebuilds
   only the finite positive ancestry on MEMBER, but independently reconstructs
   the exact PB normal forms, all selected lift-null raw rows, the raw
   equality, `mu1`, `M`, and all three zero endpoints.  For A5 NONMEMBER it
   retains the complete v3 negative obligations.  For resource terminals it
   authenticates the checkpoint and preserved A5 sidecar without promotion.
9. The serial GAP driver starts exactly one producer and, after a recognized
   terminal, exactly one independent checker; it preserves receipt, verdict,
   logs and checkpoint/sidecar artifacts.  ASCII only.

## Bounded static acceptance

- Python byte compilation with `python -B`.
- Frozen task198/task193/task292 source restoration and exact byte/SHA pins.
- GAP `ReadAsFunction` parse-only.
- No local production computation.
- Report exact bytes/SHA, physical input ABI, resume ABI, and honest frontier.

Stop rather than fabricate if the actual task292 core cannot consume the v3
`M` ABI without a new explicit binding.  Record the smallest real blocker in
the reply; do not build a synthetic bridge.
