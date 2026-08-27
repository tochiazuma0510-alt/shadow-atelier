# Luna reply 178: R07 cubic/coset moment oracle v2

Implemented the task178 v2 SELFTEST bundle in the five authorized files only.
Task177 v1 files were not edited.  This turn performed static reads, edits,
hashes, and ASCII inspection only; local Python, Node, GAP, git, and GHA were
not run.

## Scope and honest boundary

The fixture is a six-element noncommutative `D6=C3 semidirect C2` instance.
The producer implements free-word operations, the ordered D6 product, both
coordinate maps, the nontrivial coarse `C_i`, thick left-coset buckets, the
linked Gamma graph, residual/source replay, fibre order, v134 partial cubic
moment expansion, exact Eisenstein pairs, direct enumeration, and integral
nonnegative `(n0,n1,n2)` recovery.  The checker repeats these operations with
an independent permutation-of-three-points representation and does not import
the producer, task177, or any predecessor API.

The two toy rows include same-target F3 cancellation, two linked coordinates,
nonzero `K`, a positive row, and the all-zero negative control.  The anchor
target is literally different from its section value but is found by the
thick `C_i`-coset bucket; literal equality is a semantic mutation and is
rejected.  The linked graph is order 3 and is not a direct product.

The active theorem is v138 (commission commit `28f79f38`).  It supersedes the
withdrawn numerical conclusions of v136:
the unconditional per-row `1536` bound, all-row `9893376` bound, and
unconditional signed-64 safety are not used as production premises.  Toy
resource records expose support-weighted `M`, merged sizes, exact product,
and the balanced support-parametric toy cap.  All arithmetic is arbitrary
precision; the signed-64 field is diagnostic only.  Three resource mutations
are included, for 17 semantic mutations total, and all 17 must reject.

Production is fail-closed at exactly
`UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED`.  It has no task175/task176 positive
run registration, does not allocate a repository-local large table, and
exposes future fixed-width/mmap index and typed-cache primitives.  Actual R07
dual-support sizes have not been measured; actual R07 production/common word,
cofinal lift, fake, and Ihara witness remain pending.

## Expected markers

```text
R07_CUBIC_COSET_MOMENT_ORACLE_V2_PRODUCER_SELFTEST_PASS mutations=17 rejected=17 gamma_coarse_order=3 linked_graph_order=3
R07_CUBIC_COSET_MOMENT_ORACLE_V2_CHECKER_SELFTEST_PASS mutations=17 rejected=17 gamma_coarse_order=3 linked_graph_order=3
R07_CUBIC_COSET_MOMENT_ORACLE_V2_GHA_DRIVER_PASS mode=SELFTEST terminal=FIXTURE_PASS
```

The production envelope is typed `UNKNOWN_INPUT` and the checker terminal is
required to agree exactly with the receipt; the driver emits a corresponding
production pass sentinel only for that typed terminal.

## Driver mode preambles

The GAP driver requires the external, quote-free binding before `Read`:

```text
D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE:="SELFTEST";
D972_R07_CUBIC_COSET_MOMENT_ORACLE_V2_MODE:="PRODUCTION";
```

SELFTEST runs the producer and independent checker serially under an 1800
second shell timeout.  The sealed production envelope is serial under a
20000 second timeout and currently has no registered task175/task176 pins;
its only permitted terminal is `UNKNOWN_INPUT:PREREQUISITE_NOT_PINNED`.
The driver writes the pass artifact with formatting disabled, uses an
external `printf '%s\\n'` emitter, and rejects generated literal
backslash-newline continuations.

## Registered input pins

```text
task178 instruction: sol/luna_task_178_r07_cubic_coset_moment_oracle_v2.md
  bytes=6640 sha256=35890e33e18d0a6150f1173ef1e078eac3d8cbfb1a67dc5edf39abf9ae261ddb
task178a erratum: sol/luna_task_178a_r07_cubic_moment_resource_erratum.md
  bytes=3213 sha256=ef5062f76d7198a1eaf31c839703513f74bf4f80fd97ec11816422d0b4b5bcee
v134: sol/proof_r07_cubic_character_moment_selector_v134.md
  bytes=9402 sha256=1cd3bc0ba0291ab07570a423e6473a54d9a2d4941e310f11e7a55fa16b709477
v136 historical withdrawn: sol/proof_r07_cubic_moment_exact_resource_cap_v136.md
  bytes=4778 sha256=2af3b250aefed10933284847d39e204570b1fdf805313632988d1d49cb0e4a86
v137: sol/proof_r07_coarse_anchor_multi_projection_oracle_v137.md
  bytes=7908 sha256=8674eda702a099885da50b9c3feb664a72f345fa4574cffc138a7e892a3f3a67
v138 active: sol/proof_r07_cubic_moment_resource_cap_erratum_v138.md
  bytes=6371 sha256=9dc94b6de5120e54f3b5a5324fb58a24646ad5917b3bd85c36162af29aa86456
```

Task177 source/fixture pins are carried unchanged in the producer and GAP
driver:

```text
search/d972_r07_weighted_cell_colgen_v1.py
  bytes=29523 sha256=d955d7717f55ffca3abb92229b96ce2b8ee092ddae3d5e6c7379df92f3892d2e
crosscheck/check_d972_r07_weighted_cell_colgen_v1.py
  bytes=20157 sha256=b4d8d046c6850042e0c74778ff8410d9725ef8d0d9387ddb2f75325a6f72d50e
search/d972_r07_weighted_cell_colgen_gha_driver_v1.g
  bytes=13670 sha256=cb32e46412622e55b53859d0e2f2684932204dfdff85477244d1619f9df71304
search/certs/d972_r07_weighted_cell_colgen_selftest_v1_20260827.json
  bytes=4932 sha256=d118633552b5d827d62101f063ba9d7d60fd4335f3744169f85f6cbb2b95da8b
```

## Authorized files and final digests

```text
search/d972_r07_cubic_coset_moment_oracle_v2.py
  bytes=42320 sha256=476329117f6bb4b773b6f51dcc328e23445f09bdd3f6ad2c84bae9aa2daa5f29
crosscheck/check_d972_r07_cubic_coset_moment_oracle_v2.py
  bytes=31150 sha256=f62ab833fd566296058fa977fd285432dae6bf80d996aedf05a21f5da9052c13
search/d972_r07_cubic_coset_moment_oracle_gha_driver_v2.g
  bytes=15156 sha256=1b06b444ddeb729cf7525e9d443052c2b146489c53abdb473e93fec775306890
search/certs/d972_r07_cubic_coset_moment_oracle_selftest_v2_20260827.json
  bytes=6486 sha256=8a7fb3ae2c389b75e98b5a750ab7a2c2c5bc3f00affca8ac57f8ef67ea829aca
sol/luna_reply_178_r07_cubic_coset_moment_oracle_v2.md
  self-hash is reported in the final handoff because embedding it changes the
  file digest itself
```

No production PASS or mathematical claim is asserted by this reply.
