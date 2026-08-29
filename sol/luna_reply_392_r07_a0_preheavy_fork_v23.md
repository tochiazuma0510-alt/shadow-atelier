# Luna reply 392: A0 pre-heavy replacement-worker fork v23

## Outcome

The v23 successor is implemented as a generated wrapper over the frozen v22
producer.  The replacement `PersistentBoundaryOwner` is now constructed and
started after `last_safe_light_before_heavy` is sealed and before
`build_heavy`.  The forked workers therefore retain the light runtime while
the parent alone constructs heavy state.  Candidate arithmetic, slices,
ordinals, predicates, budgets, accepted-set semantics, checkpoint bodies,
resume cursor, cleanup, and terminal meaning are unchanged.

## Frozen v22 owners

```text
search/d972_r07_history_free_positive_fast_resume_v22.py
  3280 bytes
  1cc875afb05b7c3db189d7a77fd6d9d4e2604610a0af6a383895011ecbdd0d01
crosscheck/check_d972_r07_history_free_positive_fast_resume_v22.py
  2066 bytes
  4c79b841b5ce003e4d2eefaf1320e878aab400c20ef1a23e4f2900ea61e5cf13
search/d972_r07_history_free_positive_fast_resume_gha_driver_v22.g
  8266 bytes
  8b8f2e9a1dc0b6a30e61ab8866c8d2393328a7038c22323873350d91d5b6531d
```

Each wrapper fails closed on its frozen v22 byte/SHA pin.  The checker pins
the final v23 producer independently; the driver pins both final Python files
and cannot accept a v22 receipt as a v23 receipt.

## Exact moved interval

Generated v22 `Search.ensure_heavy` statement order was:

```text
write_checkpoint("last_safe_light_before_heavy", terminal_checkpoint=False)
build_heavy(...)
heavy digest publication checks
self.heavy_built = True
self.last_safe_phase = "heavy_complete"
self.boundary = PersistentBoundaryOwner(...)
self.boundary.start()
```

Generated v23 order is:

```text
write_checkpoint("last_safe_light_before_heavy", terminal_checkpoint=False)
self.boundary = PersistentBoundaryOwner(...)
self.boundary.start()
build_heavy(...)
heavy digest publication checks
self.heavy_built = True
self.last_safe_phase = "heavy_complete"
```

The AST audit found no other top-level or `Search` method changes.  The sole
`build_heavy` call is in the parent `ensure_heavy`; worker functions contain
none of `qstates`, `qids`, `parents`, `letters`, `stores`, `memberships`,
`emitted`, `fibres`, `delete`, `gamma`, `projected`, `coordinate_marks`, or
`A_maps`.

## Final output hashes

```text
search/d972_r07_history_free_positive_fast_resume_v23.py
  3729 bytes
  0e7ad85d5328b86b57086ca4710520ce748e591e0a0e1cc93cedeba3850fb8f3
crosscheck/check_d972_r07_history_free_positive_fast_resume_v23.py
  2066 bytes
  b0e6f447c92cf76f7735c56ce7dc71b2fa7c3a2247abab3962d50ba9e9bb926c
search/d972_r07_history_free_positive_fast_resume_gha_driver_v23.g
  8275 bytes
  3c469e03244bd4d286c8e0fb2d12544f21ef1a7c2cb1c0cf2c97574a55670313
```

All three executables are ASCII-only.  Python definition-load and generated
source compilation passed.  GAP 4.16.0 `ReadAsFunction` parse-only passed for
the driver.  `git diff --check` passed on the four requested output paths.

The driver preserves the optional all-or-none exact resume path/bytes/SHA
triple, the v20 raw-source pathname, the 10800-second producer bound, the
11100-second external producer timeout, checker timeout, atomic terminal
comparison, and typed terminal grammar.

## Honest residual risk

This is a static lifecycle repair only.  It does not establish a production
result or recompute the heavy search.  Runtime risk remains for ordinary
worker/channel timeout, process failure, cleanup failure, resource caps,
checkpoint serialization or atomic-write failure, heavy construction failure,
and external timeout/OS pressure.  The workers are forked before heavy
construction, so their light-runtime snapshot must remain sufficient for the
existing worker arithmetic and descriptor transport; this was established by
the static owner/reference audit, not by a production run.

```text
TASK392_R07_A0_V23_PREHEAVY_FORK_IMPLEMENTED_STATICALLY_UNEXECUTED
PRODUCTION_TERMINAL_NOT_RECOMPUTED
VERIFIED_FALSE
```
