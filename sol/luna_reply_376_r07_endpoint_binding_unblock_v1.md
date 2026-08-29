# Luna reply 376: endpoint-binding unblock v1

Task375's physical ABI blocker is removed by v352.  The authorized canonical
`M` path is implemented end to end.  No new executable-owner mismatch was
found.

## Files

```text
search/d972_r07_direct_relator_a5_a7_fusion_v4.py
  26841 bytes
  0f07716b38c427eeaa9bd920721a170ede85d0cad805f2fa55bbe614bd9229f1
crosscheck/check_d972_r07_direct_relator_a5_a7_fusion_v4.py
  24239 bytes
  f494d12c050e4d1c5f199fa771d56ca5326c365439e617f2cbe892cf7b3b6a01
search/d972_r07_direct_relator_a5_a7_fusion_gha_driver_v4.g
  5573 bytes
  7078a535008f8c0b82f3cc5f105a422159f5fa6204d9486c1d4eb437c50efc66
```

The reply identity is reported externally after its final bytes are fixed.

## Physical binding implemented

The producer restores the exact frozen A5/A6-v3 owner, task198-v12 runtime,
task193-v3 receipt/verdict, and task292-v2 producer core.  It never calls or
patches task292's blocked `production_literal` entry.

For every one of the eleven task198 owner rows it checks the executable
`BRIDGE_OWNER_LAYOUT`, the live context type/id and literal substitutions.  It
then reconstructs v352's `rho`, `r_o`, stored-order signed `Q_o`, `P_o`, and
`d_sources=[delta(r_o^-1)]`.  The three corrected relation words are rebuilt
from the same signed factors in frozen printed order and required literally
equal to task193's physical `relation_words`; these give
`epsilon_sources=[-delta(R_B(f))]`.  No serialized action/context map is an
input.

The v3 pairs are passed without precollection as task292 `M_terms`, with
coefficient, positive/negative words, prefix, relator index and source-term
ancestry.  The immutable `M` digest is computed inside the exact core.

The checker imports neither the v4 producer nor task198 producer helpers.  It
restores the frozen independent A5 checker, task198-v14 arithmetic and the
separately written task292 checker.  It reconstructs all literal fields from
the physical owners, independently replays the finite A5 certificate, the
full faithful Artin normal forms, the three endpoint buckets, and the ZERO
case full-C1 `D1(z_B)=0` rows.

## Terminals and honest frontier

```text
A5 complete NONMEMBER
  -> R07_ZERO_BASE_A5_A6_NONMEMBER

A5 MEMBER and canonical M has H1=H2=P=0
  -> R07_DIRECT_RELATOR_A5_A7_FUSION_MEMBER
     (A5+A6+A7 only)

A5 MEMBER and canonical M has a nonzero exact endpoint
  -> UNKNOWN_RESOURCE:phase=v351_lift_null:...
```

The third branch preserves the accepted A5/M sidecar and exact canonical
endpoint.  It is not A7 NONZERO or NONMEMBER.  Per the commander's narrowed
priority, this executable is explicitly

```text
canonical_M_only=true
v351_lift_null=NOT_IMPLEMENTED
```

Thus the finite Schreier seed roster and positive-complete lift-null dovetail
from v351 remain the next implementation, not a hidden claim of this version.
Compatible lift, A8+, fake and Ihara fields remain `NONE`.

## Resume and artifacts

The producer CLI requires fresh receipt, checkpoint and A5-sidecar output
paths.  Resume is accepted only as the all-or-none triple
`--resume-path/--resume-bytes/--resume-sha256`.  The sealed checkpoint binds
the exact v4 source, all frozen source identities, physical task198/task193
owners, A5 result, endpoint terminal/digest, and phase.  Restoration is
performed once before the A5 search call; an accepted checkpoint A5 MEMBER
skips that producer search.  Resource output retains the checkpoint and, once
A5 is positive, the independently replayable A5/M sidecar.

The ASCII GAP driver pins the exact producer/checker bytes and SHA values,
starts exactly one producer followed by exactly one checker, requires terminal
equality, and preserves receipt, verdict, both logs, checkpoint and optional
sidecar.

## Static acceptance

- Both Python files passed in-memory byte compilation with `python -B`.
- Frozen A5-v3, task292 producer/checker sources restored under non-main names
  with exact byte/SHA pins.
- GAP `ReadAsFunction` parse-only passed; only expected unbound-global warnings
  were emitted.
- All three executable files contain zero non-ASCII bytes.
- No SELFTEST, mutation campaign, retry, worker pool, GHA, network, git, or
  local production computation was run.

```text
TASK376_R07_CANONICAL_M_ENDPOINT_BINDER_V4_IMPLEMENTED_STATICALLY_UNEXECUTED
ACTUAL_ENDPOINT_TERMINAL_NOT_COMPUTED
VERIFIED_FALSE
```
