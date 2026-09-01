# Luna reply 509 — minimal checker/driver repair

Implemented only the four specified outputs. The old v6 outputs remain
unchanged. Producer v7 fixes the live dict presentation access, reuses the
non-None replay selective runtime, constructs only on `sf is None`, and skips
zero scalar scan misses.

The v7 checker independently recomputes
`expected_W = sum(sf.kernel_orders[coordinate] for coordinate,target in
formula["merged"])`, preserving target multiplicity.  It requires live
coordinates in `{0,1,2}`, every used kernel order exactly nine, and the
357128352 bound before accepting either record or cursor `W`.  Its bounded
live-path self-test reseals a wrong-W record/cursor pair and confirms rejection
at `global:W_recompute`.

Checker v7 independently recomputes W, binds `global_cursor`, checks selected
support K=0, and rejects multiple or mixed global batches. Its public pins and
binding include v431. Driver v7 restores claim-free RESOURCE transport;
COMMON alone invokes the checker, while RESOURCE requires strict false-claim
and closed-checkpoint gates. The generated shell is executed after `bash -n`.

Exact pins:

```text
search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py
4911 a66526af4b4f86019b1a4a9283212b9782f5793a21c518a93f04b9925e6bee22
crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py
9067 8de4f573a8a00da451c9518bbc87eb77c1c8cebfb2477ce38efb51e0e01c14f8
search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v7.g
9800 fd355c0428f95332c3c822e47b0e2368bfc07cbe4372c47a33fd1ebe24d5d8b7
sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md
9592 7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4
```

Frozen v6 producer source anchor: `14329 3173c9d99fc5a94713d3dbed1b2c90d4ed3a5723b428838ec0bd50d8aee3d90c`.

Bounded commands and results:

- `python -B crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py --self-test` — PASS;
- `python -B crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v7.py --pin-check` — PASS;
- GAP `ReadAsFunction(...)` parse — PASS;
- Python compile/AST parse — PASS;
- no production owner construction, GHA dispatch, git, or unbounded search.

The driver pins v7 producer/checker, v431, C99, rank51, Task451 producer/
checker, and v424/v426/v427. COMMON invokes v7 checker with timeout 5400s;
RESOURCE uses strict claim-free transport and never emits COMMON/COMPLETE.
The generated shell executes after `bash -n`.

TASK509_R07_RANK99_V6_CHECKER_DRIVER_MINIMAL_REPAIR_PASS
