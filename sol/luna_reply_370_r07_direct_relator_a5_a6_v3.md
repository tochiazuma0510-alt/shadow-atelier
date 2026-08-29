# task370 Luna reply: direct-relator A5/A6 compiler v3

Date: 2026-08-29

## Result

The requested production-first v3 implementation is now physical.  It does
not consume the v2 fictional serialized evaluator/action maps or an
`actual-input-manifest`.  The producer restores the executable task198 v12
owner, while the checker restores the independent task198 v14 arithmetic.
Both authenticate the physical task198 receipt/acceptance/attestations and
the CLI-supplied task193-v3 receipt/verdict.

Created files:

| file | bytes | SHA256 |
|---|---:|---|
| `search/d972_r07_zero_base_a5_a6_compiler_v3.py` | 59,239 | `c287011d5e573452094e62c76020ab4b1076bc427103174b1771a22a1bb4fbd8` |
| `crosscheck/check_d972_r07_zero_base_a5_a6_compiler_v3.py` | 45,942 | `e86806444efa146954213da4bbb13726a8b5dc79b16c0a4b97aaa5c7b05b1cb0` |
| `search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v3.g` | 4,255 | `5cac3f9ff13ef2697e14275376beb17b2272da824d0f50458e3794208a09c392` |

## Physical input ABI

The driver requires only:

```gap
D370Mode := "PRODUCTION";;
D370Task193Receipt := "ci/in/<accepted-task193-v3-receipt>.json";;
D370Task193Verdict := "ci/in/<independent-task193-v3-verdict>.json";;
Read("search/d972_r07_zero_base_a5_a6_compiler_gha_driver_v3.g");
```

The task193 symbolic dependency is pinned to the live adapter-v4 successor:

- producer: 2,826 bytes,
  `1ac65ca533e11ac39def79c84de0bbdcb018d463ac10bca6158db254a61da741`;
- checker: 2,792 bytes,
  `5b3c5b3e607077e0bebcf0153c592465983ba210b768c93ea62aeb2201c905c6`.
- driver: 5,798 bytes,
  `c11074bd1e634aa38d4d164699542e17087e659115c31b8f5b8cc322dc5dfd84`.

An accepted task193-v3 result is not fabricated.  Missing, UNKNOWN, wrong
schema, wrong seal, wrong source pin, or nonpositive task193 input stops at a
typed producer `UNKNOWN_INPUT`; the driver does not promote it.

Task198 is loaded through these executable wrappers:

- producer v12: 7,209 bytes,
  `816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5`;
- independent checker v14: 8,074 bytes,
  `7ff0fb8888b46febb8b373914a3ba31ee555e43c829e60dae915bacfb16b7b47`.

Each wrapper's frozen v6 source is checked, every nonempty patch is required
at cardinality one, and the patched source is executed under a non-main
module name.  The resulting `AuthorityAdapter/Runtime/BoundaryLedger` and
independent `Authority/CheckerArithmetic/Boundary` are the only task198
arithmetic ABIs used.

## Implemented mathematics

1. The task193 first-encounter affine roster is decoded back into live
   task198 affine states.  Equality is recomputed using the complete 65 typed
   PB boundary families; labels are not treated as opaque serialized action
   tables.
2. The checker and producer independently replay the task193 signs
   `d1=-D1(g760)` and `e1=-beta1` in the three disjoint blocks H1, H2, P.
3. The immutable eleven-occurrence ledger reconstructs the v225 prefixes
   `P_o`, the occurrence vector `w_o=sigma_o P_o(r_o^-1-1)`, and the exact
   occurrence decomposition of `d1`.
4. Every one of task198's 6,441 literal relators supplies the raw pre-`C`
   column
   `((b_j-1)d1,(b_j-1) odot w)`.  The marked `x+/-1,y+/-1` closure is decided
   before the printed block map `C`.
5. The joint target is exactly `(e1,0)`.  Translated outer PB3/PB4 boundary
   columns are selected by complete support-inversion correlation and enter
   the same joint echelon as equality slack.  They never enter the
   coefficient polynomial.  Cheap target reduction runs at every rank rise;
   the more expensive complete boundary correlation is shared and batched at
   64 rank rises (and at every phase/final boundary), avoiding a per-row
   restart of the old A4 oracle.
6. MEMBER expands the retained proof DAG to literal
   `(coefficient,prefix,relator_index)` ancestry and emits
   `M=sum a_gj((w r_j)-w)`.  The producer directly replays the complete raw
   joint equality before emitting it.  The independent checker rebuilds
   each selected relator column, prefix action, boundary translation, `mu1`,
   and every ordered pair in `M` using v14 arithmetic.
7. NONMEMBER is emitted only after all 6,441 seeds and the complete marked
   pre-`C` action queue exhaust.  Its checker independently reconstructs an
   ancestry-bearing pre-basis, proves containment of every seed, proves four
   marked actions of every basis row stay in the span, then independently
   exhausts the outer boundary oracle and constructs its own separating
   dual.  A bounded miss is never converted to NONMEMBER.

There is no SELFTEST route, mutation campaign, retry, worker pool, duplicate
full producer run, A7 computation, compatible-lift claim, fake claim, or
Ihara claim.  The GAP driver starts exactly one producer and, only after a
positive A5 terminal, exactly one independent checker.  It preserves both
JSON artifacts and both progress logs and pins the exact producer/checker
bytes above.

## Static checks performed

- Both Python sources compile from bytes with `python -B`: PASS.
- Producer v12 frozen-source restoration and required runtime-symbol gate:
  PASS.
- Checker v14 frozen-source restoration and required independent-symbol
  gate: PASS.
- GAP 4.16.0 `ReadAsFunction` parse-only check of the driver: PASS (only the
  expected top-level unbound-global warnings).
- All three executable sources decode as ASCII: PASS.
- Driver byte/SHA pins match the two Python files: PASS.
- Search for stale v2 task193 schema, fictional runtime overlay/manifest,
  SELFTEST, mutation, retry, and pool routes: no executable occurrence.
- No local production search, GHA dispatch, network call, or heavy task198
  authority run was performed.  The intentional Windows no-follow firewall
  also makes the real accepted-owner run a Linux/GHA operation.

## Honest frontier

This completes the v3 executable/compiler milestone, not the mathematical
terminal.  Until an accepted physical task193-v3 receipt/verdict is supplied
and the driver is run on GHA, the actual R07 target remains uncomputed.  A
future MEMBER would establish the explicit A5 multiplier and A6 pair
polynomial `M`; it would still establish neither the three exact A7 endpoint
conditions nor a compatible cofinal lift, fake certificate, or Ihara
witness.

`R07_DIRECT_RELATOR_A5_A6_COMPILER_V3_IMPLEMENTED_STATIC_NOT_RUN`
