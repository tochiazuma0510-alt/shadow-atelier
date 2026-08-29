# Luna reply 361 — A4 cap and hot-path v12/v13

## Scope and status

Static implementation only.  Python, GAP, GHA, SELFTEST, mutation, fixture,
retry, multiprocessing, and local execution were not run.  The frozen v6
producer/checker bodies remain the only arithmetic source; the new files are
versioned wrappers with unique byte-level patch gates.

The known diagnostic run `33247161395` stopped with the exact
`UNKNOWN_RESOURCE` reservation at row/query 27.  This reply does not claim a
new run or a new mathematical result.

## Changed files

| file | bytes | SHA-256 |
|---|---:|---|
| `search/d972_r07_word_independent_successor_kernel_v12.py` | 7209 | `816bae92d86ac4bf3a6feb05297f505680072c2ce793db97135154cef928e9c5` |
| `crosscheck/check_d972_r07_word_independent_successor_kernel_v13.py` | 8050 | `f563f560d5987fca4e9fda07f53ddc525b53b99b13497ace04e90d1d766948b` |
| `search/d972_r07_word_independent_successor_kernel_gha_driver_v18.g` | 5539 | `b244849a392271ae421fd99e06f4f62f8d7b47bda12d112fa18d6341b2cebe63` |

The producer wrapper pins frozen v6 at 219187 bytes,
`aaa8a60960698eeeab0c300f7fb65bb902bbae7e5507e4bef933cdff26263a6a`; the
checker wrapper pins frozen v6 at 258847 bytes,
`432bcaadfa1dcfd9526749c40fb3d56c1bdb5671a1959d571a8076c20ba29ccf`.

## Exact production changes

Both independent engines receive the same bounded changes at their unique
sites:

1. Cumulative caps are `correlation_pairs=5_000_000_000`,
   `membership_reductions=2_000_000_000`, and `dual_support=1_000_000_000`.
   Physical RSS, wall, input, and checkpoint caps are untouched.
2. `Oracle.query` already has the result of the membership reduction.  It now
   passes that `remainder` into `dual_from_projection` (producer) or
   `dual_pullback` (checker).  Those functions reduce again only when the
   optional remainder is absent, removing the duplicate reduction without
   changing the result.
3. The hot `Echelon.reduce` AXPY replaces each per-pivot sparse-dictionary
   copy with an in-place mod-3 update: zero coefficients are removed and
   nonzero coefficients are retained.  This is the same sparse F3 operation
   as the frozen `add_row`/`add_sparse` path.
4. The eleven-owner bridge invariant is moved to
   `validate_bridge_owner_once(authority)`.  It performs the existing exact
   owner/layout/coordinate checks once per authority and caches the successful
   result; each of the 6441 row traces only calls the cached gate.
5. A lightweight, flush-based `A4_PROGRESS` monitor is called at authority
   initialization and row/queue entry.  Its monotonic-time gate emits at most
   once per 60 seconds with exactly phase, row, membership query count,
   correlation-pair count, and elapsed time.  It performs no scan or
   arithmetic.
6. Initial checkpoint rows are now
   `{32,64,128,256,512,1024,2048,3072,4096,5120,6144,ROWS}` in both engines.
   Checkpoint size/resource limits were not raised; if the 32-row checkpoint
   exceeds the existing limit, the run remains a typed resource outcome.

The checker pins `PRODUCER_CODE_PATH` to
`search/d972_r07_word_independent_successor_kernel_v12.py` and reconstructs
the patched arithmetic independently; it does not import producer helpers.

## Driver boundary

`search/d972_r07_word_independent_successor_kernel_gha_driver_v18.g` retains
the v17 diagnostic/capture behavior: distinct `v18diag` receipt, verdict,
checkpoint, log, script, and sentinel paths; exact producer/checker byte/SHA
pins; fail-closed replacement gates; and capture of the final 65535 bytes of
both logs when no `.ok` sentinel exists.  It emits the success sentinel only
when the generated run creates it, and otherwise emits a diagnostic
no-sentinel marker plus log tails.

No execution result, PASS, cross-check, or verification claim is made here.
