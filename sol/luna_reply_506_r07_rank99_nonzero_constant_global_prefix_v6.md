# Luna reply 506 — bounded implementation

Implemented only the four Task506 outputs.  The v5 producer/checker remain
unchanged.  V6 adds the typed `global_nonzero_constant` cursor, scans
`0..W`, reconstructs `u_Gamma(gid) u_Q0(qid)` from retained section words,
directly evaluates all ten coordinate blobs, and preserves the old support
cursor.  The v5 closed-checkpoint path is authenticated independently before
top-level v6 migration; no full Q0 store, BFS, cache, production run, GHA,
or git operation was used.

Output pins:

```text
search/d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py
14329 3173c9d99fc5a94713d3dbed1b2c90d4ed3a5723b428838ec0bd50d8aee3d90c
crosscheck/check_d972_r07_a0_dual_anchored_rank99_durable_discovery_v6.py
12191 2f579f818b7fff01a3af4764393ac2f2a3190767f0671e6d407c7fe2517e91da
search/d972_r07_a0_dual_anchored_rank99_durable_discovery_gha_driver_v6.g
5291 bd51bb88295d2b1238233ab37de8a2bd69cf5ea598138772197dc2f2bf5f5395
sol/proof_r07_rank99_tau_free_nonzero_constant_global_prefix_v431.md
9592 7b08f2526b00f4b12e67b9de57e03b7e87936050bfe8c3f9200130ed1ef850a4
```

Bounded gates completed:

- producer fixture: PASS (direct cursor `W`, earlier cursor, ten-coordinate
  evaluation, inherited `global_candidate` sentinel untouched);
- checker `--self-test`: PASS;
- checker `--pin-check`: PASS;
- Python AST/compile parse: PASS;
- v5 owner pins and proof pin: PASS;
- driver envelope literals: `14040 < 14220 < 14400`,
  `4200000000 < 4500000000 < 5120000000`, `ulimit -v 5000000`.

TASK506_R07_RANK99_NONZERO_CONSTANT_GLOBAL_PREFIX_V6_PASS
