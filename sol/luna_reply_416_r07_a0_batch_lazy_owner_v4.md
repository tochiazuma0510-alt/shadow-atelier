# Luna reply 416 — R07 A0 batch lazy owner v4

Processed the full task instruction. Only the four task416 outputs were
created; no task411/task413/task415 file was modified. No heavy production
run, GHA dispatch, commit, or push was performed.

The v4 producer byte-pins task415/v2 and preserves formula-first correction
filtering. The lazy boundary oracle now collects active
`(block,index,translation_blob,scalar)` entries in deterministic order,
limits the batch to `--batch-cap` (default 128), and sequentially inserts the
independent rank-raising rows under the same dual. A rank increase resets the
correction cursors through the inherited v2 runner. Progress adds
`boundary_active`, `batch_added`, and the inherited examined-pair counter.
No contributor histories are retained. The default round bound is 1,000,000.

When the inherited round bound is reached, v4 writes a valid continuation
checkpoint containing the live echelon rows/order/ancestry/original columns,
cursors, and the authenticated roster binding. It does not claim a positive
terminal unless the inherited strict gates pass; no fake, Ihara, NONMEMBER, or
exhaustive claim is emitted.

Bounded gates:

```text
py_compile producer: PASS
producer --mode FIXTURE: FIXTURE_PASS
producer --help: PASS
```

Exact hashes:

```text
search/d972_r07_a0_batch_lazy_owner_v4.py
  bytes=8505
  sha256=fa7e4682fae6eadba43bc8121cae930f7a4f0bb5f4286afac8b81e2d3e10a1cd

crosscheck/check_d972_r07_a0_batch_lazy_owner_v4.py
  bytes=1765
  sha256=38952af42673ec9e03d355dd8826db9973e2e19110b43d58ca7800e6fb67af8f

search/d972_r07_a0_batch_lazy_owner_gha_driver_v4.g
  bytes=2242
  sha256=e67cb16461873e33900d8dd0cc4e9365a9ee3ad386def1913ab732261f976e0a
```
