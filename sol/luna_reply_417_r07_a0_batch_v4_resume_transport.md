# Luna reply 417 — R07 A0 batch-v4 resume transport

Processed the full task instruction. Only the two allowed files were created;
the producer, checker, workflow, and prior task files were not modified. No
129 MB checkpoint was loaded locally, and no production run, dispatch,
commit, or push was performed.

The v31 ASCII GAP driver byte-pins the existing v4 producer and checker,
requires the prior checkpoint at
`ci/in/prior/d972_r07_a0_batch_lazy_owner_v4.checkpoint`, and checks its exact
129119626-byte SHA-256 before generating the shell runner. The shell runner
uses the prior file only as `--resume`, writes a fresh `ci/out` receipt/log/
checkpoint, and invokes:

```text
python3 -u -B search/d972_r07_a0_batch_lazy_owner_v4.py \
  --mode PRODUCTION \
  --output ci/out/d972_r07_a0_batch_lazy_owner_v4_resume.json \
  --resume ci/in/prior/d972_r07_a0_batch_lazy_owner_v4.checkpoint \
  --checkpoint ci/out/d972_r07_a0_batch_lazy_owner_v4_resume.checkpoint \
  --seconds 18000 --rounds 1000000 --batch-cap 128 \
  --rss-bytes 5700000000
```

For `UNKNOWN_RESOURCE`, the driver requires the fresh checkpoint to exist
before running the unchanged checker. The unique final marker is emitted
only after the producer and checker commands return zero.

The prior terminal remains `UNKNOWN_RESOURCE` (`seconds:positive_lazy`), with
the recorded last progress round 648, rank 60258, boundary pairs 10102480,
RSS 2727055360, elapsed 6017.562 seconds. No stronger mathematical claim is
made.

Bounded local gates were limited to static inspection of the ASCII driver and
hash/size checks of the two executed current files; the prior checkpoint was
not opened or decoded.

Exact pins:

```text
prior checkpoint
  bytes=129119626
  sha256=1deed5488a8051102a3fbc80d65432b6f461fdf35c7db46e51261610b7e4a3d5
  header=D972-A0-LAZY-CP2
  payload_bytes=129119534
  payload_sha256=14f38dedf5e1704dbac48ae41e7374adbd397b0f5e98b502eb7e554066bad96d

producer v4
  bytes=8505
  sha256=fa7e4682fae6eadba43bc8121cae930f7a4f0bb5f4286afac8b81e2d3e10a1cd

checker v4
  bytes=1765
  sha256=38952af42673ec9e03d355dd8826db9973e2e19110b43d58ca7800e6fb67af8f

driver v31
  bytes=2852
  sha256=161192258bdb21ed25875061b5a1388227b491bf9fb38932b7a3e47d36566bf2
```
