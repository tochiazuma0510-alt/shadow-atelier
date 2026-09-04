# Luna Task759 - A0 endpoint v7 finite release repair + workflow v12

```text
RESULT=COMPLETE
SAFE_FOR_INDEPENDENT_AUDIT=yes
REAL_PARENT_REPLAY=NOT_RUN
FRESH_RHO2=NOT_PRODUCED
A0/FAKE/IHARA=NOT_DECLARED
verified=false
```

Created exactly the three commissioned files:

- `search/d972_r07_a0_fresh_precision2_endpoint_signature_v7.py`
- `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v12.yml`
- `sol/luna_reply_759_r07_a0_endpoint_hotspot_v7_and_workflow_v12.md`

No real parent was read, no rho2 was produced, no GHA workflow was dispatched,
and no commit or push was performed.

## Exact receipts

All measured files are LF-only, end in LF, and contain zero CR bytes.

| path | bytes | LF | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v6.py` | 52,114 | 859 | `81265a0e198d0228bd10871c92e7f6944b8c4c48f0909d0002df49911e47e734` |
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v7.py` | 54,803 | 925 | `6e26e6b96eb610e29dfd191040cea604e7768a643ed2ef916033c8449373e465` |
| `search/check_d972_r07_a0_fresh_precision2_endpoint_signature_v4.py` | 93,236 | 1,592 | `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v11.yml` | 11,866 | 182 | `b1b5dce5dbd97364d019420d47e6325073b48c33822360671bfe2f5e174d88e9` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v12.yml` | 11,976 | 183 | `1ac07ad79e218f7926e1db95bf19fcfa94042dc80c4f80fadcb32815015f2d3d` |

The v6-to-v7 mechanical diff is 84 inserted and 18 deleted lines.  The
v11-to-v12 workflow diff is 13 inserted and 12 deleted lines.

## v6 to v7 finite repairs

1. The payload deliberately retains checker-v4's wire contract:
   schema `d972.r07.a0.fresh-precision2-endpoint-signature.v4`, marker
   `R07_FRESH_PRECISION2_ENDPOINT_SIGNATURE_V4_CANDIDATE`, and exactly these
   eight `occurrence` keys:
   `count`, `types`, `coordinates`, `signs`, `base_checks`,
   `max_base_checks`, `all_seven_canary`, and
   `first_six_typed_restriction`.  Profiling counters remain only in selftest
   output and this report.
2. Every `extend_signature` slot now checks both the parent and atom tags
   against `E3` in slots 0--5 and `E4` in slots 6--10 before unpacking or
   multiplying.  It emits the checked expected tag rather than copying an
   unchecked input tag.
3. The recurrence fixture now uses a 3-cycle and transposition on three points
   and a 4-cycle and transposition on four points.  These are genuinely
   noncommuting S3/S4 images.  Four live `parent * atom` cases agree with
   direct evaluation in both the E3 and E4 slots; the explicit reversed
   `atom * parent` mutant disagrees in both blocks in all four cases.  Two of
   those cases end in negative signed atoms.
4. Exact bounded mutations reject a `None` atom, a mislabeled parent slot, and
   a mislabeled atom slot, with three distinct typed failure reasons.
5. `direct_column` and `precision2_aggregation` each have one explicit start
   and one explicit completion line.  Each completed item retains
   `guard(started)` and calls the existing 60-second-throttled `meter.check`
   with a numeric `done/total` phase.  There is no per-item
   `endpoint_checkpoint`, reducing the possible explicit flushed large-loop
   lines from 410,488 to exactly four.

The v495 cache remains intact.  Production has exactly four generic atom
signature evaluations plus one generic endpoint evaluation for each reached
seed: `4+R`, where `0 <= R <= 44`.  It performs zero generic empty-word
evaluations and zero direct full-prefix signature comparisons.  The candidate
universe, free reduction, direct columns, bucket arithmetic, precision-two
aggregation, lower-zero gate, rho2 construction, and every claim flag are
unchanged.

## Workflow v12

Workflow v12 is a minimal clone of v11 with:

- its name, path trigger, fire token, and artifact names advanced to v12;
- producer v7 pinned at 54,803 bytes and SHA-256
  `6e26e6b96eb610e29dfd191040cea604e7768a643ed2ef916033c8449373e465`;
- unchanged checker-v4 pinned at 93,236 bytes and SHA-256
  `581f9a5a9aa65ae298bf6d6f785ed1063ddfb0caf8a0c06e15f30ec2e713fd6f`;
- producer compile, selftest, and real invocation switched to v7;
- checker compile, selftest, real invocation, immutable parent identities,
  authentication gates, stdout/stderr/time logging, and failure-log upload
  preserved.

The fire token is exactly `[fire-fresh-precision2-endpoint-v12]`.  It was not
used.

## Bounded checks

Compilation placed its explicit `.pyc` outputs under `%TEMP%`, not in the
repository.

```text
producer-v7 py_compile: PASS
checker-v4 py_compile:  PASS

producer-v7 --selftest: PASS
  actor_atom_generic_evaluations=4
  empty_endpoint_generic_evaluations=0
  full_prefix_generic_comparisons=0
  typed_signature_mutation_rejections=3
  noncommuting_recurrence_cases=4
  signed_noncommuting_recurrence_cases=2
  recurrence_cases=7

checker-v4 --selftest: PASS
  fixture=PASS
  mutation_count=44

workflow-v12 YAML parse: PASS
```

The source/AST probes additionally returned:

```text
AST_SOURCE_PROBE_PASS generic_coordinates=4+R R<=44 empty=0 prefix_direct=0 occurrence_keys=8 explicit_large_boundaries=4 per_item_meter=2
WORKFLOW_SOURCE_PROBE_PASS v7_pinned_invoked=1 checker_v4_pinned_invoked=1 parent_gates_preserved=1
```

This is a finite implementation release only.  Independent audit and an
authorized actual GHA run remain necessary before any fresh rho2 or A0 claim.
