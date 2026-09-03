# Task701 result — v9 minimal endpoint deletion

Status: `CANDIDATE_ONLY`; no commit, push, dispatch, GHA run, or real 59,049-state build was performed.

## Bounded implementation

In `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py`:

- Added `install_endpoint_deletion(runtime)` immediately after the pinned
  `build_light` return and before the producer is used.
- Translated only the v12f deletion prefix: `build_fine_deletion`, the two
  Q0 marked rows, `make_deleter`, and installation of `runtime['delete']` and
  `runtime['deletion_public']`.
- Enforced `fine_public['source_order'] == 59049` and an installed callable.
  The fine table is passed once into `make_deleter`; no later heavy object is
  constructed or copied.
- Added the bounded zero-word consumer canary: five E3 identity producer
  blobs followed by five E4 identity producer blobs.
- Added one fake-runtime fixture. It proves the installer call, callable
  installation/use, rejection of source order 59048, and that a fake
  `build_heavy` trap is not called.

Serial checks passed:

```text
python -B -m py_compile search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py
producer --selftest: PASS
checker --selftest: PASS
```

Producer fixture receipt:

```json
{"build_heavy_trap_called":false,"endpoint_fine_source_order":59049,"endpoint_installer":"PASS","fixture":"PASS","wrong_fine_order_rejected":1}
```

## Exact receipts

| file | bytes | LF bytes | SHA-256 |
|---|---:|---:|---|
| `search/d972_r07_a0_fresh_precision2_endpoint_signature_v3.py` | 31609 | 383 | `8719929bfd6d134320da8c6fc1a8df527f458c1523f8edb0330b539649097206` |
| `.github/workflows/d972-r07-a0-fresh-precision2-endpoint-v9.yml` | 10225 | 162 | `b381c5ebd8d791bdd36925898d25f4292a05fc62e83588f1782b0e32242e7186` |

## Normalized v8 → v9 workflow diff

Exactly seven line changes against v8:

1. workflow name `v8` → `v9`;
2. workflow path trigger `v8.yml` → `v9.yml`;
3. `PRODUCER_SHA256` updated to
   `8719929bfd6d134320da8c6fc1a8df527f458c1523f8edb0330b539649097206`;
4. job guard receives the inert prefix `false &&`, with the marker changed
   to `[fire-fresh-precision2-endpoint-v9]`;
5. authentication step label `v8` → `v9`;
6. residual artifact name `task640-fresh-rho2-v8` → `...-v9`;
7. log artifact name `task640-fresh-rho2-v8-logs` → `...-v9-logs`.

All action SHAs, caps/timeouts, commands, pins other than the producer pin,
and payload/checker schema are unchanged.
